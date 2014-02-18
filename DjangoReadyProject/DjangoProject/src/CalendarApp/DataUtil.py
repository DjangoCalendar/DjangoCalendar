'''
Created on 11 sty 2014

@author: Mateusz Bacal
'''
import string
import smtplib
from time import time
from itertools import chain
from random import seed, choice, sample
from django.contrib.auth.models import User
from GGLibrary.Exceptions import GGNotLogged
from GGLibrary.pygglib import GGSession
from django.contrib.sessions.models import Session
#from FBPack.facehack import FaceHack
Page = {
    'Master':'CalendarApp/master.html',
    'Index':'CalendarApp/index.html',
    'Login':'CalendarApp/login.html',
    'Register':'CalendarApp/register.html',
    'PasswordChange': 'CalendarApp/passwordchange.html',
    'Accountdetails': 'CalendarApp/accountdetails.html',
	'main': 'CalendarApp/main.html',
    'month':'CalendarApp/month.html',
    'day': 'CalendarApp/day.html',
    'settings': 'CalendarApp/settings.html'
    }

Messages = {
             'FirstPass': 'Welcome! \n Do not respond on this adress. Below you can see automatically generated password. \n You can changed it after first loggin in Settings. \n Your password is: {0}',
            }

#based on example from - http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
def GeneratePassword(length=21, digits=3, upper=3, lower=3):
    """Create a random password

    Create a random password with the specified length and no. of
    digit, upper and lower case letters.

    :param length: Maximum no. of characters in the password
    :type length: int

    :param digits: Minimum no. of digits in the password
    :type digits: int

    :param upper: Minimum no. of upper case letters in the password
    :type upper: int

    :param lower: Minimum no. of lower case letters in the password
    :type lower: int

    :returns: A random password with the above constaints
    :rtype: str
    """
    seed(time())
    lowercase = string.lowercase.translate(None,"o")
    uppercase = string.uppercase.translate(None,"O")
    letters = "{0:s}{1:s}".format(lowercase, uppercase)
    
    password = list (
                     chain(
                            (choice(uppercase) for _ in range(upper)),
                            (choice(lowercase) for _ in range(lower)),
                            (choice(string.digits) for _ in range(digits)),
                            (choice(uppercase) for _ in range(upper)),
                            (choice(letters) for _ in range((length - digits - upper - lower)))
                          )
                    )
    generatedPassword = "".join(sample(password, len(password)))
    
    return generatedPassword

#based on example from http://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python
def SendGeneretatedPassword(Login, Password):
    try:
        fromaddr = 'djangocalendar@gmail.com'
        u = User.objects.get(username=Login)
        toaddrs  = u.email
        msg = Messages['FirstPass'].format(Password)
        username = 'djangocalendar@gmail.com'
        password = 'Master1234'
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    except Exception,e:
        raise Exception("Exception from Password Sender : {0} \n".format(e.message))

#GG Number:49651904
#PWD: Master1234    
#based on example from https://boty.gg.pl/przyklady/ - example 5  
def SendGGMessage(Login):
    try:
        u = User.objects.get(username=Login)
        uA = u.accounts
        userGG = uA.GGNumber
        gg = GGSession(49651904, 'Master1234')
        gg.login()
        gg.send_msg(int(userGG),'Testowa wiadomosc z bota do projektu z AMSI dla uzytkownika {0} ;)'.format(Login))
        gg.logout()
    except GGNotLogged:
        return True
    except Exception,e:
        raise Exception("Exception from GG Message Sender : {0}.\n".format(e.message))

# Get Logged User
def GetLoggedUser(request):
    try:
        key = request.session.session_key
        session = Session.objects.get(session_key = key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return user
    except Exception:
        return None

# djangocalendar@gmail.com
# Master1234
#def SendFbMessage(text, fbId):
#    try :
#        fh = FaceHack()
#        fh.login("bonzai1990@o2.pl","master1")
#        fh.status("Hakkin Facebook")      
#    except Exception,e:
#        raise Exception("Exception from Facebook Message Sender : {0}.\n".format(e.message))