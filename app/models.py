import datetime

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, func

from app.index import register


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(100))
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(String(50))
    phone_number = db.Column(String(10))
    username = db.Column(String(50), nullable=False)
    password = db.Column(String(50))
    email = db.Column(String(50), nullable=False)
    create_at = db.Column(datetime, default=func.now())
    address = db.Column(String(255))
    citizen_id = db.Column(String(12), nullable=False)
    roles = db.relationship('Role', backref="users", lazy='dynamic')
    customer_type_id = relationship('CustomerType', backref='users', lazy='dynamic')
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id, nullable=False))
    evaluation_id = Column(Integer, ForeignKey(Evaluation.id, nullable=False))


class Room(db.Model):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    style_room = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    status = Column(Boolean, default=False, nullable=False)
    description = db.Column(db.String(100))
    comment_id = Column(Integer, ForeignKey(Comment.id), nullable=False)
    evaluation_id = Column(Integer, ForeignKey(Evaluation.id), nullable=False)
    floors = relationship('Floor', backref='room', lazy=True)
    booking_detail = relationship('BookingDetail', backref='room', lazy=True)


class Floor(db.Model):
    __tablename__ = "floor"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_floor = Column(Integer, nullable=False, unique=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


class CustomerType(db.Model):
    __tablename__ = "customer_style"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Customer_style = Column(String(50), unique=True)
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comments = Column(String(255))
    create_at = Column(DateTime, default=func.now())
    users = db.relationship('User', backref='comment', lazy=True)
    rooms = relationship('Room', backref='comments', lazy=True)


class Evaluation(db.Model):
    __tablename__ = "evaluation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    point = Column(Float)
    create_at = Column(DateTime, default=func.now())
    users = db.relationship('User', backref='evaluation', lazy=True)
    rooms = relationship('Room', backref='evaluation', lazy=True)


class Policy(db.Model):
    __tablename__ = "policy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True)
    value = Column(Float, nullable=False, default=0)


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    check_in_date = Column(Date, nullable=False, default=date.today)
    check_out_date = Column(Date, nullable=False, default=date.today)
    check_in_time = Column(Time, nullable=False, default=time(hour=14, minute=0))
    check_out_time = Column(Time, nullable=False, default=time(hour=14, minute=0))
    users = db.relationship('User', backref='booking', lazy=True)
    styles = relationship('Style', backref='booking', lazy=True)
    payment_methods = relationship('PaymentMethod', backref='booking', lazy=True)
    booking_detail = relationship('BookingDetail', backref='booking', lazy=True)


class BookingDetail(db.Model):
    __tablename__ = "booking_detail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_customer = Column(Integer, nullable=False, default=0)
    total_amount = Column(Float, nullable=False, default=0)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)


class Style(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ballot_type = Column(Sring(50), nullable=False, unique=True)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()





