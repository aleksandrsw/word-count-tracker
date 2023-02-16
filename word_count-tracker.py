import csv
from pathlib import Path

first_time = True
if Path('./wc_totals.txt').is_file():
  first_time = False

new_day = False
total_yesterday = 0
total_today = 0
day = 0
total = 0
written = 0

if first_time:
  print("Is there a previous word total? (Y/N)")
  if input().strip().capitalize() == 'Y':
    print("\nEnter the previous word total.")
    total_yesterday = int(input())

    print("Enter the word total today.")
    total_today = int(input())

    total = total_today - total_yesterday
    written = total
  else:
    print("Enter the word total today.")
    total, total_today, written = input()
else:
  print("Is it tomorrow already? (Y/N)")
  if input().strip().capitalize() == 'Y':
    print("Okay! Thanks for telling me.\n")
    new_day = True

  with open('wc_totals.txt', mode='r') as csv_file:
      last_line = csv_file.readlines()[-1]
      strs = last_line.split(',')
      day = int(strs[0])
      if new_day:
        day = day + 1
        total_yesterday = int(strs[1])
        print("Enter the word total today.")
        total_today = int(input())
        total = total_today - total_yesterday
        written = total
      else:
        total_today_old = int(strs[1])
        print("Enter the word total today.")
        total_today = int(input())
        total = total_today - total_today_old
        written = int(strs[2]) + total
        total = written

print("\nIt is day", day+1, "and you've written", total, "words out of a total of", total_today, "words.")

with open('wc_totals.txt', mode='a', newline='') as csv_file:
  fieldnames = ['day', 'total', 'written']
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

  if first_time: writer.writeheader()
  writer.writerow({'day': day, 'total': total_today, 'written': written})

print("\nPress any key to exit.")
input()
