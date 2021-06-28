from django.urls import path
from . import views

urlpatterns=[
    path('', views.dashboard),
    path('logout', views.logout),
    path('new', views.new),
    path('remove/<int:wish_id>', views.remove),
    path('edit/<int:wish_id>', views.edit),
    path('granted/<int:wish_id>', views.granted),
    path('update/<int:wish_id>', views.update),
    path('add_wish', views.add_wish),
    path('likes/<int:wish_id>', views.likes),
    path('stats', views.stats),
]