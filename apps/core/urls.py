from django.urls import path
from core.views import  SocialMediaList, SocialMediaCreate, SocialMediaDetail, TermsAndConditionsList, TermsAndConditionsCreate, TermsAndConditionsDetail, WhyUsItemList, WhyUsItemCreate, WhyUsItemDetail
app_name = "core"
urlpatterns = [

    path('socialmedialist/', SocialMediaList.as_view()),
    path('socialmediacreate/', SocialMediaCreate.as_view()), 
    path('socialmediadetail/<int:pk>', SocialMediaDetail.as_view()),
    path('termsandconditionslist/', TermsAndConditionsList.as_view()),
    path('termsandconditionscreate/', TermsAndConditionsCreate.as_view()), 
    path('termsandconditionsdetail/<int:pk>', TermsAndConditionsDetail.as_view()),
    path('whyusitemlist/', WhyUsItemList.as_view()),
    path('whyusitemcreate/', WhyUsItemCreate.as_view()), 
    path('whyusitemdetail/<int:pk>', WhyUsItemDetail.as_view()),

]

