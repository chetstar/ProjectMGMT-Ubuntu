rm app.db
python db_create.py

python
from app import db, models
x=models.User(name='Chet Meinzer',email='meinzerc@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
g=models.Staff(staff='Unassigned',privelage='')
x=models.Staff(staff='Chet Meinzer',privelage='admin')
y=models.Staff(staff='fake user',privelage='')

a=models.Status(status='fake status')
db.session.add(a)
db.session.add(y)
db.session.add(x)
db.session.add(g)
db.session.commit()


quit()

python run.py