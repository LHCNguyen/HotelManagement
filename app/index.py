import math
from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import dao

from flask import redirect, request, render_template_string

from admin import *


@app.route('/')
def home():
    kw = request.args.get('kw')
    room_id = request.args.get('room_id')
    page = request.args.get('page', 1)
    num = dao.count_room()
    page_size = app.config["PAGE_SIZE"]
    pro = dao.get_room(kw, room_id, page)
    cart_stats = session.get('cart_stats', {"total_quantity": 0})
    total_pages = math.ceil(num / page_size)
    return render_template(
        'index.html', pages=total_pages, produces=pro, cart_stats=cart_stats, kw=kw, room_id=room_id, page=page)


@app.route('/rooms/<id>')
def info_room(id):
    room = dao.get_room_by_id(id)
    return render_template('info.html', room=room)


@app.route('/login_user')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


#
# @app.route('/profile')
# def profile():
#     # Kiểm tra nếu người dùng đã đăng nhập
#     if 'user_id' in session:
#         # Lấy thông tin user từ cơ sở dữ liệu hoặc session
#         user_info = {
#             "name": "Nguyễn Văn A",
#             "email": "nguyenvana@example.com",
#         }
#         return render_template('profile.html', user=user_info)
#     else:
#         # Nếu chưa đăng nhập, chuyển hướng về trang đăng nhập
#         return redirect(url_for('login'))


@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    rooms_in_cart = []
    total_price = 0
    for room_id in cart:
        room = dao.get_room_cart(room_id)
        if room:
            rooms_in_cart.append(room)
            total_price += room.price
    cart_stats = session.get('cart_stats', {"total_quantity": len(cart)})

    return render_template('cart.html', rooms=rooms_in_cart, total=total_price, cart_stats=cart_stats)


@app.route('/add_to_cart/<int:room_id>', methods=['POST'])
def add_to_cart(room_id):
    cart = session.get('cart', [])
    if room_id not in cart:
        cart.append(room_id)
    session['cart'] = cart
    session['cart_stats'] = {"total_quantity": len(cart)}  # Cập nhật số lượng

    return jsonify({"success": True, "cart_size": session['cart_stats']['total_quantity']})


@app.route('/remove_from_cart/<int:room_id>', methods=['POST'])
def remove_from_cart(room_id):
    cart = session.get('cart', [])
    if room_id in cart:
        cart.remove(room_id)
    session['cart'] = cart

    rooms_in_cart = [dao.get_room_cart(room_id) for room_id in cart]
    total_price = sum(room.price for room in rooms_in_cart if room)

    cart_stats = {"total_quantity": len(cart)}
    session['cart_stats'] = cart_stats

    return jsonify({
        "success": True,
        "cart_size": cart_stats['total_quantity'],
        "total": total_price
    })

@app.context_processor
def common_responses():
    cart = session.get('cart', [])
    cart_stats = dao.count_cart(cart)
    return {
        'cart_stats': cart_stats
    }
if __name__ == "__main__":
    app.run(debug=True)
