from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include('hello.urls')),
    path(r'api/', include('tutorials.urls')), #r is to include raw strings, like 
    # eg r'\n' is equivalent of the '\\n'
    path(r'api/', include('customers.urls'))
]
