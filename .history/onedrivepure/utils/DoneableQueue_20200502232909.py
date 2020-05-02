from multiprocessing import JoinableQueue

def all_done(self):


JoinableQueue.all_done = all_done
class DoneableQueue(JoinableQueue):
    def __init__(self,)
