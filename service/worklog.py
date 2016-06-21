from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.session import SqlSessionAware
from model.worklog import User, WorkLog

import logging

class CommuteLogger(SqlSessionAware):
    def __init__(self):
        super(CommuteLogger, self).__init__()

    def enter_office(self, user_key):
        user = self._get_or_create_user(user_key)
        pass

    def leave_office(self, user_key):
        pass
    
    def _get_or_create_user(self, user_key):
        try:
            return self.session.query(User).filter(User.user_key == user_key).one()
        except:
            logging.debug('creating new user')
            user = User(user_key, 'name not set yet')
            self.session.add(user)
            self.session.commit()
            return user

    def _get_or_create_worklog(self, user):
        worklog = self.session.query(WorkLog).filter(WorkLog.user_id == user.id)
        pass
        
