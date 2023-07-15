from pyracing.client import Client
import asyncio
import datetime
username = 'nicoto123@gmail.com'
password = 'iRacing2023!'

# Authentication is automated and will be initiated on first request
ir = Client(username, password)

# Example async function with hardcoded results
async def main():

  seasons_list = await ir.current_seasons()

  for season in seasons_list:

    print(f'Schedule for {season.series_name_short}' 
      f' ({season.season_year} S{season.season_quarter})')
    print(f'{season.date_start} -' 
      f' ({season.date_end}, race week :{season.race_week})')
    # for t in season.tracks:
    #   print(f'\tWeek {t.race_week} will take place at {t.name} ({t.config})')
    # driver_status = await ir.driver_status(cust_id=455246)
    # end_date = datetime.datetime.now()
    # start_date = end_date - datetime.timedelta(days=7)
    # seriesRaceResults =await ir.series_race_results(season.season_id, season.race_week)
    # all_subsessions = await ir.all_subsessions(subsession_id=season.season_id)
    # private_results = await ir.private_results(cust_id=455246, start_time_lower=start_date, start_time_upper=end_date)
    # event_results = await ir.event_results(cust_id=455246, quarter=3)
    
    # print(seriesRaceResults)

asyncio.run(main())