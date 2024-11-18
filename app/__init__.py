from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = "1234567890!@#$%^&*()qwertyuioplkjhgfdsazxcvbnm,./ASDFGHJKLZMXNCBVQWERTYUIOP"
app.config["SQLALCHEMY_DATABASE_URI"] = ("mysql+pymysql://root:%s@localhost/dbhotel?charset=utf8mb4"
                                         % quote("d@Ikaquan2301"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6


db = SQLAlchemy(app)

admin = Admin(app, name='Quản lý Khách Sạn', template_mode='bootstrap4')