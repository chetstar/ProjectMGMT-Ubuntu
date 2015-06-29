rm app.db
python db_create.py

python
from app import db, models
x=models.User(name='Chet Meinzer',email='meinzerc@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
x=models.Staff(staff='Chet Meinzer',privelage='admin')
y=models.Staff(staff='fake user',privelage='')
db.session.add(y)
db.session.add(x)
db.session.commit()

quit()

python run.py