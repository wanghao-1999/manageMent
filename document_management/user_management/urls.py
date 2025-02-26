from django.urls import path
from . import views

urlpatterns = [
    path('user-list/', views.user_list, name='user_list'),
    path('department/', views.department_settings, name='department_settings'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('department-list/', views.department_list, name='department_list'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    # 添加其他 URL 配置
]
