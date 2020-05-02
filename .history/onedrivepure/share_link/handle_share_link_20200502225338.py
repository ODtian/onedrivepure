import requests
import json
import time
from urllib.parse import unquote

s = requests.session()

stream_link = \
    'https://{tenant_name}/personal/{account_name}'\
    '/_api/web/GetListUsingPath(DecodedUrl=@a1)'\
    '/RenderListDataAsStream'\

stream_params = {
    '@a1': '\'/personal/{account_name}/Documents\'',
    'TryNewExperienceSingle': 'True'
}

download_link = \
    'https://{tenant_name}/personal/{account_name}'\
    '/_layouts/15/download.aspx?UniqueId={unique_id}'

stream_file_link = \
    'https://{tenant_name}/personal/{account_name}'\
    '/_api/web/GetList(@listUrl)/RenderListDataAsStream'\

stream_file_params = {
    '@listUrl': '\'/personal/{account_name}/Documents\'',
    'View=': ''
}

stream_root_folder_params = {
    'RootFolder': '/personal/{account_name}/Documents{ref_path}'
}

file_xml = \
    '<View Scope=\"RecursiveAll\">'\
    '<Query><Where><Eq>'\
    '<FieldRef Name=\"FileRef\" /><Value Type=\"Text\">'\
    '<![CDATA[{file_path}]]>'\
    '</Value></Eq></Where></Query>'\
    '<RowLimit Paged=\"True\">1</RowLimit>'\
    '</View>'


def merge(*dicts):
    result = {}
    for d in dicts:
        result = {**result, **d}
    return result


def handle_link(link, show_json=False, save=False):
    if link.startswith('!'):
        link = link[1:]
        is_file = True
    else:
        is_file = False

    if not link.startswith('http'):
        data = json.load(
            open(link, 'r')
        )
        return data['data'], data['sharelink']

    split_name = link.lstrip('https://').split('/')
    tenant_name = split_name[0]
    account_name = split_name[4]

    s = requests.session()
    get_cookie = s.get(link)

    if is_file:
        file_path = \
            get_cookie\
            .history[0]\
            .headers['Location']\
            .split('/')[7]\
            .split('&')[0]\
            .lstrip('onedrive.aspx?id=')

        data = get_stream_file(s, file_path, tenant_name, account_name)
    else:
        base_path = '/'+'/'.join(
            get_cookie
            .history[0]           # 获取302请求
            .headers['Location']  # 获取重定向URL
            .split('/')[7]        # 获取分享链接文件的路径
            .split('&')[0]
            .lstrip('onedrive.aspx?id=')
            .split('%2F')[4:]
        )

        data = get_stream_list(s, base_path, tenant_name, account_name)

    file_name = 'shared_'+str(int(time.time()))+'.json'
    dict_data = {
        'data': data,
        'sharelink': link
    }

    json_data = json.dumps(dict_data, sort_keys=True, indent=2)

    if save:
        with open(file_name, 'w') as f:
            f.write(json_data)
    if show_json:
        print(json_data)

    return data, link


def get_stream_file(s, file_path, tenant_name, account_name):
    url = stream_file_link.format(
        tenant_name=tenant_name, account_name=account_name
    )

    params = merge(stream_file_params)
    params['@listUrl'] = params['@listUrl'].format(account_name=account_name)

    data = json.dumps({
        "parameters": {
            "__metadata": {
                "type": "SP.RenderListDataParameters"
            },
            "RenderOptions": 12295,
            "ViewXml": file_xml.format(file_path=unquote(file_path, 'utf-8')),
            "AddRequiredFields": True
        }
    })

    headers = {
        'Content-Type': 'application/json;odata=verbose'
    }

    result = s.post(url, data=data, headers=headers, params=params)
    row = result.json()['ListData']['Row'][0]

    unique_id = row['UniqueId'].lstrip('{').rstrip('}')
    download_url = download_link.format(
        tenant_name=tenant_name, account_name=account_name, unique_id=unique_id
    )
    path = '/'+row['FileLeafRef']
    size = int(row['FileSizeDisplay'])

    return [{
            'download_url': download_url,
            'path': path,
            'size': size
            }]


def get_stream_list(
    s,
    ref_path,
    tenant_name,
    account_name,
    add_params=None,
    option=464647
):

    if not add_params:
        params = merge(stream_params, stream_root_folder_params)
        params['RootFolder'] = params['RootFolder'].format(
            account_name=account_name, ref_path=ref_path
        )
    else:
        params = merge(stream_params, add_params)
    params['@a1'] = params['@a1'].format(
        account_name=account_name
    )

    url = stream_link.format(
        tenant_name=tenant_name,
        account_name=account_name
    )
    data = json.dumps({
        'parameters': {
            '__metadata': {
                'type': 'SP.RenderListDataParameters'
            },
            'RenderOptions': option,
            'AllowMultipleValueFilterForTaxonomyFields': True,
            'AddRequiredFields': True
        }
    })
    headers = {
        'Content-Type': 'application/json;odata=verbose'
    }

    result = s.post(url, data=data, headers=headers, params=params)
    print('Find dir:', ref_path)
    list_data = result.json()['ListData']
    dirs = []
    result_list = []

    for row in list_data['Row']:
        is_dir = row['.fileType'] == '' and row['.hasPdf'] == ''
        row_ref_path = row['FileRef']

        if is_dir:
            dirs.append('/' + '/'.join(row_ref_path.split('/')[4:]))
        else:
            unique_id = row['UniqueId'].lstrip('{').rstrip('}')
            download_url = download_link.format(
                tenant_name=tenant_name,
                account_name=account_name,
                unique_id=unique_id
            )
            path = '/' + '/'.join(row_ref_path.split('/')[4:])
            size = int(row['FileSizeDisplay'])

            print('    '+'Find:', path)

            result_list.append({
                'download_url': download_url,
                'path': path,
                'size': size
            })

    next_href = list_data.get('NextHref')
    if next_href:
        params = {
            i.split('=')[0]: i.split('=')[1]
            for i in next_href.strip('?').split('&')
        }
        result_list += get_stream_list(
            s,
            ref_path,
            tenant_name,
            account_name,
            add_params=params,
            option=167943
        )

    for dir_path in dirs:
        result_list += get_stream_list(s, dir_path, tenant_name, account_name)

    return result_list


if __name__ == '__main__':
    t = handle_link(
        'https://acdf8-my.sharepoint.com/:f:/g/personal/1_lolicon_live/'
        'En3vBGypN6RJoV_TS7JCJeUBwwCA2F4Fw7Lhu4mTVFOs5Q?e=cITgzq',
        show_json=True
    )
