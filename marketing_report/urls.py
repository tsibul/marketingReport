from django.urls import path
from . import views

app_name = 'marketing_report'

urlpatterns = [
    path('', views.index, name='main'),
    path('report/', views.reports, name='reports'),
    path('json_report/<int:report_no>/<str:report_type>/<str:period>/<str:date_begin>/<str:date_end>/<str:argument>',
         views.json_periods, name='json_report'),

    path('customer/', views.customer, name='customer'),


    path('dictionary/', views.dictionary, name='dictionary'),
    path('dictionary_last_id/<str:dict_type>', views.dictionary_last_id, name='dictionary_last_id'),
    path('dict_update/<str:dict_type>', views.dictionary_update, name='dictionary_update'),
    path('dict_delete/<str:dict_type>/<int:id_no>', views.dictionary_delete, name='dictionary_delete'),
    path('json_dict_next_20/<str:dict_type>/<int:id_no>/<str:order>/<str:search_string>', views.dictionary_json,
         name='dictionary_json'),

    path('imports/', views.imports, name='imports'),
    path('import_file/', views.import_file, name='import_file'),
    path('edit_temporary_base/', views.edit_temporary_base, name='edit_temporary_base'),
    path('import_new_customers/', views.customers_new_to_main_db, name='import_new_customers'),
    path('import_changed_customers/', views.customer_change_to_customer, name='import_changed_customers'),

    path('admin/', views.admin, name='admin_site'),
    path('customer_export/', views.customer_export, name='customer_export'),
    path('goods_export/', views.goods_export, name='goods_export'),
    path('customer_group_json/', views.customer_group_json, name='customer_group_json'),

]
