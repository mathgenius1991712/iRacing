from pyracing.client import Client
from .key import key
from .models import MetaInfo, Member
from cryptography.fernet import Fernet
from asgiref.sync import sync_to_async, async_to_sync
from iracingdataapi.client import irDataClient
import datetime

from asyncer import syncify

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
  wins = 0
  laps = 0
  top_5 = 0
  top_10 = 0
  laps_lead = 0
  cautions = 0
  caution_laps = 0
  i_rating_gain_loss = 0
  for each_series in series:
    each_series_start_date = datetime.datetime.strptime(each_series['start_time'], "%Y-%m-%dT%H:%M:%SZ")
    if each_series_start_date > end_date:
      break
    result_each_series = ir2.result(subsession_id=each_series["subsession_id"], include_licenses=True)
    session_results = result_each_series["session_results"][0]["results"]
    rank = 0
    for driver_rank in session_results:
      rank += 1
      if driver_rank["cust_id"] == customer_id:
        if rank == 1:
          wins += 1
        if rank <= 5:
          top_5 += 1
        if rank <= 10:
          top_10 += 1
        laps_lead += driver_rank["laps_lead"]
        laps += driver_rank["laps_complete"]
        if each_series["num_cautions"] != -1:
          cautions += each_series["num_cautions"]
        if each_series["num_caution_laps"] != -1:
          caution_laps += each_series["num_caution_laps"]
        i_rating_gain_loss += (each_series["newi_rating"]-each_series["oldi_rating"])
    series_in_range.append(each_series)
    #if(each_series)

  data = {}
  data["name"] = member.name
  data["starts"] = len(series_in_range)
  data["wins"] = wins
  data["laps"] = laps
  data["top_5"] = top_5
  data["top_10"] = top_10
  data["laps_lead"] = laps_lead
  data["cautions"] = cautions
  data["caution_laps"] = caution_laps
  data["i_rating_gain_loss"] = i_rating_gain_loss
  data["safety_gain_loss"] = 0

  return data
  
  

def getData(start_date, end_date):
  data = []
  members = Member.objects.all()
  for member in members:
    data.append(getDataForOneMember(start_date=start_date, end_date=end_date, customer_id=member.customer_id))
  return data
  
  
  