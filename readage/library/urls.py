from django.conf.urls import patterns, url

from library import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^search/$', views.search, name='search'),
    url(r'^book/(\d+)/$', views.book, name='book'),
    url(r'^comment/(\d+)/$', views.comment, name='comment'),
    url(r'^ajax/comment/(\d+)/$', views.ajax_comment, name='ajax_comment'),

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user/$', views.user, name='user'),
    url(r'^user/edit/$', views.user_edit, name='user_edit'),
    url(r'^user/upward/$', views.user_upward, name='user_upward'),
    url(r'^user/forget/$', views.user_forget, name='user_forget'),
    url(r'^feedback/$', views.feedback, name='feedback'),

    url(r'^queue/(\d+)/$', views.queue, name='queue'),
    url(r'^reborrow/(\d+)/$', views.reborrow, name='reborrow'),
    url(r'^queue/(\d+)/del/$', views.queue_del, name='queue_del'),

    url(r'^borrow/(\d+)/u(\d+)/$', views.borrow, name='borrow'),
    url(r'^return/(\d+)/$', views.back, name='return'),
    url(r'^next/(\d+)/u(\d+)/$', views.queue_next, name='queue_next'),
    url(r'^readify/(\d+)/$', views.readify, name='readify'),
    url(r'^disappear/(\d+)/$', views.disappear, name='disappear'),

    url(r'^book/add/$', views.book_add, name='book_add'),
    url(r'^book/(\d+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^book/(\d+)/add/$', views.copy_add, name='copy_add'),
    url(r'^copy/(\d+)/del/$', views.copy_del, name='copy_del'),
    url(r'^comment/(\d+)/del/$', views.comment_del, name='comment_del'),

    url(r'^(reg_pass|upward|downward)/u(\d+)/$', views.updown, name='updown'),

    url(r'^admin/book/$', views.ad_book, name='ad_book'),
    url(r'^admin/user/$', views.ad_user, name='ad_user'),
    url(r'^ajax/myuser/$', views.ajax_myuser, name='ajax_myuser'),

    url(r'^info/list/$', views.info, name='info'),
    url(r'^info/(\d+)/$', views.info_detail, name='info_detail'),
    url(r'^info/add/$', views.info_add, name='info_add'),

    url(r'^rank/$', views.rank, name='rank'),
    url(r'^rank/(\d+)/$', views.rank, name='rank_old'),
    )
