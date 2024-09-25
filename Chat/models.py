from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class GroupType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.type 

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user')
    img = models.ImageField(null=True,blank=True,upload_to='profile_pic',default='profile_pic/profile.png')
    country_name = models.CharField(max_length=100,null=True,blank=True)
    last_seen = models.DateTimeField(null=True,blank=True,auto_now=True)
    phone_no = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=True) 
    about = models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.user.username
    

class Group(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True)
    type = models.ForeignKey(GroupType,on_delete=models.CASCADE,null=True,blank=True,related_name='type_name')
    members = models.ManyToManyField(UserProfile,blank=True,related_name='members')
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    members_count = models.BigIntegerField(default=0,null=True,blank=True)
    img = models.ImageField(upload_to='groups_pics',default='groups_pics/group.png',null=True,blank=True)
    description = models.TextField(default='Welcome to the group')
    def __str__(self) -> str:
        return self.name


class Chat(models.Model):
    message = models.CharField(max_length=1000)
    file = models.FileField(upload_to='chat-files/',null=True,blank=True)
    send_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='send_by')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='group')
    timestamp = models.DateTimeField(auto_now=True,null=True,blank=True)
    ftype = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    reply_to = models.ForeignKey('self',null=True,blank=True,unique=False,on_delete=models.SET_NULL,related_name='reply')


