from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('profile/<str:username>/', views.profile, name="profile"),
    path('profile/<str:username>/post/<int:id>/', views.post_detail, name="post-detail"),
    path('profile/<str:username>/post/<int:id>/delete', views.post_delete, name="post-delete"),
    path('edit/', views.edit, name="edit"),
    path('create/', views.create_post, name="create-post"),
    path('register/', views.register, name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)