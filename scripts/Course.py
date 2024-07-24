from Gradescope import Gradescope_Class as GSC
from Canvas import Canvas_Class as CC
from Calendar import Google_Calendar
from Message import Gmail
import datetime as dt
from enviorVars import SENDER_EMAIL, RECEIVER_EMAIL

class Course:
    # initiating the calendar
    calendar = Google_Calendar()
    # initiating the email
    mail = Gmail()

    def __init__(self, name:str, weights:dict, cal_id:str, gradescope_id:int=0, canvas_id:int=0):
        self.GS_ID = gradescope_id
        self.name = name
        self.weights = weights
        self.C_ID = canvas_id
        self.cal_id = cal_id
        self.assignments =  []
    
    def get_assignments(self,online=True):
        gradescope_assignments = []
        canvas_assignments = []
        self.assignments = []
        categories = list(self.weights.keys())

        # getting assignments
        if online:
            if self.GS_ID:
                gradescope_assignments = GSC(self.GS_ID).get_assignments(categories)
            if self.C_ID:
                canvas_assignments = CC(self.C_ID).get_assignments(categories)

        # tracking the names that have already been added
        already_in = []
        
        # adding gradescope assignments
        for G_assignment in gradescope_assignments:
            if not (G_assignment.name in already_in):
                self.assignments.append(G_assignment)
                already_in.append(G_assignment.name)

        # adding canvas assignments
        for C_assignment in canvas_assignments:
            if not (C_assignment.name in already_in):
                self.assignments.append(C_assignment)
                already_in.append(C_assignment.name)

        return self.assignments

    def get_average(self,category:str) -> float:
        custom_filter = self.weights[category][0]
        assignments_in_category = []
        grades = []

        # filtering the assignments by category
        for assignment in self.assignments:
            if assignment.category == category:
                # making it so unsubmitted grades before the due date have no grade
                if (not assignment.submitted) and (type(assignment.due_date) != type(None)):
                    if (assignment.due_date.replace(tzinfo=None) > dt.datetime.now()):
                        assignment.grade = None
                # adding assignment to a category
                assignments_in_category.append(assignment)

        # filtering the assignments using a filter if desired
        if type(custom_filter) != type(None):
            grades = custom_filter(assignments_in_category)
        else:
            for assignment in assignments_in_category:
                if type(assignment.grade) != type(None):
                    grades.append(assignment.grade)
        
        # returns 0 if there are no grades yet
        if not len(grades):
            return 0
        
        return sum(grades)/len(grades)
    
    # need to have gotten assignments first
    def print_assignments(self):
        for assignment in self.assignments:
            print(assignment)
            print()
    
    def add_assignments(self) -> None:
        events = self.calendar.get_events(self.cal_id)['items']
        event_map = {}
        email_body = ""

        # making the events easily accessible
        for event in events:
            if 'dateTime' in event['start'].keys():
                event_map[event['summary']] = (event['start']['dateTime'], event['id'])
            else:
                event_map[event['summary']] = (event['start']['date'], event['id'])


        
        # adding/updating events only if the event is not in the calendar
        for assignment in self.assignments:
            if type(assignment.due_date) != type(None):
                if assignment.name in event_map.keys():
                    # updating event
                    old_date = dt.datetime.fromisoformat(event_map[assignment.name][0])
                    if assignment.due_date != old_date:
                        self.calendar.update_event(self.cal_id,event_map[assignment.name][1],assignment.due_date,
                                                (assignment.due_date + dt.timedelta(minutes=30)))
                        email_body += f"UPDATED DUE DATE: {assignment.name} now due at {assignment.due_date.date()}\n\n"
                # adding event
                else:
                    self.calendar.add_event(self.cal_id,assignment.name,assignment.due_date,(assignment.due_date + dt.timedelta(minutes=30)))
                    email_body += f"NEW ASSIGNMENT: {assignment.name} due at {assignment.due_date.date()}\n\n"
        
        if email_body:
            self.mail.send_message(RECEIVER_EMAIL,f'Schedule Update: {self.name}', email_body)
    
    def __repr__(self):
        represent_string = f"{self.name}:\n"
        total = 0
        for category, weight_tup in self.weights.items():
            average = self.get_average(category)
            represent_string += f"  {category}: {average}\n"
            total += average * weight_tup[1]
        
        represent_string += f"  total: {total}"

        return represent_string
            

