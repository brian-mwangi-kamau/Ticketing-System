from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Ticket, Comment, StaffInfo


class StaffSignupForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=10)
    staff_id = forms.CharField(max_length=10)
    
    class Meta():
        model = CustomUser
        fields = ('email', 'username', 'staff_id')


class UserSignupForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=10)
    
    class Meta():
        model = CustomUser
        fields = ('email', 'username')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    
class StaffProfileForm(forms.ModelForm):
    class Meta():
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'profile_picture')
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'profile_picture')
    profile_picture = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)


class StaffInfoForm(forms.ModelForm):
    class Meta():
        model = StaffInfo
        fields = ('department', 'staff_id')
                  
        
class TicketForm(forms.ModelForm):
    class Meta():
        model = Ticket
        fields = ('title', 'message', 'image', 'priority', 'category')
        
        
class CommentForm(forms.ModelForm): 
    class Meta():
        model = Comment
        fields = ('message', 'image')
        

class StatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('status',)