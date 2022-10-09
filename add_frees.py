PERIODS = [
    "Period 1",
    "Period 2",
    "Period 3",
    "Period 4",
    "Period 5",
    "First Lunch",
    "Second Lunch",
    "Homeroom",
    "Special",
]

def get_times(day):

    day = int(day.split(" ")[1])

    if day % 2 == 0:
        period1_start = "8:20 AM"
        period1_end = "9:35 AM"
        period3_start = "11:00 AM"
        period3_end = "12:00 PM"
        first_lunch_start = "12:00 PM"
        first_lunch_end = "12:30 PM"
        special_start = "9:35 AM"
        special_end = "9:50 AM"
    else:
        period1_start = "8:20 AM"
        period1_end = "9:20 AM"
        period3_start = "11:00 AM"
        period3_end = "12:15 PM"
        first_lunch_start = "12:15 PM"
        first_lunch_end = "12:30 PM"
        special_start = "9:20 AM"
        special_end = "9:35 AM"

    return {
        "Period 1": {
            "start_time": period1_start,
            "end_time": period1_end,
        },
        "Period 2": {
            "start_time": "9:55 AM",
            "end_time" : "10:55 AM",
        },
        "Period 3": {
            "start_time": period3_start,
            "end_time": period3_end,
        },
        "Period 4": {
            "start_time": "1:05 PM",
            "end_time": "2:05 PM",
        },
        "Period 5": {
            "start_time": "2:10 PM",
            "end_time" : "3:10 PM",
        },
        "First Lunch": {
            "start_time": first_lunch_start,
            "end_time": first_lunch_end,
        },
        "Second Lunch": {
            "start_time": "12:15 PM",
            "end_time": "12:20 PM",
        },
        "Homeroom": {
            "start_time": "8:05 AM",
            "end_time": "8:15 AM",
        },
        "Special": {
            "start_time": special_start,
            "end_time": special_end,
        },
    }
        

# load schedules.json as dictionary
import json
with open('schedules.json') as f:
    schedules = json.load(f)

for email in schedules:
    grade = schedules[email]['grade']

    days = schedules[email]['days']
    for day in days:
        the_day = day["day"]
        periods = day['periods']

        frees = []

        existing_periods = []
        for period in periods:
            existing_periods.append(period['period'])

        for period in PERIODS:
            if period not in existing_periods:
                if period != "First Lunch" and period != "Second Lunch": 
                    frees.append({
                        "course": {
                            "name": "Free",
                            "teacher": "N/A",
                            "upper_or_lower": "US",
                        },
                        "period": period,
                        "start_time": get_times(the_day)[period]['start_time'],
                        "end_time": get_times(the_day)[period]['end_time'],
                    })
                elif period == "First Lunch" and grade < 11:
                    frees.append({
                        "course": {
                            "name": "First Lunch",
                            "teacher": "N/A",
                            "upper_or_lower": "US",
                        },
                        "period": period,
                        "start_time": get_times(the_day)[period]['start_time'],
                        "end_time": get_times(the_day)[period]['end_time'],
                    })
                elif period == "Second Lunch" and grade > 10:
                    frees.append({
                        "course": {
                            "name": "Second Lunch",
                            "teacher": "N/A",
                            "upper_or_lower": "US",
                        },
                        "period": period,
                        "start_time": get_times(the_day)[period]['start_time'],
                        "end_time": get_times(the_day)[period]['end_time'],
                    })
                else:
                    frees.append({
                        "course": {
                            "name": "Free",
                            "teacher": "N/A",
                            "upper_or_lower": "US",
                        },
                        "period": period,
                        "start_time": get_times(the_day)[period]['start_time'],
                        "end_time": get_times(the_day)[period]['end_time'],
                    })

        periods.append(frees)   


with open('frees_schedules.json', 'w') as f:
    json.dump(schedules, f, indent=4)