from django.conf.urls import patterns, include, url
from CookeryMaster import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EateryMaster.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),
    url(r'^signup/$', views.signup),
    url(r'^login/$', views.login),
    url(r'^logout/$',views.logout),
    url(r'^about/$',views.about),
    url(r'^guestbook/$',views.guestbook),
    url(r'^guestbook/reply/$',views.reply),
    url(r'^addrestaurant/$',views.addrestaurant),
    url(r'^adddish/$',views.adddish),
    url(r'^image/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIAS_PATH}),
)
