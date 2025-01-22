from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/sections/', views.SectionListView.as_view(), name='section_list'),
    path('manage/sections/add/', views.SectionCreateView.as_view(), name='section_add'),
    path('manage/sections/edit/<int:pk>/', views.SectionUpdateView.as_view(), name='section_edit'),
    path('manage/sections/delete/<int:pk>/', views.SectionDeleteView.as_view(), name='section_delete'),
    
    path('manage/users/', views.UserListView.as_view(), name='user_list'),
    path('manage/users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('manage/users/edit/<int:pk>/', views.UserUpdateView.as_view(), name='user_edit'),
    path('manage/users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]
