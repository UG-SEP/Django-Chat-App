import json
from django.shortcuts import render,redirect
import datetime
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from channels.layers import get_channel_layer
from .models import Chat,Group,UserProfile
from asgiref.sync import async_to_sync 
from django.contrib.auth.decorators import login_required
import mimetypes
from .serializers import ChatSerializer
from .forms import AllGroupsForm
from django.contrib import messages
# Create your views here.
def ChatRoom(request,grpslug):
    print(grpslug)
    group = Group.objects.get(slug=grpslug)
    group.members.order_by('-last_seen')
    chats = Chat.objects.select_related('send_by','group','reply_to').filter(group=group,is_active=True)
    profile,group_form = None,None
    if request.user.is_authenticated:
        profile = UserProfile.objects.select_related('user').get(user=request.user)
        group_form = AllGroupsForm(UserProfile.objects.select_related('user').filter(user=request.user))
    return render(request,'chat/chatroom.html',{'group':group,'chats':chats,'profile':profile,'form':group_form})

@login_required
def Join_Group(request,grpslug):
    user = UserProfile.objects.select_related('user').get(user=request.user)
    group=Group.objects.prefetch_related('members').get(slug=grpslug)
    group.members.add(user)
    group.members_count+=1
    group.save()
    messages.success(request,'Hurray! you are now the member of '+group.name+' Group')
    return redirect(request.GET.get('next'))

@login_required
def add_msg(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        msg = request.POST.get('msg')
        grpslug = request.POST.get('grpslug')
        group = Group.objects.prefetch_related('members').select_related('type').get(slug=grpslug)
        profile = UserProfile.objects.select_related('user').get(user=request.user)
        chat=Chat.objects.create(message=msg,group=group,send_by=profile,timestamp=datetime.datetime.now(),file=file)
        type,encoding = mimetypes.guess_type(chat.file.name)  
        print(type)
        if type!=None and 'image' in type:
            chat.ftype = 'image'
        elif type!=None and 'video' in type:
            chat.ftype = 'video'
        else:
            chat.ftype = 'other'
        chat.save()
        chat_dict = ChatSerializer(chat).data
        chat_dict['action']='add'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(grpslug,
            {
                'type' : 'message.action',
                'data' : json.dumps(chat_dict)
            })
        return JsonResponse({'success':"Yes"})

@login_required
def forward_msg(request):
    if request.method == 'POST':
        form = AllGroupsForm(UserProfile.objects.select_related('user').filter(user=request.user),request.POST)
        if form.is_valid():
            groups = form.cleaned_data['groups']
            send_by = UserProfile.objects.select_related('user').get(user=request.user)
            chat_id = request.POST.get('msg_id')
            chat = Chat.objects.select_related('send_by','group','reply_to').get(id=chat_id)
            print(chat.file)
            for group in groups:
                if chat.file:
                    chat=Chat.objects.create(message=chat.message,file=chat.file,send_by=send_by,group=group,timestamp=datetime.datetime.now(),
                    ftype=chat.ftype)
                else:
                    chat=Chat.objects.create(message=chat.message,send_by=send_by,group=group,timestamp=datetime.datetime.now())

                chat_dict = ChatSerializer(chat).data
                chat_dict['action']='add'
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(group.slug,
                    {
                        'type' : 'message.action',
                        'data' : json.dumps(chat_dict)
                    })
        return JsonResponse({'success':'true'})
