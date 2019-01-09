# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Optional


class LoginForm(Form):
    account = StringField(u'身份代码或邮箱', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])


class OrderForm(Form):
    count = IntegerField(u'身份代码或邮箱', validators=[DataRequired()])


class PayForm(Form):
    count = IntegerField(u'支付金额', validators=[DataRequired()])


class RegisterForm(Form):
    introduce_user_code = StringField(u'推荐人身份代码', validators=[DataRequired()])

    qq = StringField(u'您联系我时用的QQ', validators=[DataRequired()])
    phone = StringField(u'手机号,如果需要一折试用就需要填写,不需要则可以不填', validators=[Optional()])
    wechat = StringField(u'您打算用哪个微信号码和我联系', validators=[DataRequired()])
    email = StringField(u'您通过哪个电子邮件接收数据', validators=[DataRequired(), Email()])
    password = StringField(u'密码', validators=[DataRequired()])
    password_repeat = PasswordField(u'重复您的密码', validators=[DataRequired()])
