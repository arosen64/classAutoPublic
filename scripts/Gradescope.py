from enviorVars import USER_EMAIL, USER_PASSWORD
from gradescopeapi.classes.connection import GSConnection
from Assigned import Assigned

class Gradescope_Class:
    def __init__(self,ID):
        self.connection = GSConnection()
        self.connection.login(USER_EMAIL, USER_PASSWORD)
        self.id = ID
    
    def get_assignments(self,category_list:list=[]) -> list:
        assignments_list = []
        assignments = self.connection.account.get_assignments(self.id)
        
        # getting assignments
        for assignment in assignments:
            submitted = (assignment.submissions_status == 'Submitted')
            added = False
            
            # grade is 0 if have not submitted
            if not submitted:
                grade =  0
            elif (type(assignment.grade) == type(None)) or (not assignment.max_grade):
                grade = None
            else:
                grade = (assignment.grade/assignment.max_grade) * 100
            
            submitted = (assignment.submissions_status == 'Submitted')

            # adding a category
            added = False
            for cat in category_list:
                # making it so there can be multiple keywords
                if "!" in cat:
                    cats = cat.split('!')
                    key_word_count = 0
                    for split_cat in cats:
                        if split_cat in assignment.name.lower():
                            key_word_count += 1

                    # has to have all keywords exactly
                    if len(cats) == key_word_count:
                        assignments_list.append(Assigned(assignment.due_date,assignment.name,category=cat,submitted=submitted,grade=grade))
                        added = True
                        break
                
                elif cat in assignment.name.lower():
                    assignments_list.append(Assigned(assignment.due_date,assignment.name,category=cat,submitted=submitted,grade=grade))
                    added = True
                    break

            if not added:
                assignments_list.append(Assigned(assignment.due_date,assignment.name,submitted=submitted,grade=grade))
        
        return assignments_list

                    
                    
        

if __name__ == "__main__":
    IP_gradescope = Gradescope_Class(701550)
    assignment_list = IP_gradescope.get_assignments([])
    for assignment in assignment_list:
        print(assignment)
        print()