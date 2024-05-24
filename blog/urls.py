from django.urls import path
from . import views

urlpatterns = [

    path("", views.PostListView.as_view(), name="josram-blog"),
    path("<slug:slug>", views.PostDetails.as_view(), name="post-detail-page"),

]