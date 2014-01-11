from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate
from DataUtil import Page
from CalendarApp.forms import LoginForm,RegisterForm
from CalendarApp.models import Accounts


def index(request):
    return render_to_response(Page['Index'], {'Message':"Hello, world. You're at the Main Page."})

def detail(request, poll_id):
    return HttpResponse("You're looking at ID %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of ID %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on ID %s." % poll_id)

@csrf_exempt
def login(request):
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
                    renderer = render_to_response(Page['Index'],{'welcome':'You are logged in - welcome'})
                else:
                    renderer = render_to_response(Page['Login'],{'message':'Your login or password is correct but your account is not active','form':LoginForm()})
        else:
            renderer = render_to_response(Page['Login'],{'form':form})
    else: #GET Request
        form = LoginForm()
        renderer = render_to_response(Page['Login'],{'form':form})
    return renderer

def logout_view(request):
    logout(request)
    return render_to_response(Page['Index'], {'Message':"Hello, world. You're at the Main Page."})

@csrf_exempt
def register(request):
    if request.method == 'GET':
        regForm = RegisterForm()
    else:
        regForm = RegisterForm(request.POST)
        if regForm.is_valid():
            inf = regForm.cleaned_data
            login = inf['Login']
            passw= inf['Password']
            email1 = inf['Email']
            firstName = inf['FirstName']
            lastName = inf['LastName']
            ggnumber = inf['GGNumber']
            facebId = inf['FacebookId']
            try:
                user = User.objects.create_user(username=login,password=passw,email=email1, first_name=firstName,last_name=lastName)
                user.save()
                acc = Accounts(Login=user,GGNumber=ggnumber,FacebookId=facebId)
                acc.save()
                return render_to_response(Page['Register'], {'error':'Account Created'})
            except Exception, e:
                errorMsg = e.message
                return render_to_response(Page['Register'], {'error':errorMsg,'form':RegisterForm()})
        else:
                return render_to_response(Page['Register'], {'form':regForm})     
    return render_to_response(Page['Register'], {'form':regForm})
        
