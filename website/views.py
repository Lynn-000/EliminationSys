from flask import Blueprint,render_template
from flask_login import login_user, login_required, logout_user, current_user
from .models import Teams,Competitors,Match
from . import db
from sqlalchemy.sql import text
from sqlalchemy import insert, nullslast, delete
import math
views = Blueprint('views', __name__)

def insertprevdupl(Bye, x):
    i=0
    j = 0
    k = 0
    print(len(x))
    while k < len(Bye):
        same = Match.query.filter_by(T1id = Bye[k][0]).first()
        if same:
            print("Prevented duplicate byes")
        else:
            stmt = insert(Match).values(T1id = Bye[k][0], T2id = None, T1Name = Bye[k][1], T2Name = "Bye", T1Score = 0, T2Score = 0)
            db.session.execute(stmt)
        k += 1
    while i < int(len(x)):
        same = Match.query.filter_by(T1id = x[i][0]).first()
        revsame = Match.query.filter_by (T2id = x[i][0]).first()
        same2 = Match.query.filter_by(T1id = x[i][1]).first()
        revsame2 = Match.query.filter_by(T2id = x[i][1]).first()
        if same or revsame or same2 or revsame2 : 
            print(same, revsame, same2, revsame2)
            print("Prevented duplicate match")
        else:
            stmt = insert(Match).values(T1id = x[i][0], T2id = x[i][1], T1Name = x[i][2], T2Name = x[i][3], T1Score = 0, T2Score = 0)
            db.session.execute(stmt)
        i+=1


@views.route('/')
def home():
    teams = Match.query.all()
    print(teams)
    return render_template("home.html", teams = teams, user = current_user)

@views.route('/manageteams')

@login_required
def addteams():
    teams = Teams.query.all()
    return render_template("manageteams.html", teams = teams, user = current_user)

@views.route('/updatematch')

@login_required
def update():
    a = db.session.execute(text('''SELECT id, TName FROM Teams ORDER BY seedRank ASC NULLS LAST'''))
    c = a.fetchall()
    print(c)
    Bye = []
    print(len(c))
    expo = int(math.log2(len(c))) + 1
    print(pow(2, expo))
    for i in range(pow(2, expo) - len(c)):
        Bye.append(c[i])
    print(Bye)
    a = db.session.execute(text('''SELECT TA.id,TB.id, TA.TName, TB.TName FROM Teams TA, Teams TB WHERE TA.id < TB.id'''))
    x = a.fetchall()
    #print(x)
    #print(len(x))
    insertprevdupl(Bye, x)
    db.session.commit()
    return render_template("update.html", user = current_user)



@views.route('/truncate')
@login_required
def trunc():
    db.session.execute(text('''DELETE FROM Match'''))
    db.session.commit()
    #stmt.execute()
    return render_template("Truncate.html", user = current_user)