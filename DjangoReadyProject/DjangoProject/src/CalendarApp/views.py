from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the Main Page.")

def detail(request, poll_id):
    return HttpResponse("You're looking at ID %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of ID %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on ID %s." % poll_id)
