#urls to be matched with request functions in the views
from django.urls import re_path,path
from tutorials import views 
 
 
app_name = "tutorials"

urlpatterns = [ 
    path(r'tutorials', views.tutorial_list),
    path(r'tutorials/<int:pk>', views.tutorial_detail),
    path('tutorials/published', views.tutorial_list_published)
    # re_path(r'api/tutorials', views.tutorial_list),
    # re_path(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    # re_path(r'^api/tutorials/published$', views.tutorial_list_published)
]