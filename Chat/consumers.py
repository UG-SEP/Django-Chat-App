from channels.exceptions import StopConsumer
import json
from .models import Group,Chat,UserProfile
import datetime
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from Chat.serializers import ChatSerializer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
class ChatConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        print("Websocket connect!")
        await database_sync_to_async(self.change_status)(True)
        self.grpslug = self.scope['url_route']['kwargs']['grpslug']
        await self.channel_layer.group_add(self.grpslug,self.channel_name)
        if self.scope['user'] != AnonymousUser:
            await self.accept()

    async def receive_json(self,content,**kwargs):
        if content['action'] == 'add':
            json_data = await database_sync_to_async(save_to_database)(self.scope['user'],self.grpslug,content)
            await self.channel_layer.group_send(self.grpslug,
            {
                'type' : 'message.action',
                'data' : json.dumps(json_data)
            })
        elif(content['action']=='delete'):
            chat_id = await database_sync_to_async(delete_from_database)(content['msg_id'])
            chat_id['action']='delete'
            await self.channel_layer.group_send(self.grpslug,
            {
                'type' : 'message.action',
                'data' : json.dumps(chat_id)
            })
        elif(content['action']=='edit'):
            json_data = await database_sync_to_async(edit_to_database)(content)
            
            await self.channel_layer.group_send(self.grpslug,{
                'type' : 'message.action',
                'data' : json.dumps(json_data)
            })

    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.grpslug,self.channel_name)
        await database_sync_to_async(self.change_status)()
        self.close()
        raise StopConsumer()
    
    async def message_action(self,event):
        await self.send(event['data'])
    
    def change_status(self,status=False):
        profile = UserProfile.objects.select_related('user').get(user=self.scope['user'])
        profile.status = status
        profile.save()

def save_to_database(user,grpslug,content):
        group = Group.objects.prefetch_related('members').select_related('type').get(slug=grpslug)
        profile = UserProfile.objects.select_related('user').get(user=user)
        chat=Chat.objects.create(message=content['msg'],group=group,send_by=profile,timestamp=datetime.datetime.now())
        if 'reply_id' in content:
            print(chat)
            chat.reply_to = Chat.objects.select_related('send_by','group','reply_to').get(id=content['reply_id'])
        chat.save()
        json_data = ChatSerializer(chat).data
        json_data['action'] = 'add'
        return json_data 

def delete_from_database(chat_id):
    chat = Chat.objects.get(id=chat_id)
    chat.is_active = False
    chat.save()
    return {'id':chat_id}

def edit_to_database(content):
    chat = Chat.objects.select_related('send_by','group','reply_to').get(id=content['msg_id'])
    chat.message = content['msg']
    chat.timestamp = datetime.datetime.now()
    chat.is_edited = True
    chat.save()
    json_data = ChatSerializer(chat).data
    json_data['action']='edit'
    return json_data