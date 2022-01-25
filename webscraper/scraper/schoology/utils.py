# splits the schoology href tag link and returns the associated schoology code
def parse_link_to_course_code(link):
    elements = link.split('/')
    return elements[2]