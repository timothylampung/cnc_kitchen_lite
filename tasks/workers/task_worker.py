from rq import Worker as BaseClass


class TaskWorker(BaseClass):
    def __init__(self, queues=None, name=None, *args, **kwargs):
        u'''
        Constructor.

        Accepts the same arguments as the constructor of
        ``rq.worker.Worker``.
        '''

        super().__init__(queues, name, *args, **kwargs)