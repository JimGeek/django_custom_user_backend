from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from custom_user_auth.models import MyUser
from django.contrib.auth import login as auth_login

def index(request):
	context = RequestContext(request)
	context_dict = {'message': "Nest is sold to google for $2.9B"}
	return render_to_response('index.html',context_dict,context)

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html',c)

def auth_view(request):
    uid = request.POST.get('uid','')
    user = authenticate(uid=uid)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')

def loggedin(request):
    return render_to_response('loggedin.html',{'full_name': request.user.email })

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def send(request):
    print(request.POST.get('first_name',''))
    try:
        user = MyUser.objects.get(email=request.POST.get('email',''))
        if user is not None:
            auth_login(request,user)
        else:
            print("Something went wrong")
    except:
        user = MyUser(email=request.POST.get('email',''),first_name=request.POST.get('first_name',''),last_name=request.POST.get('last_name',''),uid=request.POST.get('uid',''))
        user.save()
        auth_login(request,user)
    return render_to_response('loggedin.html',{'full_name': request.POST.get('first_name','')})