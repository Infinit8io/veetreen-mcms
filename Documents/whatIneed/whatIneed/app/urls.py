"""whatIneed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from app import views
from app.views import EventCreate, EventUpdate, Items, BringItems

urlpatterns = [
    url(r'^$', views.landing_page, name="homepage"),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^create/$', EventCreate.as_view(), name='create-event'),
    url(r'^update/(?P<id>[0-9]+)/$',EventUpdate.as_view(),name='event-update'),
    url(r'^show/(?P<slug>[\w\-]+)/$', views.event, name='show-event'),
    url(r'^items/(?P<slug>[\w\-]+)/$', Items.as_view(), name='item-add'),
    url(r'^go/(?P<slug>[\w\-]+)/$', views.go_to, name='go-to'),
    url(r'^show/(?P<slug>[\w\-]+)/bring/(?P<item_id>[0-9]+)/$',BringItems.as_view(), name="bring-item")
]
