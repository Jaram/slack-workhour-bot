# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.session import SqlSessionAware
from model.worklog import User, WorkLog

import logging

class CommuteLogger(SqlSessionAware):
    def __init__(self):
        super(CommuteLogger, self).__init__()

    def enter_office(self, user_info):
        user = self._get_or_create_user(user_info.user_key)
        worklog = self._create_worklog(user)
        user.user_name = user_info.user_name
        self.session.commit()

    def leave_office(self, user_info):
        user = self._get_or_create_user(user_info.user_key)
        worklog = self._get_latest_worklog(user)
        if not worklog:
            logging.error('did not entered the office')
            raise Exception('no worklog')
        worklog.end_time = datetime.now()
        self.session.commit()
        return worklog
    
    def _get_or_create_user(self, user_key):
        try:
            return self.session.query(User).filter(User.user_key == user_key).one()
        except:
            logging.debug('creating new user')
            user = User(user_key, 'name not set yet')
            self.session.add(user)
            self.session.commit()
            return user

    def _create_worklog(self, user):
        worklog = WorkLog(user, datetime.now())
        self.session.add(worklog)
        self.session.commit()
        return worklog
        
    def _get_latest_worklog(self, user):
        return self.session.query(WorkLog).filter(WorkLog.user_id == user.id).order_by(WorkLog.start_time.desc()).first()
