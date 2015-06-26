from app import db, models
x=models.User(name='Chet Meinzer',email='meinzerc@acbhcs.org',authenticated=1)
db.session.add(x)
db.session.commit()
quit()
