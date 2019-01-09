# coding: utf-8
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User, Order, UserPermission
from .forms import LoginForm, RegisterForm, OrderForm, PayForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.account.data).first()

        if user is None:
            user = User.query.filter_by(user_code=form.account.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash(u'登陆成功！欢迎回来，{}'.format(user.email), 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('auth/register.html', form=form)
    elif form.validate_on_submit():
        intro = User.query.filter_by(user_code=form.introduce_user_code.data).first()
        if intro is None:
            flash(u'注册失败！，没有找到用户代码对应的推荐人!', 'danger')
            return render_template('auth/register.html', form=form)
        elif form.password.data == form.password_repeat.data:
            user = User.create(
                email=form.email.data,
                qq=form.qq.data,
                phone=form.phone.data,
                wechat=form.wechat.data,
                introduce_user_code=form.introduce_user_code.data,
                password=form.password.data,
                role=UserPermission.NORMAL)
            if user is not None:
                login_user(user)
                flash(u'注册成功！欢迎，{}!'.format(user.email), 'success')
                return redirect(url_for('main.index'))
            else:
                flash(u'注册失败！创建用户【{}】失败'.format(user), 'danger')
    if form.errors:
        flash(u'注册失败,错误信息:{}'.format(form.errors), 'danger')

    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('main.index'))


@auth.route('/withdraw')
@login_required
def withdraw():
    return redirect(url_for('main.index'))


@auth.route('/order', methods=['POST'])
@login_required
def order():
    form = OrderForm()
    if form.validate_on_submit():
        if form.count.data < 0:
            flash(u'提交失败！不能小于0!', 'danger')
            return redirect(url_for('auth.order'))
        else:
            flash(u'提交成功!', 'success')
            u = User.query.filter_by(id=current_user.id).first()
            if u.user_code.data > 0:
                o = Order.create(
                    user_code=u.user_code,
                    introduce_user_code=u.introduce_user_code,
                    email=u.email,
                    number=form.count.data
                )
                flash(u'提交失败,错误信息:{}'.format(form.errors), 'danger')
                return o

    if form.errors:
        flash(u'提交失败,错误信息:{}'.format(form.errors), 'danger')
    return redirect(url_for('auth.order'))


@auth.route('/user', methods=['GET'])
@login_required
def user():
    u = current_user
    form = PayForm()
    if u.is_anonymous:
        flash(u'匿名用户！')
        return redirect(url_for('main.index'))
    else:
        u = User.query.filter_by(id=u.id).first()
        register_from_me = User.query.filter_by(introduce_user_code=u.user_code).all()
        payed = [user for user in register_from_me if user.user_code is not None and len(user.user_code) > 0]

        def calculate(o):
            step = 15000
            accounts = o.accounts
            commission = 0
            weight = 1.0
            while True:
                accounts -= step
                commission += weight * 5000
                weight -= 0.1
                if weight < 0.1 or accounts < step:
                    return commission

        os_ = []
        for p in payed:
            o = Order.query.filter_by(user_code=p.user_code).filter_by(enable=True).first()
            commission = calculate(o)

            os_.append({
                'commission': commission,
                'code': o.user_code,
                'date': o.created_time,
            })

        all_commission = 0
        for o in os_:
            all_commission += o['commission']

        code = u.user_code if len(u.user_code) > 0 else u.email
        msg = {
            'user_code': code,
            'register_from_me': register_from_me,
            'payed': os_,
            'withdraw': u.withdraw,
            'all_commission': all_commission,
            'rest': all_commission - u.withdraw
        }

        return render_template('auth/user.html', form=form, msg=msg)
