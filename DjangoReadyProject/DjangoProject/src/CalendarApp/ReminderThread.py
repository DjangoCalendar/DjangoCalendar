from threading import Thread
from django.contrib.auth.models import User
from GGLibrary.pygglib import GGSession
from datetime import datetime,timedelta
import time

class ReminderThread(Thread):
    def __init__(self): 
        super(ReminderThread, self).__init__()    
    
    def run(self):
        try:
            work = True
            today = datetime.now()
            while(work): 
                today = today.replace(hour=7, minute=0,second=0, microsecond=0)
                gg = GGSession(49651904, 'Master1234')
                gg.login()
                print 'Hello'
                year, month, day = time.localtime()[:3]
                for user in User.objects.all():
                    needtobereminded = user.entry_set.filter(remind=True,date__year=year,date__month=month,date__day=day)
                    if needtobereminded.count()!=0:
                        print 'Uzytkownik {0} ma jakies eventy na dzisiaj'.format(user.username)
                        uA = user.accounts
                        userGG = uA.GGNumber
                        gg.send_msg(int(userGG),'Hej. To wiadomosc z Django Calendar-a.\nMasz na dzisiaj zapisane pare Eventow w naszym Serwisie.\nOto one:')
                        for event in needtobereminded:
                            gg.send_msg(int(userGG),'Title: {0} \n Snippet: {1}\n Body: {2}\n'.format(event.title,event.snippet,event.body))
                        gg.send_msg(int(userGG),'Do Uslyszenia - Zespol Django Calendar')
                work = False
                while(work == False):
                    if datetime.now().replace(microsecond=0) == (today + timedelta(days=1)).replace(minute=0,second=0, microsecond=0):
                        today = (today + timedelta(days=1))
                        print 'Watek Rusza:'
                        print today
                        work = True   
            gg.logout()
        except Exception,e:
            print e.message     