from app import db
from sqlalchemy.orm import relationship, backref

db.Model.metadata.reflect(db.engine)


# class test1(db.Model):
#     __bind_key__ = 'test'
#     __tablename__ =  'test1'
#     id = db.Column(db.Integer, primary_key=True)
#     test = db.Column(db.String(80), unique=True)

class staging_providers(db.Model):
    __table__ =  db.Model.metadata.tables['staging_providers']
    # id = db.Column(db.Integer, primary_key=True)
    # test = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return '<Provider %r>' % (self.provider_name)

class procedures(db.Model):
    __table__ =  db.Model.metadata.tables['procedures']
    # id = db.Column(db.Integer, primary_key=True)
    # test = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return '<procedures %r>' % (self.provider_name)

class dashboards(db.Model):
    __table__ =  db.Model.metadata.tables['dashboards']
    questions = db.relationship('dashboards_questions', lazy='dynamic', backref='questionback',cascade="all, delete-orphan")
    systems = db.relationship('dashboards_systems', lazy='dynamic', backref='systemback',cascade="all, delete-orphan")
    reviews = db.relationship('dashboards_reviews', lazy='dynamic', backref='reviewback',cascade="all, delete-orphan")
    # id = db.Column(db.Integer, primary_key=True)
    # test = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return '%r' % (self.title)

class dashboards_questions(db.Model):
    __table__ =  db.Model.metadata.tables['dashboards_questions']
    def __repr__(self):
        return ' %r' % (self.question)

class dashboards_systems(db.Model):
    __table__ =  db.Model.metadata.tables['dashboards_systems']
    def __repr__(self):
        return '%r' % (self.system_of_care)

class dashboards_reviews(db.Model):
    __table__ =  db.Model.metadata.tables['dashboards_reviews']
    def __repr__(self):
        return '%' % (self.category)

class providers(db.Model):
    __table__ =  db.Model.metadata.tables['providers']
    # id = db.Column(db.Integer, primary_key=True)
    # test = db.Column(db.String(80), unique=True)
    def __repr__(self):
        return '<Provider %r>' % (self.provider_name)

# class test(db.Model):
#     __bind_key__ = 'test'
#     # __tablename__ = 'test'
#     id = db.Column(db.Integer, primary_key=True)
#     test = db.Column(db.String(80), unique=True)

# class rutable(db.Model):
#     __tablename__ = 'rutable'
#     __bind_key__ = 'ubuntuweb'
#     id = db.Column(db.Integer, primary_key=True)
#     oldRU =db.Column(db.Integer)
#     ru    =db.Column(db.String(6), db.ForeignKey('rustage.ru'),unique=True)      
#     agency    =db.Column(db.String(40), index=True)    
#     county    =db.Column(db.Integer)    
#     kidsru    =db.Column(db.Integer)    
#     school    =db.Column(db.Integer)    
#     Level3Classic    =db.Column(db.Integer)    
#     cds_Code    =db.Column(db.String(14), index=True)    
#     ab3632RU    =db.Column(db.Integer)    
#     DayTx    =db.Column(db.Integer)    
#     CESDC    =db.Column(db.Integer)    
#     EPSDTGroup    =db.Column(db.String(15), index=True)    
#     psmask2    =db.Column(db.Integer)    
#     svcType    =db.Column(db.String(25), index=True)    
#     RU2    =db.Column(db.String(6), index=True)    
#     TAYru    =db.Column(db.Integer)    
#     Level2    =db.Column(db.Integer)    
#     DBserviceModality    =db.Column(db.String(25), index=True)    
#     svcType3    =db.Column(db.String(25), index=True)    
#     OutCty    =db.Column(db.Integer)    
#     OurKids    =db.Column(db.Integer)    
#     SafePassages    =db.Column(db.Integer)    
#     MHSA    =db.Column(db.Integer)    
#     OAru    =db.Column(db.Integer)    
#     program    =db.Column(db.Integer)    
#     Residential    =db.Column(db.Integer)    
#     TBS    =db.Column(db.Integer)    
#     CalWorks    =db.Column(db.Integer)    
#     RUCITY    =db.Column(db.String(30), index=True)    
#     UMBRELLA    =db.Column(db.Integer)    
#     svcmode    =db.Column(db.String(2), index=True)    
#     provname    =db.Column(db.String(30), index=True)    
#     start_dt    =db.Column(db.Integer)    
#     end_dt    =db.Column(db.Integer)
#     start    = db.Column(db.Date)     
#     end    = db.Column(db.Date)     
#     frc    =db.Column(db.Integer)   
#     reviewEdit  = db.Column(db.Boolean())  

# class test(db.Model):
#     __tablename__ = db.Model.metadata.tables['test']
#     __bind_key__ = 'ubuntuweb'

# class staging_providers(db.Model):
#     __bind_key__ = 'ubuntuweb'
#     __table__ =db.Model.metadata.tables['staging_providers']

# class providers(db.Model):
#     __bind_key__ = 'ubuntuweb'
#     __table__ =db.Model.metadata.tables['providers']

# class Projects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     projectleader = db.Column(db.String(35))    

#     def __repr__(self):
#         return '<Project %r>' % (self.name)


# class staging_providers(db.Model):
#     __tablename__ = 'staging_providers'
#     __bind_key__ = 'test'
#     old_ru =db.Column(db.String(40))
#     in_school =db.Column(db.Boolean())
#     cesdc =db.Column(db.Boolean())
#     psmask2  =db.Column(db.Integer)
#     kidsru =db.Column(db.Boolean())
#     ab3632 =db.Column(db.Boolean())
#     dbservicemodality =db.Column(db.String(40))
#     agency =db.Column(db.String(40))
#     county_run =db.Column(db.Boolean())
#     level_3_classic =db.Column(db.Boolean())
#     school_cds_id =db.Column(db.String(40))
#     day_treatment =db.Column(db.Boolean())
#     epsdtgroup =db.Column(db.String(40))
#     predesessor =db.Column(db.String(40))
#     svctype =db.Column(db.String(40))
#     tay =db.Column(db.Boolean())
#     level_2 =db.Column(db.Boolean())
#     svctype3 =db.Column(db.String(40))
#     out_of_county =db.Column(db.Boolean())
#     our_kids =db.Column(db.Boolean())
#     safe_passages =db.Column(db.Boolean())
#     mhsa =db.Column(db.Boolean())
#     older_adult =db.Column(db.Boolean())
#     program =db.Column(db.Boolean())
#     residential =db.Column(db.Boolean())
#     tbs =db.Column(db.Boolean())
#     calworks =db.Column(db.Boolean())
#     psmask=text =db.Column(db.String(40))
#     access =db.Column(db.Boolean())
#     adult =db.Column(db.Boolean())
#     child =db.Column(db.Boolean())
#     childrens_specialized_services =db.Column(db.Boolean())
#     clc =db.Column(db.Boolean())
#     community_support_services =db.Column(db.Boolean())
#     crisis_services =db.Column(db.Boolean())
#     crisis_stabilization =db.Column(db.Boolean())
#     ctf =db.Column(db.Boolean())
#     day_treament_day_unit=db.Column(db.Integer)
#     day_treatment_hour_unit=db.Column(db.Integer)
#     destiny =db.Column(db.Boolean())
#     dual_dx =db.Column(db.Boolean())
#     exception_ru =db.Column(db.Boolean())
#     forensic =db.Column(db.Boolean())
#     foster =db.Column(db.Boolean())
#     hospital =db.Column(db.Boolean())
#     hospital_local =db.Column(db.Boolean())
#     indigent_script =db.Column(db.Boolean())
#     intensive =db.Column(db.Boolean())
#     involuntary_holds =db.Column(db.Boolean())
#     jail_or_juvie =db.Column(db.Boolean())
#     level_3_doc =db.Column(db.Boolean())
#     level_3_org =db.Column(db.Boolean())
#     medication_clinic =db.Column(db.Boolean())
#     mhsa_full_service_partnership =db.Column(db.Boolean())
#     neurobehavioral =db.Column(db.Boolean())
#     outpatient_services =db.Column(db.Boolean())
#     pei =db.Column(db.Boolean())
#     phf =db.Column(db.Boolean())
#     residential_treatment =db.Column(db.Boolean())
#     school =db.Column(db.Boolean())
#     school_based_outpatient_services =db.Column(db.Boolean())
#     service_team =db.Column(db.Boolean())
#     subacute =db.Column(db.Boolean())
#     support_services =db.Column(db.Boolean())
#     wellness_center =db.Column(db.Boolean())
#     contract_model =db.Column(db.String(40))
#     blended_funding =db.Column(db.String(40))
#     budget_category =db.Column(db.String(40))
#     budget_grouping =db.Column(db.String(40))
#     level =db.Column(db.String(40))
#     modality =db.Column(db.String(40))
#     referral_code =db.Column(db.String(40))
#     provider_name =db.Column(db.String(40))
#     short_provider_name =db.Column(db.String(40))
#     provider_type =db.Column(db.String(40))
#     medicare_license_number =db.Column(db.String(40))
#     dx_group =db.Column(db.String(40))
#     provider_attribute_mask=db.Column(db.Integer)
#     default_procedure_code=db.Column(db.Integer)
#     mode_of_service =db.Column(db.String(40))
#     medical_mode_of_service =db.Column(db.String(40))
#     cds_provider_code =db.Column(db.String(40))
#     provider_data_entry_form=db.Column(db.Integer)
#     financial_responsibility=db.Column(db.Integer)
#     program_physician  =db.Column(db.Integer)
#     umbrella_organization=db.Column(db.Integer)
#     sub_bureau =db.Column(db.String(40))
#     region =db.Column(db.String(40))
#     street_address =db.Column(db.String(40))
#     city =db.Column(db.String(40))
#     state =db.Column(db.String(40))
#     zip_code =db.Column(db.String(40))
#     zip_plus_four =db.Column(db.String(40))
#     phone_number =db.Column(db.String(40))
#     start_date=db.Column(db.Date)
#     end_date=db.Column(db.Date)
#     day_of_operation_string =db.Column(db.String(40))
#     provider_master_stamp = db.Column(db.DateTime, index=True)
#     last_change_stamp = db.Column(db.DateTime, index=True)
#     blue_cross_license_number =db.Column(db.String(40))
#     subset_mask=db.Column(db.Integer)
#     provider_subset_mask  =db.Column(db.Integer)
#     provider_attribute_mask2  =db.Column(db.Integer)
#     provider_capacity=db.Column(db.Integer)
#     hospital_license_number =db.Column(db.String(40))
#     referral_source_ub82_box18 =db.Column(db.String(40))
#     referral_dest_ub82_box21 =db.Column(db.String(40))
#     gl_account_code =db.Column(db.String(40))
#     cds_provider_name =db.Column(db.String(40))
#     oshpd_disposition_of_patient =db.Column(db.String(40))
#     oshpd_admission_source=db.Column(db.Integer)
#     medicaid_license =db.Column(db.String(40))
#     medicaid_type  =db.Column(db.Integer)
#     ur_type  =db.Column(db.Integer)
#     reporting_unit =db.Column(db.String(40))
#     medicaid_eligibility_pin =db.Column(db.String(40))
#     caladds_provider_code =db.Column(db.String(40))
#     caladds_service_type=db.Column(db.Integer)
#     collect_caladds =db.Column(db.String(40))
#     default_detox_procedure=db.Column(db.Integer)
#     default_dosing_procedure=db.Column(db.Integer)
#     default_pharm_urine_procedure=db.Column(db.Integer)
#     dose_type_mask  =db.Column(db.Integer)
#     label_location =db.Column(db.String(40))
#     medical_program_code =db.Column(db.String(40))
#     recommended_maximum_stay=db.Column(db.Integer)
#     csc_license_number =db.Column(db.String(40))
#     provider_class =db.Column(db.String(40))
#     medicaid_eligibility_provider =db.Column(db.String(40))
#     legal_entity =db.Column(db.String(40))
#     taxonomy_code =db.Column(db.String(40))
#     facility_npi =db.Column(db.String(40))
#     financial_responsibility_county =db.Column(db.Boolean())
#     financial_responsibility_medicaid =db.Column(db.Boolean())
#     financial_responsibility_medicare =db.Column(db.Boolean())
#     financial_responsibility_insurance =db.Column(db.Boolean())
#     financial_responsibility_patient =db.Column(db.Boolean())



# class what(db.Model):
#     __table__ = db.Model.metadata.tables['test']
#     __bind_key__ = 'warehouse'
#     id = db.Column(db.Integer, primary_key=True) 
#     test=db.Column(db.String(40))


# class rustage(db.Model):
#     __tablename__ = 'rustage'
#     __bind_key__ = 'ubuntuweb'
#     id = db.Column(db.Integer, primary_key=True)
#     ru    =db.Column(db.String(6), index=True, unique=True)
#     oldRU =db.Column(db.Integer)  
#     agency    =db.Column(db.String(40), index=True)    
#     county    =db.Column(db.Integer)    
#     kidsru    =db.Column(db.Integer)    
#     school    =db.Column(db.Integer)    
#     Level3Classic    =db.Column(db.Integer)    
#     cds_Code    =db.Column(db.String(14), index=True)    
#     ab3632RU    =db.Column(db.Integer)    
#     DayTx    =db.Column(db.Integer)    
#     CESDC    =db.Column(db.Integer)    
#     EPSDTGroup    =db.Column(db.String(15), index=True)    
#     psmask2    =db.Column(db.Integer)    
#     svcType    =db.Column(db.String(25), index=True)    
#     RU2    =db.Column(db.String(6), index=True)    
#     TAYru    =db.Column(db.Integer)    
#     Level2    =db.Column(db.Integer)    
#     DBserviceModality    =db.Column(db.String(25), index=True)    
#     svcType3    =db.Column(db.String(25), index=True)    
#     OutCty    =db.Column(db.Integer)    
#     OurKids    =db.Column(db.Integer)    
#     SafePassages    =db.Column(db.Integer)    
#     MHSA    =db.Column(db.Integer)    
#     OAru    =db.Column(db.Integer)    
#     program    =db.Column(db.Integer)    
#     Residential    =db.Column(db.Integer)    
#     TBS    =db.Column(db.Integer)    
#     CalWorks    =db.Column(db.Integer)    
#     RUCITY    =db.Column(db.String(30), index=True)    
#     UMBRELLA    =db.Column(db.Integer)    
#     svcmode    =db.Column(db.String(2), index=True)    
#     provname    =db.Column(db.String(30), index=True)    
#     start_dt    =db.Column(db.Integer)    
#     end_dt    =db.Column(db.Integer)
#     start    = db.Column(db.Date)     
#     end    = db.Column(db.Date)     
#     frc    =db.Column(db.Integer)   
#     reviewEdit  = db.Column(db.Boolean())   
#     rutablelink = db.relationship('rutable', lazy='dynamic', backref='ruback')


class User(db.Model):
    __tablename__ = 'user'
    __bind_key__ = 'ubuntuweb'
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    # __tablename__ = 'user'
    name=db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    authenticated = db.Column(db.Boolean, default=True)
    admin =  db.Column(db.Boolean, default=False)
    form_access=db.Column(db.String)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Request(db.Model):
    __tablename__ = 'request'
    __bind_key__ = 'ubuntuweb'
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
    RejBoolsupervisor =  db.Column(db.Boolean())      
    Rejxsupervisor =  db.Column(db.String(120), index=True)
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
    __bind_key__ = 'ubuntuweb'
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    staff = db.Column(db.String(60))
    privelage = db.Column(db.String(30))
    request = db.relationship('Request', lazy='dynamic', backref='staffback',cascade="all, delete-orphan")
    def __repr__(self):
        return (self.staff)

class Status(db.Model):
    __bind_key__ = 'ubuntuweb'
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    request = db.relationship('Request', lazy='dynamic', backref='statusback',cascade="all, delete-orphan")
    def __repr__(self):
        return (self.status)

# from sqlalchemy import distinct

def getStaff():
    u = Staff.query
    return u

def getStatus():
    u = Status.query
    return u

def getAgency():
    u = staging_providers.query
    return u



from sqlalchemy.orm import relationship


class Challenge(db.Model):
    __tablename__ = 'challenge'
    __bind_key__ = 'ubuntuweb'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    initTime = db.Column(db.Date)
    Timeline = db.Column(db.String(800), index=True)
    Category = db.Column(db.String(400), index=True)
    Priority = db.Column(db.String(64), index=True)
    Rank = db.Column(db.Integer)
    Title = db.Column(db.String(300), index=True)
    Description = db.Column(db.String(800), index=True)
    GraphLink = db.Column(db.String(300), index=True)
    LinkEmanio = db.Column(db.String(400), index=True)
    Status = db.Column(db.String(64), index=True)
    StatusChangeSTamp = db.Column(db.Date)
    ProjectLead = db.Column(db.String(120), index=True)
    ProjectMangement = db.Column(db.String(120), index=True)
    InterventionSuggestion = db.Column(db.String(800), index=True)
    Intervention = db.Column(db.String(800), index=True)  
    Tags = db.relationship('Tags', lazy='dynamic', backref='tagback',cascade="all, delete-orphan")


class Tags(db.Model):
    __bind_key__ = 'ubuntuweb'
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(200))
    tag_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    order = db.Column(db.Integer)                                     
    def __repr__(self):
        return (self.tag)

