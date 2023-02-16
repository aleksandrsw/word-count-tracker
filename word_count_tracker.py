import csv
from pathlib import Path
from platformdirs import *
import os

appname = "WordCountTracker"
appauthor = "Dark"
appdata = user_data_dir(appname, appauthor)
if not os.path.exists(appdata):
  os.makedirs(appdata)

first_time = True
if Path(appdata + '/wc_totals.txt').is_file():
  first_time = False

new_day = False
total_yesterday = 0
total_today = 0
day = 0
total = 0
written = 0

if Path(appdata + '/wc_totals.txt').is_file():
  print("Do you wish to reset your progress? (Y/N)")
  if input().strip().capitalize() == 'Y':
    first_time = True
    os.remove(appdata + "/wc_totals.txt")

if first_time:
  print("\nIs there a previous word total? (Y/N)")
  if input().strip().capitalize() == 'Y':
    print("\nEnter the previous word total.")
    total_yesterday = int(input())

    print("\nEnter the word total today.")
    total_today = int(input())

    total = total_today - total_yesterday
    written = total
  else:
    print("\nEnter the word total today.")
    total = int(input())
    total_today = total
    written = total
else:
  print("\nIs it tomorrow already? (Y/N)")
  if input().strip().capitalize() == 'Y':
    print("Okay! Thanks for telling me.")
    new_day = True

  with open(appdata + '/wc_totals.txt', mode='r') as csv_file:
      last_line = csv_file.readlines()[-1]
      strs = last_line.split(',')
      day = int(strs[0])
      if new_day:
        day = day + 1
        total_yesterday = int(strs[1])
        print("\nEnter the word total today.")
        total_today = int(input())
        total = total_today - total_yesterday
        written = total
      else:
        total_today_old = int(strs[1])
        print("\nEnter the word total today.")
        total_today = int(input())
        total = total_today - total_today_old
        written = int(strs[2]) + total
        total = written

print("\nIt is day", day+1, "and you've written", total, "words out of a total of", total_today, "words.")

with open(appdata + '/wc_totals.txt', mode='a', newline='') as csv_file:
  fieldnames = ['day', 'total', 'written']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

  if first_time: writer.writeheader()
  writer.writerow({'day': day, 'total': total_today, 'written': written})

input("\nPress Enter to exit.")