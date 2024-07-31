from flask import Blueprint,render_template,request,flash,g,redirect,url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Teams,Competitors,Match
from . import db
from sqlalchemy.sql import text
from sqlalchemy import insert, nullslast, delete
import math
views = Blueprint('views', __name__)

def insertprevdupl(x):
    i=0
    while i < int(len(x)):
        same = Match.query.filter_by(T1id = x[i][0]).first()
        revsame = Match.query.filter_by (T2id = x[i][0]).first()
        same2 = Match.query.filter_by(T1id = x[i][1]).first()
        revsame2 = Match.query.filter_by(T2id = x[i][1]).first()
        if same or revsame or same2 or revsame2 : 
            pass
        else:
            stmt = insert(Match).values(T1id = x[i][0], T2id = x[i][1], T1Name = x[i][2], T2Name = x[i][3], T1Score = 0, T2Score = 0, Ended = 0)
            db.session.execute(stmt)
        i+=1


@views.route('/')
def home():
    teams = Match.query.all()
    nofmatches = len(teams)
    if nofmatches == 0:
        return render_template("homeempty.html", user = current_user)
    else:
        mindex = math.log2(nofmatches * 2)
    return render_template("home.html", teams = teams, mindex = int(mindex), user = current_user)

@views.route('/teams')

def viewteams():
    teams = Teams.query.order_by(Teams.Score.desc()).all()
    return render_template("teams.html", teams = teams, user = current_user)

@views.route('/updatematch')

@login_required
def update():
    a = db.session.execute(text('''SELECT id, TName FROM Teams ORDER BY seedRank ASC NULLS LAST'''))
    c = a.fetchall()
    Bye = []
    expo = int(math.log2(len(c))) + 1
    print(pow(2, expo))
    for i in range(pow(2, expo) - len(c)):
        Bye.append(c[i])
    k = 0
    while k < len(Bye):
        same = Match.query.filter_by(T1id = Bye[k][0]).first()
        if same:
            pass
        else:
            stmt = insert(Match).values(T1id = Bye[k][0], T2id = None, T1Name = Bye[k][1], T2Name = "Bye", T1Score = 0, T2Score = 0, Ended = 0)
            db.session.execute(stmt)
        k += 1
    a = db.session.execute(text('''SELECT TA.id,TB.id, TA.TName, TB.TName FROM Teams TA, Teams TB WHERE TA.id < TB.id AND (TA.seedRank IS NOT NULL OR TB.seedRank IS NOT NULL)'''))
    x = a.fetchall()
    insertprevdupl(x)
    a = db.session.execute(text('''SELECT TA.id, TB.id, TA.TName, TB.TName FROM Teams TA, Teams TB WHERE TA.id < TB.id AND TA.School <> TB.School'''))
    x = a.fetchall()
    insertprevdupl(x)
    a = db.session.execute(text('''SELECT TA.id,TB.id, TA.TName, TB.TName FROM Teams TA, Teams TB WHERE TA.id < TB.id'''))
    x = a.fetchall()
    insertprevdupl(x)
    db.session.commit()
    return render_template("update.html", user = current_user)



@views.route('/truncate')
@login_required
def trunc():
    db.session.execute(text('''DELETE FROM Match'''))
    db.session.commit()
    return render_template("Truncate.html", user = current_user)

@views.route('/test')
def tes():
    return render_template("Test.html", user = current_user)


@views.route('/at', methods = ['GET', 'POST'])
@login_required
def addteams():
    if request.method == 'POST':
        TName =  request.form.get("TName")
        School = request.form.get("School")
        seedRank = int(request.form.get("seedRank"))
        if TName is None or School is None:
            flash('Team name or School name cannot be empty.', category = "error")
        else:
            exist = Teams.query.filter_by(TName = TName).first()
            seedexist = Teams.query.filter_by(seedRank = seedRank).first()
            if exist or seedexist:
                flash('Target team or seed rank is already present in the database. Use edit team or remove team instead.', category = "error")
            elif seedRank == 0:
                newteam = Teams(id=None, TName = TName, School = School, Score = 0, seedRank = None)
                db.session.add(newteam)
                db.session.commit()
                flash('Successfully inserted data.', category = "success")
            elif seedRank > 0 and seedRank < 5:
                newteam = Teams(id=None, TName = TName, School = School, Score = 0, seedRank = seedRank)
                db.session.add(newteam)
                db.session.commit()
                flash('Successfully inserted data.', category = "success")
            else:
                flash('Seed teams are SEMI-FINALIST of the last match. Which means TOP 4.', category = "error")
    return render_template("at.html", user = current_user)

@views.route('/rt', methods = ['GET', 'POST'])
@login_required
def removeteams():
    if request.method == 'POST':
        id = request.form.get("id")
        exist = Teams.query.filter_by(id = id).first()
        if not exist:
            flash('The targetted team is not in the database.', category = "error")
        else:
            Teams.query.filter_by(id = id).delete()
            flash('Operation Succeeded.', category = "success")
            db.session.commit()
    return render_template("rt.html", user = current_user)

@views.route('/et', methods = ['GET', 'POST'])
@login_required
def editteams():
    if request.method == 'POST':
        id = request.form.get("id")
        TName = request.form.get("TName")
        School = request.form.get("School")
        seedRank = request.form.get("seedRank")
        Score = request.form.get("Score")
        exist = Teams.query.filter_by(id=id).first()
        if not exist:
            flash('The targetted team is not in the database.', category = "error")
        else:
            target = Teams.query.filter_by(id = id).first()
            if TName != '/':
                target.TName = TName
            if School != '/':
                target.School = School
            if seedRank != '/':
                if int(seedRank) == 0 :
                    target.seedRank = None
                elif int(seedRank) > 0 and int(seedRank) < 5:
                    target.seedRank = int(seedRank)
                else: flash("Seed rank must be in between 0 and 5, excluding both.")
            if Score != '/':
                target.Score += int(Score)
            flash("Successfully altered the record of the team.", category = "success")
            db.session.commit()
    return render_template("et.html", user = current_user)

@views.route('/mts', methods = ['GET', 'POST'])
@login_required
def matchscore():
    if request.method == 'POST':
        id = request.form.get("id")
        T1Score = request.form.get("T1Score")
        T2Score = request.form.get("T2Score")
        exist = Match.query.filter_by(id = id).first()
        if not exist:
            flash('The match does not exist.', category = "error")
        else:
            target = Match.query.filter_by(id = id).first()
            target.T1Score = T1Score
            target.T2Score = T2Score
            flash('Successfully updated the record.', category = "success")
    return render_template("mts.html", user = current_user)