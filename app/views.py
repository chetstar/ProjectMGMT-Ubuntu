from app import app,models, db
# from forms import goal_form, strategy_form, project_form, task_form,DeleteRow_form,ldapA,LoginForm, Request, Which,Staff
from forms import LoginForm, TOCsystems,RequestData, Which,ldapA, filterRequests, UserRequestData, Challenges,DeleteRow_form, TOC,proced, rutable,rutablefilter,cans,AddUser,TOCquestions,TOCreview
import datetime
from sqlalchemy.orm.attributes import get_history
from werkzeug import secure_filename
import re, shutil, os, sys
from sqlalchemy.sql import  desc,func,distinct
from sqlalchemy import case
from sqlalchemy import and_
# from app.models import Tasks, Projects, Goals, Strategies
from flask.ext.admin import expose

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
from threading import Thread
from flask.ext.login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import ldap
from flask import render_template, flash, redirect,Flask,Response,request,url_for, g,session,jsonify
from flask.ext.admin.contrib import sqla
from flask.ext import admin, login
from sqlalchemy.orm.attributes import get_history
        # if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[False]:
        #     print 'changed from false to true'
        #     ptask.completeDate=datetime.datetime.utcnow()
        # if get_history(ptask, 'complete')[0]==[False] and get_history(ptask, 'complete')[2]==[True]:
        #     print 'changed from true to false'
        #     ptask.completeDate=None
        # else:
        #     if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[None]:
        #         ptask.complete=True
        #         ptask.completeDate=None

login_manager = LoginManager()
login_manager.init_app(app) 

#run this after migrate to fill up tags
# for x in [re.split(',',item.Category) for item in [i for i in models.Challenge.query.all()]]:
#   for item in x:
#   for j in x:
#     q=models.Tags(tag=j,tag_id=item.id)
#     db.session.add(q)
#     db.session.commit()

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return g.user.is_authenticated()

# photos = UploadSet('photos', IMAGES)
class MyAdminIndexView(admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not g.user.is_authenticated():
            flash('Please log in first...', 'error')
            next_url = request.url
            login_url = '%s?next=%s' % (url_for('login'), next_url)
            return redirect(login_url)
        # import pdb;pdb.set_trace()
        if g.user.admin == True:
            return super(MyAdminIndexView,self).index()
        else:
            return redirect(url_for("main"))

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is not None:
            return f(*args, **kwargs)
        else:
            flash('Please log in first...', 'error')
            next_url = request.url
            login_url = '%s?next=%s' % (url_for('login'), next_url)
            return redirect(login_url)
    return decorated_function


@login_manager.unauthorized_handler
def unauthorized():
    print 'unauthorized'
    flash("You must be logged in.")
    return redirect(url_for("login"))

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    g.user=current_user
    return models.User.query.get(user_id)

@app.route("/logout")
# @logged_in
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash("Logged Out.")
    return redirect(url_for("login"))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if app.config['ENVIRONMENT']=='dev':
            try:
                print "Authentification Successful" 
                # import pdb;pdb.set_trace()
                namedb=models.User.query.filter_by(name=unicode(form.username.data)).first()
                email=models.User.query.filter_by(name=unicode(form.username.data)).first().email         
                login_user(user_loader(unicode(email)),remember=form.remember_me.data)
                flash("Logged in successfully.")
                g.email=email
                session['logged_in'] = True
                return redirect( request.values.get('next') or url_for("main"))
            except Exception as e:
                flash("Invalid Credentials.")
                return render_template("login.html", form=form)
        else:
            try:
                # if '@' in form.username.data:
                #     form.username.data=re.sub(' /d+','', (re.sub("\d+",'', form.username.data.split('@')[0]))[1:]+(re.sub("\d+",'', form.username.data.split('@')[0]))[0:1])
                l = ldap.initialize("ldap://10.129.18.101")
                l.simple_bind_s("program\%s" % form.username.data,form.password.data)
                print "Authentification Successful"
                r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=%s)' % form.username.data,['mail','objectGUID','displayName'])
                email=r[0][1]['mail'][0]   
                GUID=r[0][1]['objectGUID'][0]   
                FullName=r[0][1]['displayName'][0] 
                import uuid
                guid = uuid.UUID(bytes=GUID)
                if not models.User.query.filter_by(email=unicode(email)).first(): 
                  p=models.User(name=FullName,email=email)
                  db.session.add(p)
                  db.session.commit()            
                login_user(user_loader(unicode(email)),remember=form.remember_me.data)
                flash("Logged in successfully.")
                g.email=email
                session['logged_in'] = True
                return redirect( request.values.get('next') or url_for("main"))
            except Exception as e:
                flash("Invalid Credentials.")
                return render_template("login.html", form=form)
    return render_template("login.html", form=form)

                # l = ldap.initialize("ldap://10.129.18.101")
                # l.simple_bind_s("program\%s" % form.username.data,form.password.data)
                # print "Authentification Successful"
                # r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % form.username.data,['mail','objectGUID','displayName'])
                # email=r[0][1]['mail'][0]   
                # GUID=r[0][1]['objectGUID'][0]   
                # FullName=r[0][1]['displayName'][0] 
                # import uuid
                # guid = uuid.UUID(bytes=GUID)
                # if not models.User.query.filter_by(email=unicode(email)).first(): 
                #   p=models.User(name=FullName,email=email)
                #   db.session.add(p)
                #   db.session.commit() 




from werkzeug import secure_filename
from flask_wtf.file import FileField
from functools import wraps



ALLOWED_EXTENSIONS = set(['TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@app.route('/editphoto/<id>', methods=['GET', 'POST'])
def edit_photo(id): 
    form = Challenges()
    challenge=models.Challenge.query.filter_by(id=id).first()
    if request.method == 'POST':
        print 'submit'
        # p=models.Request(email=g.user.email,username=g.user.name,
        #  requestDate=datetime.datetime.utcnow(),assigned="Unassigned",status="Pending Review")
        # form.agency.data=', '.join(form.agency.data)
        # form.populate_obj(p)
        file = request.files['upload']
        if file and allowed_file(file.filename):
            dateSec=str(datetime.datetime.now())
            filename = dateSec+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
        challenge.GraphLink=filename
        db.session.commit()
        return redirect(url_for('edit_challenge',id=id, edit=1,form=form))
    return render_template('edit_photo.html',id=id,form=form)

@app.route('/editchallenge/<id>/<edit>', methods=['GET', 'POST'])
def edit_challenge(id,edit): 
    challenge=models.Challenge.query.filter_by(id=id).first()
    form = Challenges(obj=challenge)
    if edit == '0' and request.method != 'POST' :
        form.Title.data="Copy "+form.Title.data
    if request.method == 'POST' and form.validate_on_submit():
        if edit == '1':#editing exisitng
            challenge.LinkEmanio=form.LinkEmanio.data
            challenge.Category= form.Category.data
            challenge.Priority=form.Priority.data
            challenge.Title=form.Title.data
            challenge.Description=form.Description.data
            Status=form.Status.data
            challenge.ProjectLead=form.ProjectLead.data
            challenge.InterventionSuggestion=form.InterventionSuggestion.data     
        else:#copy
            p=models.Challenge(email=g.user.email,username=g.user.name,LinkEmanio=form.LinkEmanio.data,GraphLink=challenge.GraphLink,
            Category= form.Category.data,Priority=form.Priority.data,Title=form.Title.data,Description=form.Description.data,
            Status=form.Status.data,ProjectLead=form.ProjectLead.data,InterventionSuggestion=form.InterventionSuggestion.data,
            initTime = datetime.datetime.utcnow(),StatusChangeSTamp=datetime.datetime.utcnow(),
            Timeline=str(datetime.datetime.utcnow())+", "+str(form.Status.data)+", ")
            db.session.add(p)       
        db.session.commit()
        return redirect(url_for('allchallenges'))
    return render_template('edit_challenge.html',id=id,form=form,LinkEmanio=challenge.LinkEmanio)


@app.route("/challengesform",methods=["GET","POST"])
@logged_in
def challengesform():
    form = Challenges()
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    if form.validate_on_submit():
        print 'submit'
        # p=models.Request(email=g.user.email,username=g.user.name,
        #  requestDate=datetime.datetime.utcnow(),assigned="Unassigned",status="Pending Review")
        # form.agency.data=', '.join(form.agency.data)
        # form.populate_obj(p)
        file = request.files['upload']
        if file and allowed_file(file.filename):
            dateSec=str(datetime.datetime.now())
            filename = dateSec+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # filename = secure_filename(form.upload.data.filename)
            # form.upload.data.save('app/static/img/' + filename)
        else:
            filename='no file'
        if form.LinkEmanio.data=='http://EmanioLink.com':
            form.LinkEmanio.data=None
        p=models.Challenge(email=g.user.email,username=g.user.name,GraphLink=filename,LinkEmanio=form.LinkEmanio.data,
        Category= form.Category.data,Priority=form.Priority.data,Title=form.Title.data,Description=form.Description.data,
        Status=form.Status.data,ProjectLead=form.ProjectLead.data,InterventionSuggestion=form.InterventionSuggestion.data,
        initTime = datetime.datetime.utcnow(),StatusChangeSTamp=datetime.datetime.utcnow(),
        Timeline=str(datetime.datetime.utcnow())+", "+str(form.Status.data)+", ")
        db.session.add(p)
        db.session.commit()
        #send email to user and admin
        flash("Changes saved")
        if form.submitSave.data:        
            return redirect(url_for('challengesform'))
        else:
            return redirect(url_for('allchallenges'))
    else:
        flash_errors(form)
        return render_template("challengesform.html",email=g.user.email,name=g.user.name,form=form)

@app.route("/challengelist",methods=["GET","POST"])
@logged_in
def allchallenges():
    challengelist= models.Challenge.query.order_by(models.Challenge.Priority).all()
    delete_form=DeleteRow_form()
    # import pdb;pdb.set_trace()
    if delete_form.validate_on_submit():
        db.session.delete(models.Challenge.query.filter_by(id=delete_form.row_id.data).first())
        db.session.commit()
        return redirect(url_for('allchallenges'))
    # sorted(q_sum, key=lambda tup: tup[7])
    return render_template("challengeview.html",email=g.user.email,name=g.user.name,challengelist=challengelist,delete_form=delete_form,admin=g.user.admin)



##############################c

##############################c

##############################c


@app.route("/procedlist",methods=["GET","POST"])
def allproced():
    procedlist= models.procedures.query.all()
    # rulist= models.staging_providers.query.filter( models.staging_providers.level_3_classic != 1).all()
    # sorted(q_sum, key=lambda tup: tup[7])
    # import pdb;pdb.set_trace()
    if procedlist==[]:
        procedlist=['no results']
    return render_template("procedview.html",procedlist=procedlist)


@app.route('/editproced/<id>/<edit>', methods=['GET', 'POST'])
@logged_in
def edit_proced(id,edit): 
    p=models.procedures.query.filter_by(procedure_code=id).first()
    form = proced()
    form = proced(obj=p)
    form.populate_obj(p) 
    # if p.discounted==None:
    #     form.discounted=''
    if request.method == 'POST' :
        # and form.validate_on_submit()
        if edit == '1':#editing exisitng
            if form.service_category.data == '':
                ru.service_category=None
            if form.medi_cal_service_category.data == '':
                ru.medi_cal_service_category=None
            if form.billing_category.data == '':
                ru.billing_category=None
            db.session.commit()
        return redirect(url_for('allproced'))
    return render_template('edit_proced.html',form=form,id=id,p=p,)

##############################c

@app.route('/editru/<id>/<edit>', methods=['GET', 'POST'])
@logged_in
def edit_ru(id,edit): 
    ru=models.staging_providers.query.filter_by(id=id).first()
    # ru.modified_on=datetime.datetime.utcnow()
    # import pdb;pdb.set_trace()
    if g.user.form_access=='all':
        form = rutable()
        form = rutable(obj=ru)
        # if ru.cans==None:
        #     form.cans.data='None'
        AT= list(set([h.agency for h in models.staging_providers.query.all()]))
        AT.append('')
        form.agency.choices=zip(sorted(AT),sorted(AT))       
    elif g.user.form_access=='cans':
        form = cans()
        form = cans(obj=ru)
        # form.populate_obj(ru)
        # ru.modified_by=g.user
    else:
        form=cans(obj=ru)
    # import pdb;pdb.set_trace()
    # if edit == '0' and request.method != 'POST' :
    #     form.Title.data="Copy "+form.Title.data
    if request.method == 'POST' :
        # and form.validate_on_submit()
        if edit == '1':#editing exisitng
            form.populate_obj(ru) 
            # ru.reviewEdit=True
            # ru.modified_on=datetime.datetime.utcnow()
            # db.session.add(p) 
            # form.oldRU.data=ru.oldRU   
            # import pdb;pdb.set_trace()
            if g.user.form_access=='all':
                if form.agency.data == '':
                    ru.agency=None
                if form.dbservicemodality.data == '':
                    ru.dbservicemodality=None
                if form.psmasktext.data == '':
                    ru.psmasktext=None
                if form.agency.data == 'None':
                    ru.agency=None
                if form.dbservicemodality.data == 'None':
                    ru.dbservicemodality=None
                if form.psmasktext.data == 'None':
                    ru.psmasktext=None
                if form.predesessor.data == '':
                    ru.predesessor=None
                if form.school_cds_id.data == '':
                    ru.school_cds_id=None
                if form.ab3632.data == 'None':
                    ru.ab3632=None
                if form.residential.data == 'None':
                    ru.residential=None
                if form.ab3632 .data == 'None': 
                    ru.ab3632 =None
                if form.calworks.data == 'None':    
                    ru.calworks=None
                if form.cesdc.data == 'None':   
                    ru.cesdc=None
                if form.county_run .data == 'None': 
                    ru.county_run =None
                if form.day_treatment.data == 'None':   
                    ru.day_treatment=None
                if form.kidsru .data == 'None': 
                    ru.kidsru =None
                # if form.level_2 .data == 'None':    
                #     ru.level_2 =None
                if form.level_3_classic .data == 'None':    
                    ru.level_3_classic =None
                if form.mhsa .data == 'None':   
                    ru.mhsa =None
                if form.older_adult .data == 'None':    
                    ru.older_adult =None
                if form.out_of_county .data == 'None':  
                    ru.out_of_county =None
                if form.program    .data == 'None': 
                    ru.program    =None
                if form.in_school.data == 'None':   
                    ru.in_school=None
                if form.tay .data == 'None':    
                    ru.tay =None
                if form.tbs .data == 'None':    
                    ru.tbs =None
                if form.meds_fall_off.data == 'None':   
                    ru.meds_fall_off=None
                if form.cesdc_model.data == 'None': 
                    ru.cesdc_model=None
                # if form.level_3_type.data == 'None':    
                #     ru.level_3_type=None
                if form.child_welfare.data == 'None':   
                    ru.child_welfare=None
                if form.family_service_expected.data == 'None': 
                    ru.family_service_expected=None
                if form.intensive_needs_clients.data == 'None': 
                    ru.intensive_needs_clients=None
                if form.case_management.data == 'None': 
                    ru.case_management=None
                # if form.level_1.data == 'None': 
                #     ru.level_1=None
                if form.deliverable_exempt.data == 'None':  
                    ru.deliverable_exempt=None
                if form.srp.data == 'None': 
                    ru.srp=None
                if form.crisis.data == 'None':  
                    ru.crisis=None
                if form.high_level.data == 'None':  
                    ru.high_level=None
                if form.follow_up_care.data == 'None':  
                    ru.follow_up_care=None
            if form.cans.data == 'None':
                ru.cans=None
            ru.modified_by=g.user.name 
            db.session.commit()
            flash("Changes saved")
        return redirect(url_for('allrus'))
    return render_template('edit_ru.html',form=form,id=id,ru=ru,form_access=g.user.form_access)

@app.route("/rusform",methods=["GET","POST"])
@logged_in
def rusform():
    form = rutable()
    AT= list(set([h.agency for h in models.staging_providers.query.all()]))
    AT.append('')
    form.agency.choices=zip(sorted(AT),sorted(AT))
    # RB= list(set([re.split(',',h.Category for h in models.staging_providers.query.all()]))
    # RB.append('No Filter')
    # form.Category.data=RB
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    # import pdb;pdb.set_trace()
    if form.validate_on_submit():
        print 'submit'
        # p=models.ru(email=g.user.email,username=g.user.name,GraphLink=filename,LinkEmanio=form.LinkEmanio.data,
        # Category= form.Category.data,Priority=form.Priority.data,Title=form.Title.data,Description=form.Description.data,
        # Status=form.Status.data,ProjectLead=form.ProjectLead.data,InterventionSuggestion=form.InterventionSuggestion.data,
        # initTime = datetime.datetime.utcnow(),StatusChangeSTamp=datetime.datetime.utcnow(),
        # Timeline=str(datetime.datetime.utcnow())+", "+str(form.Status.data)+", ")
        # db.session.add(p)
        db.session.commit()
        #send email to user and admin
        flash("Changes saved")
        # if form.submitSave.data:        
        #     return redirect(url_for('rusform'))
        # else:
        return redirect(url_for('allrus'))
    else:
        flash_errors(form)
        return render_template("rusform.html",email=g.user.email,name=g.user.name,form=form)



@app.route("/rulist",methods=["GET","POST"])
def allrus():
    formfilter=rutablefilter()
    # rulist= db.session.query(models.staging_providers.agency).distinct()
    l3c=True
    # rulist= models.staging_providers.query.filter_by( level_3_classic = l3c).all()
    if formfilter.submit.data:
        try:
            if formfilter.provsearch.data == '':
                if formfilter.missing.data=="None":
                    if formfilter.level_3_classic.data==False:
                        rulist= models.staging_providers.query.filter(models.staging_providers.level_3_classic.
                            op("IS NOT")(True)).order_by(desc(models.staging_providers.last_change_stamp)).all()
                    else:
                        rulist= models.staging_providers.query.order_by(desc(models.staging_providers.last_change_stamp)).all()               
                else:
                    if formfilter.level_3_classic.data==False:
                        # if getattr(models.staging_providers,formfilter.missing.data).property.columns[0].type.python_type==str:
                        # if type(getattr(models.staging_providers.query.first(),formfilter.missing.data))=="float":
                        #     rulist=models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data).like('')).filter((models.staging_providers.level_3_classic == None)|(models.staging_providers.level_3_classic == False)).all()
                        # else:
                            rulist=models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data) == None).filter((models.staging_providers.level_3_classic == None)|(models.staging_providers.level_3_classic == False)).all()     
                    else:
                    #     if getattr(models.staging_providers,formfilter.missing.data).property.columns[0].type.python_type==str:
                    #     # if type(getattr(models.staging_providers.query.first(),formfilter.missing.data))=="float":
                    #         rulist=models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data).like('')).filter((models.staging_providers.level_3_classic == 1)).all()
                        # else:
                            rulist=models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data) == None).filter((models.staging_providers.level_3_classic == 1)).all()     
            else:#provsearch has something in it
                if formfilter.level_3_classic.data==False:
                    # import pdb;pdb.set_trace()
                    if formfilter.missing.data=="None":
                        rulist= models.staging_providers.query.filter(( models.staging_providers.level_3_classic == None)|( models.staging_providers.level_3_classic == False)).filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()
                    else:
                        # if getattr(models.staging_providers,formfilter.missing.data).property.columns[0].type.python_type==str:
                        # #does not work yet need to add the ability to search by both
                        #     rulist= models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data).like('')).filter(( models.staging_providers.level_3_classic == None)|( models.staging_providers.level_3_classic == False)).filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()        
                        # else:
                            rulist= models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data) == None).filter(( models.staging_providers.level_3_classic == None)|( models.staging_providers.level_3_classic == False)).filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()        
                else:     
                    # import pdb;pdb.set_trace()
                    if formfilter.missing.data=="None":
                        rulist= models.staging_providers.query.filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()
                    else:
                        # if getattr(models.staging_providers,formfilter.missing.data).property.columns[0].type.python_type==str:
                        # #does not work yet need to add the ability to search by both
                        #     rulist= models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data).like('')).filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()        
                        # else:
                            rulist= models.staging_providers.query.filter(getattr(models.staging_providers, formfilter.missing.data) == None).filter(models.staging_providers.provider_name.ilike("%"+formfilter.provsearch.data+"%")|models.staging_providers.reporting_unit.ilike("%"+formfilter.provsearch.data+"%")).all()        
        except:
            rulist=['no results']
    else:
        rulist= (
            models.staging_providers.query
            .filter(models.staging_providers.end_date == None)
            .order_by(models.staging_providers.last_change_stamp.desc(),models.staging_providers.start_date.desc())
            .limit(250).all()
            )
        flash('showing 250 results with no end-dates.  Submit with no search input for full list of providers')
    # rulist= models.staging_providers.query.filter( models.staging_providers.level_3_classic != 1).all()
    # sorted(q_sum, key=lambda tup: tup[7])
    # import pdb;pdb.set_trace()
    if rulist==[]:
        rulist=['no results']
    return render_template("ruview.html",rulist=rulist,formfilter=formfilter)

@app.route("/rureview",methods=["GET","POST"])
@logged_in
def rureview():
    x=db.session.query(models.staging_providers,models.providers).outerjoin(models.providers).filter(models.staging_providers.modified_on > models.providers.modified_on)
    # import pdb;pdb.set_trace()
    return render_template("rureview.html",email=g.user.email,name=g.user.name,x=x)

from sqlalchemy.sql import exists

@app.route("/stageupdate/<rurow>",methods=["GET","POST"])
@logged_in
def stageupdate(rurow):
    # import pdb; pdb.set_trace()
    staging_providers=models.staging_providers.query.filter_by(id=rurow).first()
    if db.session.query(exists().where(models.providers.id == rurow)).scalar():
        ruprod=models.providers.query.filter_by(id=rurow).first()
        form = rutable(obj=staging_providers)
        form.populate_obj(ruprod)
        if form.agency.data == '':
            ruprod.agency=None
        if form.dbservicemodality.data == '':
            ruprod.dbservicemodality=None
        if form.provider_level.data == '':
        if form.agency.data == 'None':
            ruprod.agency=None
        if form.dbservicemodality.data == 'None':
            ruprod.dbservicemodality=None
            ruprod.provider_level=None
        if form.psmasktext.data == '':
            ruprod.psmasktext=None
        if form.predesessor.data == '':
            ruprod.predesessor=None
        if form.school_cds_id.data == '':
            ruprod.school_cds_id=None
        if form.ab3632.data == 'None':
            ruprod.ab3632=None
        if form.residential.data == 'None':
            ruprod.residential=None
        if form.ab3632 .data == 'None': 
            ruprod.ab3632 =None
        if form.calworks.data == 'None':    
            ruprod.calworks=None
        if form.cesdc.data == 'None':   
            ruprod.cesdc=None
        if form.county_run .data == 'None': 
            ruprod.county_run =None
        if form.day_treatment.data == 'None':   
            ruprod.day_treatment=None
        if form.kidsru .data == 'None': 
            ruprod.kidsru =None
        # if form.level_2 .data == 'None':    
        #     ruprod.level_2 =None
        if form.level_3_classic .data == 'None':    
            ruprod.level_3_classic =None
        if form.mhsa .data == 'None':   
            ruprod.mhsa =None
        if form.older_adult .data == 'None':    
            ruprod.older_adult =None
        if form.out_of_county .data == 'None':  
            ruprod.out_of_county =None
        if form.program    .data == 'None': 
            ruprod.program    =None
        if form.in_school.data == 'None':   
            ruprod.in_school=None
        if form.tay .data == 'None':    
            ruprod.tay =None
        if form.tbs .data == 'None':    
            ruprod.tbs =None
        # if form.cooked .data == 'None': 
        #     ruprod.cooked =None
        if form.cans.data == 'None':
            ruprod.cans=None
        if form.meds_fall_off.data == 'None':   
            ruprod.meds_fall_off=None
        if form.cesdc_model.data == 'None': 
            ruprod.cesdc_model=None
        # if form.level_3_type.data == 'None':    
        #     ruprod.level_3_type=None
        if form.child_welfare.data == 'None':   
            ruprod.child_welfare=None
        if form.family_service_expected.data == 'None': 
            ruprod.family_service_expected=None
        if form.intensive_needs_clients.data == 'None': 
            ruprod.intensive_needs_clients=None
        if form.case_management.data == 'None': 
            ruprod.case_management=None
        # if form.level_1.data == 'None': 
        #     ruprod.level_1=None
        if form.deliverable_exempt.data == 'None':  
            ruprod.deliverable_exempt=None
        if form.srp.data == 'None': 
            ruprod.srp=None
        if form.crisis.data == 'None':  
            ruprod.crisis=None
        if form.high_level.data == 'None':  
            ruprod.high_level=None
        if form.follow_up_care.data == 'None':  
            ruprod.follow_up_care=None
    # else:
    #     ruprod=rutable(ru=staging_providers.reporting_unit)
    #     form = rutable(obj=staging_providers)
    #     form.populate_obj(ruprod)
    # staging_providers.reviewEdit=False
    # ruprod.reviewEdit=False
        # ruprod.modified_on=datetime.datetime.utcnow()
        db.session.commit()
        # ruprod.modified_on=datetime.datetime.now()
        # production=models.staging_providers.query.filter_by(id=rurow).first()
        # print production.modified_on
        # production.modified_on=datetime.datetime.utcnow()
        # print production.modified_on
        # db.session.commit()
    return redirect(url_for('rureview'))

@app.route("/stagereject/<rurow>",methods=["GET","POST"])
@logged_in
def stagereject(rurow):
    production=models.providers.query.filter_by(id=rurow).first()
    if db.session.query(exists().where(models.providers.id == rurow)).scalar():
        staging=models.staging_providers.query.filter_by(id=rurow).first()
        form = rutable(obj=production)
        form.populate_obj(staging)
    # else:
    #     staging=rutable(ru=staging_providers.reporting_unit)
    #     form = rutable(obj=staging_providers)
    #     form.populate_obj(staging)
    # staging_providers.reviewEdit=False
    # staging.reviewEdit=False
        if form.dbservicemodality.data == '':
            staging.dbservicemodality=None
        if form.agency.data == '':
            staging.agency=None
        if form.dbservicemodality.data == 'None':
            staging.dbservicemodality=None
        if form.agency.data == 'None':
            staging.agency=None
        if form.provider_level.data == '':
            staging.provider_level=None
        if form.psmasktext.data == '':
            staging.psmasktext=None
        if form.predesessor.data == '':
            staging.predesessor=None
        if form.school_cds_id.data == '':
            staging.school_cds_id=None
        if form.ab3632.data == 'None':
            staging.ab3632=None
        if form.residential.data == 'None':
            staging.residential=None
        if form.ab3632 .data == 'None': 
            staging.ab3632 =None
        if form.calworks.data == 'None':    
            staging.calworks=None
        if form.cesdc.data == 'None':   
            staging.cesdc=None
        if form.county_run .data == 'None': 
            staging.county_run =None
        if form.day_treatment.data == 'None':   
            staging.day_treatment=None
        if form.kidsru .data == 'None': 
            staging.kidsru =None
        # if form.level_2 .data == 'None':    
        #     staging.level_2 =None
        if form.level_3_classic .data == 'None':    
            staging.level_3_classic =None
        if form.mhsa .data == 'None':   
            staging.mhsa =None
        if form.older_adult .data == 'None':    
            staging.older_adult =None
        if form.out_of_county .data == 'None':  
            staging.out_of_county =None
        if form.program    .data == 'None': 
            staging.program    =None
        if form.in_school.data == 'None':   
            staging.in_school=None
        if form.tay .data == 'None':    
            staging.tay =None
        if form.tbs .data == 'None':    
            staging.tbs =None
        # if form.cooked .data == 'None': 
        #     staging.cooked =None
        if form.cans.data == 'None':
            staging.cans=None
        if form.meds_fall_off.data == 'None':   
            staging.meds_fall_off=None
        if form.cesdc_model.data == 'None': 
            staging.cesdc_model=None
        # if form.level_3_type.data == 'None':    
        #     staging.level_3_type=None
        if form.child_welfare.data == 'None':   
            staging.child_welfare=None
        if form.family_service_expected.data == 'None': 
            staging.family_service_expected=None
        if form.intensive_needs_clients.data == 'None': 
            staging.intensive_needs_clients=None
        if form.case_management.data == 'None': 
            staging.case_management=None
        # if form.level_1.data == 'None': 
        #     staging.level_1=None
        if form.deliverable_exempt.data == 'None':  
            staging.deliverable_exempt=None
        if form.srp.data == 'None': 
            staging.srp=None
        if form.crisis.data == 'None':  
            staging.crisis=None
        if form.high_level.data == 'None':  
            staging.high_level=None
        if form.follow_up_care.data == 'None':  
            staging.follow_up_care=None
        db.session.commit()
        # production=models.staging_providers.query.filter_by(id=rurow).first()
        # print production.modified_on
        production.modified_on=datetime.datetime.now()
        print production.modified_on
        db.session.commit()
    return redirect(url_for('rureview'))


@app.route("/searchuser", methods=["GET", "POST"])
@logged_in
def searchuser():
    form = AddUser()
    r={}
    if request.method == 'POST':
        if form.search.data != None:
            l = ldap.initialize("ldap://10.129.18.101")
            l.simple_bind_s("program\%s" % form.username.data,form.password.data)
            # print "Authentification Successful"
            ldaplist=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(displayName=*%s*)' % form.search.data,['mail','objectGUID','displayName'])
            # import pdb;pdb.set_trace()
            for i in ldaplist:
                if 'mail' in i[1]:
                    if 'displayName' in i[1]:
                        r[i[1]['displayName'][0] ]= i[1]['mail'][0] 
                    else:
                        r['unknown' ]= i[1]['mail'][0] 
                else:
                    if 'displayName' in i[1]:
                        r[i[1]['displayName'][0] ]= 'Noemail@aol.com' 
                    else:
                        r['unknown'  ]= 'Noemail@aol.com'              
            # email=r[0][1]['mail'][0]   
            # GUID=r[0][1]['objectGUID'][0]   
            # FullName=r[0][1]['displayName'][0] 

            # import uuid
            # guid = uuid.UUID(bytes=GUID)
    return render_template("loginsearch.html", form=form,r=r,user=g.user.admin)

@app.route("/adduser/<name>/<emailx>/<r>", methods=["GET", "POST"])
def adduser(name,emailx,r):
    form = AddUser()
    if request.method == 'POST': 
        if form.search.data != None:
            l = ldap.initialize("ldap://10.129.18.101")
            l.simple_bind_s("program\%s" % form.username.data,form.password.data)
            # print "Authentification Successful"
            ldaplist=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(displayName=*%s*)' % form.search.data,['mail','objectGUID','displayName'])
            # import pdb;pdb.set_trace()
            r={}
            for i in ldaplist:
                if 'mail' in i[1]:
                    if 'displayName' in i[1]:
                        r[i[1]['displayName'][0] ]= i[1]['mail'][0] 
                    else:
                        r['unknown' ]= i[1]['mail'][0] 
                else:
                    if 'displayName' in i[1]:
                        r[i[1]['displayName'][0] ]= 'Noemail@aol.com' 
                    else:
                        r['unknown'  ]= 'Noemail@aol.com'   
        else:
            flash("That don't work")                
        return render_template("loginsearch.html", form=form,r=r) 
    if not models.User.query.filter_by(email=unicode(emailx)).first(): 
        p=models.User(name=name,email=emailx)
        db.session.add(p)
        db.session.commit()  
        flash("User Added!")
    else:
        flash("User already exists.")
    import ast
    r=ast.literal_eval(r)
    return render_template("loginsearch.html", form=form,r=r,user=g.user.admin)


#########################
@app.route("/myrequest",methods=["GET","POST"])
@logged_in
def myrequest():
    requestlist= models.Request.query.filter_by(email=g.user.email).all() 
    return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

@app.route('/viewrequest/<id>/', methods=['GET', 'POST'])
@logged_in
def view_request(id):
    test=models.Request.query.filter_by(id=int(id)).first() 
    form=RequestData(obj=test)
    # test
    if form.submitRequest.data:
        form.agency.data=','.join(form.agency.data)
        for field in requestvars:
            fbool_value=getattr(test,"RejBool"+field)
            if fbool_value==True:
                f_value =getattr(test,field)
                fform_value=getattr(form,field).data
                f_value=fform_value         
                setattr(test, field, fform_value)   
        test.UserAction=form.UserAction.data        
        db.session.commit()   
    # if form.validate_on_submit():
        # form.assigned.data=form.assigned.data.staff
        if form.status.data=="Complete":
            if ''.join(get_history(test,'status')[1])==(form.status.data) and test.completeDate != None:
                print 'still complete'
            else:
                test.completeDate=datetime.datetime.utcnow()
        else:
            test.completeDate=None
        # form.populate_obj(reqest.form, test)
        # db.session.commit()
        flash("Changes saved")
        return redirect(url_for('followup'))
        # else:
        #     flash_errors(form)
    form.agency.data=''.join(form.agency.data).split(',')
    # else:
    #     flash_errors(form)
    #     test.note=form.note.data
    #     db.session.commit()
    # if delete_form.validate_on_submit():
    #     db.session.delete(ptask)
    #     db.session.commit()
    #     return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template('view_request.html',request_to_edit =test,name=g.user.name,form=form)


@app.route('/adminedit/<id>/<a>/<s>/<r>', methods=['GET', 'POST'])
@logged_in
def admin_edit(id,a,s,r):
    request_to_edit=models.Request.query.filter_by(id=int(id)).first() 
    form=RequestData(obj=request_to_edit)
    formfilter=filterRequests()
    RB= list(set([h.requestedBy for h in models.Request.query.all()]))
    RB.append('No Filter')
    formfilter.requestedBy.choices=zip(RB,RB)
    AT= list(set([h.staffback for h in models.Request.query.all()]))
    AT.append('No Filter')
    formfilter.assigned.choices=zip(AT,AT)
    ST= list(set([h.statusback for h in models.Request.query.all()]))
    ST.append('No Filter')
    formfilter.status.choices=zip(ST,ST)
    # requestlist=rl
    # requestlist= models.Request.query.all() 
    # if request.method == 'POST' and  formFilter.submitrequest.data:
    if formfilter.submitFilter.data:
        # if formfilter.validate_on_submit():
            s=formfilter.status.data
            a=formfilter.assigned.data
            r=formfilter.requestedBy.data
            # form=RequestData(obj=request_to_edit)
            if formfilter.status.data=='No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data=='No Filter':
                    requestlist= models.Request.query.all() 
            elif formfilter.status.data != 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data=='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data)).all()
            elif formfilter.status.data == 'No Filter' and formfilter.assigned.data!='No Filter' and formfilter.requestedBy.data=='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
            elif formfilter.status.data == 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data!='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data)).all()
            elif formfilter.status.data != 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data!='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
                .filter(models.Request.statusback.has(status=formfilter.status.data)).all()
            elif formfilter.status.data == 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data!='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
                .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
            elif formfilter.status.data != 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data =='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data))\
                .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
            elif formfilter.status.data != 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data !='No Filter':
                requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data))\
                .filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
                .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
            # formfilter.status.data=s
            # formfilter.assigned.data=a
            # formfilter.requestedBy.data=r
            return redirect(url_for('admin_edit',id=id,a=a,s=s,r=r))
    formfilter.status.data=s
    formfilter.assigned.data=a
    formfilter.requestedBy.data=r
    if formfilter.status.data=='No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data=='No Filter':
            requestlist= models.Request.query.all() 
    elif formfilter.status.data != 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data=='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data)).all()
    elif formfilter.status.data == 'No Filter' and formfilter.assigned.data!='No Filter' and formfilter.requestedBy.data=='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
    elif formfilter.status.data == 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data!='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data)).all()
    elif formfilter.status.data != 'No Filter' and formfilter.assigned.data=='No Filter' and formfilter.requestedBy.data!='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
        .filter(models.Request.statusback.has(status=formfilter.status.data)).all()
    elif formfilter.status.data == 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data!='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
        .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
    elif formfilter.status.data != 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data =='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data))\
        .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
    elif formfilter.status.data != 'No Filter' and formfilter.assigned.data !='No Filter' and formfilter.requestedBy.data !='No Filter':
        requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=formfilter.status.data))\
        .filter(models.Request.requestedBy.like(formfilter.requestedBy.data))\
        .filter(models.Request.staffback.has(staff=formfilter.assigned.data)).all()
    if form.submitRequest.data:
        if form.validate_on_submit():
            form.agency.data=','.join(form.agency.data)
            # form.assigned.data=form.assigned.data.staff
            if form.statusback.data=="Complete":
                if ''.join(get_history(request_to_edit,'statusback')[1])==(form.statusback.data) and request_to_edit.completeDate != None:
                    print 'still complete'
                else:
                    request_to_edit.completeDate=datetime.datetime.utcnow()
            else:
                request_to_edit.completeDate=None
            form.populate_obj(request_to_edit)
            # request_to_edit.save()
            db.session.commit()
            flash("Changes saved")
        else:
            flash_errors(form)
    else:
        form.agency.data=''.join(form.agency.data).split(',')
        # print 'pdb inside save'
    return render_template('admin_edit.html',a=a,s=s,r=r,request_to_edit=request_to_edit,email=g.user.email,id=id,
        name=g.user.name,form=form,requestlist=requestlist,formfilter=formfilter)

@app.route('/edit_request/<id>/', methods=['GET', 'POST'])
@logged_in
def edit_request(id):
    request_to_edit=models.Request.query.filter_by(id=int(id)).first() 
    form=RequestData(obj=request_to_edit)
    # form.populate_obj(request_to_edit)
    if request.method == 'POST':
        request_to_edit.note=form.note.data
        db.session.commit()
        return redirect(url_for('myrequest'))
    # if delete_form.validate_on_submit():
    #     db.session.delete(ptask)
    #     db.session.commit()
    #     return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template('edit_request.html',request_to_edit=request_to_edit ,name=g.user.name,form=form)



@app.route("/followup",methods=["GET","POST"])
@logged_in
def followup():
    print 'follow up'
    # requestlist= models.Request.query.filter_by(email=g.user.email).all() 
    return render_template("followup.html",email=g.user.email,name=g.user.name)


@app.route("/request_management",methods=["GET","POST"])
@logged_in
def Request_management():
    form=filterRequests()
    formRequest = RequestData( )
      # db.session.query(models.Request).filter(models.Request.requestedBy.like('2'))\
      # .filter(models.Request.requestedBy.like('2'))\
      # .filter(models.Request.assigned.like('Unassigned')).all()
      # p=models.Request(email=g.user.email,username=g.user.name,jobTitle=form.jobTitle.data,deadlinedate=form.deadlinedate.data,emanio=form.emanio.data,MHorSUD=form.MHorSUD.data,
      #   keyQuestions=form.keyQuestions.data, problem=form.problem.data,specialFacts=form.specialFacts.data,requestedBy=form.requestedBy.data, priority=form.priority.data,
      #   timeframe=form.timeframe.data,timeBreakdown=form.timeBreakdown.data,specialPop=form.specialPop.data,agency=form.agency.data,ru=form.ru.data,
      #    specialInstructions=form.specialInstructions.data, typeOfService=form.typeOfService.data, timeframestart=form.timeframestart.data, timeframeend=form.timeframeend.data, 
      #    longDescription=form.longDescription.data, requestDate=datetime.datetime.utcnow(),assigned="Unassigned",
      #    audience=form.audience.data,  columnsRequired=form.columnsRequired.data, deadlinetime=form.deadlinetime.data, deadlineWhy=form.deadlineWhy.data)
      # db.session.add(p)
      # db.session.commit() 
    RB= list(set([h.requestedBy for h in models.Request.query.all()]))
    RB.append('No Filter')
    form.requestedBy.choices=zip(RB,RB)
    AT= list(set([h.staffback for h in models.Request.query.all()]))
    AT.append('No Filter')
    form.assigned.choices=zip(AT,AT)
    ST= list(set([h.statusback for h in models.Request.query.all()]))
    ST.append('No Filter')
    form.status.choices=zip(ST,ST)
    requestlist= models.Request.query.all() 
    # if form.validate_on_submit():
    if form.submitFilter.data:
        if form.status.data=='No Filter' and form.assigned.data=='No Filter' and form.requestedBy.data=='No Filter':
                requestlist= models.Request.query.all() 
        elif form.status.data != 'No Filter' and form.assigned.data=='No Filter' and form.requestedBy.data=='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=form.status.data)).all()
        elif form.status.data == 'No Filter' and form.assigned.data!='No Filter' and form.requestedBy.data=='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.staffback.has(staff=form.assigned.data)).all()
        elif form.status.data == 'No Filter' and form.assigned.data=='No Filter' and form.requestedBy.data!='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(form.requestedBy.data)).all()
        elif form.status.data != 'No Filter' and form.assigned.data=='No Filter' and form.requestedBy.data!='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(form.requestedBy.data))\
            .filter(models.Request.statusback.has(status=form.status.data)).all()
        elif form.status.data == 'No Filter' and form.assigned.data !='No Filter' and form.requestedBy.data!='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.requestedBy.like(form.requestedBy.data))\
            .filter(models.Request.staffback.has(staff=form.assigned.data)).all()
        elif form.status.data != 'No Filter' and form.assigned.data !='No Filter' and form.requestedBy.data =='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=form.status.data))\
            .filter(models.Request.staffback.has(staff=form.assigned.data)).all()
        elif form.status.data != 'No Filter' and form.assigned.data !='No Filter' and form.requestedBy.data !='No Filter':
            requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=form.status.data))\
            .filter(models.Request.requestedBy.like(form.requestedBy.data))\
            .filter(models.Request.staffback.has(staff=form.assigned.data)).all()
    else:
        form.status.data='No Filter'  
        form.assigned.data='No Filter'  
        form.requestedBy.data='No Filter'
                              # requestlist = db.session.query(models.Request).filter(models.Request.statusback.has(status=form.status.data))\
      # .filter(models.Request.requestedBy.like('2'))\
      # .filter(models.Request.assigned.like('Unassigned')).all()
    return render_template("request_management.html",email=g.user.email,name=g.user.name,requestlist=requestlist,form=form,formRequest=formRequest,
     s=form.status.data,a= form.assigned.data,r= form.requestedBy.data)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
# agency=','.join(form.agency.data)

@app.route("/requestform/<WHICH>",methods=["GET","POST"])
@logged_in
def requestform(WHICH):
    form = UserRequestData()
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    if form.validate_on_submit():
      print 'submit'
      # p=models.Request(email=g.user.email,username=g.user.name,
      #  requestDate=datetime.datetime.utcnow(),assigned="Unassigned",status="Pending Review")
      # form.agency.data=', '.join(form.agency.data)
      # form.populate_obj(p)
      if form.emanio.data==True:
        form.emanio.data=1
      else:
        form.emanio.data=0
      p=models.Request(email=g.user.email,username=g.user.name,jobTitle=form.jobTitle.data,deadlinedate=form.deadlinedate.data,
        emanio=form.emanio.data,MHorSUD=form.MHorSUD.data,supervisor=form.supervisor.data,
        keyQuestions=form.keyQuestions.data, problem=form.problem.data,specialFacts=form.specialFacts.data,requestedBy=g.user.name, 
        priority=form.priority.data,staffback=models.Staff.query.filter_by(staff="Unassigned").first(),
        statusback=models.Status.query.filter_by(status="Pending Review").first(),
        timeframe=form.timeframe.data,timeBreakdown=form.timeBreakdown.data,specialPop=form.specialPop.data,ru=form.ru.data,
        agency=','.join(form.agency.data),
         specialInstructions=form.specialInstructions.data, typeOfService=form.typeOfService.data, timeframestart=form.timeframestart.data, 
         timeframeend=form.timeframeend.data, 
         longDescription=form.longDescription.data, requestDate=datetime.datetime.utcnow(),assigned="Unassigned",status="Pending Review",
         audience=form.audience.data,  columnsRequired=form.columnsRequired.data, deadlinetime=form.deadlinetime.data, 
         deadlineWhy=form.deadlineWhy.data)
      db.session.add(p)
      db.session.commit()
      #send email to user and admin
      return redirect(url_for('Request_management'))
    else:
        flash_errors(form)
    if WHICH=='1':
        print 'short!!'
        return render_template("short.html",email=g.user.email,name=g.user.name,form=form)
    else:
        return render_template("long.html",email=g.user.email,name=g.user.name,form=form)



@app.route('/navstart', methods=['GET','POST'])
@logged_in
def navstart():
    aform=ldapA()
    email=None
    AS=None
    if aform.validate_on_submit():
        import sys
        import ldap
        l = ldap.initialize("ldap://10.129.18.101")
        email=None
        try:
            l.simple_bind_s("program\%s" % aform.username.data,aform.password.data)
            print "Authentification Successful"
            r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % aform.username.data,['mail'])
            email=r[0][1]['mail']
            AS=1
            print email
        except:
            print 'Failed'
            AS=0
        print email
        # return render_template("navStart.html",aform=aform,email=email,AS=AS)
    return render_template("navStart.html",aform=aform,email=email,AS=AS,user=g.user.admin)




@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('http://hpmxl2221nxk:5000/')


@app.route('/start', methods=['GET','POST'])
def start():
    return redirect('http://hpmxl2221nxk:5000/start')


@app.route("/pickaform",methods=["GET","POST"])
@logged_in
def pickaform():
    form = Which()
    if form.validate_on_submit():
        print form.formtype.data
        if form.formtype.data==u"Short":
            WHICH=1
        else:
            WHICH=2
        return redirect(url_for("requestform",WHICH=WHICH))
    return render_template("start.html",email=g.user.email,name=g.user.name,form=form,)


@app.route("/allrequest",methods=["GET","POST"])
@logged_in
def allrequest():
    requestlist= models.Request.query.all() 
    return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)


@app.route("/main")
@logged_in
def main():
    return render_template("main.html")


@app.route('/edittoc/<id>/', methods=['GET', 'POST'])
def edit_toc(id): 
    toc=models.dashboards.query.filter_by(id=id).first()
    # delete_form=DeleteRow_form()
    form = TOC(obj=toc)
    # import pdb;pdb.set_trace()
    if toc.went_live_on:
        form.went_live_on.data = form.went_live_on.data.strftime("%m/%d/%Y")
    # form.went_live_on.data = toc.went_live_on.strftime("%Y/%m/%d")
    if request.method == 'POST':
        form.populate_obj(toc)   
        # toc.went_live_on = form.went_live_on 
        db.session.commit()
        return redirect(url_for('alltoc'))
    # if delete_form.validate_on_submit():
    #     db.session.delete(toc)
    #     db.session.commit()
    #     return redirect(url_for('alltoc'))
    return render_template('edit_toc.html',id=id,form=form)


@app.route("/tocform",methods=["GET","POST"])
@logged_in
def tocform():
    form = TOC()
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    if form.validate_on_submit():
        # import pdb;pdb.set_trace()
        new_toc=models.dashboards(title=form.title.data,
agency=form.agency.data,
category=form.category.data,
description=form.description.data,
link=form.link.data,
purpose=form.purpose.data,identified=form.identified.data,
status=form.status.data,
went_live_on=form.went_live_on.data,
code_author=form.code_author.data,
report_author=form.report_author.data)
        # import pdb;pdb.set_trace()
        db.session.add(new_toc)
        db.session.commit()
        #send email to user and admin
        flash("Dashboard Added!")
        # new_toc=models.dashboards.query.filter_by().first() 
        toc_row=models.dashboards.query.filter_by(title=form.title.data).first()
        # toc_row=db.session.query(models.dashboards_questions.question,models.dashboards.title,models.dashboards_questions.id).join(models.dashboards).filter_by(id=new_toc.id).all()
        form=TOCquestions()
        form_review=TOCreview()
        return redirect(url_for('tocquestion',form=form,id=toc_row.id,sub='test',action='test',form_review=form_review))
        # return render_template("tocquestions.html",toc_row=toc_row,form=form,id=id)
        # return render_template("tocquestions.html",form=form,id=new_toc.id)
    else:
        flash_errors(form)
    return render_template("tocform.html",email=g.user.email,name=g.user.name,form=form)

@app.route("/tocquestion/<id>/<action>/<sub>",methods=["GET","POST"])
@logged_in
def tocquestion(id,action,sub):
    toc_row=models.dashboards.query.filter_by(id=id).first()
    # import pdb;pdb.set_trace()
    # toc_row=db.session.query(models.dashboards_questions.question,models.dashboards.title,models.dashboards_questions.id).join(models.dashboards).filter_by(id=id).all()
    form=TOCquestions()
    form_review=TOCreview()
    form_systems=TOCsystems()
    # import pdb;pdb.set_trace()
    if form.validate_on_submit():
        action='test'
        if form.submitTOCquestion.data:
            new_q=models.dashboards_questions(question=form.question.data,dashboard_id=id)
            db.session.add(new_q)
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
        if form_review.submitTOCreview.data:
            # import pdb;pdb.set_trace()
            new_q=models.dashboards_reviews(category=form_review.category.data,
                                            reviewer=g.user.name,
                                            review_date=form_review.review_date.data,
                                            dashboard_id=id)
            db.session.add(new_q)
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
        if form_systems.submitTOCsystem.data:
            new_q=models.dashboards_systems (system_of_care=form_systems.system_of_care.data,
                                            dashboard_id=id)
            db.session.add(new_q)
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
    elif action == 'delete_q':
            db.session.delete(models.dashboards_questions.query.filter_by(id=sub).first())
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
    elif action == 'delete_r':
            db.session.delete(models.dashboards_reviews.query.filter_by(id=sub).first())
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
    elif action == 'delete_s':
            db.session.delete(models.dashboards_systems.query.filter_by(id=sub).first())
            db.session.commit()
            toc_row=models.dashboards.query.filter_by(id=id).first()
    return render_template("tocquestions.html",toc_row=toc_row,form=form,id=id,form_review=form_review,form_systems=form_systems,action=action,name=g.user.name)

@app.route("/toclist",methods=["GET","POST"])
@logged_in
def alltoc():
    # toclist= models.TOC.query.order_by(models.Challenge.Priority).all()
    toclist= models.dashboards.query.all()
    # toc_row=db.session.query(models.dashboards_reviews.category,models.dashboards.title,models.dashboards_reviews.id).outerjoin(models.dashboards,models.dashboards_reviews).all()
    # import pdb;pdb.set_trace()
    # sorted(q_sum, key=lambda tup: tup[7])
    return render_template("tocview.html",email=g.user.email,name=g.user.name,toclist=toclist)



# from app import db


# @app.route('/sendemail', methods=['GET', 'POST'])
# def sendEmailV4():
#     # subject = ''
#     recipient=', '.join(['cmeinzer@acbhcs.org'])
#     body='html text'
#     subject = 'subjectline'
#     headers = ["From: " + 'chet@acbhcs.org',
#                "Subject: " + 'subject',
#                "To: " + 'cmeinzer@acbhcs.org',
#                "MIME-Version: 1.0",
#                "Content-Type: text/html"]
#     headers = "\r\n".join(headers)
#     session = smtplib.SMTP("allsmtp.acgov.org",25)
#     session.ehlo()
#     session.starttls()
#     session.ehlo
#     session.sendmail('chet@acbhcs.org', ['cmeinzer@acbhcs.org'], headers + "\r\n\r\n" + body)
#     session.quit()
#     return "it worked"

# app.config.from_object('config')
