from django.urls import path 
from .views import Index, JoinForm, SocialMedias, VendorView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'socialMedias', SocialMedias)
router.register(r'vendors', VendorView)

urlpatterns = [
    path('index/', Index.as_view()),
    path('join/', JoinForm.as_view()),
    # path('vendor/', VendorView)
    
] 

urlpatterns += router.urls
