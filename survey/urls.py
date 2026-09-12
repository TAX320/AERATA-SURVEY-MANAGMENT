from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.global_search, name='global_search'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/partial/', views.project_list_partial, name='project_list_partial'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/export/', views.export_projects_csv, name='export_projects_csv'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/update-status/', views.update_project_status, name='update_project_status'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('projects/<int:pk>/add-deliverable/', views.add_deliverable, name='add_deliverable'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/partial/', views.client_list_partial, name='client_list_partial'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
]