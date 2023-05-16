#urls to be matched with request functions in the views
from django.urls import path
from customers import views 
 
 
app_name = "customers"

urlpatterns = [ 
    path(r'customer', views.customer_list),
    path(r'customercsv', views.customer_listcsv),
    path(r'customer/company', views.company_list),
    path(r'customer/<str:company>', views.customer_company),
    path(r'customer/updatedelete/<int:pk>', views.customer_detail),
    path(r'customer/getbyid/<int:pk>', views.customer_getbyid),
    path(r'companysearch/<str:company>', views.companies_fuzzysearch),
    path(r'deleteall', views.customers_deleteall),
]