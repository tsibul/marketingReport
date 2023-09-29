from django.urls import path
from . import views

app_name = 'marketing_report'

urlpatterns = [
    path('', views.index, name='main'),
    path('report/', views.reports, name='reports'),
    path('/json_report/<int:report_no>/<str:report_type>/<str:period>/<str:date_begin>/<str:date_end>/<str:argument>',
         views.json_periods, name='json_report'),
    path('dictionary/', views.dictionary, name='dictionary'),
    path('imports/', views.imports, name='imports'),
    path('admin/', views.admin, name='admin_site'),
    path('customer_export/', views.customer_export, name='customer_export'),
    path('dict_update/<str:dict_type>', views.dictionary_update, name='dictionary_update'),
    path('json_dict_next_20/<str:dict_type>/<int:id_no>/<str:order>', views.dictionary_json, name='dictionary_json'),
    path('customer_group_json/', views.customer_group_json, name='customer_group_json'),

]
