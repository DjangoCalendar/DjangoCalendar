from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from DataUtil import Page,GeneratePassword, GetLoggedUser
from CalendarApp.forms import LoginForm,RegisterForm, ChangePasswordForm,\
    EntryForm
from CalendarApp.models import Accounts, Entry
from CalendarApp.DataUtil import SendGeneretatedPassword,SendGGMessage
from django.contrib.sessions.models import Session
from django.http.response import HttpResponseRedirect
from CalendarApp.ReminderThread import ReminderThread
import time
from datetime import date, datetime, timedelta
import calendar
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.shortcuts import render
from django.template import RequestContext
Development = True

def index(request):
    try:
        key = request.session.session_key
        session = Session.objects.get(session_key = key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        isLogged = user is not None
        username = user.username
        avatarfile = user.accounts.AvatarId
    except Exception:
        isLogged = False
        username = ''
        avatarfile=''
    return render_to_response(Page['Index'], {'Message':"Hello, world. You're at the Main Page.",'LoggedIn':isLogged,'user':username,'avatarfile':avatarfile})
    #return render(request,Page['Index'], {'Message':"Hello, world. You're at the Main Page.",'LoggedIn':isLogged,'user':username,'avatarfile':avatarfile},context_instance=RequestContext(request, processors=[reminders]))

def userDetails(request):
    try:
        key = request.session.session_key
        session = Session.objects.get(session_key = key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        isLogged = user is not None
        username = user.username
        avatarfile = user.accounts.AvatarId
    except Exception:
        isLogged = False
        username = ''
        avatarfile=''
    return  {
             'LoggedIn':isLogged,'user':username,'avatarfile':avatarfile
             }

def detail(request, poll_id):
    return HttpResponse("You're looking at ID %s." % poll_id)

@csrf_exempt
@login_required
def accountdetails(request):
    if request.method == 'GET':
        loggeduser = GetLoggedUser(request)
        useraccounts = loggeduser.accounts
        detailForm = RegisterForm(initial={'Login':loggeduser.username, 'Email':loggeduser.email,'FirstName':loggeduser.first_name,'LastName':loggeduser.last_name, 'GGNumber':useraccounts.GGNumber, 'FacebookId':useraccounts.FacebookId})
        detailForm.fields['Email'].widget.attrs['readonly'] = True
        passwordForm = ChangePasswordForm()
        return render_to_response(Page['Accountdetails'],{'detailform':detailForm,'passwordform':passwordForm, 'activetab' : 0, 'avatarfile':str(useraccounts.AvatarId[:3])})
    if request.method == 'POST':
        tab = request.POST['tab']
        return options[tab](request,Page['Accountdetails'])

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
            user = authenticate(username=nick.strip(), password=passw)
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
            testUser = User.objects.filter(email=email1)
            if testUser:
                return render_to_response(Page['Register'], {'error':'Account Not Created. \n There is already account on this email','form':regForm})
            login = inf['Login'].strip()
            if Development:
                passw = "Master1234"
            else:
                passw= GeneratePassword()
            firstName = inf['FirstName']
            lastName = inf['LastName']
            ggnumber = inf['GGNumber']
            numericGG = int(ggnumber)
            if numericGG < 100:
                return render_to_response(Page['Register'], {'error':'Account Not Created. \n GG Number is not correct','form':regForm})  
            facebId = inf['FacebookId']
            try:
                user = User.objects.create_user(username=login,password=passw,email=email1, first_name=firstName,last_name=lastName)
                user.save()
                acc = Accounts(Login=user,GGNumber=ggnumber,FacebookId=facebId)
                acc.save()
                if Development == False:
                    SendGeneretatedPassword(login,passw)
                return render_to_response(Page['Index'], {'Message':'Account Created. \n We send password on your email','LoggedIn':False})
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
    

def removeUser(request,url):
    user = GetLoggedUser(request)
    user.delete()
    return logout_view(request)

def changeUserPassword(request,url):
    loggeduser = GetLoggedUser(request)
    useraccounts = loggeduser.accounts
    detailform = RegisterForm(initial={'Login':loggeduser.username, 'Email':loggeduser.email,'FirstName':loggeduser.first_name,'LastName':loggeduser.last_name, 'GGNumber':useraccounts.GGNumber, 'FacebookId':useraccounts.FacebookId})
    detailform.fields['Email'].widget.attrs['readonly'] = True
    if request.method == 'POST':
        passwordform = ChangePasswordForm(request.POST)
        if passwordform.is_valid():
            cd = passwordform.cleaned_data
            oldpassword = cd['OldPassword']
            newpassword = cd['NewPassword']
            repeatnewpassword = cd['RepeatNewPassword']  
            if loggeduser.check_password(oldpassword):
                if newpassword == repeatnewpassword:
                    if newpassword == oldpassword:
                        render = render_to_response(url,{'messagepassword':'Old and New Password are the same','passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
                    else:
                        loggeduser.set_password(newpassword)
                        loggeduser.save()
                        render = render_to_response(url,{'messagepassword':'Password changed successfully','passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
                else:
                    render = render_to_response(url,{'messagepassword':'You type two different new passwords - correct it','passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
            else:
                render = render_to_response(url,{'messagepassword':'Your actual password is not correct','passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
        else:
            render = render_to_response(url,{'passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
    else:
        passwordform =  ChangePasswordForm()
        render = render_to_response(url,{'passwordform':passwordform, 'detailform':detailform,'activetab':'1', 'avatarfile':useraccounts.AvatarId[:3]})
    return render

def updateUserDetails(request,url):
    passwordform = ChangePasswordForm()
    detailform = RegisterForm(request.POST)
    user = GetLoggedUser(request)
    useraccounts = user.accounts
    if detailform.is_valid():
        cd = detailform.cleaned_data
        login = cd['Login']
        firstname = cd['FirstName']
        lastname = cd['LastName']
        ggnumber = cd['GGNumber']
        facebookid = cd['FacebookId']
        usercounter = User.objects.filter(username = login).count()
        message = "Details Updated."
        if user.username != login:
            if usercounter > 0:
                message += " Unable to change user nick. Nick already exists. "
            else:
                user.username = login
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        useraccounts.GGNumber = ggnumber
        useraccounts.FacebookId = facebookid
        useraccounts.save()
        return render_to_response(url,{'message': message,'detailform':detailform,'passwordform':passwordform,'activetab':0, 'avatarfile':useraccounts.AvatarId[:3]})
    else:
        return render_to_response(url,{'message': 'Some Fields are incorrect - correct it','detailform':detailform,'passwordform':passwordform,'activetab':0, 'avatarfile':useraccounts.AvatarId[:3]})
    
def updateUserAvatar(request, url):
    loggeduser = GetLoggedUser(request)
    useraccounts = loggeduser.accounts
    detailform = RegisterForm(initial={'Login':loggeduser.username, 'Email':loggeduser.email,'FirstName':loggeduser.first_name,'LastName':loggeduser.last_name, 'GGNumber':useraccounts.GGNumber, 'FacebookId':useraccounts.FacebookId})
    detailform.fields['Email'].widget.attrs['readonly'] = True
    passwordform = ChangePasswordForm()
    avatarfile = request.POST['avatar']
    useraccounts.AvatarId = avatarfile;
    loggeduser.save()
    useraccounts.save()
    return render_to_response(url,{'messageavatar': "Avatar Updated",'detailform':detailform,'passwordform':passwordform,'activetab':3, 'avatarfile':useraccounts.AvatarId[:3]})
    
    
options = {'2':removeUser, '1':changeUserPassword, '0':updateUserDetails, '3':updateUserAvatar}

def startthread(request):
    reminderTh  = ReminderThread()
    print 'Startujemy Watek'
    reminderTh.start()
    print 'Watek Wystartowany'
    return HttpResponse("Reminding Thread started")
mnames = "January February March April May June July August September October November December"
mnames = mnames.split()


@login_required
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    if year: year = int(year)
    else:    year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    # create a list of months for each year, indicating ones that contain entries and current
    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False   # are there entry(s) for this month; current month?
            entries = Entry.objects.filter(date__year=y, date__month=n+1)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    #return render_to_response(Page['main'], dict(years=lst, user=request.user, year=year,
    #                                               reminders=reminders(request)))
    return render(request,Page['main'], dict(years=lst, user=request.user, year=year,reminders=reminders(request)),context_instance=RequestContext(request, processors=[userDetails]))

def reminders(request):
    """Return the list of reminders for today and tomorrow."""
    year, month, day = time.localtime()[:3]
    reminders = Entry.objects.filter(date__year=year, date__month=month,
                                   date__day=day, creator=request.user, remind=True)
    tomorrow = datetime.now() + timedelta(days=1)
    year, month, day = tomorrow.timetuple()[:3]
    return list(reminders) + list(Entry.objects.filter(date__year=year, date__month=month,
                                   date__day=day, creator=request.user, remind=True))

@login_required
def month(request, year, month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":   mod = mdelta
        elif change == "prev": mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    # make month lists containing list of days for each week
    # each day tuple will contain list of entries and 'current' indicator
    for day in month_days:
        entries = current = False   # are there entries for this day; current day?
        tooltip = ""
        if day:
            entries = Entry.objects.filter(date__year=year, date__month=month, date__day=day)
            if not _show_users(request):
                entries = entries.filter(creator=request.user)
            if day == nday and year == nyear and month == nmonth:
                current = True
            #build string for tooltip
            #if len(entries)!=0:
            #    tooltip = ""
            for e in entries:
                tooltip+= e.title
                if e.snippet:
                    tooltip += ": "+e.snippet
                tooltip+= "<br/>"
                     
        lst[week].append((day, entries, current,tooltip))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

            # return render_to_response("CalendarApp/month.html", dict(year=year, month=month, user=request.user,
            #                     month_days=lst, mname=mnames[month-1], reminders=reminders(request)))
    return render(request,Page['month'], dict(year=year, month=month, user=request.user,
                     month_days=lst, mname=mnames[month-1], reminders=reminders(request)),context_instance=RequestContext(request, processors=[userDetails]))

@login_required
def day(request, year, month, day):
    """Entries for the day."""
    EntriesFormset = modelformset_factory(Entry,form=EntryForm, exclude=("creator", "date"),
                                          can_delete=True)
    other_entries = []
    if _show_users(request):
        other_entries = Entry.objects.filter(date__year=year, date__month=month,
                                       date__day=day).exclude(creator=request.user)

    if request.method == 'POST':
        formset = EntriesFormset(request.POST)
        if formset.is_valid():
            # add current user and date to each entry & save
            entries = formset.save(commit=False)
            for entry in entries:
                entry.creator = request.user
                entry.date = date(int(year), int(month), int(day))
                entry.save()
            return HttpResponseRedirect(reverse("CalendarApp.views.month", args=(year, month)))

    else:
        # display formset for existing enties and one extra form
        formset = EntriesFormset(queryset=Entry.objects.filter(date__year=year,
            date__month=month, date__day=day, creator=request.user))
    #return render_to_response("CalendarApp/day.html", add_csrf(request, entries=formset, year=year,
    #        month=month, day=day, other_entries=other_entries, reminders=reminders(request)))
    return render(request,Page['day'],add_csrf(request, entries=formset, year=year,
                                               month=month, day=day, other_entries=other_entries, reminders=reminders(request)),context_instance=RequestContext(request, processors=[userDetails]))


def add_csrf(request, ** kwargs):
    """Add CSRF and user to dictionary."""
    d = dict(user=request.user, ** kwargs)
    d.update(csrf(request))
    return d

def _show_users(request):
    """Return show_users setting; if it does not exist, initialize it."""
    s = request.session
    if not "show_users" in s:
        s["show_users"] = True
    return s["show_users"]

@login_required
def settings(request):
    """Settings screen."""
    s = request.session
    _show_users(request)
    if request.method == "POST":
        s["show_users"] = (True if "show_users" in request.POST else False)
    #return render_to_response("CalendarApp/settings.html", add_csrf(request, show_users=s["show_users"]))
    return render(request,Page['settings'], add_csrf(request, show_users=s["show_users"]) ,context_instance=RequestContext(request, processors=[userDetails]))
