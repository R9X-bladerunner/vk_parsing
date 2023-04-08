from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

import time
import vk

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'users'
    count = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, index=True)
    first_name = Column(String)
    last_name = Column(String)
    city = Column(String)
    photo_max_orig = Column(Text)
    can_access_closed = Column(Boolean)
    is_closed = Column(Boolean)
    track_code = Column(String)

class DataBase:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        self.db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        self.engine = create_engine(self.db_string, echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(autoflush=False, bind=self.engine)
        print('DataBase initialized')

    @staticmethod
    def user_obj_constructor(vk_user: dict):
        return User(id=vk_user.get('id'), first_name=vk_user.get('first_name'), last_name=vk_user.get('last_name'),
                    city=str(vk_user.get('city')), photo_max_orig=vk_user.get('photo_max_orig'),
                    can_access_closed=vk_user.get('can_access_closed'), is_closed=vk_user.get('is_closed'),
                    track_code=vk_user.get('track_code'))


    def add_users(self, users):
        with self.Session(autoflush=False, bind=self.engine) as db:
            records = [DataBase.user_obj_constructor(user) for user in users]

            db.add_all(records)
            db.commit()





class VkSession:
    def __init__(self, login, password):
        self.api_session = self.authorize(login, password)
        self.fields = ['city','photo_max_orig']


    def authorize(self, login: str, password: str):
        client_id = '51576983'  # App ID
        v = '5.131'  # API version
        api_session = vk.UserAPI(user_login=login, user_password=password, client_id=client_id, v=v)
        return api_session


    def get_1000_users(self):

        offset = 0
        count = 200
        users = []
        while offset < 1000:
            response = self.api_session.users.search(offset=offset, count=count, has_photo=1, fields=self.fields)
            users.extend(response['items'])
            time.sleep(0.25)
            offset += 200
        print(users)
        return users




if __name__ == '__main__':

    vk_user_login = 'user'  # change to access
    vk_user_pass = 'password'   # change to access

    database_config = {
        'db_name':'vk_users',
        'db_user':'postgres',
        'db_pass':'12345678',
        'db_host':'localhost',
        'db_port':'5432'
    }

    vk_api_session = VkSession(vk_user_login, vk_user_pass)

    db_session = DataBase(**database_config)
    db_session.add_users(vk_api_session.get_1000_users())

