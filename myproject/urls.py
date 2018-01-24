"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as account_views
from boards import views as blog_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$',account_views.signup,name='signup'),
    url(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'^$',blog_views.home,name='home'),
    url(r'^boards/(?P<pk>\d+)/$',blog_views.board_topics,name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', blog_views.new_topic, name='new_topic'),
]
