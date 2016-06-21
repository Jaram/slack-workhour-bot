from model.worklog import User, WorkLog
from datetime import datetime

_session_factory = SqlSessionFactory()

class WorkLogAccessor(object):
    def __init__(self, user_key):
        self.session = _session_factory.create()
        self.user = self.session.query(User).filter(User.user_key == user_key).one()


class WorkLogReader(WorkLogAccessor):
    def __init__(self, user_key):
        super(WorkLogReader, self).__init__(user_key)
    
    def findAll(self, year=None, month=None):
        today = datetime.now()
        if not year:
            year = today.year
        if not month:
            month = today.month

        return user.worklogs



class WorkLogWriter(WorkLogAccessor):
    def __init__(self, user_key):
        super(WorkLogWriter, self).__init__(user_key)
    
    

