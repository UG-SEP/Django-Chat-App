from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from .forms import UserUpdateForm
from Chat.models import Group,UserProfile
from django.template.defaultfilters import slugify
from .forms import ProfileFormSet
from django.http import JsonResponse
from Chat.serializers import GroupSerializer
from Chat.forms import GroupForm
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
    success_url = '/'
    form_class = UserUpdateForm
    template_name = 'settings/profile.html'
    
    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs= super(UserUpdateView,self).get_context_data(**kwargs)
        if self.request.POST:
            kwargs["profile"] = ProfileFormSet(self.request.POST,self.request.FILES,instance=self.object)
        else:
            kwargs["profile"] = ProfileFormSet(instance=self.object)
            kwargs["image"] = UserProfile.objects.only('img').get(user=self.get_object()).img
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        profile = context["profile"]
        self.object = form.save()
        if profile.is_valid():
            profile.instance = self.get_object()
            profile.save()
        messages.success(self.request,'Changes Successfully saved !')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if form.errors:
            error_msg = str(form.errors.popitem()[1][0])
            messages.error(self.request,error_msg)        
        return super().form_invalid(form)

@method_decorator(login_required,name='dispatch')
class MyGroupsListView(ListView):
    template_name='settings/my-groups.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 6
    paginate_orphans = 2
    paginator_class = Paginator
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GroupForm(label_suffix='',auto_id='$')
        return context
    def get_queryset(self):
        return super().get_queryset().prefetch_related('members').select_related('type','created_by').filter(members__user=self.request.user)

@login_required
def editGroup(request):
    if request.method == "POST":
        id=request.POST.get('id')
        print(id)
        group = Group.objects.prefetch_related('members').select_related('type','created_by').get(id=id)
        form = GroupForm(request.POST,request.FILES,instance=group)
        if form.is_valid():
            form.save()
            group.slug = slugify(form.cleaned_data['name'])
            group.save() 
            serialized_group = GroupSerializer(group).data 
            messages.success(request,'Changes Successfully Saved')
            stored_messages = messages.get_messages(request)
            messages_list = message_to_dict(stored_messages)
            return JsonResponse({"status":"Changes saved",'status_code':1,'group':json.dumps(serialized_group),
            'messages':messages_list})
        else:
            if form.errors:
                error_msg = str(form.errors.popitem()[1][0])
                messages.error(request,error_msg)
            stored_messages = messages.get_messages(request)
            messages_list = message_to_dict(stored_messages)
            return JsonResponse({'status':'Error Occurred. Please try later','status_code':0,'messages':messages_list})

@login_required
def getGroup(request):
    id = request.GET.get('id')
    serialized_group = GroupSerializer(Group.objects.prefetch_related('members').select_related('type','created_by').get(id=id)).data 
    return JsonResponse({'group':json.dumps(serialized_group)})

@login_required
def createGroup(request):
    form = GroupForm(request.POST,request.FILES)
    if form.is_valid():
            form.save()
            groups=Group.objects.filter(name=request.POST.get('name'))
            group = groups.first()
            owner = UserProfile.objects.select_related('user').get(user=request.user)
            group.members.add(owner)
            group.created_by= owner
            group.members_count+=1
            group.slug = slugify(group.name)
            group.save()  
            serialized_group = GroupSerializer(group).data
            print(type(serialized_group))
            print(serialized_group)
            print(json.dumps(serialized_group))
            messages.success(request,'Group Successfully Created')
            stored_messages = messages.get_messages(request)
            messages_list = message_to_dict(stored_messages)
            return JsonResponse({"status":"Changes saved",'status_code':1,'group':json.dumps(serialized_group),
            'messages':messages_list})
    else:
            if form.errors:
                error_msg = str(form.errors.popitem()[1][0])
                messages.error(request,error_msg)
            stored_messages = messages.get_messages(request)
            messages_list = message_to_dict(stored_messages)
            return JsonResponse({"status":"Error Occurred. Please try later",'status_code':0,'messages':messages_list})

@login_required 
def deleteGroup(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        print(id)
        group=Group.objects.prefetch_related('members').select_related('type','created_by').get(id=id)
        id = group.pk
        group.delete()
        messages.success(request,'Group Successfully Deleted')
        stored_messages = messages.get_messages(request)
        messages_list = message_to_dict(stored_messages)
        return JsonResponse({"status":"successfully delete","id":id,'messages':messages_list})


def message_to_dict(stored_messages):
    return [{'level': message.level, 'message': message.message,
        'extra_tags': message.extra_tags,'tags':message.tags} for message in stored_messages]