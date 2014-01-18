from django import forms

class LoginForm(forms.Form):
    Login = forms.CharField(min_length=6,max_length=50, required= True, label= 'Login:',
                            error_messages={'required': 'This is required field', 'max_length':'Login is to long - max 50', 'min_length': 'You login is too short - at least 6 characters'})
    Password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
class RegisterForm(forms.Form):
    Login = forms.CharField(max_length=50, required= True, label= 'Login:',
                            error_messages={'required': 'You need to set you Login', 'max_length':'Login is to long - max 50 characters'})
    #Password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password', max_length=30, required=True,
    #                           error_messages={'required':'This is required field','max_length':'Password is to long - max 30'})
    Email = forms.EmailField(required=True,label='Email',
                            error_messages={'required':'Email is required to finish registration'})
    FirstName = forms.CharField(required=False,label='First Name:', max_length=30)
    LastName = forms.CharField(required=False,label='Last Name:', max_length=30)
    #additional information
    GGNumber = forms.DecimalField(required=True,label='GG Number:', max_digits=19)
    FacebookId = forms.CharField(required=False,label='Facebook ID:', max_length=100)
    
class ChangePasswordForm(forms.Form):
    OldPassword = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Old Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
    NewPassword = forms.CharField(widget=forms.PasswordInput(render_value=False), label='New Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
    RepeatNewPassword =forms.CharField(widget=forms.PasswordInput(render_value=False), label='Repeat New Password:', max_length=30,min_length = 10, required=True,
                               error_messages={'required':'This is required field','max_length':'Password is to long - max 30','min_length':'You password is too short - at least 10 characters'})
    
class ChangeUserNameForm(forms.Form):
    NewUsername = forms.CharField(required=True, label='New User Name:',min_length=6,max_length=50, error_messages={'required': 'This is required field', 'max_length':'Login is to long - max 50', 'min_length': 'You login is too short - at least 6 characters'})    