from pyracing.client import Client
from .key import key
from .models import MetaInfo, Member
from cryptography.fernet import Fernet
from asgiref.sync import sync_to_async, async_to_sync
from iracingdataapi.client import irDataClient
import datetime

def getDataForOneMember(start_date, end_date, customer_id):
  member = Member.objects.filter(customer_id = customer_id).first()
  cur_setting = MetaInfo.objects.first()
  username = cur_setting.iRacing_username
  fernet = Fernet(key)
  password = fernet.decrypt(cur_setting.iRacing_password.encode()).decode()
  ir = Client(username, password)
  ir2 = irDataClient(username, password)
  start_range_begin=start_date.strftime('%Y-%m-%dT00:00:00Z'),
  finish_range_begin=end_date.strftime('%Y-%m-%dT00:00:00Z'),
  series = ir2.result_search_series(
    start_range_begin = start_range_begin,
    finish_range_begin = start_range_begin,
    cust_id=customer_id
  )
  series_in_range = []
  for each_series in series:
    each_series_start_date = datetime.datetime.strptime(each_series['start_time'], "%Y-%m-%dT%H:%M:%SZ")
    if each_series_start_date > end_date:
      break
    series_in_range.append(each_series)
  data = {}
  data["name"] = member.name
  data["starts"] = len(series_in_range)
  
  
  # data["wins"] = 
  return series

def getData(start_date, end_date):
  data = []
  members = Member.objects.all()
  for member in members:
    data.append(getDataForOneMember(start_date=start_date, end_date=end_date, customer_id=member.customer_id))
  return data
  
  
  