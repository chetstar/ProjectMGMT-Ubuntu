from flask.ext.wtf import Form
from wtforms import validators
from wtforms import widgets
from wtforms import TextField, BooleanField, SubmitField, DateField,TextAreaField,SelectMultipleField,IntegerField,PasswordField,StringField,DateTimeField,FormField,RadioField,SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import datetime
from wtforms.fields.html5 import DateField
from app.models import getRequestor

class Which(Form):
    formtype = RadioField('how ready are you', choices=[('Long','<h3>Standard data request form (Designed to guide you through your request)</h3><br>'),
        ('Short',"<h3>Data Partner's Advanced form (<strong>be prepared to list all of the columns in the data request</strong>)</h3><br>")],coerce=unicode)
    submit=SubmitField('Submit')

class LoginForm(Form):
    username = StringField('ACBHCS login', validators=[validators.DataRequired()])
    password = PasswordField('Password', [validators.Required()])
    remember_me = BooleanField('remember_me', default=False)
    submit=SubmitField('Submit')

# [validators.Required(),validators.Length(min=2, max=50)]
class RequestData(Form):
    # test= QuerySelectField(query_factory=Requests.with_entities(Requests.id)) 
    jobTitle= TextField('This will be the name we use to communicate about the request.',validators=[validators.Required(),validators.Length(min=2, max=50)])#,
    supervisor= TextField('Who is your supervisor.')#,
    emanio = BooleanField('Yes, I have looked at Context.', default=False)
    Rejxemanio=   TextAreaField('Explantion')
    RejBoolemanio= BooleanField('Incomplete.', default=False)
    requestDate = DateField( 'request date',  format='%m/%d/%Y',)
    RejxrequestDate=   TextAreaField('Explantion')
    RejBoolrequestDate= BooleanField('Incomplete.', default=False)
    MHorSUD= RadioField('Is this MHS or SUD Services related?', choices=[('MHS','MHS'),('SUD','SUD Services')],coerce=unicode)
    longDescription= TextAreaField('Describe what you want to investigate.',validators=[validators.Required(),validators.Length(min=2, max=120)])
    keyQuestions= TextAreaField('What are the questions you want answered?',validators=[validators.Required(),validators.Length(min=2, max=120)])
    problem= TextAreaField('If the data shows a problem, describe your intervention or what data you might you need for that intervention')
    RejBoolproblem= BooleanField('Incomplete.')
    Rejxproblem= TextAreaField('Explantion')
    audience= TextAreaField('With whom or in what forum do you plan to share this data?',)
    columnsRequired= TextAreaField('These are all the columns you will get in your report (chose <a href="//127.0.0.1:8080/long"> general form  </a>if you are unsure)<br> Be sure to include Agency/RUs needed, time frame, special population, etc.,' )
    agency= TextField('For what Agencies do you want this data?', ) 
    Rejxagency=   TextAreaField('Explantion',default='')
    RejBoolagency=  BooleanField('Incomplete.', default=False)
    ru = TextField("Leave blank if you want all RU's for Agency specified above",  ) 
    deadlinetime = SelectField(u'What Hour?',coerce=int, choices=[(8,'8 am'), (9, '9 am'), (10, '10 am'),
        (11, '11 am'), (12, 'Noon'), (13, '1 pm'), (14, '2 pm'), (15, '3 pm'), (16, '4 pm'), (17, '5 pm')])
    deadlinedate= DateField( '',  format='%m/%d/%Y',)
    deadlineWhy = TextField('Why?')
    priority= RadioField('Priority', choices=[('1','1. Just Curious'),('2','2. Low Priority'),('3','3. Medium'),('4','4. Top Priority'),('5','5. Extremely Urgent')],coerce=unicode,validators=[validators.Required()])
    requestedBy= SelectField(u"If this isn't your request, who is it for?",coerce=unicode, choices=[("test1",'test1'), ('2', 'test2')]) 
    # deliveryFormat= TextField('Format for Delivery', [validators.Required(),validators.Length(min=2, max=50)] ) 
    # start and end?
    timeframe= TextField('From what time frame do you want data? E.g., Most recent fiscal year? Most recent calendar year? Some other period?',  ) 
    timeframestart= DateField( '',  format='%m/%d/%Y',)
    timeframeend= DateField( '',  format='%m/%d/%Y',)
    timeBreakdown = TextField("If annual, specify Fiscal Year or Calendar.",  ) 
    specialPop= TextField('Are you interested in any demographics (age, ethnicity) or special populations (foster kids or disabled adults, and so on)?',  ) 
    typeOfService= TextField('Are there specific types of services you want? e.g. Crisis, Hospital, etc.', ) 
    specialInstructions= TextField('Any special instructions?',  ) 
    specialFacts= TextAreaField('Are there any facts or circumstances we should know to fulfill this request?') 
    note = TextAreaField('Note',)
    submit=SubmitField('Submit')
    assigned= TextField('Staff Assigned?') 
    completeDate= DateTimeField( 'Date Completed',  format='%c')
    reviewed= TextField('Reviewed by?') 
    Response=  TextAreaField('Explantion')
    ourdeadline= DateField( '',  format='%m/%d/%Y',)
    cc_sup=RadioField('Is this MHS or SUD Services related?', choices=[('MHS','MHS'),('SUD','SUD Services')],coerce=unicode)
    status= SelectField(u'Status?',coerce=int, choices=[(0,'Lower Priority Request'), (1, 'Incomplete Request'), (2, 'Pending review'),
        (3, 'Assigned'), (4, 'Complete'), (5, 'Rejected')])
    RejxkeyQuestions= RadioField('', choices=[('MHS','MHS'),('SUD','SUD Services')],coerce=unicode)
    RejxspecialFacts=  TextAreaField('Explantion')
    RejxrequestDate=  TextAreaField('Explantion')
    RejxrequestedBy=  TextAreaField('Explantion')
    Rejxdeadlinedate=  TextAreaField('Explantion')
    Rejxpriority=   TextAreaField('Explantion')
    RejxdeliveryFormat= TextAreaField('Explantion')
    Rejxtimeframe=  TextAreaField('Explantion')
    RejxtimeBreakdown= TextAreaField('Explantion')
    RejxspecialPop=   TextAreaField('Explantion')
    Rejxru =   TextAreaField('Explantion')
    RejxtypeOfService=   TextAreaField('Explantion')
    RejxjobTitle=   TextAreaField('Explantion')
    RejxlongDescription=  TextAreaField('Explantion')
    RejxspecialInstructions= TextAreaField('Explantion')
    Rejxaudience=  TextAreaField('Explantion')
    RejxcolumnsRequired=   TextAreaField('Explantion',default='')
    Rejxdeadlinetime =  TextAreaField('Explantion',default='')
    RejxdeadlineWhy =   TextAreaField('Explantion',default='')
    Rejxtimeframestart =  TextAreaField('Explantion',default='')
    Rejxtimeframeend=   TextAreaField('Explantion',default='')
    RejBoolkeyQuestions= BooleanField('Incomplete.', default=False)
    RejBoolspecialFacts= BooleanField('Incomplete.', default=False)
    RejBoolrequestDate= BooleanField('Incomplete.', default=False)
    RejBoolrequestedBy= BooleanField('Incomplete.', default=False)
    RejBooldeadlinedate= BooleanField('Incomplete.', default=False)
    RejBoolpriority=  BooleanField('Incomplete.', default=False)
    RejBooldeliveryFormat=BooleanField('Incomplete.', default=False)
    RejBooltimeframe= BooleanField('Incomplete.', default=False)
    RejBooltimeBreakdown=BooleanField('Incomplete.', default=False)
    RejBoolspecialPop=  BooleanField('Incomplete.', default=False)
    RejBoolru =  BooleanField('Incomplete.', default=False)
    RejBooltypeOfService=  BooleanField('Incomplete.', default=False)
    RejBooljobTitle=  BooleanField('Incomplete.', default=False)
    RejBoollongDescription= BooleanField('Incomplete.', default=False)
    RejBoolspecialInstructions=BooleanField('Incomplete.', default=False)
    RejBoolaudience= BooleanField('Incomplete.', default=False)
    RejBoolcolumnsRequired=  BooleanField('Incomplete.', default=False)
    RejBooldeadlinetime = BooleanField('Incomplete.', default=False)
    RejBooldeadlineWhy =  BooleanField('Incomplete.', default=False)
    RejBooltimeframestart = BooleanField('Incomplete.', default=False)
    RejBooltimeframeend=  BooleanField('Incomplete.', default=False)
    submit=SubmitField('Submit')

# count distinct "name" values
# session.query(func.count(distinct(User.name)))
# http://stackoverflow.com/questions/21579373/sqlalchemy-wtforms-set-default-selected-value-for-queryselectfield
class filterRequests(Form):
    status= SelectField(u'Status?',coerce=unicode, choices=[('No Filter','No Filter'),('Lower Priority Request','Lower Priority Request'),\
     ('Incomplete Request','Incomplete Request'), ('Pending Review', 'Pending Review'),
        ('Assigned', 'Assigned'), ('Complete', 'Complete'), ('Rejected', 'Rejected')],default='No Filter')
    requestedBy= SelectField(u'Requestor',default='No Filter')
    assigned= SelectField(u'Assigned',default='No Filter')
    # requestor = QuerySelectField(u'Requestor', query_factory=getRequestor, get_label='requestedBy')
    # assigned = QuerySelectField(u'Assigned', query_factory=getRequestor, get_label='assigned')
    submitFilter=SubmitField('Filter')
# class project_form(Form):
#     project = TextField('Project *', [validators.Required(),validators.Length(min=2, max=50)] ) 
#     projectleader = TextField('Project Leader *(required)', [validators.Required(),validators.Length(min=4, max=35,message='not the right length')] ) 
#     submit=SubmitField('Add Project')

# class goal_form(Form):
#     goal = TextAreaField('Goal', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
#     submit=SubmitField('Add Objective')

# class strategy_form(Form):
#     strategy = TextAreaField('Strategy', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
#     submit=SubmitField('Add Strategy')

# class task_form(Form):
#     task = TextAreaField('Task', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
#     staff = TextField('Staff Assigned')
#     complete = BooleanField('Is the task Complete?')
#     deadline =DateField( 'Deadline (mm/dd/yyyy)',  format='%m/%d/%Y',validators = [validators.Required()])
#     note = TextAreaField('Note',)
#     Order = IntegerField('Order')
#     submit=SubmitField('Submit')

# class DeleteRow_form(Form):
#     row_id = IntegerField('')
#     submitd = SubmitField('Delete')


class ldapA(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Required()])
    submitd = SubmitField('Login')