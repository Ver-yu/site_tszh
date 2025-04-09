from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum, name='forum'),
    path('vote/<int:option_id>/', views.vote, name='vote'),
    path('create/', views.create_post, name='create_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

]