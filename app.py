from distutils.errors import DistutilsByteCompileError
import email
from email.mime import image
from fileinput import filename
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import re
from flask_mail import Mail, Message
from datetime import date, timedelta
from flask_paginate import Pagination, get_page_parameter
import os

from werkzeug.utils import secure_filename
import urllib.request

from platformdirs import user_runtime_path

app = Flask(__name__)
app.secret_key = 'myapp'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sanskar'
app.config['MYSQL_DB'] = 'flask'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'palakpadalia15@gmail.com'
app.config['MAIL_PASSWORD'] = 'knymskrsuqdnnsqp'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.permanent_session_lifetime = timedelta(minutes=1000)

mysql = MySQL(app)
mail = Mail(app)


@app.route("/")
def home():
    if 'loggedin' in session:
        return render_template('admindashboard.html')

    elif 'userloggedin' in session:
        return render_template('userhome.html')

    else:
        return render_template("home.html")

#==================================================ADMIN LOGIN==================================================#


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            error = 'Please Fill the details'
            return render_template('login.html', error=error)

        elif not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9][email protected][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            email = "Please enter valid email address"
            return render_template('login.html', email=email)

        elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
            password = "Please enter password in valid format"
            return render_template('login.html', password=password)

        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM admin WHERE email = % s AND password = md5(% s)', (email, password, ))
            admin = cursor.fetchone()

            if admin:
                session['loggedin'] = True
                session['id'] = admin['id']
                session['email'] = admin['email']
                flash('You were successfully logged in !')
                return render_template('admindashboard.html')

            else:
                flash('Incorrect username / password !')
                return render_template('login.html')

    return render_template('login.html')


#==================================================SHOW ADMINS==================================================#


@app.route('/showadmins', methods=['GET', 'POST'])
def showadmins():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admin")  # Execute the SQL
        list_users = cursor.fetchall()
        return render_template('show_admin.html', users=list_users)

    else:
        return redirect('/login')

    redirect_url = request.referrer(-2)


#==================================================ADMIN_INSERT==================================================#


@app.route('/admin_insert', methods=['GET', 'POST'])
def admin_insert():
    if request.method == "POST":
        details = request.form
        email = details['email']
        password = details['password']

        if not email or not password:
            error = 'Please Fill the details'
            return render_template('add_admin.html', error=error)

        elif not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9][email protected][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            email = "Please enter valid email address"
            return render_template('add_admin.html', email=email)

        elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
            password = "Please enter password in valid format"
            return render_template('add_admin.html', password=password)

        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO admin(email, password) VALUES (%s, md5(%s))", (email, password))
            mysql.connection.commit()
            cursor.execute("SELECT * FROM admin")  # Execute the SQL
            list_users = cursor.fetchall()
            flash('Inserted Successfully ..')
            return render_template('login.html', users=list_users)
    return render_template('add_admin.html')


#==================================================ADMIN_EDIT==================================================#


@app.route('/editadmin/<id>', methods=['GET', 'POST'])
def editadmin(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE id= %s', [id])
        data = cursor.fetchall()

        print(data[0])
        return render_template("edit_admin.html", row=data[0])
    else:
        return redirect('/login')


@app.route('/updateadmin/<id>', methods=['GET', 'POST'])
def updateadmin(id):
    if 'loggedin' in session:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE id= %s', [id])
        data = cursor.fetchall()
        print(data[0])

        if not email or not password:
            error = 'Please Fill the details'
            return render_template('edit_admin.html', error=error, row=data[0])

        elif not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9][email protected][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
            email = "Please enter valid email address"
            return render_template('edit_admin.html', email=email, row=data[0])

        elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
            password = "Please enter password in valid format"
            return render_template('edit_admin.html', password=password, row=data[0])

        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'UPDATE admin SET email=%s,password=md5(%s) WHERE id = %s', (email, password, id))
            cursor.connection.commit()
            cursor.execute("SELECT * FROM admin")  # Execute the SQL
            list_users = cursor.fetchall()
            flash('The record is successfully updated !')
            return render_template('show_admin.html', users=list_users)
    else:
        return redirect('/login')


#==================================================ADMIN LOGOUT==================================================#


@app.route('/logout')
def logout():
    session.clear()
    # session.pop('loggedin', None)
    # session.pop('email', None)
    # session.pop('password', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


#==================================================SHOW USERS==================================================#


@app.route('/showusers', methods=['GET', 'POST'])
def showusers():
    if 'loggedin' in session:

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")  # Execute the SQL
        list_users = cursor.fetchall()

        return render_template('index.html', users=list_users,)

    else:
        return redirect('/login')


#==================================================USER_INSERT==================================================#


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if 'loggedin' in session:
        if request.method == "POST":
            details = request.form
            email = details['email']
            user_name = details['user_name']
            password = details['password']

            if not email or not user_name or not password:
                error = 'Please Fill the details'
                return render_template('insert.html', error=error)

            elif not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9][email protected][A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
                email = "Please enter valid email address"
                return render_template('insert.html', email=email)

            elif not re.match('[A-Za-z]+', user_name):
                user_name = "Please enter username"
                return render_template('insert.html', user_name=user_name)

            elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
                password = "Please enter password in valid format"
                return render_template('insert.html', password=password)

            else:
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "INSERT INTO users(email, user_name, password) VALUES (%s, %s, md5(%s))", (email, user_name, password))
                mysql.connection.commit()
                msg = Message(
                    'Hello ! ' + user_name +
                    'This is your username and password. You can login by this username and password.',
                    sender='palakpadalia15@gmail.com',
                    recipients=[email]
                )
                msg.body = "UserName:-" + user_name + '\n' "Password:-" + password
                # + user_name + '\n' "Password:-" + Password + '\n'
                mail.send(msg)
                cursor.execute("SELECT * FROM users")  # Execute the SQL
                list_users = cursor.fetchall()
                flash('Inserted Successfully ..')

                return render_template('index.html', users=list_users)

    else:
        return redirect('/login')

    return render_template('insert.html')


#==================================================ADMIN_DELETE==================================================#


@app.route('/admindelete/<string:id>', methods=['GET', 'POST'])
def admindelete(id):
    if 'loggedin' in session:
        flash("Record Has Been Deleted Successfully")
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM admin WHERE id=%s", (id,))
        mysql.connection.commit()
        cursor.execute("SELECT * FROM admin")  # Execute the SQL
        list_users = cursor.fetchall()
        return render_template('show_admin.html', users=list_users)
    else:
        return redirect('/login')


#==================================================USER_DELETE==================================================#


@app.route('/delete/<string:user_id>', methods=['GET', 'POST'])
def delete(user_id):

    if 'loggedin' in session:

        flash("Record Has Been Deleted Successfully")
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id= %s', [user_id, ])
        data = cursor.fetchall()

        print(data[0])

        # email = request.form['email']

        # msg = Message(
        #     'Hello ! You account is no longer available on our site !',
        #     sender='palakpadalia15@gmail.com',
        #     recipients=[email]
        # )

        # msg.body = "Thank You."
        # # + user_name + '\n' "Password:-" + Password + '\n'
        # mail.send(msg)

        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM users")  # Execute the SQL
        list_users = cursor.fetchall()
        return render_template('index.html', users=list_users)

    else:
        return redirect('/login')


#==================================================USER_UPDATE==================================================#


@app.route('/edit/<id>')
def edit(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id= %s', [id])
        data = cursor.fetchall()
        print(data[0])
        return render_template("update_user.html", row=data[0])
    else:
        return redirect('/login')


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    if 'loggedin' in session:

        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id= %s', [id, ])
        data = cursor.fetchall()
        print(data[0])

        if not password:
            error = 'Please Fill the details'
            return render_template('update_user.html', error=error, row=data[0])

        elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
            password = "Please enter password in valid format"
            return render_template('update_user.html', password=password, row=data[0])

        else:
            cursor = mysql.connection.cursor()

            cursor.execute('UPDATE users SET password=md5(%s) WHERE id = %s',
                           (password, id))
            cursor.connection.commit()

            email = request.form['email']
            msg = Message(
                'Hello ! This is your new password. Now you can login by this passowrd.',
                sender='palakpadalia15@gmail.com',
                recipients=[email]
            )
            msg.body = "New Password:-" + password
            # + user_name + '\n' "Password:-" + Password + '\n'
            mail.send(msg)

            cursor.execute("SELECT * FROM users")
            list_users = cursor.fetchall()
            flash('The password is successfully updated !')
            return render_template('index.html', users=list_users)
    else:
        return redirect('/login')


#==================================================USER_LOGIN==================================================#


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        if not user_name or not password:
            error = 'Please Fill the details'
            return render_template('user_login.html', error=error)

        elif not re.match('[A-Za-z]+', user_name):
            user_name = "Please enter username"
            return render_template('user_login.html', user_name=user_name)

        elif not re.match('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}', password):
            password = "Please enter password in valid format"
            return render_template('user_login.html', password=password)

        else:
            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE user_name= % s AND password = md5(%s)', (user_name, password, ))
            user = cursor.fetchone()
            if user:
                session['userloggedin'] = True
                session['id'] = user['id']
                session['email'] = user['email']
                session['user_name'] = user['user_name']
                flash('You are logged in successfully !')
                return render_template('userhome.html', user_name=user_name,)
            else:
                flash('Incorrect username or password!')
                return render_template('user_login.html')

    return render_template('user_login.html')


#==================================================USER_LOGOUT==================================================#


@app.route('/userlogout')
def userlogout():
    session.pop('userloggedin', None)
    session.pop('user_name', None)
    session.pop('password', None)
    session.pop('email', None)

    return redirect(url_for('user_login'))


#==================================================ADD_PROFILE==================================================#

@app.route('/checkprofile', methods=['GET', 'POST'])
def checkprofile():
    if 'userloggedin' in session:
        user_id = session['id']
        user_name = session['user_name']
        email = session['email']
        cursor = mysql.connection.cursor()
        if cursor.execute(
                'SELECT * FROM user_profile WHERE user_id= %s', [user_id]) == 1:
            data = cursor.fetchall()
            print(data[0])
            cursor.close()
            msg = "You have already created your profile ! You can only edit or show your profile ."
            return render_template('userhome.html', row=data[0], user_name=user_name, email=email, msg=msg)

        else:
            return render_template('profile.html', user_name=user_name, email=email)


@app.route('/createprofile', methods=['GET', 'POST'])
def createprofile():
    if 'userloggedin' in session:
        user_id = session['id']
        user_name = session['user_name']
        email = session['email']

        if request.method == "POST":
            user_id = session['id']
            profile = request.form
            first_name = profile['first_name']
            last_name = profile['last_name']
            date_of_birth = profile['date_of_birth']
            dobc = request.files['dobc']
            mobile_number = profile['mobile_number']
            gender = profile['gender']
            address = profile['address']
            city = profile['city']
            state = profile['state']
            zipcode = profile['zipcode']
            file = request.files['file']

            UPLOAD_FOLDER = 'static/profilepic/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            PDF_FOLDER = 'static/birthcertificate/'
            app.config['PDF_FOLDER'] = PDF_FOLDER

            if allowed_file(file.filename):

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                dobcer = secure_filename(dobc.filename)
                dobc.save(os.path.join(app.config['PDF_FOLDER'], dobcer))

                cursor = mysql.connection.cursor()
                cursor.execute("INSERT INTO user_profile (user_id, first_name, last_name, date_of_birth, dobc, mobile_number, gender, address, city, state, zipcode, image, profile_updated_dt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, curdate())",
                               (user_id, first_name, last_name, date_of_birth, dobcer, mobile_number, gender, address, city, state, zipcode, filename))
                mysql.connection.commit()
                flash('The profile is added !')
                cursor.execute(
                    'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
                data = cursor.fetchall()

                print(data[0])
                return render_template('showprofile.html', row=data[0], user_name=user_name, email=email, filename=filename, dobcer=dobcer)

            else:
                flash('Allowed image types are -> png, jpg')
                return render_template('profile.html', user_name=user_name, email=email)

        else:
            return render_template('profile.html', user_name=user_name, email=email,)

    else:
        return render_template('user_login.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='profilepic/' + filename))


@app.route('/dob/<dobcer>')
def display_pdf(dobcer):
    return redirect(url_for('static', filename='birthcertificate/' + dobcer))


#==================================================SHOW_PROFILE==================================================#


@app.route('/showprofile')
def showprofile():

    if 'userloggedin' in session:
        user_id = session['id']
        user_name = session['user_name']
        email = session['email']

        cursor = mysql.connection.cursor()

        if cursor.execute('SELECT * FROM user_profile WHERE user_id= %s', [user_id]) == 1:

            data = cursor.fetchall()

            print(data[0])

            cursor.execute(
                'SELECT image FROM user_profile WHERE user_id= %s', [user_id])
            img = cursor.fetchone()
            filename = img.get('image')

            cursor.execute(
                'SELECT dobc FROM user_profile WHERE user_id= %s', [user_id])
            dobcer = cursor.fetchone()
            dobcer = dobcer.get('dobc')

            cursor.close()
            return render_template('showprofile.html', row=data[0], user_name=user_name, email=email, filename=filename, dobcer=dobcer)

        else:
            msg = " First of all you have to create profile so then after \n you can show or edit your profile !"
            return render_template('userhome.html', msg=msg, user_name=user_name, email=email)

    else:
        return render_template('user_login.html')


#==================================================EDIT_PROFILE==================================================#


@app.route('/editprofile')
def editprofile():

    UPLOAD_FOLDER = 'static/profilepic/'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    PDF_FOLDER = 'static/birthcertificate/'
    app.config['PDF_FOLDER'] = PDF_FOLDER

    if 'userloggedin' in session:
        user_id = session['id']
        user_name = session['user_name']
        email = session['email']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
        data = cursor.fetchall()
        print(data[0])
        return render_template('editprofile.html', row=data[0], user_name=user_name, email=email)
    else:
        return render_template('user_login.html')


@app.route('/profileupdate', methods=['GET', 'POST'])
def profileupdate():

    UPLOAD_FOLDER = 'static/profilepic/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    PDF_FOLDER = 'static/birthcertificate/'
    app.config['PDF_FOLDER'] = PDF_FOLDER

    user_id = session['id']
    user_name = session['user_name']
    email = session['email']

    if 'userloggedin' in session:
        if request.method == "POST":
            user_id = request.args.get('user_id')
            user_id = session['id']
            profile = request.form
            first_name = profile['first_name']
            last_name = profile['last_name']
            date_of_birth = profile['date_of_birth']
            dobc = request.files['dobc']
            mobile_number = profile['mobile_number']
            gender = profile['gender']
            address = profile['address']
            city = profile['city']
            state = profile['state']
            zipcode = profile['zipcode']
            file = request.files['file']

            PDF_FOLDER = 'static/birthcertificate/'
            app.config['PDF_FOLDER'] = PDF_FOLDER

            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
            data = cursor.fetchall()
            print(data[0])

            if not first_name or not last_name or not date_of_birth or not dobc or not mobile_number or not gender or not address or not city or not state or not zipcode or not file:
                error = 'Please Fill the details'
                return render_template('editprofile.html', error=error, row=data[0])

            elif not re.match('[A-Za-z]+', first_name):
                first_name = "Please enter first name"
                return render_template('editprofile.html', first_name=first_name, row=data[0])

            elif not re.match('[A-Za-z]+', last_name):
                last_name = "Please enter first name"
                return render_template('editprofile.html', last_name=last_name, row=data[0])

            elif not re.match('[0-9]{10}', mobile_number):
                mobile_number = "Please enter mobile number in the digits"
                return render_template('editprofile.html', mobile_number=mobile_number, row=data[0])

            elif not re.match('[A-Za-z]+', gender):
                gender = "Please enter your gender"
                return render_template('editprofile.html', gender=gender, row=data[0])

            elif not re.match('[a-z]', address):
                address = "Please enter your address"
                return render_template('editprofile.html', address=address, row=data[0])

            elif not re.match('[A-Za-z]+', city):
                city = "Please enter your city"
                return render_template('editprofile.html', city=city, row=data[0])

            elif not re.match('[A-Za-z]+', state):
                state = "Please enter your state"
                return render_template('editprofile.html', state=state, row=data[0])

            elif not re.match('[0-9]+', zipcode):
                zipcode = "Please enter your zipcode"
                return render_template('editprofile.html', zipcode=zipcode, row=data[0])

            else:
                if allowed_file(file.filename):

                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                if allowed_file(dobc.filename):
                    dobcer = secure_filename(dobc.filename)
                    dobc.save(os.path.join(app.config['PDF_FOLDER'], dobcer))

                    cursor = mysql.connection.cursor()
                    flash('Your profile will successfully updated !')
                    cursor.execute('UPDATE user_profile SET first_name=%s, last_name=%s, date_of_birth=%s, dobc=%s, mobile_number=%s, gender=%s, address=%s, city=%s, state=%s, zipcode=%s, image=%s, profile_updated_dt=curdate() WHERE user_id=%s',
                                   (first_name, last_name, date_of_birth, dobcer, mobile_number, gender, address, city, state, zipcode, filename, user_id))
                    cursor.connection.commit()

                    cursor.execute(
                        'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
                    data = cursor.fetchall()
                    cursor.close()
                    print(data[0])
                    return render_template('showprofile.html', row=data[0], user_name=user_name, email=email, filename=filename, dobcer=dobcer)

                else:
                    # cursor.execute(
                    #     'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
                    # data = cursor.fetchall()
                    # print(data[0])
                    flash('Allowed image types are -> png, jpg')
                    return render_template('editprofile.html', user_name=user_name, email=email)

        return render_template('showprofile.html', user_id=user_id,  user_name=user_name, email=email)
    else:
        return render_template('user_login.html')


#==================================================EDIT USER PROFILE[ADMIN SIDE]==================================================#


@app.route('/edituserprofile/<user_id>')
def edituserprofile(user_id):

    UPLOAD_FOLDER = 'static/profilepic/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    PDF_FOLDER = 'static/birthcertificate/'
    app.config['PDF_FOLDER'] = PDF_FOLDER

    cursor = mysql.connection.cursor()
    if cursor.execute('SELECT * FROM user_profile WHERE user_id= %s', [user_id]) == 1:
        data = cursor.fetchall()
        print(data[0])

        cursor.execute(
            'SELECT image FROM user_profile WHERE user_id= %s', [user_id])
        img = cursor.fetchone()
        filename = img.get('image')

        cursor.execute(
            'SELECT dobc FROM user_profile WHERE user_id= %s', [user_id])
        dobcer = cursor.fetchone()
        dobcer = dobcer.get('dobc')

        cursor.execute('SELECT user_name FROM users WHERE id= %s', [user_id])
        user_name = cursor.fetchone()
        user_name = user_name.get('user_name')

        cursor.execute('SELECT email FROM users WHERE id= %s', [user_id])
        email = cursor.fetchone()
        email = email.get('email')

        return render_template('edituserprofile.html', row=data[0], filename=filename, dobcer=dobcer, user_name=user_name, email=email)

    else:
        msg = "The profile is not created of this user"
        cursor.execute("SELECT * FROM users")  # Execute the SQL
        list_users = cursor.fetchall()
        return render_template('index.html', users=list_users, msg=msg)


@app.route('/userprofileupdate/<user_id>', methods=['GET', 'POST'])
def userprofileupdate(user_id=0):

    UPLOAD_FOLDER = 'static/profilepic/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    PDF_FOLDER = 'static/birthcertificate/'
    app.config['PDF_FOLDER'] = PDF_FOLDER

    if request.method == "POST":
        user_id = session['id']
        profile = request.form
        first_name = profile['first_name']
        last_name = profile['last_name']
        date_of_birth = profile['date_of_birth']
        mobile_number = profile['mobile_number']
        gender = profile['gender']
        address = profile['address']
        city = profile['city']
        state = profile['state']
        zipcode = profile['zipcode']

        UPLOAD_FOLDER = 'static/profilepic/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        PDF_FOLDER = 'static/birthcertificate/'
        app.config['PDF_FOLDER'] = PDF_FOLDER

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM user_profile WHERE user_id= %s', [user_id])
        data = cursor.fetchall()
        print(data[0])

        if not first_name or not last_name or not date_of_birth or not mobile_number or not gender or not address or not city or not state or not zipcode:
            error = 'Please Fill the details'
            return render_template('edituserprofile.html', error=error, row=data[0])

        elif not re.match('[A-Za-z]+', first_name):
            first_name = "Please enter first name"
            return render_template('edituserprofile.html', first_name=first_name, row=data[0])

        elif not re.match('[A-Za-z]+', last_name):
            last_name = "Please enter first name"
            return render_template('edituserprofile.html', last_name=last_name, row=data[0])

        elif not re.match('[0-9]{10}', mobile_number):
            mobile_number = "Please enter mobile number in the digits"
            return render_template('edituserprofile.html', mobile_number=mobile_number, row=data[0])

        elif not re.match('[A-Za-z]+', gender):
            gender = "Please enter your gender"
            return render_template('edituserprofile.html', gender=gender, row=data[0])

        elif not re.match('[a-z]', address):
            address = "Please enter your address"
            return render_template('edituserprofile.html', address=address, row=data[0])

        elif not re.match('[A-Za-z]+', city):
            city = "Please enter your city"
            return render_template('edituserprofile.html', city=city, row=data[0])

        elif not re.match('[A-Za-z]+', state):
            state = "Please enter your city"
            return render_template('edituserprofile.html', state=state, row=data[0])

        elif not re.match('[0-9]', zipcode):
            zipcode = "Please enter your zipcode"
            return render_template('edituserprofile.html', zipcode=zipcode, row=data[0])

        else:
            cursor = mysql.connection.cursor()
            flash('Your profile will successfully updated !')
            cursor.execute('UPDATE user_profile SET first_name=%s, last_name=%s, date_of_birth=%s, mobile_number=%s, gender=%s, address=%s, city=%s, state=%s, zipcode=%s, profile_updated_dt=curdate() WHERE user_id=%s',
                           (first_name, last_name, date_of_birth, mobile_number, gender, address, city, state, zipcode,  user_id))
            cursor.connection.commit()

            cursor.execute("SELECT * FROM users")  # Execute the SQL
            list_users = cursor.fetchall()

            cursor.execute(
                'SELECT image FROM user_profile WHERE user_id= %s', [user_id])
            img = cursor.fetchone()
            filename = img.get('image')

            cursor.execute(
                'SELECT dobc FROM user_profile WHERE user_id= %s', [user_id])
            dobcer = cursor.fetchone()
            dobcer = dobcer.get('dobc')

            return render_template('index.html', users=list_users, filename=filename, dobcer=dobcer)

    return render_template('index.html')


#==================================================RESET PASSWORD==================================================#


@app.route('/editpassowrd')
def editpassowrd():
    if 'userloggedin' in session:
        user_id = session['id']
        user_name = session['user_name']
        email = session['email']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT user_name and password FROM users WHERE id= %s', [user_id])
        data = cursor.fetchall()
        print(data[0])
        return render_template('resetpassword.html', row=data[0], user_name=user_name, email=email)
    else:
        return render_template('user_login.html')


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    user_id = session['id']
    password = request.form['password']
    # email=request.form['email']

    if 'userloggedin' in session:
        if request.method == "POST":
            user_id = session['id']
            user_name = session['user_name']
            # email = session['email']
            # email = session['email']

            cursor = mysql.connection.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE id= %s', [user_id])
            data = cursor.fetchall()
            print(data[0])
            cursor.execute('UPDATE users SET password=md5(%s) WHERE id = %s',
                           (password, user_id))
            list_users = cursor.fetchone()
            cursor.connection.commit()

            email = session['email']

            msg = Message(
                'Hello ! This is your new password.',
                sender='palakpadalia15@gmail.com',
                recipients=[email]
            )
            msg.body = "New Password:-" + password + \
                "\nNow you can login by this password. You can also login by this link \nhttp://127.0.0.1:5000/user_login"
            # + user_name + '\n' "Password:-" + Password + '\n'
            mail.send(msg)

            return render_template('userhome.html', users=list_users, user_name=user_name)
        else:
            return redirect('/userhome')
    else:
        return render_template('user_login.html')


# =================================================================================================================

if __name__ == '__main__':
    app.run(debug=True)
