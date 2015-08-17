from app import app,models, db
# from forms import goal_form, strategy_form, project_form, task_form,DeleteRow_form,ldapA,LoginForm, Request, Which,Staff
from forms import LoginForm, RequestData, Which,ldapA, filterRequests, UserRequestData, Challenges,DeleteRow_form, TOC, rutable
import datetime
from sqlalchemy.orm.attributes import get_history
from werkzeug import secure_filename
import re, shutil, os, sys
from sqlalchemy.sql import func
from sqlalchemy import case
from sqlalchemy import and_
# from app.models import Tasks, Projects, Goals, Strategies
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
from threading import Thread
from flask.ext.login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import ldap
from flask import render_template, flash, redirect,Flask,Response,request,url_for, g,session,jsonify
login_manager = LoginManager()
login_manager.init_app(app) 

# photos = UploadSet('photos', IMAGES)

requestvars=['agency',
'audience',
'columnsRequired',
'deadlinedate',
'deadlinetime',
'deadlineWhy',
'jobTitle',
'keyQuestions',
'longDescription',
'priority',
'problem',
'requestDate',
'requestedBy',
'ru',
'specialFacts',
'specialInstructions',
'specialPop',
'timeBreakdown',
'timeframe',
'timeframeend',
'timeframestart',
'typeOfService',
'emanio',
'MHorSUD',]





from werkzeug import secure_filename
from flask_wtf.file import FileField
from functools import wraps

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

@app.route("/main")
@logged_in
def main():
    return render_template("main.html")

@app.route("/demo",methods=["GET","POST"])
def demo():
    challengelist= models.Challenge.query.order_by(models.Challenge.Priority).all()
    return render_template("demo.html",challengelist=challengelist)

@app.route("/logout")
# @logged_in
def logout():
    logout_user()
    session.pop('logged_in', None)
    flash("Logged Out.")
    # import pdb;pdb.set_trace()
    return redirect(url_for("login"))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # import pdb;pdb.set_trace()
    if form.validate_on_submit():
        if app.config['ENVIRONMENT']=='dev':
            try:
                print "Authentification Successful" 
                namedb=models.User.query.filter_by(name=unicode(form.username.data)).first()
                email=models.User.query.first().email         
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
                if '@' in form.username.data:
                    form.username.data=re.sub(' /d+','', (re.sub("\d+",'', form.username.data.split('@')[0]))[1:]+(re.sub("\d+",'', form.username.data.split('@')[0]))[0:1])
                # import pdb;pdb.set_trace()
                l = ldap.initialize("ldap://10.129.18.101")
                l.simple_bind_s("program\%s" % form.username.data,form.password.data)
                print "Authentification Successful"
                r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % form.username.data,['mail','objectGUID','displayName'])
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





@app.route('/edittoc/<id>/<core>', methods=['GET', 'POST'])
def edit_toc(id,core): 
    toc=models.TOC.query.filter_by(id=id).first()
    delete_form=DeleteRow_form()
    form = TOC(obj=toc)
    if core == 1:
                flash("You are editing and existing entry")
    if request.method == 'POST' and form.validate_on_submit():
        if core==1:
            form.populate_obj(toc)    
            db.session.commit()
        else:
            x=TOC(Agency=form.Agency.data,
                kill=form.kill.data,
                DashboardQuestion=form.DashboardQuestion.data,
                DashboardReportSort=form.DashboardReportSort.data,
                DorR=form.DorR.data,
                DashboardReport=form.DashboardReport.data,
                SystemofCare=form.SystemofCare.data,
                ServiceArea=form.ServiceArea.data,
                Description=form.Description.data,
                Purpose=form.Purpose.data,
                iddeid=form.iddeid.data,
                TargetedAudience=form.TargetedAudience.data,
                Supportswhichmeeting=form.Supportswhichmeeting.data,
                Ready=form.Ready.data,
                Link=form.Link.data,
                KeyQuestions=form.KeyQuestions.data,
                BornOnDate=form.BornOnDate.data,
                FinalCodeReviewDate=form.FinalCodeReviewDate.data,
                CodeAuthor=form.CodeAuthor.data,
                CodeReviewer=form.CodeReviewer.data,
                FinalReportReviewDate=form.FinalReportReviewDate.data,
                ReportAuthor=form.ReportAuthor.data,
                ReportReviewer=form.ReportReviewer.data)
            db.session.add(x)
            db.session.commit()
        return redirect(url_for('alltoc'))
    if delete_form.validate_on_submit():
        db.session.delete(toc)
        db.session.commit()
        return redirect(url_for('alltoc'))
    return render_template('edit_toc.html',id=id,form=form,delete_form=delete_form)


@app.route("/tocform",methods=["GET","POST"])
@logged_in
def tocform():
    form = TOC()
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    if form.validate_on_submit():
        print 'submit'
    else:
        flash_errors(form)
        return render_template("tocform.html",email=g.user.email,name=g.user.name,form=form)


@app.route("/toclist",methods=["GET","POST"])
@logged_in
def alltoc():
    # toclist= models.TOC.query.order_by(models.Challenge.Priority).all()
    toclist= models.TOC.query.all()
    # sorted(q_sum, key=lambda tup: tup[7])
    # import pdb;pdb.set_trace()
    return render_template("tocview.html",email=g.user.email,name=g.user.name,toclist=toclist)


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
        # import pdb;pdb.set_trace()
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
            # import pdb; pdb.set_trace()
            db.session.add(p)       
        db.session.commit()
        return redirect(url_for('allchallenges'))
    return render_template('edit_challenge.html',id=id,form=form,LinkEmanio=challenge.LinkEmanio)


@app.route("/challengesform",methods=["GET","POST"])
@logged_in
def challengesform():
    form = Challenges()
    # form.staffback.data=models.Staff.query.filter_by(staff="Unassigned").first()
    # import pdb;pdb.set_trace()
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
        # import pdb; pdb.set_trace()
        p=models.Challenge(email=g.user.email,username=g.user.name,GraphLink=filename,LinkEmanio=form.LinkEmanio.data,
        Category= form.Category.data,Priority=form.Priority.data,Title=form.Title.data,Description=form.Description.data,
        Status=form.Status.data,ProjectLead=form.ProjectLead.data,InterventionSuggestion=form.InterventionSuggestion.data,
        initTime = datetime.datetime.utcnow(),StatusChangeSTamp=datetime.datetime.utcnow(),
        Timeline=str(datetime.datetime.utcnow())+", "+str(form.Status.data)+", ")
        # import pdb; pdb.set_trace()
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

@app.route("/pickaform",methods=["GET","POST"])
@logged_in
def pickaform():
    form = Which()
    if form.validate_on_submit():
        # import pdb;pdb.set_trace()
        print form.formtype.data
        if form.formtype.data==u"Short":
            WHICH=1
        else:
            WHICH=2
        return redirect(url_for("requestform",WHICH=WHICH))
    return render_template("start.html",email=g.user.email,name=g.user.name,form=form,)


# @app.route("/requests",methods=["GET","POST"])
# @logged_in
# def requests():
#     requestlist=models.Request.query.all()
#     return render_template("requests.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

@app.route("/allrequest",methods=["GET","POST"])
@logged_in
def allrequest():
    requestlist= models.Request.query.all() 
    # import pdb;pdb.set_trace()
    return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

@app.route("/challengelist",methods=["GET","POST"])
@logged_in
def allchallenges():
    challengelist= models.Challenge.query.order_by(models.Challenge.Priority).all()
    delete_form=DeleteRow_form()
    # import pdb;pdb.set_trace()
    if delete_form.validate_on_submit():
        db.session.delete(models.Challenge.query.filter_by(id=delete_form.row_id.data).first())
        # import pdb;pdb.set_trace()
        db.session.commit()
        return redirect(url_for('allchallenges'))
    # sorted(q_sum, key=lambda tup: tup[7])
    # import pdb;pdb.set_trace()
    return render_template("challengeview.html",email=g.user.email,name=g.user.name,challengelist=challengelist,delete_form=delete_form)

@app.route("/myrequest",methods=["GET","POST"])
@logged_in
def myrequest():
    requestlist= models.Request.query.filter_by(email=g.user.email).all() 
    # import pdb;pdb.set_trace()
    return render_template("followup.html",email=g.user.email,name=g.user.name,requestlist=requestlist)

@app.route('/viewrequest/<id>/', methods=['GET', 'POST'])
@logged_in
def view_request(id):
    test=models.Request.query.filter_by(id=int(id)).first() 
    form=RequestData(obj=test)
    test
    # import pdb;pdb.set_trace()
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
        import pdb;pdb.set_trace()
        db.session.commit()   
    # if form.validate_on_submit():
        # import pdb;pdb.set_trace()                
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
    #     # import pdb;pdb.set_trace()
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
    # import pdb;pdb.set_trace()
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
    # import pdb;pdb.set_trace()

    # if request.method == 'POST' and  formFilter.submitrequest.data:
    # import pdb;pdb.set_trace()
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
            # import pdb;pdb.set_trace()                
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
        # import pdb;pdb.set_trace()
    # import pdb;pdb.set_trace()
    return render_template('admin_edit.html',a=a,s=s,r=r,request_to_edit=request_to_edit,email=g.user.email,id=id,
        name=g.user.name,form=form,requestlist=requestlist,formfilter=formfilter)

@app.route('/edit_request/<id>/', methods=['GET', 'POST'])
@logged_in
def edit_request(id):
    request_to_edit=models.Request.query.filter_by(id=int(id)).first() 
    form=RequestData(obj=request_to_edit)
    # form.populate_obj(request_to_edit)
    # import pdb;pdb.set_trace()
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
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
    # import pdb;pdb.set_trace()
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
      # import pdb;pdb.set_trace()
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
    # import pdb;pdb.set_trace()
    if form.validate_on_submit():
      print 'submit'
      # import pdb;pdb.set_trace()
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
    return render_template("navStart.html",aform=aform,email=email,AS=AS)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect('http://hpmxl2221nxk:5000/')


@app.route('/start', methods=['GET','POST'])
def start():
    return redirect('http://hpmxl2221nxk:5000/start')



from app import db


