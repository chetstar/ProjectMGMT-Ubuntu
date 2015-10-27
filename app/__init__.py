from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager, UserMixin, login_required

# import datetime
# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('index.html')
# from flask.ext.admin import BaseView

# class MyView(BaseView):
#     def is_accessible(self):
#         return login.current_user.is_authenticated()

#     def _handle_view(self, name, **kwargs):
#         if not self.is_accessible():
#             return redirect(url_for('login', next=request.url))

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'app/static'
# # These are the extension that we are accepting to be uploaded
# app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','sps','sav','xlsx','doc', 'docx', 'xls','XLS','XLSX'])

app.config.from_object('config')
# import pdb;pdb.set_trace()

# class HackedSQLAlchemy(SQLAlchemy):
#     def apply_driver_hacks(self, app, info, options):
#         print "Applying driver hacks"
#         super(HackedSQLAlchemy, self).apply_driver_hacks(app, info, options)
#         options["supports_unicode_binds"] = False
# db = HackedSQLAlchemy(app)
db = SQLAlchemy(app)


# db.Model.metadata.reflect(db.engine)

# class what(db.Model):
#     __table__ = db.Model.metadata.tables['test']
#     __bind_key__ = 'warehouse'
#     id = db.Column(db.Integer, primary_key=True) 
#     test=db.Column(db.String(40))

# engine = create_engine('sqlite:///webmgmt.db', convert_unicode=True, echo=False)
# Base = declarative_base()
# Base.metadata.reflect(engine)

@app.template_filter('reverse')
def reverse_filter(s):
    if s > datetime.date.today():
      return 0
    else:
       return 1

import re
@app.template_filter('iterateover')
def reverse_filter(s):
       return [i+'chet' for i in re.split(',',s)]

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



Bootstrap(app)
# from flask.ext.mail import Mail
# mail = Mail(app)
from app import views, models
admin = Admin(app)


admin.add_view(ModelView(models.User, db.session))
# admin.add_view(ModelView(models.rutable, db.session))
# admin.add_view(ModelView(models.rustage, db.session))
admin.add_view(ModelView(models.staging_providers, db.session))
# admin.add_view(ModelView(models.test, db.session))
admin.add_view(ModelView(models.Request, db.session))
admin.add_view(ModelView(models.Staff, db.session))
admin.add_view(ModelView(models.Status, db.session))
admin.add_view(ModelView(models.Challenge, db.session))
# admin.add_view(ModelView(models.Strategies, db.session))
# admin.add_view(ModelView(models.Tasks, db.session))