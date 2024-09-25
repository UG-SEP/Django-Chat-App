from django.template import Library
from Chat.models import Group
from django.utils import timezone
register = Library()

def is_user_online(last_seen):
    online_threshold = timezone.now() - timezone.timedelta(minutes=1)
    return last_seen > online_threshold 

def is_joined(name,profile):
    if Group.objects.get(name=name).members.contains(profile):
        return True
    else:
        return False

@register.filter
def getStatus(last_seen):
    if is_user_online(last_seen):
        return 'Online'
    else:
        return 'Offline'

register.filter('is_joined',is_joined)
