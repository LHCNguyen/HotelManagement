import datetime
import hashlib
from enum import unique

from sqlalchemy import Column, Integer, Boolean, String, Date, Time,Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from flask_security import RoleMixin
from flask_login import UserMixin
from app.index import register


from app import db, app


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Floor(db.Model):
    __tablename__ = "floor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_floor = Column(Integer, nullable=False, unique=True)
    rooms = relationship('Room', backref='floors', lazy=True)



class CustomerType(db.Model):
    __tablename__ = "customer_style"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_style = Column(String(50), unique=True)
    users = db.relationship('User', backref='customer_types', lazy=True)

class Room(db.Model):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String(5), nullable=False)
    style_room = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    status = Column(Boolean, nullable=False, default=False)
    description = db.Column(db.String(100))
    floor_id = Column(Integer, ForeignKey(Floor.id), nullable=False)
    booking_detail = relationship('BookingDetail', backref='rooms', lazy=True)
    comments = relationship('Comment', backref='rooms', lazy=True)
    evaluations = relationship('Evaluation', backref='rooms', lazy=True)



class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    position = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fullname = db.Column(String(50), nullable=False)
    phone_number = db.Column(String(10), nullable=False, unique=True)
    username = db.Column(String(50), nullable=False, unique=True)
    password = db.Column(String(255), nullable=False)
    email = db.Column(String(50), nullable=False, unique=True)
    create_at = db.Column(DateTime, default=func.now())
    address = db.Column(String(255), nullable=True)
    citizen_id = db.Column(String(12), nullable=False, unique=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref='users', lazy='dynamic')
    customer_type_id = Column(Integer, ForeignKey(CustomerType.id), nullable=False)
    bookings = db.relationship('Booking', backref='users', lazy=True)
    comments = relationship('Comment', backref='users', lazy=True)
    evaluations = relationship('Evaluation', backref='users', lazy=True)


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    bookings = relationship('Booking', backref='payment_methods', lazy=True)


class Style(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ballot_type = Column(String(50), nullable=False, unique=True)
    bookings = relationship('Booking', backref='styles', lazy=True)



class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    check_in_date = Column(Date, nullable=False, default=datetime.date.today)
    check_out_date = Column(Date, nullable=False, default=datetime.date.today)
    check_in_time = Column(Time, nullable=True, default=datetime.time(hour=14, minute=0))
    check_out_time = Column(Time, nullable=True, default=datetime.time(hour=14, minute=0))
    booking_detail = relationship('BookingDetail', backref='bookings', lazy=True)
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)
    payment_method_id = Column(Integer, ForeignKey(PaymentMethod.id), nullable=False)
    style_id = Column(Integer, ForeignKey(Style.id), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comments = Column(String(255))
    create_at = Column(DateTime, default=func.now())
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


class Evaluation(db.Model):
    __tablename__ = "evaluation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(Float)
    create_at = Column(DateTime, default=func.now())
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


class Policy(db.Model):
    __tablename__ = "policy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True)
    value = Column(Float, nullable=False, default=0)



class BookingDetail(db.Model):
    __tablename__ = "booking_detail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_customer = Column(Integer, nullable=False, default=0)
    total_amount = Column(Float, nullable=False, default=0)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user_role = Role(position="Khách Hàng")
        staff_role = Role(position="Nhân Viên")
        admin_role = Role(position="Người Quản Trị")
        db.session.add_all([user_role, staff_role, admin_role])
        db.session.commit()

        c1 = CustomerType(customer_style="Nội địa")
        c2 = CustomerType(customer_style="Nước ngoài")
        db.session.add_all([c1, c2])
        db.session.commit()

        f1 = Floor(number_floor=1)
        f2 = Floor(number_floor=2)
        f3 = Floor(number_floor=3)
        f4 = Floor(number_floor=4)
        f5 = Floor(number_floor=5)
        f6 = Floor(number_floor=6)
        f7 = Floor(number_floor=7)
        f8 = Floor(number_floor=8)
        f9 = Floor(number_floor=9)
        f10 = Floor(number_floor=10)
        db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8 ,f9 ,f10])
        db.session.commit()

        s1 = Style(ballot_type="Trực tuyến")
        s2 = Style(ballot_type="Trực tiếp")
        db.session.add_all([s1,s2])
        db.session.commit()

        p1 = Policy(key="Thời điểm nhận phòng", value=28)
        p2 = Policy(key="Số khách mỗi phòng", value=3)
        p3 = Policy(key="Hệ số phụ thu", value=0.25)
        p4 = Policy(key="Hệ số khách nước ngoài", value=1.5)
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        b1 = Room(room_number="101", style_room="Loại phòng 2 người", price=350000, floor_id=1)
        b2 = Room(room_number="201", style_room="Loại phòng 3 người", price=400000, floor_id=2)
        b3 = Room(room_number="301", style_room="Loại phòng 2 người", price=450000, floor_id=3)
        b4 = Room(room_number="401", style_room="Loại phòng 3 người", price=500000, floor_id=4)
        b5 = Room(room_number="501", style_room="Loại phòng 2 người", price=550000, floor_id=5)
        db.session.add_all([b1, b2, b3, b4, b5])
        db.session.commit()

        u1 = User(fullname="Trần Minh Quân"
                  , phone_number="0522526015"
                  , username="QuanMinh"
                  , password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest())
                  , email="user@gmail.com"
                  , address="VN"
                  , citizen_id="123456789876"
                  , roles=[user_role]
                  , customer_type_id=1)
        u2 = User(fullname="Lâm Huỳnh Chấn Nguyên"
                  , phone_number="1243567567"
                  , username="ChanNguyen"
                  , password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest())
                  , email="staff@gmail.com"
                  , address="VN"
                  , citizen_id="029482039293"
                  , roles=[staff_role]
                  , customer_type_id=1)
        u3 = User(fullname="Trần Văn A"
                  , phone_number="039480238"
                  , username="VanA"
                  , password=str(hashlib.md5('12345'.encode('utf-8')).hexdigest())
                  , email="admin@gmail.com"
                  , address="VN"
                  , citizen_id="038520394820"
                  , roles=[admin_role]
                  , customer_type_id=1)
        db.session.add_all([u1, u2, u3])
        db.session.commit()



