""" def write_courses(courses, user_id, db):
    user_dict = db.collection(u'USERS').document(f"{user_id}").get().to_dict()

    user_courses = user_dict['COURSES']
    if user_courses is None:
        user_courses = []

    for course in courses:
        course = course.serialize()
        user_courses.append(course)

    user_dict['COURSES'] = user_courses
    db.collection(u'USERS').document(f"{user_id}").set(user_dict)


     """