import csv
import sqlite3
import bcrypt
from flask import Flask, session, redirect, render_template, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, login_manager
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.secret_key = 'qwerty'
login_manager = LoginManager()
login_manager.init_app(app)
# without setting the login_view, attempting to access @login_required endpoints will result in an error
# this way, it will redirect to the login page
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///users.sqlite'
db = SQLAlchemy(app)

from models import DBUser


class SessionUser(UserMixin):
    def __init__(self, _id, first_name, last_name, mother_name, father_name, gender, username, email, password=None):
        self.id = _id
        self.firstName = first_name
        self.lastName = last_name
        self.motherName = mother_name
        self.fatherName = father_name
        self.gender = gender
        self.username = username
        self.email = email
        self.password = password


# this is used by flask_login to get a user object for the current user
@login_manager.user_loader
def load_user(user_id):
    user = DBUser.query.filter_by(id=user_id).first()
    # user could be None
    if user:
        # if not None, hide the password by setting it to None
        user.password = None
    return SessionUser(user.id, user.firstName, user.lastName,
                       user.motherName, user.fatherName, user.gender, user.username, user.email, user.password)


def find_user(email):
    # res = db.session.execute(db.select(DBUser).filter_by(username=username)).first()
    # retrieve from database and get a list of all records
    # res = DBUser.query.all()
    # retrieve from database and get data(instance) use any condition restricted by the columns'
    # res = DBUser.query.filter(DBUser.email == email).first()
    # retrieve according column, no condition just a parameter
    res = DBUser.query.filter_by(email=email).first()
    if res:
        # user = SessionUser(res[0].username, res[0].email, res[0].phone, res[0].password)
        user = SessionUser(res.id, res.firstName, res.lastName, res.motherName, res.fatherName, res.gender,
                           res.username, res.email, res.password)
    else:
        user = None
    return user


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html", username=session.get('firstName'))


@app.route('/school')
def school():
    return render_template("school.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.email.data)
        # user could be None
        # passwords are kept in hashed form, using the bcrypt algorithm
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            # flash('Logged in successfully.')

            # check if the next page is set in the session by the @login_required decorator
            # if not set, it will default to '/'
            next_page = session.get('next', '/')
            # reset the next page to default '/'
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash(str(session))
    return redirect('/')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = RegisterForm()
    if form.validate_on_submit():
        # check first if user already exists
        user = find_user(form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            user = DBUser(firstName=form.firstName.data, lastName=form.lastName.data, motherName=form.motherName.data,
                          fatherName=form.fatherName.data, gender=form.gender.data, username=form.username.data, email=form.email.data,
                          password=password.decode())
            db.session.add(user)
            db.session.commit()
            flash('Registered successfully.')
            return redirect('/login')
        else:
            flash('This username already exists, choose another one')
    return render_template('sign_in.html', form=form)


@app.route('/info')
def info():
    return render_template("info.html")


@app.route('/careers')
def careers():
    job_list = [('High School teachers needed (2)',
                 'https://ca.indeed.com/viewjob?jk=70ef9f97fdb0fe33&q=school+teacher&l=Canada&tk=1gkk23ookgb78805&from=web&advn=9121251738005313&adid=402800040&ad=-6NYlbfkN0AOdnjUnXGrlOBnUawcODIbiRKTBobb1ZCRLsBhhutacW3Q2No_9JLgwBlNP9tYLjrZjijB5HjqwvQ9fLvDxKzAFcV8C0vAkMXzxM0cpeNVkTI0Ip_eSeqZNYpo6Q3Vu73BiNk2ew6swZKjHrSkPMvEBhazEBLtsrd0Yf__811h_RznNxWqI-Mq-Ckh-6Pq1IRFxXepTk2aBxeHWgev1IQMDnqDD-E1aL29jWZ7LrT_oszkg35Mma68Qc0GHaZSdfOvtYlFXl3F02aYLtBnLPyvd9Vkj6r6UN581QFpBAmcrlZBdpGvDhEfPQqjt0EoQkjlHiln8AV5a26TfNhJKXtBL15zq796crKJW9WAhz-YtfPxghzmNZ49v3HQ7ghFnoKwCSjTv0hwuw%3D%3D&pub=4a1b367933fd867b19b072952f68dceb&xkcb=SoDA-_M3VUMAxfQY650KbzkdCdPP&vjs=3'),
                ('High School Teacher - Instructor',
                 'https://ca.indeed.com/viewjob?cmp=HANSON-ACADEMY&t=High+School+Teacher&jk=5e803e7ed4f10f26&q=school+teacher&vjs=3'),
                ('Teacher Sem 2 PGSS French 8 Limited Duration Position',
                 'https://ca.indeed.com/viewjob?jk=c8a4bac04ecda08f&tk=1gkk2ggs2g0lp803&from=serp&vjs=3&advn=9468103412555390&adid=378959002&ad=-6NYlbfkN0ARYRJ_JTah5-2LqGj6Mekbbszl17Uu3uxFcavR2uPZsoSXLIkLFgjqqKokZtC5xBRU1Wm8PywXO_xzeBUWPePTjEJj47HP4S_1B_pkgfMoikE1wZJ_s0y0xtZzlLZxNpjTKBzFRPS3U3H2f9eKPCUTFm5EyySdCD07chgDElwDTGA6JtTiFnjGd8IpAyx3Quz_Qu53J_PN2mCvDn9aECQwuHbYhlRUdhECTNGYj-BXGCLPueAudZjRavx6QooST41ITFIzxZIe-LTO04Ft7OQ9WmyeCn1ZBQ2Yjfv5wuYMdHQ1uFfExRS4WT-3QVi3cAm8Egf48KF1oFA0BYqIoSfk93R6sWmIf8K8tDAq8aswG41LV1-48FUbbfDRewmkCHQ=&sjdu=kF8e6b8NANdjkifYjNl5rc6x01fF505av5Ws7sE4wlbG5c7tnHRm9-PqxDbhHRfOGny1Zdq-Gp0YttveXh8Dp13kV65S_Y-rDnvN5-O1s5FHYXlwhflKOlBFXOvhcWzsz1CiL0IgqwCRha0rKSxvjueg4AtIH-jSUWjZuy4yay2gVFhw3zzjBPFm5c6q4wWVSX9RiQW1RYVEqgAfKEKUO3roBnYoakNj3uyKbkIxKzGEO2UedzOeFs1KDrqTpw2ghkIAGu94WoAoYytT0UMI29LuNFTR4fhpGnJyxzrTzKZqbXNbUQuQ-or2I_4SiH_K')]
    return render_template("careers.html", job_list=job_list)


@app.route('/news')
def news():
    with open('data/news_doc.csv') as f:
        news_list = list(csv.reader(f))[1:]
    return render_template("news.html", news_list=news_list)


if __name__ == '__main__':
    app.run()
