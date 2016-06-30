# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.session import SqlSessionAware
from model.worklog import User, WorkLog

import logging

class CommuteLogger(SqlSessionAware):
    def __init__(self):
        super(CommuteLogger, self).__init__()

    def enter_office(self, user_info, time):
        user = self._get_or_create_user(user_info.user_key)
        worklog = self._create_worklog(user, self._date_string_to_date_time(time))
        user.user_name = user_info.user_name
        self.session.commit()
        return worklog

    def leave_office(self, user_info, time):
        user = self._get_or_create_user(user_info.user_key)
        worklog = self._get_latest_worklog(user)
        if not worklog:
            logging.error('did not entered the office')
            raise Exception('no worklog')
        worklog.end_time = self._date_string_to_date_time(time)
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

    def _create_worklog(self, user, date_time):
        worklog = WorkLog(user, date_time)
        self.session.add(worklog)
        self.session.commit()
        return worklog
        
    def _get_latest_worklog(self, user):
        return self.session.query(WorkLog).filter(WorkLog.user_id == user.id).order_by(WorkLog.id.desc()).first()

    def _date_string_to_date_time(self, date_string):
        date = datetime.now()
        if date_string is not None:
            datas = date_string.split(':')
            hour = datas[0]
            minute = datas[1]
            date = datetime.now()
            date = date.replace(hour=int(hour), minute=int(minute), second=0)
        return date
