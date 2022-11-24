import json

# open the schedules.json file as a dictionary
with open('archive/schedules.json') as f:
    schedules = json.load(f).copy()

print("started")
for key in schedules:
    user = schedules[key]
    for day in user['days']:
        the_day = day['day']
        for period in day['periods']:
            if period['course']['name'] == "Free" and period['start_time'] == "8:20 AM":
                if the_day == "Day 1" or the_day == "Day 3" or the_day == "Day 5" or the_day == "Day 7":
                    period['end_time'] = "9:35 AM"
                else:
                    period['end_time'] = "9:20 AM"

with open('src/schedules.json', 'w') as f:
    print('writing')
    json.dump(schedules, f, indent=4)
