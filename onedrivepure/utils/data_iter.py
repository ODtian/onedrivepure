class dataIter:
    def __init__(self, file_piece, bar, step_size):
        self.bar = bar  # 进度条
        self.step_size = step_size  # 每次生成的文件块大小 越大进度条刷新越频繁

        self.file_piece = file_piece
        self.file_piece_size = len(self.file_piece)

    def get_step(self, start, end):
        return self.file_piece[start:end]

    def get_range(self):
        return range(0, self.file_piece_size, self.step_size)

    def __iter__(self):
        range = self.get_range()
        for i in range:
            step = self.get_step(i, i + self.step_size)
            yield step
            self.bar.update(len(step))

    def __len__(self):
        return self.file_piece_size
