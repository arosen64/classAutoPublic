import json
from Course import Course
from Message import Gmail
import datetime as dt
from enviorVars import RECEIVER_EMAIL

"""
IMPORTANT SET UP NOTES:
    1. MULTIPLE KEYWORD WEIGHTS NEED TO BE FIRST AND ALL CHARACTERS HAVE TO BE LOWER CASE
    2. grades.json needs to be initiated with all the courses and they need to be empty
    3. gradescope assignments are prioritized over canvas assignments
"""

# EXAMPLE FROM LAST SEMESTER
def MFCS_quiz_filter(assignment_list):
    grades = []
    for assignment in assignment_list:
        grades.append(assignment.grade)
    grades.sort()
    # drops the lowest 2 quizzes
    return grades[2:]

def IP_midterm_filter(assignment_list):
    grades = []
    for assignment in assignment_list:
        if not ('project' in assignment.name.lower()):
            grades.append(assignment.grade)
    return grades

semester = [

    Course(name='MFCS',
           weights={'/':(None,.03),'prepwork':(None, .05), 'worksheet':(None, .05), 'quiz':(MFCS_quiz_filter, .09),'midterm':(None, .48), 'final':(None,.3)},
           cal_id='c6a8c5ea35f66c508373dbfbd97813b4d16e19ab61ddfceec03f9bfa561d4c85@group.calendar.google.com',
           canvas_id=67897,
           gradescope_id=722639
    ),

    Course(name='IP',
           weights={'roll call':(None, .05), 'written': (None, .06), 'hw!coding': (None, .3), 'midterm!project': (None,.14), 'midterm': (IP_midterm_filter,.15), 'final project': (None,.15), 'final exam':(None,.15)},
           cal_id='2bdd14e3f70985c29b9c45f2605550f1af732ba95b40442bd9f77e5a2f1ac4d7@group.calendar.google.com',
           gradescope_id=701550, 
           canvas_id=64623
    ),

    Course(name='Reintro',
           weights={'feeder':(None,.2),'podcast':(None,.2), 'policy brief':(None,.2), 'personal essay':(None, .2), 'engagement':(None,.2)},
           cal_id='6b6cb61fb0c500f6d426b637d23bea716f4e0e6b01ea21a1df76809e3fe088cb@group.calendar.google.com',
           canvas_id=49346
    ),

    Course(name='gateway',
           weights={'class prep':(None, .08), 'attendance':(None, .02), 'quiz':(None, .3), 'project':(None, .35), 'final exam': (None, .25)},
           cal_id='asdfg@group.calendar.google.com',
           canvas_id=49415,
           gradescope_id=587131
    )
]

new_grades = {}
mail = Gmail()
for course in semester:
    print(f'getting assignments for: {course.name}...')
    course.get_assignments()
    print('got assignments!')
    print(f'adding assignments for: {course.name}...')
    course.add_assignments()
    print('added assignments!')
    new_grades[course.name] = f'{course}'


with open('../grades.json','r') as f:
    old_grades = json.load(f)

# checking if there are any updates to the grades:
alert = ""
for course in new_grades.keys():
    if old_grades[course] != f'{new_grades[course]}':
        alert += f'{new_grades[course]}\n\n'

# sends message if there is a change
if alert:
    mail.send_message(RECEIVER_EMAIL,f'Class Update ({dt.datetime.now().date()})', alert)

    # writes the new grades to the grades file
    with open('../grades.json','w') as f:
        f.write(json.dumps(new_grades))

    print("new grades!")




