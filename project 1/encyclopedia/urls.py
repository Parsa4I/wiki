from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki', views.index, name='wiki'),
    path('wiki/<str:title>', views.entry, name='entry'),
    path('newpage', views.newpage, name='newpage'),
    path('random', views.randent, name='randent'),
    path('wiki/abc/<str:abc>', views.abc, name='abc')
]
