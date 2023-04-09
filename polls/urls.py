from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('photos/', views.PhotoView.as_view(), name='photo'),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),
    path('photos/add/', views.PhotoAddView.as_view(), name='photo_add'),
    path('photos/add/upload/', views.photo_upload, name='photo_upload'),
    path('photos/add/comment/', views.photo_comment, name='photo_comment'),
    path('photos/like/', views.photo_likes, name='photo_likes'),
]