import json

with open('schedules.json') as f:
    schedules = json.load(f)

with open('schedule.json') as f:
    template = json.load(f)

users = {}

for key in schedules:
    schedule = schedules[key]
    courses = schedule['classes']

    new_courses = []

    for course in courses:
        course_name = course['course_name']
        block = course['block']
        teacher = course['teacher']
        upper_or_lower = course['upper_or_lower']
        days = course['day']

        meetings = []
        for day in days:
            if len(block) == 1:
                block = block[0]
                if '*' in block:
                    block = block.replace('*', '').upper()
                times = template[f"Day {day}"][block] 
            else:
                if day == 3 and schedule['student_grade'] < 11:
                    times = template[f"Day {day}"]["LN-2"]
                elif day == 5 and schedule['student_grade'] >= 11:
                    times = template[f"Day {day}"]["LN-1"]
                elif day == 7 and schedule['student_grade'] < 11:
                    times = template[f"Day {day}"]["2"]
                elif day == 1 and schedule['student_grade'] >= 11:
                    times = template[f"Day {day}"]["2"] 
            
            start_time = times['start']
            end_time = times['end']
            meetings.append(
                {
                    "day": day,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )

        course = {
            "name": course_name,
            "teacher": teacher,
            "upper_or_lower": upper_or_lower,
            "meetings": meetings
        }

        new_courses.append(course)

    office_hours = {
        "name": "OFFICE HOURS",    
        "teacher": "N/A",
        "upper_or_lower": "US",
        "meetings": [
            {
                "day": 4,
                "start_time": "9:20",
                "end_time": "9:50"
            },
            {
                "day": 8,
                "start_time": "9:20",
                "end_time": "9:50"
            }
        ]
    }
    new_courses.append(office_hours)

    if schedule['student_grade'] == 12:
        new_courses.append(
            {
                "name": "ASSEMBLY/MEETING TIME",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 2,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    },
                    {
                        "day": 5,
                        "start_time": "9:35",
                        "end_time": "9:50",
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "CC 12 (FALL) - ALLEN HALL",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 6,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "CHAPEL TALK",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 3,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "GRADE 12 MEETING (CHAPEL)",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 7,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    }
                ]
            }
        )
    elif schedule['student_grade'] == 11:
        new_courses.append(
            {
                "name": "ASSEMBLY/MEETING TIME",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 2,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    },
                    {
                        "day": 5,
                        "start_time": "9:35",
                        "end_time": "9:50",
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "CC 11 (SPRING) - ALLEN HALL",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 6,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "GRADE 11 MEETING (LR)",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 7,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    },
                    {
                        "day": 3,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    }
                ]
            }
        )
    elif schedule['student_grade'] == 10:
        new_courses.append(
            {
                "name": "ASSEMBLY/MEETING TIME",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 2,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    },
                    {
                        "day": 5,
                        "start_time": "9:35",
                        "end_time": "9:50",
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "GRADE 10 MEETING (CHAPEL)",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 1,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    },
                    {
                        "day": 6,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    }
                ]
            }
        )
    elif schedule['student_grade'] == 9:
        new_courses.append(
            {
                "name": "ASSEMBLY/MEETING TIME",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 2,
                        "start_time": "9:20",
                        "end_time": "9:50"
                    },
                    {
                        "day": 5,
                        "start_time": "9:35",
                        "end_time": "9:50",
                    }
                ]
            }
        )
        new_courses.append(
            {
                "name": "GRADE 9 MEETING (LR)",
                "teacher": "N/A",
                "upper_or_lower": 'US',
                "meetings": [
                    {
                        "day": 1,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    },
                    {
                        "day": 6,
                        "start_time": "9:35",
                        "end_time": "9:50"
                    }
                ]
            }
        )

    user = {
        'name': schedule['student_name'],
        'email': schedule['student_email'],
        'grade': schedule['student_grade'],
        'courses': new_courses
    }

    users[user['email']] = user


with open('users.json', 'w') as f:
    json.dump(users, f, indent=4)