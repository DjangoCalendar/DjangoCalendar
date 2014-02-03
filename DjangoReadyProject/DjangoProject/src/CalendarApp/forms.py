from django import forms

class LoginForm(forms.Form):
    Login = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Username', 'class':'form-control' }), min_length=6,max_length=50, required= True,
                            error_messages={'required': 'This is required field', 'max_length':'Login is to long - max 50', 'min_length': 'You login is too short - at least 6 characters'})
    Password = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Password', 'class':'form-control' }), max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
class RegisterForm(forms.Form):
    Login = forms.CharField(widget=forms.TextInput(attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Username', 'class':'form-control' }),max_length=50, required= True, label= 'Login:',
                            error_messages={'required': 'You need to set you Login', 'max_length':'Login is to long - max 50 characters'})
    Email = forms.EmailField(widget=forms.TextInput(attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Email', 'class':'form-control' }),required=True,label='Email',
                            error_messages={'required':'Email is required to finish registration'})
    FirstName = forms.CharField(widget=forms.TextInput(attrs={  'autofocus': 'true','placeholder': 'First Name', 'class':'form-control' }),required=False,label='First Name:', max_length=30)
    LastName = forms.CharField(widget=forms.TextInput(attrs={ 'autofocus': 'true','placeholder': 'Last Name', 'class':'form-control' }),required=False,label='Last Name:', max_length=30)
    GGNumber = forms.DecimalField(widget=forms.TextInput(attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'GG Number', 'class':'form-control' }),required=True,label='GG Number:', max_digits=19)
    FacebookId = forms.CharField(widget=forms.TextInput(attrs={ 'autofocus': 'true','placeholder': 'Facebook ID', 'class':'form-control' }),required=False,label='Facebook ID:', max_length=100)
    
class ChangePasswordForm(forms.Form):
    OldPassword = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Old Password', 'class':'form-control' }), label='Old Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
    NewPassword = forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'New Password', 'class':'form-control' }), label='New Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
    RepeatNewPassword =forms.CharField(widget=forms.PasswordInput(render_value=False,attrs={ 'required': 'true', 'autofocus': 'true','placeholder': 'Repeat New Password', 'class':'form-control' }), label='Repeat New Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})