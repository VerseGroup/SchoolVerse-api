def write_courses(courses, user_id, db):
    for course in courses:
        write_course(course, user_id, db)

def write_course(course, user_id, db):
    user_ref = db.collection(u'USERS').document(user_id)
    user_dict = user_ref.get().to_dict()

    if user_dict['courses'] is None:
        user_dict['courses'] = [course]
    else:
        updated_courses = user_dict['courses'].append(course)
        user_ref.update({"courses": updated_courses})

    