# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt, datetime

#REGEX

# any letter and -, min 3.
NAME_REGEX = re.compile(r'^^[a-zA-Z-\s]{3,}$')
# min 3, max 20 any letter, number or. -_
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.\.-_]{3,20}$')
# 8-20 characters, 1 cap, 1 lower, 1 number, 1 symbol.
PW_REGEX = re.compile(r'^.{8,}$')

# MANAGERS
class UserManager(models.Manager):
    def login(self, postData):
        username = postData['username']
        password = postData['password']
        check_user = self.filter(username=username)
        login_valid = {
            'errors': [],
        }
        if check_user:
            print check_user
            user = check_user[0]
            print user.username
            hashed_pw = bcrypt.hashpw(password.encode(), user.password.encode())
            if user.password == hashed_pw:
                login_valid['user'] = user
                print user
                return login_valid
        login_valid['errors'].append('Invalid username or password')
        return login_valid

    def register(self, postData):
        errors = [];
        check_user = self.filter(username=postData['username'])
        if check_user:
            errors.append('Username already exists')
        if not USERNAME_REGEX.match(postData['username']):
            errors.append('Not a valid username')
        if not NAME_REGEX.match(postData['name']):
            errors.append('Name must be minimum 3 characters and can only contain letters, and - if neccessary')
        if not postData['date_hired']:
            errors.append('Nate hired cannot be blank')
        if not PW_REGEX.match(postData['password']):
            errors.append('password must be minimum 8 characters')
        if postData['password'] != postData['passconf']:
            errors.append('passwords must match')
        return errors

# MODELS
class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name="item_added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def in_wishlist(self):
        return list(self.item_wishlist.all().values_list('user_id', flat=True))

class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="user_wishlist")
    item = models.ForeignKey(Item, related_name="item_wishlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # def in_wishlist(self):
    #     return list(self.all().values_list('user_id', flat=True))
