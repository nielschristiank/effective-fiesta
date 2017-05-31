from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^register$', views.register, name="register"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^wish_items/create$', views.show_add_item, name="show_add_item"),
    url(r'^wish_items/create/add_item$', views.add_item, name="add_item"),
    url(r'^wish_items/(?P<id>\d+)$', views.show_item, name="show_item"),
    url(r'^wish_items/(?P<id>\d+)/add_wish_item$', views.add_wish_item, name="add_wish_item"),
    url(r'^wish_items/(?P<id>\d+)/remove_wish_item$', views.remove_wish_item, name="remove_wish_item"),
    url(r'^wish_items/(?P<id>\d+)/delete$', views.delete_item, name="delete_item"),
    url(r'^logout$', views.logout, name="logout")
]
