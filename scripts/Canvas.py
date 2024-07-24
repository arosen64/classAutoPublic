from enviorVars import CANVAS_KEY, CANVAS_HEADER, USER_ID
from Assigned import Assigned
import datetime as dt
import requests as rq
import json

class Canvas_Class:
    def __init__(self,ID:int):
        self.ID = ID
        self.grades = []
    
    def get_assignments(self,category_list:list=[]) -> list:
        # get assignment categories
        response_cats = rq.get(f'{CANVAS_HEADER}/courses/{self.ID}/assignment_groups?access_token={CANVAS_KEY}')
        categories = response_cats.json()
        for category in categories:
            category_id = category['id']
            response_assign = rq.get(f'{CANVAS_HEADER}/courses/{self.ID}/assignment_groups/{category_id}/assignments?access_token={CANVAS_KEY}')

            # getting actual assignments
            for assignment in response_assign.json():
                # getting high level assignment info
                assignment_id = assignment['id']
                name = assignment['name']
                points_possible = assignment['points_possible']
                is_quiz = assignment['is_quiz_assignment']
                due_date = assignment['due_at']

                # retrieving assignment specific information
                assignment_specifics = rq.get(f'{CANVAS_HEADER}/courses/{self.ID}/assignments/{assignment_id}/submissions/{USER_ID}?access_token={CANVAS_KEY}').json()
                if ('score' in  assignment_specifics.keys()):
                    if (assignment_specifics['score'] != None) and (points_possible != None):
                        grade = (float(assignment_specifics['score'])/float(points_possible))*100
                else:
                    grade = None

                # formatting time
                if (type(due_date) == type(None)) and (is_quiz):
                    due_date = dt.datetime.fromisoformat(assignment['unlock_at']) 
                elif type(due_date) != type(None):
                    due_date = dt.datetime.fromisoformat(due_date)

                if type(assignment_specifics['submitted_at']) != type(None):
                    submitted = True
                else:
                    submitted = False
                
                # adding a category
                added = False
                for cat in category_list:
                    # making it so there can be multiple keywords
                    if "!" in cat:
                        cats = cat.split('!')
                        key_word_count = 0
                        for split_cat in cats:
                            if split_cat in name.lower():
                                # has to have all keywords exactly
                                key_word_count += 1
                        
                        # has to have all keywords exactly to be added
                        if key_word_count == len(cats):
                            self.grades.append(Assigned(due_date,name,cat,submitted,grade))
                            added = True
                            break
                    
                    elif cat in name.lower():
                        # putting all the info in an Assigned object
                        self.grades.append(Assigned(due_date,name,cat,submitted,grade))
                        added = True
                    
                # putting all the info in an Assigned object
                if not added:
                    self.grades.append(Assigned(due_date,name,submitted=submitted,grade=grade))


        return self.grades