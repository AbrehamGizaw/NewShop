from rest_framework.urls import path 
from .views import VendorDetail, SearchVendor

urlpatterns = [
    path('detail/', VendorDetail.as_view(),),
    path('search-vendor/', SearchVendor.as_view(), )
]