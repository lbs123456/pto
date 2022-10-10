from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
import os
from pto import app, db
from pto.models import User, Usern, Intro
from PIL import Image
count=5

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = Usern.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('home'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('home'))  # 重定向回首页


allowed_extensions = set(['png', 'jpg', 'jpg', 'png', 'gif', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/add', methods=['GET', 'POST'])

def add():

    if request.method == 'POST':
        global count
        img = request.files.get('photo')
        name = request.form.get('name')
        age = request.form.get('age')
        height = request.form.get('height')
        gender = request.form.get('gender')
        origo = request.form.get('origo')
        path = basedir + "\static\\"
        new_filename =f"{count}" + '.' + "png"
        file_path = path + new_filename
        img.save(file_path)
        sImg = Image.open(file_path)
        dImg = sImg.resize((130, 150), Image.ANTIALIAS)
        dImg.save(file_path)
        if not (gender =='男' or  gender =='女'):
            flash('gender Invalid input.')
            return redirect(url_for('add'))

        names = User(name=name)
        db.session.add(names)
        intros = Intro(age=age, height=height, gender=gender, origo=origo,user_id=count)
        db.session.add(intros)
        db.session.commit()
        count = count + 1
        flash('Item created.')
        return redirect (url_for('home'))
    return render_template("add.html")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/introduce')
def introduce():
    return render_template("introduce.html")


@app.route('/detail/<name>')
@app.route('/detail/<int:id>')
def detail(id):
    user=User.query.get(id)
    adr =f'{id}.png'
    return render_template("detail.html",user=user,adr=adr)




@app.route('/movie/delete/<int:id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(id):
    user = User.query.get_or_404(id)  # 获取电影记录
    intro = Intro.query.get_or_404(id)
    db.session.delete(user)
    db.session.delete(intro)
    # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    path1 = basedir + "\static\\"
    new_filename = f"{id}" + '.' + "jpg"
    path = path1 + new_filename
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)
    flash('Item deleted.')
    return redirect(url_for('home'))  # 重定向回主页

