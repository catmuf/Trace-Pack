from django.forms import ModelForm
from .models import TrackingNumber, Courier
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class AddTrackingForm(ModelForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        # Match whitespace character and non-whitespace (characters)
        self.fields['title'].widget.attrs.update({ 
            'type': 'text', 
            'name': 'title',
            'class': 'form-control',
            'id': 'title',
            'pattern': '^[\s\S]{1,50}$',
            'title': 'Input title.',
            'required': ''
        })
        
        # Lowercase, uppercase characters and numbers allowed, at least 8 characters
        self.fields['tracking_number'].widget.attrs.update({ 
            'type': 'text', 
            'name': 'tracking_number',
            'class': 'form-control',
            'id': 'tracking_number',
            'pattern': '^[a-zA-Z0-9]{8,50}$',
            'title': 'Input minimum 8 characters.',
            'required': ''
        }) 
        self.fields['delivery_type'].widget.attrs.update({  
            'name': 'delivery_type',
            'class': 'form-control',
            'id': 'delivery_type',
            'required': ''
        })

    class Meta:
        model = TrackingNumber
        fields = ['title', 'tracking_number', 'delivery_type']

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['email'].widget.attrs.update({ 
            'type': 'email', 
            'name': 'email',
            'class': 'form-control',
            'onkeyup': 'validateSignUp(this)',
            'id': 'email',
        }) 
        self.fields['username'].widget.attrs.update({ 
            'type': 'text', 
            'name': 'username',
            'class': 'form-control',
            'onkeyup': 'validateSignUp(this)',
            'id': 'username',
        }) 
        self.fields['password1'].widget.attrs.update({ 
            'type': 'password', 
            'name': 'password1',
            'class': 'form-control',
            'onkeyup': 'validateSignUp(this)',
            'id': 'password',
        }) 
        self.fields['password2'].widget.attrs.update({ 
            'type': 'password', 
            'name': 'password2',
            'onkeyup': 'validateSignUp(this)',
            'class': 'form-control',
            'id': 'repeatPassword',
        }) 

        
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['old_password'].widget.attrs.update({ 
            'type': 'password', 
            'name': 'old_password',
            'class': 'form-control',
            'onkeyup': 'validatePasswordProfile(this)',
            'id': 'current_password',
        }) 
        self.fields['new_password1'].widget.attrs.update({ 
            'type': 'password', 
            'name': 'new_password1',
            'class': 'form-control',
            'onkeyup': 'validatePasswordProfile(this)',
            'id': 'password',
        }) 
        self.fields['new_password2'].widget.attrs.update({ 
            'type': 'password', 
            'name': 'new_password2',
            'onkeyup': 'validatePasswordProfile(this)',
            'class': 'form-control',
            'id': 'repeatPassword',
        }) 

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]