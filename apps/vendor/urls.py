from django.urls import path
from vendor.views import VendorList, VendorCreate, VendorDetail, ImageCreate, ImageList, ImageDetail, VendorContentList, VendorContentCreate, VendorContentDetail, VendorAddressList, VendorAddressCreate, VendorAddressDetail, VendorWhyList, VendorWhyCreate, VendorWhyDetail, VendorSocialMediaList, VendorSocialMediaCreate, VendorSocialMediaDetail, VendorCategoryCreate, VendorCategoryList, VendorCategoryDetail


app_name = "vendor"
urlpatterns = [
    path('vendorlist/', VendorList.as_view()),
    path('vendorcreate/', VendorCreate.as_view()), 
    path('vendordetail/<int:pk>', VendorDetail.as_view()),
    path('vendorcategorylist/', VendorCategoryList.as_view()),
    path('vendorcategorycreate/', VendorCategoryCreate.as_view()), 
    path('vendorcategorydetail/<int:pk>', VendorCategoryDetail.as_view()),
    path('vendorcontentlist/', VendorContentList.as_view()),
    path('vendorcontentcreate/', VendorContentCreate.as_view()), 
    path('vendorcontentdetail/<int:pk>', VendorContentDetail.as_view()),
    path('imagelist/', ImageList.as_view()),
    path('imagecreate/', ImageCreate.as_view()), 
    path('imagedetail/<int:pk>', ImageDetail.as_view()),
    path('vendoraddresslist/', VendorAddressList.as_view()),
    path('vendoraddresscreate/', VendorAddressCreate.as_view()), 
    path('vendoraddressdetail/<int:pk>', VendorAddressDetail.as_view()),
    path('vendorwhylist/', VendorWhyList.as_view()),
    path('vendorwhycreate/', VendorWhyCreate.as_view()), 
    path('vendorwhydetail/<int:pk>', VendorWhyDetail.as_view()),
    path('vendorsocialmedialist/', VendorSocialMediaList.as_view()),
    path('vendorsocialmediacreate/', VendorSocialMediaCreate.as_view()), 
    path('vendorsocialmediadetail/<int:pk>', VendorSocialMediaDetail.as_view()),


]

