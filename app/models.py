from app import db
from sqlalchemy.orm import relationship
# class Projects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     projectleader = db.Column(db.String(35))    

#     def __repr__(self):
#         return '<Project %r>' % (self.name)








class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    name=db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    authenticated = db.Column(db.Boolean, default=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    emanio= db.Column(db.Integer)
    MHorSUD= db.Column(db.String(64), index=True)
    keyQuestions= db.Column(db.String(64), index=True)
    problem= db.Column(db.String(64), index=True)
    specialFacts= db.Column(db.String(64), index=True)
    requestDate= db.Column(db.DateTime, index=True)
    requestDeadlineLapse= db.Column(db.Integer)
    requestedBy= db.Column(db.String(64), index=True)
    deadlinedate= db.Column(db.Date)
    priority= db.Column(db.String(64), index=True)
    deliveryFormat= db.Column(db.String(64), index=True)
    timeframe= db.Column(db.String(64), index=True)
    timeBreakdown= db.Column(db.String(64), index=True)
    specialPop= db.Column(db.String(64), index=True)
    agency= db.Column(db.String(400), index=True)
    ru = db.Column(db.String(64), index=True)
    typeOfService= db.Column(db.String(64), index=True)
    jobTitle= db.Column(db.String(64), unique=True)
    longDescription= db.Column(db.String(64), index=True)
    specialInstructions= db.Column(db.String(64), index=True)
    audience= db.Column(db.String(64), index=True)
    columnsRequired= db.Column(db.String(64), index=True)
    assigned= db.Column(db.String(64), index=True)
    completeDate= db.Column(db.Date)
    reviewed= db.Column(db.Boolean())
    userCategory= db.Column(db.String(64), index=True)
    deadlinetime =db.Column(db.Integer)
    deadlineWhy =  db.Column(db.String(64), index=True)
    timeframestart =db.Column(db.Date)
    timeframeend= db.Column(db.Date)
    note= db.Column(db.String(120), index=True)
    Response= db.Column(db.String(120), index=True)
    ourdeadline= db.Column(db.Date)
    supervisor= db.Column(db.String(120), index=True)
    cc_sup=db.Column(db.Boolean())
    status= db.Column(db.String(120), index=True)
    RejBoolkeyQuestions= db.Column(db.Boolean())   
    RejxkeyQuestions= db.Column(db.String(120), index=True)
    RejBoolproblem= db.Column(db.Boolean())       
    Rejxproblem= db.Column(db.String(120), index=True)
    RejBoolspecialFacts= db.Column(db.Boolean())      
    RejxspecialFacts= db.Column(db.String(120), index=True)
    RejBoolrequestDate= db.Column(db.Boolean())       
    RejxrequestDate= db.Column(db.String(120), index=True)
    RejBoolrequestedBy=  db.Column(db.Boolean())      
    RejxrequestedBy=  db.Column(db.String(120), index=True)
    RejBooldeadlinedate=  db.Column(db.Boolean())     
    Rejxdeadlinedate=  db.Column(db.String(120), index=True)
    RejBoolpriority=  db.Column(db.Boolean())     
    Rejxpriority=  db.Column(db.String(120), index=True)
    RejBooldeliveryFormat=  db.Column(db.Boolean())       
    RejxdeliveryFormat=  db.Column(db.String(120), index=True)
    RejBooltimeframe= db.Column(db.Boolean())     
    Rejxtimeframe= db.Column(db.String(120), index=True)
    RejBooltimeBreakdown=  db.Column(db.Boolean())        
    RejxtimeBreakdown=  db.Column(db.String(120), index=True)
    RejBoolspecialPop=  db.Column(db.Boolean())       
    RejxspecialPop=  db.Column(db.String(120), index=True)
    RejBoolagency=  db.Column(db.Boolean())       
    Rejxagency=  db.Column(db.String(120), index=True)
    RejBoolru =  db.Column(db.Boolean())      
    Rejxru =  db.Column(db.String(120), index=True)
    RejBooltypeOfService=  db.Column(db.Boolean())        
    RejxtypeOfService=  db.Column(db.String(120), index=True)
    RejBooljobTitle=  db.Column(db.Boolean())     
    RejxjobTitle=  db.Column(db.String(120), index=True)
    RejBoollongDescription=  db.Column(db.Boolean())      
    RejxlongDescription=  db.Column(db.String(120), index=True)
    RejBoolspecialInstructions=  db.Column(db.Boolean())      
    RejxspecialInstructions=  db.Column(db.String(120), index=True)
    RejBoolaudience=  db.Column(db.Boolean())     
    Rejxaudience=  db.Column(db.String(120), index=True)
    RejBoolcolumnsRequired=  db.Column(db.Boolean())      
    RejxcolumnsRequired=  db.Column(db.String(120), index=True)
    RejBooldeadlinetime = db.Column(db.Boolean())     
    Rejxdeadlinetime = db.Column(db.String(120), index=True)
    RejBooldeadlineWhy =   db.Column(db.Boolean())        
    RejxdeadlineWhy =   db.Column(db.String(120), index=True)
    RejBooltimeframestart = db.Column(db.Boolean())       
    Rejxtimeframestart = db.Column(db.String(120), index=True)
    RejBooltimeframeend=  db.Column(db.Boolean())     
    Rejxtimeframeend=  db.Column(db.String(120), index=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    Rejxemanio=  db.Column(db.String(120), index=True)
    RejBoolemanio=  db.Column(db.Boolean()) 
    RejxMHorSUD=  db.Column(db.String(120), index=True)
    RejBoolMHorSUD=  db.Column(db.Boolean())   
    UserAction=  db.Column(db.String(120), index=True)
    def __repr__(self):
        return '%r' % (self.jobTitle)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff = db.Column(db.String(60))
    privelage = db.Column(db.String(30))
    request = db.relationship('Request', lazy='dynamic', backref='staffback',cascade="all, delete-orphan")
    def __repr__(self):
        return (self.staff)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    request = db.relationship('Request', lazy='dynamic', backref='statusback',cascade="all, delete-orphan")
    def __repr__(self):
        return (self.status)

from sqlalchemy import distinct

def getStaff():
    u = Staff.query
    return u

def getStatus():
    u = Status.query
    return u
