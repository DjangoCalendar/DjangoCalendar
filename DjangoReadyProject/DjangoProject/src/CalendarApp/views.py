from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from DataUtil import Page,GeneratePassword
from CalendarApp.forms import LoginForm,RegisterForm, ChangePasswordForm,\
    ChangeUserNameForm
from CalendarApp.models import Accounts
from CalendarApp.DataUtil import SendGeneretatedPassword,SendGGMessage
from django.contrib.sessions.models import Session
from django.http.response import HttpResponseRedirect
from CalendarApp import DataUtil


def index(request):
    try:
        key = request.session.session_key
        session = Session.objects.get(session_key = key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        isLogged = user is not None
        username = user.username
    except Exception:
        isLogged = False
        username = ''
    return render_to_response(Page['Index'], {'Message':"Hello, world. You're at the Main Page.",'LoggedIn':isLogged,'Nick':username})

def detail(request, poll_id):
    return HttpResponse("You're looking at ID %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of ID %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on ID %s." % poll_id)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            nick = cd['Login']
            passw = cd['Password']
            user = authenticate(username=nick, password=passw)
            if user is None:
                renderer = render_to_response(Page['Login'],{'message':'Your login or password are incorrect','form':LoginForm()})
            else:
                if user.is_active:
                    login(request, user)
                    nextParam = request.GET.get('next', None)
                    if nextParam is not None:
                        renderer = HttpResponseRedirect(nextParam)
                    else:
                        renderer = HttpResponseRedirect('/calendar/')
                else:
                    renderer = render_to_response(Page['Login'],{'message':'Your login or password is correct but your account is not active','form':LoginForm()})
        else:
            renderer = render_to_response(Page['Login'],{'form':form})
    else: #GET Request
        form = LoginForm()
        renderer = render_to_response(Page['Login'],{'form':form})
    return renderer

@login_required
def logout_view(request):
    logout(request)
    return render_to_response(Page['Index'], {'Message':"Hello, world. You're at the Main Page. - Logged out",'LoggedIn':False,})

@csrf_exempt
def register(request):
    if request.method == 'GET':
        regForm = RegisterForm()
    else:
        regForm = RegisterForm(request.POST)
        if regForm.is_valid():
            inf = regForm.cleaned_data
            email1 = inf['Email']
            if User.objects.filter(email=email1):
                return render_to_response(Page['Register'], {'error':'Account Not Created. \n There is already account on this email','form':regForm})
            login = inf['Login']
            passw= GeneratePassword()
            firstName = inf['FirstName']
            lastName = inf['LastName']
            ggnumber = inf['GGNumber']
            facebId = inf['FacebookId']
            try:
                user = User.objects.create_user(username=login,password=passw,email=email1, first_name=firstName,last_name=lastName)
                user.save()
                acc = Accounts(Login=user,GGNumber=ggnumber,FacebookId=facebId)
                acc.save()
                SendGeneretatedPassword(login,passw)
                return render_to_response(Page['Register'], {'error':'Account Created. \n We send password on your email'})
            except Exception, e:
                errorMsg = e.message
                return render_to_response(Page['Register'], {'error':errorMsg,'form':RegisterForm()})
        else:
                return render_to_response(Page['Register'], {'form':regForm})     
    return render_to_response(Page['Register'], {'form':regForm})

@login_required
@csrf_exempt
def changepassword(request):
    form = ChangePasswordForm()
    if request.method == 'GET':
        render = render_to_response(Page['PasswordChange'],{'form':form}) 
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            key = request.session.session_key
            session = Session.objects.get(session_key = key)
            uid = session.get_decoded().get('_auth_user_id')
            user = User.objects.get(pk=uid)
            oldpassword = cd['OldPassword']
            newpassword = cd['NewPassword']
            repeatnewpassword = cd['RepeatNewPassword']  
            if user.check_password(oldpassword):
                if newpassword == repeatnewpassword:
                    if newpassword == oldpassword:
                        render = render_to_response(Page['PasswordChange'],{'message':'Old and New Password are the same','form':form})
                    else:
                        user.set_password(newpassword)
                        user.save()
                        render = render_to_response(Page['PasswordChange'],{'message':'Password changed successfully'})
                else:
                    render = render_to_response(Page['PasswordChange'],{'message':'You type two new different passwords','form':form})
            else:
                render = render_to_response(Page['PasswordChange'],{'message':'Your actuall password is incorrect','form':form})
        else:
            render = render_to_response(Page['PasswordChange'], {'form':form})
    return render

@login_required
@csrf_exempt
def changeusername(request):
    if request.method == 'POST':
        form = ChangeUserNameForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            NewUserName = DataUtil.GetUserByUserName(cd['NewUsername'])
            if NewUserName is not None:
                renderer = render_to_response(Page['UserNameChange'],{'form':form,'message':'This login already exists in database'})
            else:
                user = DataUtil.GetLoggedUser(request)
                if user is not None:
                    user.username = cd['NewUsername']
                    user.save()
                    renderer = logout(request)
                    renderer = HttpResponseRedirect('/calendar/')
                else:
                    renderer = render_to_response(Page['UserNameChange'],{'form':form,'message':'This is not possible that you are logged in'})
        else:
            renderer = render_to_response(Page['UserNameChange'],{'form':form})         
    else:
        renderer = render_to_response(Page['UserNameChange'],{'form':ChangeUserNameForm()})
    return renderer;

def ggmessage_view(request):
    try:
        key = request.session.session_key
        session = Session.objects.get(session_key = key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        username = user.username
        SendGGMessage(username)
        return HttpResponse('Wyslanie wiadomosci na gg powiodlo sie')
    except Exception,e:
        return HttpResponse('Blad w ggmessage_view {0}'.format(e.message))