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
if Path(appdata + '/wc_totals.csv').is_file():
  first_time = False

new_day = False
total_yesterday = 0
total_today = 0
day = 0
total = 0
written = 0

class InvalidChoiceException(Exception):
  "Raised when something other than Y or N is passed"
  pass

repeat = True
skip = False
while repeat:
  if Path(appdata + '/wc_totals.csv').is_file() and not skip:
    flag = True
    while flag:
      try:
        answer = input("Do you wish to reset your progress? (Y/N)\n")
        if answer.strip().capitalize() == 'Y':
          first_time = True
          os.remove(appdata + "/wc_totals.csv")
          flag = False
        elif answer.strip().capitalize() == 'N':
          flag = False
        else: raise InvalidChoiceException
      except InvalidChoiceException:
        print("\nPlease try again.\n")

  if first_time:
    flag = True
    while flag:
      try:
        answer = input("\nIs there a previous word total? (Y/N)\n")
        if answer.strip().capitalize() == 'Y':
          flag2 = True
          while flag2:
            try:
              print("\nEnter the previous word total.")
              total_yesterday = int(input())
              flag2 = False
            except ValueError:
              print("\nPlease try again.")

          flag2 = True
          while flag2:
            try:
              print("\nEnter the word total today.")
              total_today = int(input())
              flag2 = False
            except ValueError:
              print("\nPlease try again.")

          total = total_today - total_yesterday
          written = total
          flag = False
        elif answer.strip().capitalize() == 'N':
          flag2 = True
          while flag:
            try:
              print("\nEnter the word total today.")
              total = int(input())
              flag2 = False
            except ValueError:
              print("\nPlease try again.")

          total_today = total
          written = total
          flag = False
        else: raise InvalidChoiceException
      except InvalidChoiceException:
        print("\nPlease try again.")
  else:
    if not skip:
      flag = True
      while flag:
        try:
          answer = input("\nIs it your first time writing today? (Y/N)\n")
          if answer.strip().capitalize() == 'Y':
            print("\nOkay! Thanks for telling me.")
            new_day = True
            flag = False
          elif answer.strip().capitalize() == 'N':
            flag = False
          else: raise InvalidChoiceException
        except InvalidChoiceException:
          print("\nPlease try again.")

    with open(appdata + '/wc_totals.csv', mode='r') as csv_file:
        last_line = csv_file.readlines()[-1]
        strs = last_line.split(',')
        day = int(strs[0])
        if new_day:
          day = day + 1
          total_yesterday = int(strs[1])
          flag = True
          while flag:
            try:
              print("\nEnter the word total today.")
              total_today = int(input())
              flag = False
            except ValueError:
              print("\nPlease try again.")
          total = total_today - total_yesterday
          written = total
        else:
          total_today_old = int(strs[1])
          flag = True
          while flag:
            try:
              print("\nEnter the word total today.")
              total_today = int(input())
              flag = False
            except ValueError:
              print("\nPlease try again.")
          total = total_today - total_today_old
          written = int(strs[2]) + total
          total = written
      
  print("\nIt is day", day+1, "and you have written", total, "words out of a total of", total_today, "words.")

  with open(appdata + '/wc_totals.csv', mode='a', newline='') as csv_file:
    fieldnames = ['day', 'total', 'written']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if first_time: writer.writeheader()
    if not skip: writer.writerow({'day': day, 'total': total_today, 'written': written})

  flag = True
  while flag:
    try:
      answer = input("\nHave you written more? (Y/N)\n")
      if answer.strip().capitalize() == 'Y':
        flag = False
        first_time = False
        skip = True
      elif answer.strip().capitalize() == 'N':
        repeat = False
        flag = False
      else: raise InvalidChoiceException
    except InvalidChoiceException:
      print("\nPlease try again.")

if skip:
  with open(appdata + '/wc_totals.csv', mode='a', newline='') as csv_file:
    fieldnames = ['day', 'total', 'written']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writerow({'day': day, 'total': total_today, 'written': written})

input("\nPress Enter to exit.\n")