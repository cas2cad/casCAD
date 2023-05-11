from flask import Blueprint, render_template, redirect, url_for, request, flash
from cascad.models.datamodel import User
from flask_login import login_user

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login_post():
    # 获取表单数据
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        password = request.form['password']

        # 查询用户名和密码是否正确
        user = User.objects(username=username).first()
        if user and user.check_password(password):  
            login_user(user,force=True)  # 登录成功
            return redirect(url_for('home_bp.index'))
        else:
            flash('Invalid username or password.')  # 登录失败,显示错误消息
    return render_template('login.html')

@auth_bp.route('/register')
def register():
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register_post():
    # 获取表单数据
    username = request.form['username']
    password = request.form['password']

    # 查询用户名是否存在
    user = User.objects(username=username).first()
    if user:
        flash('Username already exists.')  # 用户名已存在,显示错误消息
        return redirect(url_for('auth_bp.register'))

    # 用户名不存在,创建新用户
    user = User(username=username)
    user.hash_password(password) 
    user.save()

    # 注册成功,跳转到登录页面
    flash('Registration successful.')
    return redirect(url_for('auth_bp.login_post'))
