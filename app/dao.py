from sqlalchemy import or_, func

from app.models import *

def get_user_by_id(user_id):
    return User.query.get(user_id)

def authenticated_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                                User.password.__eq__(password)).first()


def get_room(kw, room_id, page):
    room = Room.query
    if kw:
        room = room.filter(or_(func.lower(Room.style_room).contains(func.lower(kw)),
                               func.lower(Room.price).contains(func.lower(kw)),
                               func.lower(Room.status == False)))
        if 'còn phòng' in kw.lower():
            room = room.filter(Room.status == False)
        elif 'hết phòng' in kw.lower():
            room = room.filter(Room.status == True)

    if room_id:
        room = room.filter(Room.id.__eq__(room_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return room.slice(start, start + page_size).all()

    return room.all()

def get_room_cart(room_id):
    return Room.query.get(room_id)


def count_room():
    return Room.query.count()

def get_room_by_id(id):
    return Room.query.get(id)


def count_cart(cart):
    def count_cart(cart):
        total_amount, total_quantity = 0, 0

        if cart:
            for room_id in cart:
                room = get_room_cart(room_id)
                if room:
                    total_quantity += 1
                    total_amount += room.price

        return {
            "total_amount": total_amount,
            "total_quantity": total_quantity
        }