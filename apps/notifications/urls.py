from django.urls import path
from notifications.views import SubscribeForNewsLetter, SubscriberList, SubscriberCreate, SubscriberDetail, ImageCreate, ImageList, ImageDetail, NewsletterList, NewsletterCreate, NewsletterDetail, NewsletterSentList, NewsletterSentCreate, NewsletterSentDetail, NewsTagList, NewsTagCreate, NewsTagDetail, TagCategoryList, TagCategoryCreate, TagCategoryDetail


app_name = "notification"
urlpatterns = [
    path('subscribe_newsletter/',SubscribeForNewsLetter.as_view(), name='subscribe_newsletter'),

    path('subscriberlist/', SubscriberList.as_view()),
    path('subscribercreate/', SubscriberCreate.as_view()), 
    path('subscriberdetail/<int:pk>', SubscriberDetail.as_view()),
    path('newsletterlist/', NewsletterList.as_view()),
    path('newslettercreate/', NewsletterCreate.as_view()), 
    path('newsletterdetail/<int:pk>', NewsletterDetail.as_view()),
    path('imagelist/', ImageList.as_view()),
    path('imagecreate/', ImageCreate.as_view()), 
    path('imagedetail/<int:pk>', ImageDetail.as_view()),
    path('newslettersentlist/', NewsletterSentList.as_view()),
    path('newslettersentcreate/', NewsletterSentCreate.as_view()), 
    path('newslettersentdetail/<int:pk>', NewsletterSentDetail.as_view()),
    path('newstaglist/', NewsTagList.as_view()),
    path('newstagcreate/', NewsTagCreate.as_view()), 
    path('newstagdetail/<int:pk>', NewsTagDetail.as_view()),
    path('tagcategorylist/', TagCategoryList.as_view()),
    path('tagcategorycreate/', TagCategoryCreate.as_view()), 
    path('tagcategorydetail/<int:pk>', TagCategoryDetail.as_view()),


]

