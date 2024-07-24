# PREREQUISITES:
**1. python3.12**

**2. Canvas api key**

**3. Gradescope user id**

**4. google api config file with google calendar and gmail permissions**

enabling apis: https://console.cloud.google.com/apis/library

getting config file (might need to look up tutorial for this one): https://console.cloud.google.com/apis

# SETUP:
**1. create .env file with the following variables (should be placed in the scripts directory):**
```
CANVAS_KEY=KeyRetrievedEarlier 
USER_ID=GradescopeUserID
RECEIVER_EMAIL=emailForNotifsToBeSentTo
SENDER_EMAIL=gmailAccountThatWillSendTheNotifs
USER_PASSWORD=GradescopePassword
```

**2. put the google config file from before in the scripts directory**

**3. create a grades.json file in the main directory (should resemble below, but with as many classes as desired):**
```
{"Classname1": "",
"Classname2": "",
"Classname3": "",
"Classname4": ""}
```

**4. create a virtual environment using requirements.txt (write commands from the command line in the main directory)**

*step 1:*

```
python -m venv .venv
```

*step 2:*

**WINDOWS:**
```
.venv/Scripts/activate
```
**LINUX & MAC**
```
source .venv/bin/activate
```

*step 3:*
```
pip install -r requirements.txt
```

**5. change the gradescopeapi**

*step 1:*

open the file
```
.venv/Lib/site-packages/gradescopeapi/classes/_helpers/_assignment_helpers.py
```
in your favorite IDE

*step 2:*

paste the following at around line 137 over the assignments of the release_date, due_date, and late_due_date variables
```
# change to datetime objects
        try:
            release_date = (
            datetime.fromisoformat(release_date) if release_date else release_date
            )
        except UnboundLocalError:
            release_date = None

        try:
            due_date = datetime.fromisoformat(due_date) if due_date else due_date
        except UnboundLocalError:
            due_date = None

        try:
            late_due_date = (
                datetime.fromisoformat(late_due_date) if late_due_date else late_due_date
            )
        except UnboundLocalError:
            late_due_date = None
```

**6. replace the examples in main.py with your own classes and run!**










