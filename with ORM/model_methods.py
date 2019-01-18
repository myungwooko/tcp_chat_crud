from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



Base = declarative_base()
engine = create_engine('sqlite:///tcp_chat.db?check_same_thread=False', echo=True)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()



class ChatRoomNumber(Base):
    __tablename__ = 'chatRoomNumbers'

    id = Column(Integer, Sequence('chatRoomNumber_id_seq'), primary_key=True)
    room_number = Column(Integer)

    def __repr__(self):
            return "<ChatRoomNumber(id='%s', room_number='%s')>" \
                   % (self.id, self.room_number)



class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
        username = Column(String(250))
        unique_number = Column(Integer)
        chatRoomNumber_id = Column(Integer, ForeignKey("chatRoomNumbers.id"))

        chatRoomNumber = relationship("ChatRoomNumber", back_populates="users")


        def __repr__(self):
                return "<User(id='%s', username='%s', unique_number='%s', chatRoomNumber_id='%s')>" \
                       % (self.id, self.username, self.unique_number, self.chatRoomNumber_id)


ChatRoomNumber.users = relationship(
        "User", order_by= User.id, back_populates="chatRoomNumber")


# will occur by this reverse way
# User.chatRoomNumbers = relationship(
#         "ChatRoomNumber", order_by= ChatRoomNumber.id, back_populates="User")




class Msg(Base):
        __tablename__ = 'msgs'

        id = Column(Integer, Sequence('msg_id_seq'), primary_key=True)
        message = Column(String(250))
        sender_id = Column(Integer, ForeignKey("users.id"))
        receivers_id = Column(String(250))
        chatRoomNumber_id = Column(Integer, ForeignKey("chatRoomNumbers.id"))
        created_at = Column(DateTime)
        user = relationship("User", back_populates="msgs")
        chatRoomNumber = relationship("ChatRoomNumber", back_populates="msgs")


User.msgs = relationship(
        "Msg", order_by= Msg.id, back_populates="user")

ChatRoomNumber.msgs = relationship(
        "Msg", order_by= Msg.id, back_populates="chatRoomNumber")



Base.metadata.create_all(engine)  # ----------------------> 이건 shcema 정의한 다음에 해주어야 table생성 해주는 거니까  맞는 거니까 이렇게 정의후에






#  test & data 넣는 형태, session.add(ele), session.commit()에 관하-----------------------------------------------------------------

# cr1 = ChatRoomNumber(room_number=12)
# cr2 = ChatRoomNumber(room_number=3)
# session.add(cr1)
# session.add(cr2)
#
# session.commit()##################################################################### 아래것과 함께 두개가 있어야 한다
#
#
# user1 = User(username='Ko', unique_number=123, chatRoomNumber_id=cr1.id)
#
# session.add(user1)
# session.commit()##################################################################### 왜냐하면 논리적으로 추가가 되어졌어야 아이디가
#                 ####################################################################  있는거고 그래야 넣을수 있으니까
#
# print(cr1.id)
# print(cr1.room_number)
# print(user1.id)
# print(user1.chatRoomNumber_id)
#
# ts = time.time()
# st = datetime.fromtimestamp(ts)
#
#
# msg1 = Msg(message='Hi', sender_id=user1.id, receivers_id='1,2', chatRoomNumber_id=cr1.id, created_at=st)
#
#
#
#
# session.add(msg1)
# session.commit()
#
# msg1
#
#




#-------------------------------------------------------------------------------------------------------------------------------



def add_user(username, unique_number, chat_room_number_id):
        user = User(username=username, unique_number=unique_number, chatRoomNumber_id=chat_room_number_id[0])#############################################
        session.add(user)
        session.commit


def insert_msg(msg, sender, clients, chatRoomNumber_id, st):
        msg = msg.decode("utf8")
        sender_id = user_id_by_tuple(sender)
        receivers_ids = ""
        pre_receivers = clients.values()
        last_idx = len(pre_receivers) - 1
        counter = 0
        for receiver in pre_receivers:
            receiver_id = user_id_by_tuple(receiver)
            if counter != last_idx:
                receivers_ids = receivers_ids + str(receiver_id) + ", "
                counter = counter + 1
            else:
                receivers_ids = receivers_ids + str(receiver_id)
        msg = Msg(message=msg, sender_id=sender_id, receivers_id=receivers_ids, chatRoomNumber_id=chatRoomNumber_id[0], created_at=st)
        session.add(msg)
        session.commit()


def add_new_chatroom_id(unique_number):
        roomId = ChatRoomNumber(room_number=unique_number)
        session.add(roomId)
        session.commit()


def getting_chatroom_id():
        return  session.query(ChatRoomNumber.id).order_by(ChatRoomNumber.id.desc()).first()



def user_id_by_tuple(tuple):
        users = session.query(User).all()
        for user in users:
            if user.username == tuple[0] and user.unique_number == tuple[1]:
                    result = user.id
                    return result


def getting_username_by_id(str_or_int):
        id = int(str_or_int)
        users = session.query(User).all()
        for user in users:
            if user.id == id:
                return user.username


def all_users(chatRoomNumber_id):
        return session.query(User.username).filter(User.chatRoomNumber_id.like(chatRoomNumber_id))


def delete_user(name):
        session.query(User).filter(User.username == name).delete()


def all_messages(chatRoomNumber_id):
        return session.query(Msg).filter(Msg.chatRoomNumber_id.like(chatRoomNumber_id))



