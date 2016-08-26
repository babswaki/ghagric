from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<page>[1-9]+)/$', views.IndexView.as_view(), name='index_page'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<post_id>[0-9]+)/(?P<slug>[-\w\d]+)/$', views.detail, name='detail'),
    url(r'^detail/(?P<post_id>[0-9]+)/(?P<slug>[-\w\d]+)/$', views.detail, name='detail'),
    # url(r'^month/$', views.month, name='month'),
    # Example: /2012/aug/
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        views.PostMonthArchiveView.as_view(),name="archive_month"),

    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^detail/$', views.detail, name='detail'),


    url(r'^hello/', views.hello),
]
