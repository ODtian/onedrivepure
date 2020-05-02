from multiprocessing import JoinableQueue

class DoneableQueue(JoinableQueue):
    def __init__(self,)