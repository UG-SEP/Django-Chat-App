from django.urls import path
from .views import Home,Search,update_last_seen
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('group/search-result/',Search.as_view(),name='search-group'),
    path('user/update-last-seen',update_last_seen,name='update-last-seen'),
]