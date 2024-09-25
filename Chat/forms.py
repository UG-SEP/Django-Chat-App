from django import forms
from Chat.models import GroupType,Group,UserProfile
from django.contrib.auth.models import User
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['img','name','type','description']
        widgets = {'img': forms.FileInput(attrs={'class':'form-control img'}),
        'name': forms.TextInput(attrs={'class':'form-control name'}),
        'description': forms.Textarea(attrs={'class':'form-control description','rows':2,'cols':4})
        }
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['img'].required = False
        self.fields['type'] = forms.ModelChoiceField(queryset=GroupType.objects.all(),widget=forms.Select(attrs={'class':'form-control type'}),
        initial=GroupType.objects.first())
        self.fields['img'].label = 'Image'  

class AllGroupsForm(forms.Form):
    def __init__(self,profile=None,*args,**kwargs):
        super(AllGroupsForm,self).__init__(*args,**kwargs)
        if profile is not None:
            specified_group = Group.objects.filter(members__in =profile)
        else:
            specified_group = Group.objects.all()
        self.fields['groups'] = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=specified_group)
