from django.urls import path
from notifications.views import SubscribeForNewsLetter, SubscriberList, SubscriberCreate, SubscriberDetail, ImageCreate, ImageList, ImageDetail, NewsletterList, NewsletterCreate, NewsletterDetail, NewsletterSentList, NewsletterSentCreate, NewsletterSentDetail, NewsTagList, NewsTagCreate, NewsTagDetail, TagCategoryList, TagCategoryCreate, TagCategoryDetail


app_name = "notification"
urlpatterns = [
    path('subscribe_newsletter/',SubscribeForNewsLetter.as_view(), name='subscribe_newsletter'),

    path('subscriberlist/', SubscriberList.as_view()),
    path('subscribercreate/', SubscriberCreate.as_view()), 
    path('subscriberdetail/', SubscriberDetail.as_view()),
    path('newsletterlist/', NewsletterList.as_view()),
    path('newslettercreate/', NewsletterCreate.as_view()), 
    path('newsletterdetail/', NewsletterDetail.as_view()),
    path('imagelist/', ImageList.as_view()),
    path('imagecreate/', ImageCreate.as_view()), 
    path('imagedetail/', ImageDetail.as_view()),
    path('newsletterSentlist/', NewsletterSentList.as_view()),
    path('newsletterSentcreate/', NewsletterSentCreate.as_view()), 
    path('newsletterSentdetail/', NewsletterSentDetail.as_view()),
    path('newstaglist/', NewsTagList.as_view()),
    path('newstagcreate/', NewsTagCreate.as_view()), 
    path('newstagdetail/', NewsTagDetail.as_view()),
    path('tagcategorylist/', TagCategoryList.as_view()),
    path('tagcategorycreate/', TagCategoryCreate.as_view()), 
    path('tagcategorydetail/', TagCategoryDetail.as_view()),


]

