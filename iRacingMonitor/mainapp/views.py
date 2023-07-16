from django.shortcuts import render, redirect
from .validation import validate_login
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import MetaInfo, CustomUser, Member
from django.http import HttpResponse
import datetime
from .api import getData, saveData, readData, generateImage
from cryptography.fernet import Fernet
from .key import key
import os
# Create your views here.

#login
def login(request):
  if request.method == 'GET':
    return render(request, 'mainapp/pages/login.html')
  elif request.method == 'POST':
    result, message = validate_login(request)
    if result == False:
      viewParams = {}
      viewParams["login_result"] = result
      viewParams["message"] = message
      return render(request, 'mainapp/pages/login.html', viewParams)
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(email=email, password=password)
    
    user.save()
    auth_login(request, user)
    return redirect(stats)

#members
@login_required
def members(request):
  members = Member.objects.all().values()
  viewParams = {}
  viewParams['members'] = members
  if request.method == 'GET':
    return render(request, 'mainapp/pages/members.html', viewParams)

#add_member
@login_required
def add_member(request):
  customer_id = request.POST.get("customer_id")
  name = request.POST.get("name")
  if Member.objects.filter(customer_id = customer_id).exists():
    return HttpResponse('Already Registered Member')
  member = Member(customer_id = customer_id, name=name)
  member.save()   
  return redirect(members)
#edit_member
@login_required
def edit_member(request):
  id = request.POST.get("id")
  customer_id = request.POST.get("customer_id")
  name = request.POST.get("name")
  member = Member.objects.get(id=id)
  member.customer_id = customer_id
  member.name = name
  member.save()
  return redirect(members)

#delete_member
@login_required
def delete_member(request, id):
  member = Member.objects.get(id = str(id))
  member.delete()
  return redirect(members)

#stats
@login_required
def stats(request):
  if request.method == 'GET':
    if os.path.exists('output.json'):
      viewParams= readData()
      return render(request, 'mainapp/pages/stats.html', viewParams)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    
  if request.method == 'POST':
    start_date_str = request.POST.get("start_date")
    end_date_str = request.POST.get("end_date")
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
  
  data = getData(start_date=start_date, end_date=end_date)
  saveData(data, start_date, end_date)
  
  viewParams = {}
  viewParams["data"] = data
  viewParams["start_date"] = start_date.strftime('%Y-%m-%d')
  viewParams["end_date"] = end_date.strftime('%Y-%m-%d')
  return render(request, 'mainapp/pages/stats.html', viewParams)



#export_stats
@login_required
def export_stats(request):
  generateImage()
  return render(request, 'mainapp/pages/export_stats.html')

#meta
@login_required
def meta(request):
  cur_setting = MetaInfo.objects.first()
  print(cur_setting)
  viewParams = {}
  if cur_setting is not None:
    viewParams['iRacing_username'] = cur_setting.iRacing_username
    fernet = Fernet(key)
    iRacing_password = fernet.decrypt(cur_setting.iRacing_password.encode()).decode()
    viewParams['iRacing_password'] = iRacing_password
    viewParams['heading_color'] = cur_setting.heading_color
    viewParams['data_color'] = cur_setting.data_color
    viewParams['total_color'] = cur_setting.total_color
    viewParams['name_color'] = cur_setting.name_color
    viewParams['heading_font'] = cur_setting.heading_font
    viewParams['data_font'] = cur_setting.data_font
    viewParams['total_font'] = cur_setting.total_font
    viewParams['name_font'] = cur_setting.name_font
  if request.method == 'GET':
    return render(request, 'mainapp/pages/meta.html', viewParams)

#change_meta
@login_required
def change_meta(request):
  iRacing_username = request.POST.get("iRacing_username")
  iRacing_password = request.POST.get("iRacing_password")
  fernet = Fernet(key)
  iRacing_password = fernet.encrypt(iRacing_password.encode()).decode()
  heading_color = request.POST.get("heading_color", "black")
  data_color = request.POST.get("data_color", "black")
  total_color = request.POST.get("total_color", "black")
  name_color = request.POST.get("name_color", "black")
  heading_font = request.POST.get("heading_font", "Calibri")
  data_font = request.POST.get("data_font", "Calibri")
  total_font = request.POST.get("heading_color", "Calibri")
  name_font = request.POST.get("name_font", "Calibri")

  cur_setting = MetaInfo.objects.first()
  if cur_setting is None:
    cur_setting = MetaInfo(
      iRacing_username = iRacing_username, iRacing_password = iRacing_password,
      heading_color=heading_color, data_color=data_color, total_color=total_color, name_color=name_color,
      heading_font=heading_font, data_font=data_font, total_font=total_font, name_font=name_font
    )
    cur_setting.save()
  else:
    cur_setting.heading_color = heading_color
    cur_setting.data_color = data_color
    cur_setting.total_color = total_color
    cur_setting.name_color = name_color
    cur_setting.heading_font = heading_font
    cur_setting.data_font = data_font
    cur_setting.total_font = total_font
    cur_setting.name_font = name_font
    cur_setting.save()
    
  return redirect(stats)


