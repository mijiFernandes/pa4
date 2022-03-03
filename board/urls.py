from django.urls import path, re_path
from board import views

app_name = 'board'

urlpatterns = [
    # Example: /blog/
    path('', views.PostLV.as_view(), name='index'),

    # Example: /blog/post/
    path('post/', views.PostLV.as_view(), name='post_list'),

    # Example: /blog/post/django-example/ 한글도 인식 가능
    re_path(r'^post/(?P<slug>[-\w]+)/$', views.PostDV.as_view(), name='post_detail'),

    path('add/', views.PostCreateView.as_view(), name='add'),

    path('change/', views.PostChangeLV.as_view(), name='change'),

    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),

    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    ]
