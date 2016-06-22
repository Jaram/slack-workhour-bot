from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_key = Column(String(50), nullable=False)
    user_name = Column(String(150), nullable=True)
    worklogs = relationship('WorkLog')

    def __init__(self, user_key, user_name):
        self.user_key = user_key
        self.user_name = user_name

    def __repr__(self):
        return "User<id:{}, user_key:{}>".format(self.id, self.user_key)


class WorkLog(Base):
    __tablename__ = 'worklog'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)

    def __init__(self, user, start_time):
        self.user_id = user.id
        self.start_time = start_time

    def __repr__(self):
        return "WorkLog<id:{}, user_id:{}, start_time:{}, end_time:{}>"\
            .format(self.id, self.user_id, self.start_time, self.end_time)
