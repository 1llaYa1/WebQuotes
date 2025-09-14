from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.template import loader
from .models import Quote, Source, User
import random
from django.contrib.auth import authenticate, login, logout, get_user

def auth_view(request):
    template = loader.get_template("randomquote/auth.html")
    context = {}
    if request.user.is_authenticated:
        return redirect("auth_complete")
    return HttpResponse(template.render(context, request))

def auth(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True, 'message': 'Authentication complete!'})
    else:
        return JsonResponse({"success": False, 'message': 'Wrong username or password!'})

def registration_view(request):
    template = loader.get_template("randomquote/registration.html")
    context = {}
    return HttpResponse(template.render(context, request))

def registration(request):
    data = json.loads(request.body)
    username = data["username"]
    password = data["password"]
    #user = authenticate(request, username=username, password=password)
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return JsonResponse({"success": True, 'message': 'Registration complete!'})
    if user is None:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({"success": True, 'message': 'Registration complete!'})
    else:
        return JsonResponse({"success": False, 'message': 'User already exists!'})

def auth_complete(request):
    template = loader.get_template("randomquote/auth_complete.html")
    context = {}
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect("authenticate")

def index(request):
    quoteList = []
    for q in Quote.objects.all():
        quoteList += [q] * q.weight
    random.shuffle(quoteList)
    random_quote = quoteList[random.randint(0, len(quoteList)-1)]
    template = loader.get_template("randomquote/index.html")
    context = {"quote": random_quote}
    inst = Quote.objects.get(pk=random_quote.pk)
    inst.views += 1
    inst.save()
    return HttpResponse(template.render(context, request))

def popular(request):
    popular_quotes = Quote.objects.order_by("-likes")[:10]
    data = []
    template = loader.get_template("randomquote/popular.html")
    context = {"popular_quotes": popular_quotes}
    for i in popular_quotes:
        inst = Quote.objects.get(pk=i.pk)
        inst.views += 1
        inst.save()
    return HttpResponse(template.render(context, request))

@login_required
def addquote(request):
    template = loader.get_template("randomquote/addquote.html")
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def newquote(request):
    data = json.loads(request.body)
    text = data["text"]
    weight = int(data["weight"])
    if weight > 100:
        weight = 100
    elif weight < 1:
        weight = 1
    source = Source.objects.filter(name=data["source"])
    if source.count() == 0:
        new_source = Source(name=data["source"])
        new_source.save()
    source = source.get()
    if source.get_quotes_count() < 3:
        try:
            new_quote = Quote(text=data["text"], source=source, weight=weight)
            new_quote.save()
            return JsonResponse({'success': True, 'message': "Success!"})
        except:
            return JsonResponse({"success": False, "message": "The quote already exists or the data is incorect!"})
    return JsonResponse({"success": False, "message": "Unable to create more than 3 quotes for one source!"})
    
@login_required
def vote(request, quote_id):
    data = json.loads(request.body)
    like_btn = data["like_btn"]
    user =  User.objects.filter(id=get_user(request).id).get()
    isQuoteLiked  = Quote.objects.filter(id=quote_id, likes=user).count() != 0
    isQuoteDisliked  = Quote.objects.filter(id=quote_id, dislikes=user).count() != 0
    quote  = Quote.objects.filter(id=quote_id).get()
    if like_btn:
        quote.dislikes.remove(user)
        if isQuoteLiked:
            quote.likes.remove(user)
            return JsonResponse({"liked": False, "disliked": False, "likes_val": quote.get_likes(), "dislikes_val": quote.get_dislikes()})
        else:
            quote.likes.add(user)
            return JsonResponse({"liked": True, "disliked": False, "likes_val": quote.get_likes(), "dislikes_val": quote.get_dislikes()})
    else:
        quote.likes.remove(user)
        if isQuoteDisliked:
            quote.dislikes.remove(user)
            return JsonResponse({"liked": False, "disliked": False, "likes_val": quote.get_likes(), "dislikes_val": quote.get_dislikes()})
        else:
            quote.dislikes.add(user)
            return JsonResponse({"liked": False, "disliked": True, "likes_val": quote.get_likes(), "dislikes_val": quote.get_dislikes()})
    
    