from pickle import FRAME

from flask import Flask, render_template, session, redirect, url_for
from app.models import *
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/profile')
def profile():
    # Kiểm tra nếu người dùng đã đăng nhập
    if 'user_id' in session:
        # Lấy thông tin user từ cơ sở dữ liệu hoặc session
        user_info = {
            "name": "Nguyễn Văn A",
            "email": "nguyenvana@example.com",
        }
        return render_template('profile.html', user=user_info)
    else:
        # Nếu chưa đăng nhập, chuyển hướng về trang đăng nhập
        return redirect(url_for('login'))


@app.route('/cart')
def cart():
    # Ví dụ về danh sách sản phẩm/dịch vụ trong giỏ hàng
    cart_items = [
        {"name": "Phòng Đơn", "price": 1000000, "quantity": 1},
        {"name": "Phòng Đôi", "price": 1800000, "quantity": 1},
        {"name": "Dịch vụ Spa", "price": 500000, "quantity": 2}
    ]

    # Tính tổng giá
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)




if __name__ == "__main__":
    app.run(debug=True)