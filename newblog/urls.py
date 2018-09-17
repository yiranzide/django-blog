from django.conf.urls import url
from newblog.views import user_views, blog_views


urlpatterns = [
    url(r'^register/$', user_views.register, name='newblogregister'),
    url(r'^login/$', user_views.login, name='newbloglogin'),
    url(r'^addlog/$', blog_views.addBlog, name='newaddblog'),
    url(r'^bloglist/$', blog_views.blogList, name='newbloglist'),
    url(r'^detailblog/$', blog_views.detailBlog, name='newdetailblog'),
    url(r'^editblog/$', blog_views.editBlog, name='neweditblog'),
    url(r'^commentblog/$', blog_views.commentBlog, name='newcommentblog'),
    url(r'^delblog/$', blog_views.delBlog, name='newdelblog'),
    url(r'^search/$', blog_views.search, name='newsearch'),
    url(r'^logout/$', user_views.logout, name='newlogout'),
]