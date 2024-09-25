from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import UserUpdateView,MyGroupsListView,editGroup,getGroup,createGroup,deleteGroup
from Chat.models import Group
urlpatterns = [
    path('',UserUpdateView.as_view(),name='profile'),
    path('my-groups/',MyGroupsListView.as_view(),name='my-groups'),
    path('edit-group/',editGroup,name='edit-group'),
    path('get-group/',getGroup,name='get-group'),
    path('create-group/',createGroup,name='create-group'),
    path('delete-group/',deleteGroup,name='delete-group')
]