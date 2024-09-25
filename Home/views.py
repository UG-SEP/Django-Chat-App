import json
from django.http import JsonResponse
from django.views.generic.list import ListView
from Chat.models import Group,UserProfile
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.utils import timezone
from Chat.templatetags.group_tags import is_user_online

# Create your views here.
class Home(ListView):
    template_name = 'Home/home.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 6
    paginate_orphans = 2
    paginator_class = Paginator

    def get_queryset(self):
        return super().get_queryset().all().order_by('name').select_related('type','created_by').defer('members','description')
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['profile']=UserProfile.objects.only('id').get(user=self.request.user)
        return context
        
class Search(ListView):
    template_name = 'Home/search-result.html'
    model = Group
    context_object_name = 'groups'
    paginate_by = 6
    paginate_orphans = 2
    paginator_class = Paginator

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['expression']=self.request.GET.get('expression')
        return context

    def get_queryset(self):
        return super().get_queryset().filter(name__icontains=self.request.GET.get('expression')).order_by('name').select_related('type','created_by').defer('members','description')


@login_required
def update_last_seen(request):
    grpslug = request.GET.get('grpslug')
    group = Group.objects.get(slug=grpslug)
    profile = UserProfile.objects.get(user=request.user)
    profile.last_seen = timezone.now()
    usersStatus = {}
    i=1
    for profile in group.members.all():
        if is_user_online(profile.last_seen):
            usersStatus[profile.user.username] = ['Online',profile.img.url]
        else:
            usersStatus[profile.user.username] = ['Offline',profile.img.url]
        i+=1

    return JsonResponse({'usersStatus':usersStatus})
