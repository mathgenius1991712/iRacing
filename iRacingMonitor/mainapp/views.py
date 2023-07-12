from django.shortcuts import render, redirect
from .validation import validate_login
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.

#login
def login(request):
  if request.method == 'GET':
    return render(request, 'mainapp/pages/login.html')
  elif request.method == 'POST':
    result, message = validate_login(request)
    if result == False:
      context = {}
      context["login_result"] = result
      context["message"] = message
      return render(request, 'mainapp/pages/login.html', context)
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(email=email, password=password)
    
    user.save()
    auth_login(request, user)
    return redirect(stats)

#members
@login_required
def members(request):
  if request.method == 'GET':
    return render(request, 'mainapp/pages/members.html')

#add_member
@login_required
def add_member(request):
  print("add_member")

#edit_member
@login_required
def edit_member(request):
  print("edit_member")

#delete_member
@login_required
def delete_member(request):
  print("delete_member")

#stats
@login_required
def stats(request):
  if request.method == 'GET':
    return render(request, 'mainapp/pages/stats.html')


#export_stats
@login_required
def export_stats(request):
  print("export_stats")

#meta
@login_required
def meta(request):
  if request.method == 'GET':
    return render(request, 'mainapp/pages/meta.html')

#change_meta
@login_required
def change_meta(request):
  print("change_meta")
