from multiprocessing import JoinableQueue

def all_done(self):
    is_done = self._unfinished_tasks._semlock._is_zero()
    return 

JoinableQueue.all_done = all_done
DoneableQueue = JoinableQueue
