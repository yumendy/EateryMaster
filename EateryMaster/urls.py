from django.conf.urls import patterns, include, url
from CookeryMaster import views, recommend
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EateryMaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^admin/$',views.admin),
    url(r'^admin/restaurant/add/$',views.addrestaurant),
    url(r'^admin/window/add/$',views.addwindow),
    url(r'^admin/dish/add/$',views.adddish),
    url(r'^admin/news/$', views.adminnews),

    url(r'^$',views.index),
    url(r'^signup/$', views.signup),
    url(r'^login/$', views.login),
    url(r'^logout/$',views.logout),
    url(r'^user/$', views.userpanel),

    url(r'^about/$',views.about),
    url(r'^guestbook/$',views.guestbook),
    url(r'^guestbook/reply/$',views.reply),
    url(r'^canteens/$',views.canteens),
    url(r'^windows/$',views.windows),
    url(r'^dishes/$',views.dishes),
    url(r'^recommend/$', recommend.recommend),
    url(r'^assessments/$', views.allassessments),
    url(r'^news/$', views.newsindex),
    url(r'^news/show/$', views.shownews),
    url(r'^news/del/$', views.delnews),
    url(r'^news/edit/$', views.editnews),
    url(r'^news/add/$', views.addnews),
    url(r'^news/addanno/$', views.addanno),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIAS_PATH}),
)
