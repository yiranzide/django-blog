from django.shortcuts import render,redirect
from newblog.models import User
from newblog import models
from django.http import HttpResponse
from newblog.newblogform import newform
from django.core.urlresolvers import reverse #引入重定向的包
import redis


red = redis.Redis(host='localhost', port=6379, db=1)



#验证用户是否登录
def checkLogin(session):
    #session 键user_id如果不存在对应的值
    id = session.get('user_id',None)
    if id==None:
        #转到登录页面
        return False,redirect(reverse('newblog:newbloglogin'))
    else:
        return True,id


#增加博客内容
def addBlog(request):
    #强制登录验证
    boolValue,next=checkLogin(request.session)
    if not boolValue:
        return next
    if request.method == 'GET':
       blogform = newform.BlogForm()
       return render(request,'addblog.html',{'blogform':blogform})
    elif request.method == 'POST':
        submitForm = newform.BlogForm(request.POST,request.FILES)
        if submitForm.is_valid():
            newBlog = models.Blog()
            newBlog.pic = submitForm.cleaned_data['pic']
            newBlog.title = submitForm.cleaned_data['title']
            newBlog.content = submitForm.cleaned_data['content']
            newBlog.authorId = request.session['user_id']
            newBlog.save()
            red.set('readcount'+str(newBlog.id), 0)
            red.set(newBlog.id, 0)
            red.lpush('comment'+str(newBlog.id), {'context':'', 'user_id':0})
            return HttpResponse('发表成功.')
        else:
            errors = submitForm.errors
            return render(request,'addblog.html',{'blogform':submitForm, 'error':errors})


#显示博客列表
def blogList(request):
    boolValue,next=checkLogin(request.session)
    if not boolValue:
        return next
    userId = request.session.get('user_id')
    #查找authorId和session中和user_id一致的博客, 并且没有被删除的博客
    list = models.Blog.objects.filter(authorId=userId).filter(isDelete=1)
    for l in list:
        l.count = red.get(l.id).decode('utf-8')
        print(l.count)
    return render(request,'bloglist.html',{'blogs':list})


#显示博客文章内容
def detailBlog(request):
    boolValue,next=checkLogin(request.session)
    if not boolValue:
        return next
    #从选择器中提取博客ID
    blogId = request.GET.get('blogid',0) #默认为0
    blog = models.Blog.objects.get(pk=blogId)
    red.incr('readcount'+str(blogId))
    blog.readcount = red.get('readcount'+str(blogId)).decode('utf-8')
    comment = red.lrange('comment'+str(blogId), 0, -1)
    l = []
    for c in comment:
        c = c.decode('utf-8')
        c = eval(c)
        if c['user_id'] != 0:
           u = User.objects.get(pk=c['user_id'])
           c['name'] = u.username
           l.append(c)
    return render(request,'detailblog.html',{'blog':blog, 'l':l})


#修改博客内容
def editBlog(request):
    boolValue,next=checkLogin(request.session)
    if not boolValue:
        return next
    if request.method == 'GET':
        #从选择器中提取博客ID
        blogId = request.GET.get('blogid',0)
        blog = models.Blog.objects.get(pk=blogId)
        blogform = newform.BlogForm(initial={
                'title':blog.title,
                'content':blog.content,
                'pic':blog.pic
        })
        return render(request,'editblog.html',{'blogform':blogform,'id':blogId})
    elif request.method == 'POST':
        submitForm = newform.BlogForm(request.POST,request.FILES)
        id = request.POST.get('id',0)
        blogid = request.POST.get('blogid', 0)
        if submitForm.is_valid():
            user_id = request.session['user_id']
            #查找当前用户发表的博客
            # print(id)
            newBlog = models.Blog.objects.filter(id=blogid, isDelete=1)[0]
            newBlog.pic = submitForm.cleaned_data['pic']
            newBlog.title = submitForm.cleaned_data['title']
            newBlog.content = submitForm.cleaned_data['content']
            # newBlog.update(pic=submitForm.cleaned_data['pic'],
            #                title=submitForm.cleaned_data['title'],
            #                content=submitForm.cleaned_data['content'],
            #                id=blogid,
            #                )
            newBlog.save()
            return redirect(reverse('newblog:newbloglist')) #重定向到博客首页

        else:
            return render(request,'editblog.html',{'blogform':submitForm,'id':blogid})


#删除博客内容
def delBlog(request):
    boolValue,next=checkLogin(request.session)
    if not boolValue:
        return next
    if request.method == 'GET':
        blogId = request.GET.get('blogid',0)
        blog = models.Blog.objects.get(pk=blogId)
        if blog.authorId == request.session['user_id']:
            blog.isDelete=0
            blog.save()
            blog = models.Blog.objects.all().filter(isDelete=1)
            return redirect(reverse('newblog:newbloglist')) #重定向到博客首页
        else:
            return HttpResponse('抱歉，您无权进行此操作！！！')


#查找博客内容
def search(request):
    boolValue, next = checkLogin(request.session)
    if not boolValue:
        return next
    userId = request.session.get('user_id')
    #得到关键词
    keyword = request.GET.get('keyword',None)
    # 查找authorId和session中和user_id一致的博客
    list = models.Blog.objects.filter(authorId=userId).filter(isDelete=1).filter(title__contains=keyword)
    #注意这里的title__contains是双划线
    return render(request, 'bloglist.html', {'blogs': list})


# 评论博客内容
def commentBlog(request):
    boolValue, next = checkLogin(request.session)
    if not boolValue:
        return next
    if request.method == 'GET':
        blogId = request.GET.get('blogid', 0)
        blogform = newform.comment()
        return render(request, 'commentblog.html', {'blogform': blogform, 'id':blogId})
    elif request.method == 'POST':
        submitForm = newform.comment(request.POST, request.FILES)
        if submitForm.is_valid():
            comment = models.Comment()
            comment.context = submitForm.cleaned_data['context']
            comment.user_id = request.session['user_id']
            comment.blog_id = blogid = request.POST.get('blog_id', 0)
            comment.save()
            red.incr(comment.blog_id)
            dict = {
                'context': comment.context,
                'user_id': comment.user_id,
            }
            red.lpush('comment'+str(comment.blog_id), dict)
            return HttpResponse('评论成功.')
        else:
            errors = submitForm.errors
            return render(request, 'commentblog.html', {'blogform': submitForm, 'error': errors})

