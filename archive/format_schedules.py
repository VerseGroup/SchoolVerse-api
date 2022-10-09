import json

# open the schedules.json file as a dictionary
with open('schedules.json') as f:
    schedules = json.load(f)

keys = {
    '8:05 AM' : 'Homeroom',
    '8:20 AM' : 'Period 1',
    '9:20 AM' : 'Special',
    '9:35 AM' : 'Special',
    '9:55 AM' : 'Period 2',
    '11:00 AM' : 'Period 3',
    '12:00 PM' : 'First Lunch',
    '12:15 PM' : 'First Lunch',
    '12:30 PM' : 'Second Lunch',
    '1:05 PM' : 'Period 4',
    '2:10 PM' : 'Period 5',
}

new_schedules = {}

for email in schedules:
    schedule = schedules[email]

    days = {}

    for x in range(1,9):
        days[x] = {
            'day' : 'Day ' + str(x),
            'periods' : []
        }

    courses = schedule['courses']
    for course in courses:
        name = course['name']
        teacher = course['teacher']
        upper_or_lower = course['upper_or_lower']

        for meeting in course['meetings']:
            day = meeting['day']
            start_time = meeting['start_time']
            end_time = meeting['end_time']

            # bug
            if start_time == "9:20":
                start_time = "9:20 AM"
            if start_time == "9:35":
                start_time = "9:35 AM"
            if end_time == "9:50":
                end_time = "9:55 AM"

            try:
                period = keys[start_time]
            except KeyError:
                period = 'N/A'

            days[day]['periods'].append({
                'course' : {
                    'name' : name,
                    'teacher' : teacher,
                    'upper_or_lower' : upper_or_lower,
                },
                'start_time' : start_time,
                'end_time' : end_time,
                'period' : period
            })

    
    new_schedule = {
        'email' : email,
        'name' : schedule['name'],
        'grade' : schedule['grade'],
        'days' : days,
    }

    new_schedules[email] = new_schedule

with open('formatted_schedules.json', 'w') as f:
    json.dump(new_schedules, f, indent=4)