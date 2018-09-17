from django.shortcuts import render, redirect
from newblog.models import User
from django.http import HttpResponse
from newblog.newblogform import newform
from newblog import models


# 注册功能
def register(request):
    # 判断请求方法
    if request.method == 'GET':
        form = newform.register()
        return render(request, 'register.html', {'form':form})
    elif request.method == 'POST':
        form = newform.register(request.POST)
        # 验证数据，返回指定数据是否有效的布尔值
        # clean会在form.is_valid()方法中被调用
        if form.is_valid():
            # cleaned_data属性访问干净数据
            # 获取数据库里面当前用户的记录，判断是否存在
            usertemp = User.objects.filter(username=form.cleaned_data['username']).exists()
            if usertemp == False:
                user = User()
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
                user.save()
                # 跳转到登录页面
                return HttpResponse('''注册成功!请登录.
                    <a href="/newblog/login">登录</a>''')
            else:
                error = '用户名已经存在，请重新注册!'
                return render(request, 'register.html', {'form': form, 'error': error})
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        loginform = newform.login()
        return render(request, 'login.html', {'loginform': loginform})
    elif request.method == 'POST':
        loginform = newform.login(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']

            user = models.User.objects.filter(username=username).filter(password=password)
            if user.exists():
                request.session['user_id'] = user[0].id

                return render(request, 'loginsuc.html')
            else:
                error = '用户名或者密码输入有误，请重试'
                return render(request, 'login.html', {'loginform': loginform, 'error': error})
        else:
            return render(request, 'login.html', {'loginform': loginform})
    else:
        return HttpResponse('request method get not supported')


#注销功能
def logout(request):
    userId = request.session.get('user_id',None)
    if not userId == None:
        del request.session['user_id']
        return HttpResponse('注销成功')
    else:
        return HttpResponse('你的操作不合法')
