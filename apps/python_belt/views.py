# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Item, Wishlist
from django.contrib import messages
from django.db.models import Count
import bcrypt

# VIEWS
def index(request):
    if 'logged_user' in request.session:
        return redirect(reverse('dashboard'))
    return render(request, 'python_belt/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)

        else:
            messages.success(request, 'Successfully Registered. Please Login')
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(
                username=request.POST['username'],
                name=request.POST['name'],
                password=hashed_pw,
                date_hired=request.POST['date_hired']
            )
    return redirect('index')

def login(request):
    if request.method == "POST":
        login_valid = User.objects.login(request.POST)
        if login_valid['errors']:
            for error in login_valid['errors']:
                messages.error(request, error)
                return redirect('index')
        else:
            user = User.objects.get(pk=login_valid['user'].id)
            request.session['logged_user'] = user.id
            return redirect('dashboard')
    return redirect('index')

def logout(request):
    request.session.clear()
    return redirect('index')

def dashboard(request):
    user = User.objects.get(pk=request.session.get('logged_user'))
    context = {
        'logged_user': user,
        'wish_items': Wishlist.objects.filter(user=user).order_by('-item__created_at'),
        'other_items': Item.objects.exclude(item_wishlist__user=user).order_by('-created_at')
    }
    return render(request, 'python_belt/dashboard.html', context)

def show_add_item(request):
    return render(request, 'python_belt/add_item.html')

def add_item(request):
    if request.method == "POST":
        user = user = User.objects.get(pk=request.session.get('logged_user'))
        check_item = Item.objects.filter(item_name=request.POST['item_name'])
        if check_item:
            messages.error(request, 'Item already exists')
            return redirect('show_add_item')
        if not request.POST['item_name']:
            messages.error(request, 'Item name cannot be empty')
            return redirect('show_add_item')
        if len(request.POST['item_name']) < 3:
            messages.error(request, 'Item name must be minimum 3 characters')
            return redirect('show_add_item')
        user = User.objects.get(pk=request.session.get('logged_user'))
        item = Item.objects.create(item_name=request.POST['item_name'], added_by=user)
        Wishlist.objects.create(user=user, item=item)
        return redirect('dashboard')
    return redirect('show_add_item')

def show_item(request, id):
    item = Item.objects.get(pk=id)
    context = {
        'item': item,
        'users': User.objects.filter(user_wishlist__item=item).order_by('-user_wishlist__created_at')
    }
    return render(request, 'python_belt/item.html', context)

def add_wish_item(request, id):
    user = User.objects.get(pk=request.session.get('logged_user'))
    item = Item.objects.get(pk=id)
    if not user.id in item.in_wishlist():
        Wishlist.objects.create(user=user, item=item)
    return redirect('dashboard')

def remove_wish_item(request, id):
    Wishlist.objects.get(pk=id).delete()
    return redirect('dashboard')

def delete_item(request, id):
    Item.objects.get(pk=id).delete()
    return redirect('dashboard')
