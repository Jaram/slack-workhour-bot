from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SqlSessionFactory():
    def __init__(self, sqlite_path, sqlalchemy_base_class):
        self.engine = create_engine(sqlite_path)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)
        sqlalchemy_base_class.metadata.create_all(self.engine)

    def create(self):
        return self.session_maker()
