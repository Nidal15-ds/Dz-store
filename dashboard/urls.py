from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),

    path('products/', views.product_list, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('orders/', views.order_list, name='orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    path('report/', views.report, name='report'),
    path('settings/', views.settings_view, name='settings'),
]
