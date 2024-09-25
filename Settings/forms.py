from django import forms
from Chat.models import UserProfile
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','readonly':True}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

ProfileFormSet = inlineformset_factory(
    User, UserProfile,fields=['phone_no','country_name','about','img'],
    extra=0, can_delete=False,
    widgets = {'country_name':forms.TextInput(attrs={'class':'form-control'}),
        'phone_no':forms.TextInput(attrs={'class':'form-control'}),
        'img':forms.FileInput(attrs={'class':'form-control','id':'img'}),
        'about':forms.Textarea(attrs={'class':'form-control','cols':4,'rows':3}),
        }
)
