from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/new/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/edit/', views.sale_update, name='sale_update'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/xlsx/', views.export_xlsx, name='export_xlsx'),
    path('api/sales/summary/', views.sales_summary_api, name='sales_summary_api'),
]
