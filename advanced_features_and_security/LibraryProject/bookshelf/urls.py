from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('edit/<int:book_id>/', views.book_edit, name='book_edit'),
    path('delete/<int:book_id>/', views.book_delete, name='book_delete'),
    path('example-form/', views.example_form_view, name='example_form'),
    path('secure-demo/', views.secure_form_demo, name='secure_demo'),
]
