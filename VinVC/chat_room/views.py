# from django.core.context_processors import csrf NO HACE FALTA, VA EN EL HTML
from django.views.decorators.csrf import csrf_exempt
# from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from chat_room.models import Message, ChatUser
from django.shortcuts import render, redirect
import json
import datetime
from django.utils.timezone import now as utcnow


def index(request):
    # if request.user.username and request.user.profile.is_chat_user:

    if request.user.username:
        # intial chat json data
        r = Message.objects.order_by('-time')[:20]
        res = []
        for msgs in reversed(r):
            res.append({'id': msgs.id, 'user': msgs.user, 'msg': msgs.message,
                        'time': msgs.time.strftime('%I:%M:%S %p').lstrip('0'), 'gravatar': msgs.gravatar})
        data = json.dumps(res)
        # end json
        context = {'data': mark_safe(data)}
        return render(request, 'chat_room/index.html', context)
    else:
        return HttpResponseRedirect(reverse('chat_room:login'))
    # return redirect('user:index')


# def login(request):
# 	if request.user.username and request.user.profile.is_chat_user:
# 		return HttpResponseRedirect(reverse('chat_room:index'))
# 	context = {'error':''}
#
# 	if request.method == 'POST':
# 		username = request.POST.get('username','') #return '' if no username
# 		password = request.POST.get('password','')
# 		user = auth.authenticate(username=username,password=password)
#
# 		if user is not None:
# 			auth.login(request, user)
# 			cu = request.user.profile
# 			cu.is_chat_user = True
# 			cu.last_accessed = utcnow()
# 			cu.save()
# 			return redirect('chat_room:index')
# 		else:
# 			# context['error'] = ' wrong credentials try again'
# 			return redirect('chat_room:login')
#
#
# 	#context.update(csrf(request))
# 	context.update(request)
# 	return render(request,'chat_room/login.html',context)


# def login(request):
#     """Loginn user from POST data"""
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         auth_login(request, user)
#         return redirect('user:index')
#     else:
#         return redirect('login:index')

# def logout(request):
# 	cu = request.user.profile
# 	cu.is_chat_user = False
# 	cu.save()
# 	return HttpResponse('succesfully logged out of chat')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        d = json.loads(request.body)
        msg = d.get('msg')
        user = request.user.username
        gravatar = request.user.profile.gravatar_url
        m = Message(user=user, message=msg, gravatar=gravatar)
        m.save()
        res = {'id': m.id, 'msg': m.message,
               'user': m.user, 'time': m.time.strftime('%I:%M:%S %p').lstrip('0'), 'gravatar': m.gravatar}
        data = json.dumps(res)
        return HttpResponse(data, content_type="application/json")
    # get request
    r = Message.objects.order_by('-time')[:20]
    res = []
    for msgs in reversed(r):
        res.append({'id': msgs.id, 'user': msgs.user, 'msg': msgs.message, \
                    'time': msgs.time.strftime('%I:%M:%S %p').lstrip('0'), 'gravatar': msgs.gravatar})

    data = json.dumps(res)
    return HttpResponse(data, content_type="application/json")


def logged_chat_users(request):
    users = ChatUser.objects.filter(is_chat_user=True)
    for k in users:
        print(k.username)
    for j in users:
        elapsed = utcnow() - j.last_accessed
        if elapsed > datetime.timedelta(seconds=45):
            print(elapsed)
            j.is_chat_user = False
            j.save()

    uu = ChatUser.objects.filter(is_chat_user=True)
    print("after check time and update")
    for k in uu:
        print(k.username)

    d = []
    for i in uu:
        d.append({'username': i.username, 'gravatar': i.gravatar_url, 'id': i.userID})
    data = json.dumps(d)
    return HttpResponse(data, content_type="application/json")


def update_time(request):
    if request.user.username:
        print(request.user.username)
        u = request.user.profile
        print(u.last_accessed)
        print(utcnow())
        u.last_accessed = utcnow()
        u.is_chat_user = True
        u.save()
        print(u.last_accessed)
        return HttpResponse('updated')
    return HttpResponse('who are you?')
