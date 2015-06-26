from app import db
from sqlalchemy.orm import relationship
# class Projects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     projectleader = db.Column(db.String(35))    
#     goals = db.relationship('Goals', lazy='dynamic', backref='proj',cascade="all, delete-orphan"
#                                )
#     def __repr__(self):
#         return '<Project %r>' % (self.name)

# class Goals(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     goal = db.Column(db.String(200))
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
#     strategies = db.relationship('Strategies',lazy='dynamic',order_by="Strategies.order", backref='goa',cascade="all, delete-orphan")
#     order = db.Column(db.Integer)                                     

#     def __repr__(self):
#         return '<Goals %r>' % (self.goal)

# class Strategies(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     strategy = db.Column(db.String(200))
#     goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'))
#     tasks = db.relationship('Tasks', lazy='dynamic',order_by="Tasks.order",backref='strat',cascade="all, delete-orphan")
#     order = db.Column(db.Integer)                            
#     def __repr__(self):
#         return '<Strategy %r>' % (self.strategy)

# class Tasks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     task = db.Column(db.String(200))
#     note = db.Column(db.String(400))  
#     complete = db.Column(db.Boolean())
#     staff = db.Column(db.String(50))
#     deadline = db.Column(db.Date)
#     completeDate = db.Column(db.Date)
#     created = db.Column(db.Date)
#     strategy_id = db.Column(db.Integer, db.ForeignKey('strategies.id'))
#     order = db.Column(db.Integer)
#     def __repr__(self):
#         return '<Tasks %r>' % (self.task)

# class FileUpload(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender = db.Column(db.String(50))
#     note = db.Column(db.String(400))  
#     def __repr__(self):
#         return '<sender %r>' % (self.strategy)

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


# class Request(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True)
#     email = db.Column(db.String(120), index=True)
#     emanio= db.Column(db.Integer)
#     MHorSUD= db.Column(db.String(64), index=True)
#     keyQuestions= db.Column(db.String(64), index=True)
#     problem= db.Column(db.String(64), index=True)
#     specialFacts= db.Column(db.String(64), index=True)
#     requestDate= db.Column(db.DateTime, index=True)
#     requestDeadlineLapse= db.Column(db.Integer)
#     requestedBy= db.Column(db.String(64), index=True)
#     deadlinedate= db.Column(db.Date)
#     priority= db.Column(db.String(64), index=True)
#     deliveryFormat= db.Column(db.String(64), index=True)
#     timeframe= db.Column(db.String(64), index=True)
#     timeBreakdown= db.Column(db.String(64), index=True)
#     specialPop= db.Column(db.String(64), index=True)
#     agency= db.Column(db.String(64), index=True)
#     ru = db.Column(db.String(64), index=True)
#     typeOfService= db.Column(db.String(64), index=True)
#     jobTitle= db.Column(db.String(64), unique=True)
#     longDescription= db.Column(db.String(64), index=True)
#     specialInstructions= db.Column(db.String(64), index=True)
#     audience= db.Column(db.String(64), index=True)
#     columnsRequired= db.Column(db.String(64), index=True)
#     assinged= db.Column(db.String(64), index=True)
#     completeDate= db.Column(db.Date)
#     reviewed= db.Column(db.String(64), index=True)
#     userCategory= db.Column(db.String(64), index=True)
#     deadlinetime =db.Column(db.Integer)
#     deadlineWhy = db.Column(db.String(64), index=True)
#     timeframestart =db.Column(db.Date)
#     timeframeend= db.Column(db.Date)
#     note= db.Column(db.String(120), index=True)
#     Response= db.Column(db.String(120), index=True)


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
    assinged= db.Column(db.String(64), index=True)
    assigned= db.Column(db.String(64), index=True)
    completeDate= db.Column(db.Date)
    reviewed= db.Column(db.String(64), index=True)
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

# class Request(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True)
#     email = db.Column(db.String(120), index=True)
#     emanio= db.Column(db.Integer)
#     MHorSUD= db.Column(db.String(64), index=True)
#     keyQuestions= db.Column(db.String(64), index=True)
#     problem= db.Column(db.String(64), index=True)
#     specialFacts= db.Column(db.String(64), index=True)
#     requestDate= db.Column(db.DateTime, index=True)
#     requestDeadlineLapse= db.Column(db.Integer)
#     requestedBy= db.Column(db.String(64), index=True)
#     deadlinedate= db.Column(db.Date)
#     priority= db.Column(db.String(64), index=True)
#     deliveryFormat= db.Column(db.String(64), index=True)
#     timeframe= db.Column(db.String(64), index=True)
#     timeBreakdown= db.Column(db.String(64), index=True)
#     specialPop= db.Column(db.String(64), index=True)
#     agency= db.Column(db.String(64), index=True)
#     ru = db.Column(db.String(64), index=True)
#     typeOfService= db.Column(db.String(64), index=True)
#     jobTitle= db.Column(db.String(64), unique=True)
#     longDescription= db.Column(db.String(64), index=True)
#     specialInstructions= db.Column(db.String(64), index=True)
#     audience= db.Column(db.String(64), index=True)
#     columnsRequired= db.Column(db.String(64), index=True)
#     assinged= db.Column(db.String(64), index=True)
#     assigned= db.Column(db.String(64), index=True)
#     completeDate= db.Column(db.Date)
#     reviewed= db.Column(db.String(64), index=True)
#     userCategory= db.Column(db.String(64), index=True)
#     deadlinetime =db.Column(db.Integer)
#     deadlineWhy =  db.Column(db.String(64), index=True)
#     timeframestart =db.Column(db.Date)
#     timeframeend= db.Column(db.Date)
#     note= db.Column(db.String(120), index=True)
#     Response= db.Column(db.String(120), index=True)
#     ourdeadline= db.Column(db.Date)
#     supervisor= db.Column(db.String(120), index=True)
#     cc_sup=db.Column(db.Boolean())
#     status= db.Column(db.String(120), index=True)
#     RejkeyQuestions= db.Column(db.Boolean())   
#     RejBoolkeyQuestions= db.Column(db.String(120), index=True)
#     Rejproblem= db.Column(db.Boolean())       
#     RejBoolproblem= db.Column(db.String(120), index=True)
#     RejspecialFacts= db.Column(db.Boolean())      
#     RejBoolspecialFacts= db.Column(db.String(120), index=True)
#     RejrequestDate= db.Column(db.Boolean())       
#     RejBoolrequestDate= db.Column(db.String(120), index=True)
#     RejrequestedBy=  db.Column(db.Boolean())      
#     RejBoolrequestedBy=  db.Column(db.String(120), index=True)
#     Rejdeadlinedate=  db.Column(db.Boolean())     
#     RejBooldeadlinedate=  db.Column(db.String(120), index=True)
#     Rejpriority=  db.Column(db.Boolean())     
#     RejBoolpriority=  db.Column(db.String(120), index=True)
#     RejdeliveryFormat=  db.Column(db.Boolean())       
#     RejBooldeliveryFormat=  db.Column(db.String(120), index=True)
#     Rejtimeframe= db.Column(db.Boolean())     
#     RejBooltimeframe= db.Column(db.String(120), index=True)
#     RejtimeBreakdown=  db.Column(db.Boolean())        
#     RejBooltimeBreakdown=  db.Column(db.String(120), index=True)
#     RejspecialPop=  db.Column(db.Boolean())       
#     RejBoolspecialPop=  db.Column(db.String(120), index=True)
#     Rejagency=  db.Column(db.Boolean())       
#     RejBoolagency=  db.Column(db.String(120), index=True)
#     Rejru =  db.Column(db.Boolean())      
#     RejBoolru =  db.Column(db.String(120), index=True)
#     RejtypeOfService=  db.Column(db.Boolean())        
#     RejBooltypeOfService=  db.Column(db.String(120), index=True)
#     RejjobTitle=  db.Column(db.Boolean())     
#     RejBooljobTitle=  db.Column(db.String(120), index=True)
#     RejlongDescription=  db.Column(db.Boolean())      
#     RejBoollongDescription=  db.Column(db.String(120), index=True)
#     RejspecialInstructions=  db.Column(db.Boolean())      
#     RejBoolspecialInstructions=  db.Column(db.String(120), index=True)
#     Rejaudience=  db.Column(db.Boolean())     
#     RejBoolaudience=  db.Column(db.String(120), index=True)
#     RejcolumnsRequired=  db.Column(db.Boolean())      
#     RejBoolcolumnsRequired=  db.Column(db.String(120), index=True)
#     Rejdeadlinetime = db.Column(db.Boolean())     
#     RejBooldeadlinetime = db.Column(db.String(120), index=True)
#     RejdeadlineWhy =   db.Column(db.Boolean())        
#     RejBooldeadlineWhy =   db.Column(db.String(120), index=True)
#     Rejtimeframestart = db.Column(db.Boolean())       
#     RejBooltimeframestart = db.Column(db.String(120), index=True)
#     Rejtimeframeend=  db.Column(db.Boolean())     
#     RejBooltimeframeend=  db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<%r>' % (self.jobTitle)

from sqlalchemy import distinct

def getRequestor():
    u = db.session.query(distinct(Request.requestedBy)).all
    return u


