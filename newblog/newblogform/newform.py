from django.forms import Form, widgets, ValidationError, fields
from django.core.validators import RegexValidator
import re


class register(Form):
    username = fields.CharField(max_length=10, min_length=5)
    password = fields.CharField(max_length=10, min_length=5, widget=widgets.PasswordInput)
    repassword = fields.CharField(max_length=10, widget=widgets.PasswordInput)

    def clean(self):
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['repassword']
        if not password == repassword:
            myerror = '两次密码不一致,请重新输入'
            raise ValidationError(myerror)
        return self.cleaned_data


class login(Form):
    username = fields.CharField(max_length=10)
    password = fields.CharField(max_length=10, widget=widgets.PasswordInput)


# 自定义验证规则
# def pic_validate(value):
#     print('ij')
#     pic_re = re.compile(r'^.+[jpg|gif|png]$')
#     if not pic_re.match(str(value)):
#         raise ValidationError('图片格式错误')
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class BlogForm(Form):
    title = fields.CharField(max_length=20,
                            min_length=5,
                            error_messages={'required': '标题不能为空',
                                            'min_length': '标题最少为5个字符',
                                            'max_length': '标题最多为20个字符'},
                            widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'placeholder': '标题5-20个字符'}))
    content = fields.CharField(min_length=10,
                            error_messages={'required': '内容不能为空',
                                            'min_length': '内容最少为10个字符'},
                            widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'placeholder': '内容最少10个字符'}))
    pic = fields.ImageField(required=True,
                            error_messages={'required': '图片不能为空','invalid': '图片格式错误'})


class comment(Form):

    context = fields.CharField(min_length=5,
                            error_messages={'required': '内容不能为空',
                                            'min_length': '内容最少为5个字符'},
                            widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'placeholder': '内容最少5个字符'}))
