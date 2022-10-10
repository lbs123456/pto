from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from pto import db


class Usern(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    __tablename__ ="user"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    intros = db.relationship("Intro", backref="user")

class Intro(db.Model):  # 表名将会是 intro
    __tablename__ ="intro"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    height = db.Column(db.String(3))  #
    age = db.Column(db.String(2))  #
    gender = db.Column(db.Enum("男", "女"), nullable=False)
    origo = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

