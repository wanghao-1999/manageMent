from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login'),  # 设置登陆页面URL对应的视图函数
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),    # 设置文档管理页面URL对应的视图函数
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 使用Django自带的LogoutView
    path('upload/', views.upload_document, name='upload_document'),
    path('batch_upload/', views.batch_upload_document, name='batch_upload_document'),
    path('preview/<int:document_id>/', views.preview_document, name='preview_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('request_preview/<int:document_id>/', views.request_preview, name='request_preview'),
    path('edit_document/<int:document_id>/', views.edit_document, name='edit_document'),

    path('payment_terms/', views.payment_terms_list, name='payment_terms_list'),
    path('payment_terms/add/', views.add_payment_term, name='add_payment_term'),
    path('payment_terms/edit/<int:payment_term_id>/', views.edit_payment_term, name='edit_payment_term'),
    path('payment_terms/delete/<int:payment_term_id>/', views.delete_payment_term, name='delete_payment_term'),



    # 添加其他URL配置
]


