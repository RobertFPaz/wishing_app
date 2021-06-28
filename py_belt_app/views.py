from django.shortcuts import render, redirect
from .models import Wish
from django.apps import apps
User = apps.get_model('login_app', 'User')
from django.contrib import messages
from datetime import date
from pytz import timezone


def dashboard(request):
    if 'user_id' in request.session:
        context={
            "wishes": Wish.objects.all(),
            "user": User.objects.get(id=request.session['user_id']),
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect("/")

def remove(request, wish_id):
   user_wish=Wish.objects.get(id=wish_id)
   user_wish.delete()
   return redirect('/wishes')

def edit(request, wish_id):
    
    context={
        "wish": Wish.objects.get(id=wish_id),
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'edit.html', context)
    
def update(request, wish_id):
    user_wish =Wish.objects.get(id=wish_id)
    if request.method == "POST":
        errors=Wish.objects.wish_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect(f"/wishes/edit/{user_wish.id}")
        else:
            user_wish.item = request.POST['item']
            user_wish.description = request.POST['description']
            user_wish.save()
            return redirect('/wishes')
    else:
        return redirect('/wishes')

def granted(request, wish_id):
    user_wish=Wish.objects.get(id=wish_id)
    user_wish.granted = date.today()
    user_wish.save()
    return redirect('/wishes')

def new(request):
    context={
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'make_wish.html', context)

def add_wish(request):
    if request.method == "POST":
        errors=Wish.objects.wish_validation(request.POST)
        if errors:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect("/wishes/new")
        else:
            logged_user = User.objects.get(id=request.session['user_id'])
            new_wish=Wish.objects.create(item=request.POST['item'], description=request.POST['description'], user=logged_user)
            return redirect('/wishes')
    else:
        return redirect('/wishes')

def likes(request, wish_id):
    wish=Wish.objects.get(id=wish_id)
    logged_user=User.objects.get(id=request.session['user_id'])
    liked_wishes=logged_user.user_likes.all()
    for user_wish in logged_user.wishes.all():
        if user_wish.id == wish_id:
            return redirect('/wishes')
    for one_wish in liked_wishes:
        if one_wish.id == wish_id:
            return redirect('/wishes')
    wish.likes.add(logged_user)
    return redirect('/wishes')

def stats(request):
    all_wishes=Wish.objects.count()
    null_granted=Wish.objects.filter(granted__isnull=True).count()
    only_granted=all_wishes - null_granted
    logged_user=User.objects.get(id=request.session['user_id'])
    user_non_granted=Wish.objects.filter(granted__isnull=True).filter(user=logged_user).count()
    user_wishes=len(logged_user.wishes.all())
    granted_wishes=user_wishes - user_non_granted
    context={
        "user": User.objects.get(id=request.session['user_id']),
        "all_granted_wishes": only_granted,
        "user_granted":granted_wishes,
        "user_pending":user_non_granted,
    }
    return render(request, "stats.html", context)