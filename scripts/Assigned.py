class Assigned:
    def __init__(self,due_date,name,category=None,submitted=False,grade=None):
        self.due_date = due_date
        self.category = category
        self.name = name
        self.submitted = submitted
        self.grade = grade
    
    def __repr__(self):
        string = ""
        string += f'{self.name}:\n DUE DATE: {self.due_date}\n SUBMITTED: {self.submitted}\n GRADE : {self.grade}'
        return string
    
    def __eq__(self, other) -> bool:
        return (self.name.lower() == other.name.lower())