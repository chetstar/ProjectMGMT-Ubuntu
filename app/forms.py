from flask.ext.wtf import Form
from wtforms import validators
from wtforms import widgets
from wtforms import TextField, BooleanField, SubmitField, DateField,TextAreaField,SelectMultipleField,IntegerField,PasswordField,StringField,DateTimeField,FormField,RadioField,SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
import datetime
from wtforms.fields.html5 import DateField
from app.models import getStaff, getStatus
from flask.ext.uploads import UploadSet, IMAGES
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import URLField
from wtforms.validators import url

agenList=[
('A Better Way','A Better Way'),
('A COLLABORATIVE EFFORT GROUP','A COLLABORATIVE EFFORT GROUP'),
('Abode Services','Abode Services'),
('Achieve','Achieve'),
('ACMC HIGHLAND HOSPITAL AOD/MH','ACMC HIGHLAND HOSPITAL AOD/MH'),
('Adode Services','Adode Services'),
('Afghan Coalition','Afghan Coalition'),
('Alameda','Alameda'),
('ALAMEDA COUNTY FOSTER CARE ASO','ALAMEDA COUNTY FOSTER CARE ASO'),
('Alameda Family Services','Alameda Family Services'),
('ALLIED PSYCHOLOGICAL SERVICES','ALLIED PSYCHOLOGICAL SERVICES'),
('ALLIED PSYCHOLOGY GROUP INC','ALLIED PSYCHOLOGY GROUP INC'),
('Alta Bates','Alta Bates'),
('Alternative Family Services','Alternative Family Services'),
('ANKA','ANKA'),
('Ann Martin','Ann Martin'),
('Asian Community','Asian Community'),
('BACS','BACS'),
('BAY AREA CHILDREN FIRST PRG','BAY AREA CHILDREN FIRST PRG'),
('BAY AREA CLINIC FOR SELF & REL','BAY AREA CLINIC FOR SELF & REL'),
('Bay Area Community Resources','Bay Area Community Resources'),
('Bay Area Youth Center','Bay Area Youth Center'),
('BAY PSYCHIATRIC ASSOC GRP','BAY PSYCHIATRIC ASSOC GRP'),
('Bayfront','Bayfront'),
('Behavioral Health Care','Behavioral Health Care'),
('BEHAVIORAL HEALTH QUEST GRP','BEHAVIORAL HEALTH QUEST GRP'),
('BEHAVIORAL PED. OF BAY AREA','BEHAVIORAL PED. OF BAY AREA'),
('Berkeley','Berkeley'),
('Berkeley Academy','Berkeley Academy'),
('Berkeley Place','Berkeley Place'),
('BERKELEY THERAPY INSTITUTE','BERKELEY THERAPY INSTITUTE'),
('Bonita','Bonita'),
('Boss','Boss'),
('Brighter Beginnings','Brighter Beginnings'),
('Building Future Calworks','Building Future Calworks'),
('Burt Center','Burt Center'),
('BYA','BYA'),
('CALIFORNIA SCHOOL PROF PSYCHOL','CALIFORNIA SCHOOL PROF PSYCHOL'),
('California Specialty','California Specialty'),
('CAPE','CAPE'),
('CATHOLIC CHARTIES ARCHDCSE SF','CATHOLIC CHARTIES ARCHDCSE SF'),
('CATHOLIC COUNSELING SERVICE','CATHOLIC COUNSELING SERVICE'),
('CAUCUS OF SAN LEANDRO','CAUCUS OF SAN LEANDRO'),
('Center for Discovery','Center for Discovery'),
('Center for Family Counseling','Center for Family Counseling'),
('Center for Independent Living','Center for Independent Living'),
('CERI','CERI'),
('CHAA','CHAA'),
('Charis','Charis'),
('Charter','Charter'),
('Child and Youth Crisis Team','Child and Youth Crisis Team'),
('CHILD THERAPY INST OF MARIN','CHILD THERAPY INST OF MARIN'),
("Children's Learning Center","Children's Learning Center"),
('Childrens Hospital','Childrens Hospital'),
('Circle PreSchool','Circle PreSchool'),
('City of Fremont','City of Fremont'),
('CJ Mental Health','CJ Mental Health'),
('COMMUNITY DRUG COUNCIL','COMMUNITY DRUG COUNCIL'),
('COMPREHENSIVE PSYCHIATRIC SERV','COMPREHENSIVE PSYCHIATRIC SERV'),
('Con Rep','Con Rep'),
('Conservatorship','Conservatorship'),
('County Access Svcs','County Access Svcs'),
('County MHS','County MHS'),
('Crestwood','Crestwood'),
('Crisis Response','Crisis Response'),
('CSS','CSS'),
('DAVIS STREET COMMUN CNTR PRG','DAVIS STREET COMMUN CNTR PRG'),
('Devereaux','Devereaux'),
('DN Associates','DN Associates'),
('Early Childhood','Early Childhood'),
('Earth Circles','Earth Circles'),
('East Oakland','East Oakland'),
('EBAC','EBAC'),
('EBCRP','EBCRP'),
('Eden','Eden'),
('Eden Hospital','Eden Hospital'),
('Edgewood','Edgewood'),
('EMQ','EMQ'),
('Esther Clark','Esther Clark'),
('Families First','Families First'),
('Family Paths','Family Paths'),
('Family Service Agency SF','Family Service Agency SF'),
('Family Service San Leandro','Family Service San Leandro'),
('Family Services','Family Services'),
('Family Stress','Family Stress'),
('Family Support Services','Family Support Services'),
('FELDMAN JANICE S','FELDMAN JANICE S'),
('FFS ARROYO COUNSELING SERVICE','FFS ARROYO COUNSELING SERVICE'),
('FFS BAY AREA PSYCHOTHERAPY SVC','FFS BAY AREA PSYCHOTHERAPY SVC'),
('FFS BEHAVIORAL PEDIATRICS INC','FFS BEHAVIORAL PEDIATRICS INC'),
('FFS CALIF MEDICAL FOUNDATION','FFS CALIF MEDICAL FOUNDATION'),
('FFS CENTER FOR FAMILY COUNSEL','FFS CENTER FOR FAMILY COUNSEL'),
('FFS CHARIS YOUTH CENTER','FFS CHARIS YOUTH CENTER'),
('FFS DEL VALLE CLINIC','FFS DEL VALLE CLINIC'),
('FFS FULL CIRCLE PROGRAMS INC','FFS FULL CIRCLE PROGRAMS INC'),
('FFS OASIS CENTER INC','FFS OASIS CENTER INC'),
('FFS SCRIPPS PSYCHOLOGICAL ASSC','FFS SCRIPPS PSYCHOLOGICAL ASSC'),
('FFS SURVIVORS INTERNATIONAL','FFS SURVIVORS INTERNATIONAL'),
('FFS THE 14TH ST MEDICAL GROUP','FFS THE 14TH ST MEDICAL GROUP'),
('Fred Finch','Fred Finch'),
('FREMONT PSYCHIATRY MED GROUP','FREMONT PSYCHIATRY MED GROUP'),
('FRUGE PSYCHOLOGICAL ASSOC GRP','FRUGE PSYCHOLOGICAL ASSOC GRP'),
('GART','GART'),
('GATEWAY COUNSELING GROUP','GATEWAY COUNSELING GROUP'),
("Girl's Inc.","Girl's Inc."),
('Girls Inc','Girls Inc'),
('Glass','Glass'),
('Goals for Women','Goals for Women'),
('Guidance Clinic','Guidance Clinic'),
('HCSA','HCSA'),
('HIAWATHA HARRIS INC.','HIAWATHA HARRIS INC.'),
('Highland','Highland'),
('HIGHVIEW CONVALESCENT HOSPITAL','HIGHVIEW CONVALESCENT HOSPITAL'),
('Hold for next provider','Hold for next provider'),
('Horizon','Horizon'),
('Hospital','Hospital'),
('HUMBOLDT COUNTY MNTL HLTH DEPT','HUMBOLDT COUNTY MNTL HLTH DEPT'),
('Hume Center','Hume Center'),
('INTEGRATED COUNSEL/CONSULTSRVC','INTEGRATED COUNSEL/CONSULTSRVC'),
('INTERNATIONAL PSY CONSLTG INST','INTERNATIONAL PSY CONSLTG INST'),
('JDT Consultants','JDT Consultants'),
('Jewish Family','Jewish Family'),
('John George','John George'),
('KAIR IN-HOME SOCIAL SRVCS GRP','KAIR IN-HOME SOCIAL SRVCS GRP'),
('KAIROS UNLIMITED','KAIROS UNLIMITED'),
('KAISER PERMANENTE GRP PRACTICE','KAISER PERMANENTE GRP PRACTICE'),
('Kidango','Kidango'),
('La Cheim','La Cheim'),
('La Clinica','La Clinica'),
('La Familia','La Familia'),
('Langley Porter','Langley Porter'),
('LifeLong','LifeLong'),
('Lincoln','Lincoln'),
('MEDICAL HILL BAY AREA NEUROPGM','MEDICAL HILL BAY AREA NEUROPGM'),
('MEDICAL HILL SNF DAY AUGMENTAT','MEDICAL HILL SNF DAY AUGMENTAT'),
('Milhous','Milhous'),
('Mt Diablo','Mt Diablo'),
('Multilingual Counseling','Multilingual Counseling'),
('Napa','Napa'),
('Native American','Native American'),
('Neuro Psych Alliance GRP','Neuro Psych Alliance GRP'),
('New Bridge','New Bridge'),
('NORTH BERKELEY COUNSELING CENT','NORTH BERKELEY COUNSELING CENT'),
('NURSES IN ACTION','NURSES IN ACTION'),
('Oakland','Oakland'),
('Opportunity Plus','Opportunity Plus'),
('Options','Options'),
('OUSD','OUSD'),
('Out of County Hospital','Out of County Hospital'),
('PACIFIC CENTER FOR HUMAN GROWT','PACIFIC CENTER FOR HUMAN GROWT'),
("Pacific Children's Center","Pacific Children's Center"),
('PACIFIC FORENSIC PSY ASSOC GRP','PACIFIC FORENSIC PSY ASSOC GRP'),
('Pathways to Wellness','Pathways to Wellness'),
('PSC','PSC'),
('PSY THERAPY INST INDIV FAM&COM','PSY THERAPY INST INDIV FAM&COM'),
('PSYCHOLOGICAL TREATMENT SVCS','PSYCHOLOGICAL TREATMENT SVCS'),
('R & R','R & R'),
('R House','R House'),
('Recovery Innovations','Recovery Innovations'),
('Refuge','Refuge'),
('RICHARD G JIMENEZ MD INC','RICHARD G JIMENEZ MD INC'),
('RIDING HIGH EQUESTRIAN PROGRAM','RIDING HIGH EQUESTRIAN PROGRAM'),
('River Oak','River Oak'),
('Ross Hospital','Ross Hospital'),
("Saint Vincent's","Saint Vincent's"),
('SANTA CLARA VALLEY MNTL HLTH','SANTA CLARA VALLEY MNTL HLTH'),
('Schuman Liles','Schuman Liles'),
('SECOND CHANCE','SECOND CHANCE'),
('Seneca','Seneca'),
('SENIOR PSYCHOLOGY SERVICES','SENIOR PSYCHOLOGY SERVICES'),
('SHASTA COUNTY MNTL HLTH DEPT','SHASTA COUNTY MNTL HLTH DEPT'),
('SHERIFF YFSB','SHERIFF YFSB'),
('Sierra Vista','Sierra Vista'),
('ST JOSEPHS CNTR DEAF/HARD HEAR','ST JOSEPHS CNTR DEAF/HARD HEAR'),
("St Luke's Hospital","St Luke's Hospital"),
("ST MARY'S CENTER","ST MARY'S CENTER"),
("ST. MARY'S MEDICAL CENTER","ST. MARY'S MEDICAL CENTER"),
('STANISLAUS COUNTY DEP MNTL HLT','STANISLAUS COUNTY DEP MNTL HLT'),
('Star View','Star View'),
('Starlight','Starlight'),
('Stars','Stars'),
('Summit View','Summit View'),
('Sunbridge','Sunbridge'),
('Sunny Hills','Sunny Hills'),
('SUTTER-YUBA MENTAL HLTH SRVCS','SUTTER-YUBA MENTAL HLTH SRVCS'),
('System of Care','System of Care'),
('TEENS IN CRISIS','TEENS IN CRISIS'),
('TeleCare','TeleCare'),
('The Help Group','The Help Group'),
('THE LINK TO CHILDREN PRG','THE LINK TO CHILDREN PRG'),
('The Wright Institute','The Wright Institute'),
('Through the Looking Glass','Through the Looking Glass'),
('Thunder Road','Thunder Road'),
('Tiburcio Vasquez','Tiburcio Vasquez'),
('TRADITIONS BEHAV HEALTH GROUP','TRADITIONS BEHAV HEALTH GROUP'),
('TRADITIONS BEHAVIORAL HLTH GRP','TRADITIONS BEHAVIORAL HLTH GRP'),
('Tri-City','Tri-City'),
('TRI-CITY HEALTH CENTER GRP','TRI-CITY HEALTH CENTER GRP'),
('TRI-VALLEY HAVEN','TRI-VALLEY HAVEN'),
('TRIAD FAMILY SERVICES','TRIAD FAMILY SERVICES'),
('TRINITY HEALTH CENTER','TRINITY HEALTH CENTER'),
('True to Life','True to Life'),
('TRUST','TRUST'),
('TURNING POINT COUNSELING CNTR','TURNING POINT COUNSELING CNTR'),
('UCSF Center on Deafness','UCSF Center on Deafness'),
('Unity','Unity'),
('Unity Care','Unity Care'),
('UNITY CONCEPTS INC','UNITY CONCEPTS INC'),
('Valley','Valley'),
('VALLEY COMMUNITY HEALTH CTR','VALLEY COMMUNITY HEALTH CTR'),
('VALUE OPTIONS INC','VALUE OPTIONS INC'),
('Victor','Victor'),
('Vocational','Vocational'),
('West Coast','West Coast'),
('West Oakland','West Oakland'),
('WILLIAM SPIVEY PHD INC dba F/C','WILLIAM SPIVEY PHD INC dba F/C'),
('YOUTH HOMES INC','YOUTH HOMES INC'),
('Youth Uprising','Youth Uprising'),
]

images = UploadSet('images', IMAGES)


class rutablefilter(Form):
    provsearch=TextField('Search Providor name')
    level_3_classic=BooleanField('Include Level 3 (doctors)', default=False)
    missing    = SelectField(u"Show missing by....",coerce=unicode, choices=[('None','None'),
('ab3632','ab3632'),
('agency','agency'),
('calworks','calworks'),
('cesdc','cesdc'),
('county_run','county_run'),
('day_treatment','day_treatment'),
('dbservicemodality','dbservicemodality'),
('end_date','end_date'),
('epsdtgroup','epsdtgroup'),
('financial_responsibility','financial_responsibility'),
('kidsru','kidsru'),
('level_2','level_2'),
('level_3_classic','level_3_classic'),
('mhsa','mhsa'),
('older_adult','older_adult'),
('old_ru','old_ru'),
('cans','cans'),
('out_of_county','out_of_county'),
('program','program'),
('provider_name','provider_name'),
('psmasktext','psmasktext'),
('residential','residential'),
('reporting_unit','reporting_unit'),
('predesessor','predesessor'),
('city','city'),
('in_school','in_school'),
('school_cds_id','school_cds_id'),
('start_date','start_date'),
('mode_of_service','mode_of_service'),
('svctype','svctype'),
('svctype3','svctype3'),
('tay','tay'),
('tbs','tbs'),
('umbrella_organization','umbrella_organization')],default="None") 
    submit=SubmitField('Submit')
   
class rutable(Form):
    # Tags = QuerySelectField(u'Category', query_factory=getTags, get_label='Category',default="Unassigned")
    ab3632        = BooleanField('ab3632')  
    agency        =TextField('agency')  
    calworks        = BooleanField('calworks')  
    school_cds_id       =TextField('school_cds_id')  
    cesdc        = BooleanField('cesdc')  
    county_run        = BooleanField('county')   
    day_treatment        = BooleanField('day_treatment')  
    dbservicemodality      =  SelectField(u"Service Modality",coerce=unicode, choices=[
        ('',"None"),
    ('SubAcute','SubAcute'),
    ('Residential Treatment','Residential Treatment'),
    ('Outpatient Services','Outpatient Services'),
    ('JailOrJuvJusticeCenter','JailOrJuvJusticeCenter'),
    ('CrisisStabilization','CrisisStabilization'),
    ('Day Treatment','Day Treatment'),
    ('SvcTeamFSP','SvcTeamFSP'),  
        ('Hospital','Hospital')
        ]     
        )
    # end_date        = DateTimeField('end_date')  
    epsdtgroup        =TextField('epsdtgroup')   
    # financial_responsibility    = IntegerField('financial_responsibility')   
    kidsru        = BooleanField('kidsru')  
    level_2        = BooleanField('level_2') 
    level_3_classic        = BooleanField('Level3Classic')  
    mhsa        = BooleanField('mhsa')  
    older_adult        = BooleanField('older_adult')  
    # old_ru     = IntegerField('old RU') 
    cans        = BooleanField('cans')  
    out_of_county        = BooleanField('out_of_county')   
    program        = BooleanField('program')  
    # provider_name        =TextField('provname')  
    psmasktext        = SelectField(u"PSmask Text",coerce=unicode, choices=[
        ('',"None"),
("Children's Crisis Services","Children's Crisis Services"),
('MHRC/Subacute',' MHRC/Subacute'),
('Adult Residential Treament',' Adult Residential Treament'),
('Adult  Crisis Services',' Adult  Crisis Services'),
('Adult Day Treatment',' Adult Day Treatment'),
('Adult Medication Clinics',' Adult Medication Clinics'),
('MHSA Full Service Partnerships',' MHSA Full Service Partnerships'),
('Other MHS Adult',' Other MHS Adult'),
( 'Child Day Treament Day Unit',' Child Day Treament Day Unit'),
('Child Community Support Services',' Child Community Support Services'),
('School-Based Outpatient Services',' School-Based Outpatient Services'),
("Children's Medication Clinics","Children's Medication Clinics"),
('Child Day Treatment Hour Unit',' Child Day Treatment Hour Unit'),
('Adult Community Support Services',' Adult Community Support Services'),
('Children in Out-of-County Placeme',' Children in Out-of-County Placeme'),
('Support Services',' Support Services'),
('Forensic',' Forensic'),
('NeuroBehavioral/OBS',' NeuroBehavioral/OBS'),
('Local Hospital',' Local Hospital'),
("Other Children's Service"," Other Children's Service"),
        ]     
        )
    residential        = BooleanField('residential')  
    # reporting_unit        =TextField('ru') 
    # predesessor        =TextField('predesessor')   
    # city        =TextField('city')  
    # safe_passages        = BooleanField('safe_passages')
    school        = BooleanField('school')   
    # start_date        = DateTimeField('start_date')  
    # mode_of_service        =TextField('mode_of_service')   
    svctype        =TextField('svctype')  
    svctype3        =TextField('svctype3')   
    tay        = BooleanField('tay')   
    tbs        = BooleanField('tbs')  
    # umbrella_organization        = IntegerField('umbrella_organization')  
    submitRU=SubmitField('Submit')

class cans(Form):
    cans = BooleanField('cans') 
    submitRU=SubmitField('Submit')

class TOC(Form):
    Agency= TextField("What Agency is included in the report")
    kill = IntegerField("Record a 1 if the dashboard or report is not to be show in the Context! Table of Contents; record 0 otherwise")
    DashboardQuestion = IntegerField("What question(s) does the report or dashboard answer?")
    DashboardReportSort = IntegerField("1 if it a Dashboard, 2 if it is a Report")
    DorR =TextField('Record "Dashboard" or "Report')
    DashboardReport = TextField("Record the name of the dashboard or report")
    SystemofCare = TextField("Record the System(s) of Care the dashboard or report is relevant to.")
    ServiceArea = TextField("Record the service area the report covers.")
    Description = TextAreaField("Describe the dashboard or report.")
    Purpose =TextAreaField("Describe the purpose of the dashboard or report.")
    iddeid =TextAreaField("Is the dashboard or report identified or de-identified?")
    TargetedAudience =TextAreaField("Who is the target audience for the dashboard or report?")
    Supportswhichmeeting = IntegerField("Which meeting does the report or dashboard support?")
    Ready = IntegerField("Is the dashboard or report ready for deployment?")
    Link =TextAreaField("Copy and paste the dashboard or report link from Context!")
    KeyQuestions =TextAreaField("What are the key questions the dashboard or report answers?")
    BornOnDate   =  DateField( "Record the date on which a dashboard or report was born",  format="%m/%d/%Y",)
    FinalCodeReviewDate    = DateField("On what date was the code approved?", format="%m/%d/%Y",)
    CodeAuthor     =TextAreaField("Who was/were the author(s) of the code?")
    CodeReviewer   =TextAreaField("Who was the final reviewer of the code?")
    FinalReportReviewDate    = DateField("On what date was the dashboard or report approved?",  format="%m/%d/%Y",)  
    ReportAuthor   =TextAreaField("Who was/were the author(s) of the dashboard or report?")
    ReportReviewer    = IntegerField("Who was the final reviewer of the dashboard or report?")     
    submitTOC=SubmitField('Submit')

class Challenges(Form):
    Category = TextField('List relevant tags.',validators=[validators.Required(),validators.Length(min=2, max=400)])
    Rank = IntegerField('Rank among other challenges')
    Priority= RadioField('Priority', choices=[('1','1. Critical'),('2','2. High Priority'),('3','3. Medium'),('4','4. Priority'),('5','5. Low Priority')],coerce=unicode,validators=[validators.Required()])
    Title = TextField('This will be the name we use to communicate about the challenge.',validators=[validators.Required(),validators.Length(min=2, max=300)])
    Description = TextAreaField('Describe the challenge.',validators=[validators.Required(),validators.Length(min=2, max=800)])
    GraphLink = TextField('location of picture.')
    LinkEmanio =  URLField(default='http://EmanioLink.com')
    Status = SelectField(u"How is the challenge being addressed?",coerce=unicode, choices=[("Problem Identified",'Problem Identified'),("Pre-Exploration",'Pre-Exploration'), ('Challenge Assgined', 'Challenge Assgined')]) 
    ProjectLead = TextField('Who is assigned to work on this challenge?')
    ProjectMangement = TextField('link to project mgmt web.')
    InterventionSuggestion = TextAreaField('Suggested intervention.')
    Intervention = TextAreaField('Planned intervention.')
    upload = FileField('Image evidence of the challenge.', )
    submitChallenge=SubmitField('Submit')
    submitSave=SubmitField('Save Add More')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput() 


class Which(Form):
    formtype = RadioField('how ready are you', choices=[('Long','<h3>Standard data request form (Designed to guide you through your request)</h3><br>'),
        ('Short',"<h3>Data Partner's Advanced form (<strong>be prepared to list all of the columns in the data request</strong>)</h3><br>")],coerce=unicode)
    submit=SubmitField('Submit')

class LoginForm(Form):
    username = StringField('ACBHCS login ', validators=[validators.DataRequired()])
    password = PasswordField('Password', [validators.Required()])
    remember_me = BooleanField('remember_me', default=False)
    submit=SubmitField('Submit')

class AddUser(Form):
    username = StringField('ACBHCS login ')
    password = PasswordField('Password')
    search = StringField('search for a name')
    name = StringField('search for a name')
    admin = BooleanField('Yes, I have looked at Context.', default=False)
    form_access = StringField('search for a name')
    submit=SubmitField('Submit')


# [validators.Required(),validators.Length(min=2, max=50)]
class RequestData(Form):
    # test= QuerySelectField(query_factory=Requests.with_entities(Requests.id)) 
    jobTitle= TextField('This will be the name we use to communicate about the request.',validators=[validators.Required(),validators.Length(min=2, max=50)])#,
    supervisor= SelectField(u"Who is your supervisor?",coerce=unicode, choices=[("test1",'test1'), ('2', 'test2')]) 
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
    agency= SelectMultipleField('For what Agencies do you want this data?',coerce=unicode, choices=agenList)
    Rejxagency=   TextAreaField('Explantion',default='')
    RejBoolagency=  BooleanField('Incomplete.', default=False)
    ru = TextField("Leave blank if you want all RU's for Agency specified above",  ) 
    deadlinetime = SelectField(u'What Hour?',coerce=int, choices=[(8,'8 am'), (9, '9 am'), (10, '10 am'),
        (11, '11 am'), (12, 'Noon'), (13, '1 pm'), (14, '2 pm'), (15, '3 pm'), (16, '4 pm'), (17, '5 pm')])
    deadlinedate= DateField( '',  format='%m/%d/%Y',)
    deadlineWhy = TextField('Why?')
    priority= RadioField('Priority', choices=[('1','1. Just Curious'),('2','2. Low Priority'),('3','3. Medium'),('4','4. Top Priority'),('5','5. Extremely Urgent')],coerce=unicode,validators=[validators.Required()])
    requestedBy= TextField('Requested By?')
    # SelectField(u"If this isn't your request, who is it for?",coerce=unicode, choices=[("test1",'test1'), ('2', 'test2')]) 
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
    # assigned = QuerySelectField(u'Staff', query_factory=getRequestor, get_label='staff')
    staffback = QuerySelectField(u'Staff', query_factory=getStaff, get_label='staff',default="Unassigned")
    # staff_id = QuerySelectField(u'Staff', query_factory=getRequestor, get_label='staff')
    # assigned= SelectField('Staff Assigned?',choices=[('Chet','Chet'),('Gabriel','Gabriel'),
     # ('John','John'), ('Dr. Hall', 'Dr. Hall'),('Assigned', 'Assigned'), ('Complete', 'Complete'), ('Rejected', 'Rejected'),("Unassigned","Unassigned")],default = "Unassigned") 
    # completeDate= DateTimeField( 'Date Completed',  format='%m/%d/%Y')
    reviewed= BooleanField('Have you revised the request and want to send it back to DS?') 
    Response=  TextAreaField('Explantion')
    ourdeadline= DateField( '',  format='%m/%d/%Y',)
    cc_sup=BooleanField('Send request to supervisor?', default=False)
    statusback = QuerySelectField(u'Status', query_factory=getStatus, get_label='status',default="Pending Review")
    # status= SelectField(u'Status?',coerce=unicode, choices=[('No Filter','No Filter'),('User Responded','User Responded'),('Needs Action','Needs Action'),('Lower Priority Request','Lower Priority Request'),\
    #  ('Incomplete Request','Incomplete Request'), ('Pending Review', 'Pending Review'),
    #     ('Assigned', 'Assigned'), ('Complete', 'Complete'), ('Rejected-Hold', 'Rejected-Hold'),("Rejected-Send Back to user","Rejected-Send Back to user")],default='No Filter')
    RejxkeyQuestions= TextAreaField('Explantion')
    RejxspecialFacts=  TextAreaField('Explantion')
    RejxrequestDate=  TextAreaField('Explantion')
    RejxrequestedBy=  TextAreaField('Explantion')
    Rejxsupervisor=  TextAreaField('Explantion')
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
    RejxMHorSUD=   TextAreaField('Explantion',default='')
    RejBoolMHorSUD= BooleanField('Incomplete.', default=0)
    RejBoolkeyQuestions= BooleanField('Incomplete.', default=0)
    RejBoolspecialFacts= BooleanField('Incomplete.', default=0)
    RejBoolrequestDate= BooleanField('Incomplete.', default=0)
    RejBoolrequestedBy= BooleanField('Incomplete.', default=0)
    RejBoolsupervisor= BooleanField('Incomplete.', default=0)
    RejBooldeadlinedate= BooleanField('Incomplete.', default=0)
    RejBoolpriority=  BooleanField('Incomplete.', default=0)
    RejBooldeliveryFormat=BooleanField('Incomplete.', default=0)
    RejBooltimeframe= BooleanField('Incomplete.', default=0)
    RejBooltimeBreakdown=BooleanField('Incomplete.', default=0)
    RejBoolspecialPop=  BooleanField('Incomplete.', default=0)
    RejBoolru =  BooleanField('Incomplete.', default=0)
    RejBooltypeOfService=  BooleanField('Incomplete.', default=0)
    RejBooljobTitle=  BooleanField('Incomplete.', default=0)
    RejBoollongDescription= BooleanField('Incomplete.', default=0)
    RejBoolspecialInstructions=BooleanField('Incomplete.', default=0)
    RejBoolaudience= BooleanField('Incomplete.', default=0)
    RejBoolcolumnsRequired=  BooleanField('Incomplete.', default=0)
    RejBooldeadlinetime = BooleanField('Incomplete.', default=0)
    RejBooldeadlineWhy =  BooleanField('Incomplete.', default=0)
    RejBooltimeframestart = BooleanField('Incomplete.', default=0)
    RejBooltimeframeend=  BooleanField('Incomplete.', default=0)
    UserAction= SelectField('Are you finished editing?',choices=[('No, I want save and keep working','No, I want save and keep working'),
        ('Save, and send back for review','Save, and send back for review')],default = "No, I want save and keep working") 
    submitRequest=SubmitField('Submit')

class UserRequestData(Form):
    # test= QuerySelectField(query_factory=Requests.with_entities(Requests.id)) 
    jobTitle= TextField('This will be the name we use to communicate about the request.',validators=[validators.Required(),validators.Length(min=2, max=50)])#,
    supervisor= SelectField(u"Who is your supervisor?",coerce=unicode, choices=[("test1",'test1'), ('2', 'test2')]) 
    emanio = BooleanField('Yes, I have looked at Context.', default=False)
    requestDate = DateField( 'request date',  format='%m/%d/%Y',)
    MHorSUD= RadioField('Is this MHS or SUD Services related?', choices=[('MHS','MHS'),('SUD','SUD Services')],coerce=unicode)
    longDescription= TextAreaField('Describe what you want to investigate.',validators=[validators.Required(),validators.Length(min=2, max=120)])
    keyQuestions= TextAreaField('What are the questions you want answered?',validators=[validators.Required(),validators.Length(min=2, max=120)])
    problem= TextAreaField('If the data shows a problem, describe your intervention or what data you might you need for that intervention')
    audience= TextAreaField('With whom or in what forum do you plan to share this data?',)
    columnsRequired= TextAreaField('These are all the columns you will get in your report (chose <a href="//127.0.0.1:8080/long"> general form  </a>if you are unsure)<br> Be sure to include Agency/RUs needed, time frame, special population, etc.,' )
    agency= SelectMultipleField('For what Agencies do you want this data?',coerce=unicode, choices=agenList)
    ru = TextField("Leave blank if you want all RU's for Agency specified above",  ) 
    deadlinetime = SelectField(u'What Hour?',coerce=int, choices=[(8,'8 am'), (9, '9 am'), (10, '10 am'),
        (11, '11 am'), (12, 'Noon'), (13, '1 pm'), (14, '2 pm'), (15, '3 pm'), (16, '4 pm'), (17, '5 pm')])
    deadlinedate= DateField( '',  format='%m/%d/%Y',)
    deadlineWhy = TextField('Why?')
    priority= RadioField('Priority', choices=[('1','1. Just Curious'),('2','2. Low Priority'),('3','3. Medium'),('4','4. Top Priority'),('5','5. Extremely Urgent')],coerce=unicode,validators=[validators.Required()])
    # requestedBy= SelectField(u"If this isn't your request, who is it for?",coerce=unicode, choices=[("test1",'test1'), ('2', 'test2')]) 
    timeframe= TextField('From what time frame do you want data? E.g., Most recent fiscal year? Most recent calendar year? Some other period?',  ) 
    timeframestart= DateField( '',  format='%m/%d/%Y',)
    timeframeend= DateField( '',  format='%m/%d/%Y',)
    timeBreakdown = TextField("If annual, specify Fiscal Year or Calendar.",  ) 
    specialPop= TextField('Are you interested in any demographics (age, ethnicity) or special populations (foster kids or disabled adults, and so on)?',  ) 
    typeOfService= TextField('Are there specific types of services you want? e.g. Crisis, Hospital, etc.', ) 
    specialInstructions= TextField('Any special instructions?',  ) 
    specialFacts= TextAreaField('Are there any facts or circumstances we should know to fulfill this request?') 
    UserAction= SelectField('Are you finished editing?',choices=[('Save and Hold','Save and Hold'),
        ('Save and Submit','Save and Submit')],default = "Save and Hold") 
    submitRequest=SubmitField('Submit')

# count distinct "name" values
# session.query(func.count(distinct(User.name)))
# http://stackoverflow.com/questions/21579373/sqlalchemy-wtforms-set-default-selected-value-for-queryselectfield
class filterRequests(Form):
    # status= SelectField(u'Status?',coerce=unicode, choices=[('No Filter','No Filter'),('User Responded','User Responded'),('Needs Action','Needs Action'),('Lower Priority Request','Lower Priority Request'),\
    #  ('Incomplete Request','Incomplete Request'), ('Pending Review', 'Pending Review'),
    #     ('Assigned', 'Assigned'), ('Complete', 'Complete'), ('Rejected-Hold', 'Rejected-Hold'),("Rejected-Send Back to user","Rejected-Send Back to user")],default='No Filter')
    status= SelectField(u'Status',default='No Filter')
    requestedBy= SelectField(u'Requestor',default='No Filter')
    assigned= SelectField(u'Assigned',default='No Filter')
    # requestor = QuerySelectField(u'Requestor', query_factory=getRequestor, get_label='requestedBy')
    # staff = QuerySelectField(u'Staff', query_factory=getRequestor, get_label='staff')
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

class DeleteRow_form(Form):
    row_id = IntegerField('')
    submitd = SubmitField('Delete')
