from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat,Group,GroupType,UserProfile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        exclude = ['is_active']

class GroupTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupType
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True,read_only=True)
    type = GroupTypeSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    class Meta:
        model = Group
        fields = '__all__'
        
class ChatSerializer(serializers.ModelSerializer):
    send_by = UserProfileSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    def get_fields(self):
        fields = super(ChatSerializer, self).get_fields()
        fields['subcategories'] = ChatSerializer(read_only=True)
        return fields
    class Meta:
        model = Chat
        exclude = ['is_active']
