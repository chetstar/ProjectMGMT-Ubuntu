rm app.db
python db_create.py

python
from app import db, models
x=models.User(name='Chet Meinzer',email='meinzerc@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
x=models.User(name='Janet Biblin',email='jbiblin@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
x=models.User(name='John Engstrom',email='jEngstrom@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
g=models.Staff(staff='Unassigned',privelage='')
x=models.Staff(staff='Chet Meinzer',privelage='admin')
y=models.Staff(staff='Hall',privelage='')

db.session.add(y)
db.session.add(x)
db.session.add(g)
db.session.commit()


# a=models.Status(status='No Filter')
# db.session.add(a)
# db.session.commit()
a=models.Status(status='Needs Review')
db.session.add(a)
db.session.commit()
a=models.Status(status='Lower Priority Request')
db.session.add(a)
db.session.commit()
a=models.Status(status='Incomplete Request')
db.session.add(a)
db.session.commit()
a=models.Status(status='Pending Review')
db.session.add(a)
db.session.commit()
a=models.Status(status='Assigned')
db.session.add(a)
db.session.commit()
a=models.Status(status='Rejected-Hold')
db.session.add(a)
db.session.commit()
a=models.Status(status='Rejected-Send Back to user')
db.session.add(a)
db.session.commit()
a=models.Status(status='Complete')
db.session.add(a)
db.session.commit()
import datetime

p=models.Request(email='cmeinzer@acbhcs.org',username='chet',jobTitle='faketest',deadlinedate=datetime.datetime.utcnow(),
        emanio=True,MHorSUD='MHS',agency='A Better Way',
        keyQuestions='jjj', problem='jjjj',requestedBy='chet', 
        priority=1,staffback=models.Staff.query.filter_by(staff="Unassigned").first(),
        statusback=models.Status.query.filter_by(status="Pending Review").first(), timeframestart=datetime.datetime.utcnow(),
         timeframeend=datetime.datetime.utcnow(), 
         longDescription='xxx', requestDate=datetime.datetime.utcnow(),assigned="Unassigned",status="Pending Review",
        deadlinetime=datetime.datetime.utcnow())
db.session.add(p)
db.session.commit()

# a=models.Status(status='No Filter')
# db.session.add(a)
# db.session.commit()
# a=models.Status(status='No Filter')
# db.session.add(a)
# db.session.commit()




quit()

python run.py


# status= SelectField(u'Status?',coerce=unicode, choices=[('No Filter','No Filter'),('Needs Action','Needs Action'),('Lower Priority Request','Lower Priority Request'),\
#      ('Incomplete Request','Incomplete Request'), ('Pending Review', 'Pending Review'),
#         ('Assigned', 'Assigned'), ('Complete', 'Complete'), ('Rejected-Hold', 'Rejected-Hold'),("Rejected-Send Back to user","Rejected-Send Back to user")],default='No Filter')
