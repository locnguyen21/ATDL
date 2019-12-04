from flask import Flask, request, jsonify, render_template, redirect,session, url_for
from user import *
from security import *
import sqlite3
from Anderson import *
import time
app = Flask(__name__)
app.secret_key = 'locnguyen'

@app.route("/logout")
def logout():
    print("kiem tra truoc" + str(session))
    if 'username' not in session:
        session.pop('otp', None)
        return "No user log in"
    #loai bo username khoi session
    session.pop('username', None)
    session.pop('otp',None)
    print("kiem tra sau" + str(session))
    return "Already logout"

@app.route("/login", methods = ['POST', 'GET'])
def login():
    #status 1 la khoa hoan toan
    #status 2 la phat time
    #status 3 la khong ton tai user
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        #check co bi lock ko, 1 la khoa, 0 la unlock
        user = User.find_by_user(username)
        # print(user.lock)
        # print(type(user.lock))
        
        if user and user.lock == 1:
            return render_template("login.html", status = 1,username = username)

        elif user and user.lock == 0:
            if user.password == password:
                session['username'] = user.username
                print("Dang nhap dung vs username: " + str(session['username']))
                return redirect(url_for('otp'))
                #sau nay phai render_temple de get so OTP

            #dang nhap sai
            else:
            #check da dang nhap bao h chua, neu chua thi bat dau
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                query = "SELECT * FROM logs WHERE username = ?"
                result = cursor.execute(query, (username,))
                row = result.fetchone()
                #da co dang nhap luu o log
                so_sai = None

                if row:
                    user = {'username': row[0], 'wnum': row[1]}
                    user['wnum'] += 1
                    so_sai = user['wnum']
                    #qua 3 lan roi khoa lai o bang users

                    if user['wnum'] == 3:
                        query = "UPDATE users SET lock = 1 WHERE username = ?"
                        cursor.execute(query, (username,))
                        query = "UPDATE logs set wrongnum = ? WHERE username = ?"
                        cursor.execute(query, (user['wnum'], user['username']))
                        connection.commit()
                        connection.close()
                        return render_template("login.html", status=1, so_sai=so_sai, username = username)

                    #chua qua 3 lan thi them 1 lan sai o cho log
                    else:
                        query = "UPDATE logs set wrongnum = ? WHERE username = ?"
                        cursor.execute(query, (user['wnum'], user['username']))
                        connection.commit()
                        connection.close()
                        return render_template("login.html", status=2, so_sai=so_sai)

                #chua dang nhap bao h
                elif row is None:
                    user = {'username': username, 'wnum': 1}
                    query = "INSERT INTO logs VALUES (?,?)"
                    cursor.execute(query, (user['username'], user['wnum']))
                    so_sai = user['wnum']
                    connection.commit()
                    connection.close()
                    return render_template("login.html", status = 2, so_sai = so_sai)

        elif user is None:
            return render_template("login.html", status = 3, username = username)

    elif (request.method == 'GET'):
        if ('username' in session):
            return "already login"
        else:
            return render_template("login.html")

@app.route("/otp", methods = ['POST', 'GET'])
def otp():
    if (request.method == 'POST'):
        if (request.form['submit'] == 'Get OTP'):
            username = session['username']
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM otp_users WHERE username = ?"
            result = cursor.execute(query, (username,))
            row = result.fetchone()

            #if exist va het han OTP
            if (row and row[3] <= int(time.time())):
                otp = random.randint(1000, 9999)
                starttime = int(time.time())
                endtime = starttime + 30
                #session['otp'] = otp
                query = "UPDATE otp_users SET OTP=?,start=?,end=? WHERE username=?"
                cursor.execute(query, (otp,starttime,endtime,username))
                connection.commit()
                connection.close()
                return render_template("otp.html", check=1, otp=otp)

            #ton tai va con han OTP
            if (row and row[3] >= int(time.time())):
                connection.commit()
                connection.close()
                timeleft = row[3] - int(time.time())
                return render_template("otp.html", check = 2, timeleft = timeleft, otp = row[1])

            elif row is None:
                otp = random.randint(1000,9999)
                starttime = int(time.time())
                endtime = starttime + 30
                #session['otp'] = otp
                user_otp = (username, otp, starttime, endtime)
                query = "INSERT INTO otp_users VALUES (?,?,?,?)"
                cursor.execute(query, user_otp)
                connection.commit()
                connection.close()
                return render_template("otp.html", check = 3, otp = otp)

        elif (request.form['submit'] == 'Submit OTP'):
            OTP = request.form['otp']
            if (OTP.isdigit() == False):
                OTP = "ma OTP la so"
                return render_template("otp.html", otp = OTP)

            if (OTP.isdigit() == True):
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                query = "SELECT * FROM otp_users WHERE username = ?"
                result = cursor.execute(query, (session['username'],))
                row = result.fetchone()
                connection.commit()
                connection.close()
                if (row[3] >= int(time.time()) and int(OTP) == row[1]):
                    session['otp'] = int(OTP)
                    print("nhap dung otp vs user:" + str(session['username']))
                    return "RIGHT OTP RIGHT TIME"

                elif (row[3] <= int(time.time())):
                    return render_template("otp.html", check=4, otp = OTP)

                elif (row[3] >= int(time.time()) and int(OTP) != row[1]):
                    OTP = "Wrong_OTP"
                    return render_template("otp.html", otp=OTP)

    elif request.method == 'GET':
        #print(session['username'])
        if ('username' not in session):
            return "Log in first"
        else:
            print("Da dang nhap va vao site otp: " + str(session['username']))
            return render_template("otp.html")

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        if (request.form['Sign up'] == 'Check password'):
            do_dai, khong_gian_do_dai, N = LengthPass(password)
            G = math.pow(10, 7)
            T = 80 * 3 * 24 * 60 * 60
            P = Anderson_formula(T,G,N)
            classpass = Class(P)
            return render_template("signup.html", do_dai = do_dai, khong_gian_do_dai = khong_gian_do_dai, classpass = classpass, check = 1
                               ,username = username, password = password)

        elif (request.form['Sign up'] == 'Sign up'):
            if (request.form['cpassword'] != password):
                return render_template("signup.html", check = 4, username = username)

            else:
                user = User.find_by_user(username)
                if user:
                    return render_template("signup.html", check = 3, username = username)

                else:
                    user = (username, password,0)
                    connection = sqlite3.connect('data.db')
                    cursor = connection.cursor()
                    query = "INSERT INTO users VALUES (NUll,?,?,?,3)"
                    cursor.execute(query, user)
                    connection.commit()
                    connection.close()

                    return render_template("signup.html", check = 2, username = username)

        elif (request.form['Sign up'] == 'Go to log in'):
            return redirect('/login')

        elif (request.form['Sign up'] == 'Salting'):
            password = request.form['password']
            salt, newpassword = Salting(password)
            return render_template("signup.html", check = 5, username = username, salt = salt
                                   ,oldpassword = password, password = newpassword)

    elif (request.method == 'GET'):
        return render_template('signup.html')

@app.route("/post", methods = ['POST', 'GET'])
def postforum():
    if (request.method == 'POST'):
        username = session['username']
        user = User.find_by_user(username)
        idrole = user.role
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()

        query = "SELECT * FROM roledetail where idrole = ?"
        result = cursor.execute(query, (idrole,))
        row = result.fetchone()
        role = row[1]
        if (role == "admin" or role == "mod"):
            tittle = request.form['tittle']
            linkpost = request.form['linkpost']

            query = "SELECT * FROM baiviet WHERE linkpost = ?"
            result = cursor.execute(query, (linkpost,))
            row = result.fetchone()
            if (row is None):
                content = request.form['content']
                comment = 'this is a comment \r\nThis is a second comment'
                print("ng dang bai tu cach la: " + str(role) + "vs ten la: " + str(username))

                post = (username, tittle,linkpost,content, comment)
                query = "INSERT INTO baiviet VALUES (NULL,?,?,?,?,?)"
                cursor.execute(query,post)
                connect.commit()
                connect.close()
                return "Create done"
            else:
                return render_template("formpost.html", check = 1, tittle = tittle, linkpost = linkpost)
        elif (role == "user"):
            return render_template("formpost.html", check = 2)

    elif (request.method == 'GET'):
        if ('username' not in session):
            return "Log in first"
        else:
            return render_template("formpost.html")

@app.route('/post/<string:linkpost>', methods = ['GET', 'POST'])
def baiviet(linkpost):
    if request.method == 'GET':
        linkpost = linkpost
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM baiviet WHERE linkpost = ?"
        result = cursor.execute(query,(linkpost,))
        row = result.fetchone()
        if row is not None:
            content = row[4]
            print(content)
            comment = row[5]
            print(type(comment))
            tittle = row[2]
            connection.commit()
            connection.close()
            return render_template("userpost.html", content = content, comment = comment, tittle = tittle)
        elif row is None:
            return "bài viết không tồn tại, hãy thử lại đường link khác"

    elif request.method == 'POST':
        username = session['username']
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM baiviet WHERE linkpost = ?"
        result = cursor.execute(query, (linkpost,))
        row = result.fetchone()
        print(row)

        if request.form['submit'] == 'Comment':
            newcomment = request.form['comment']
            print(newcomment)
            comment = row[5]
            content = row[4]
            tittle = row[2]
            newcomment = str(comment) + "\r\n" + str(username) + ": " + newcomment

            query = "UPDATE baiviet SET comment = ? WHERE linkpost = ?"
            cursor.execute(query, (newcomment,linkpost))
            connection.commit()
            connection.close()
            return render_template("userpost.html", content = content, comment = newcomment, tittle = tittle )

        if request.form['submit'] == 'Delete post':
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            #tim quyen cua tk dang login
            usersession = session['username']
            user = User.find_by_user(usersession)
            role = user.role
            query = "SELECT * FROM roledetail WHERE idrole = ?"
            result = cursor.execute(query, (role,))
            row = result.fetchone()

            #lay ten chu post
            query = "SELECT * FROM baiviet WHERE linkpost = ?"
            result1 = cursor.execute(query, (linkpost,))
            row1 = result1.fetchone()
            userpost = row1[1]

            if (row[1] == 'admin'):
                query = "DELETE FROM baiviet WHERE linkpost = ?"
                cursor.execute(query, (linkpost,))
                connection.commit()
                connection.close()
                return "Admin xóa bài thành công"

            elif (row[1] == 'mod' and userpost == session['username']):
                query = "DELETE FROM baiviet WHERE linkpost = ?"
                cursor.execute(query, (linkpost,))
                connection.commit()
                connection.close()
                return "User xóa bài thành công"

            elif (row[1] == 'mod' and userpost != session['username']):
                return "Bạn không phải chủ nhân bài viết cũng không phải admin"

            else:
                return "User chỉ được phép comment"
        if request.form['submit'] == 'Change post':
            return render_template("changepost.html", tittle = row[2], linkpost = linkpost, username = row[1], content = row[4])

@app.route('/setright', methods = ['GET', 'POST'])
def setright():
    if 'username' not in session:
        return "Chưa đăng nhập, phải đăng nhập dưới quyền admin"

    elif request.method == 'GET':
        username = session['username']
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        #kiem tra xem day co phai admin khong
        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        idrole = row[4]
        query = "SELECT * FROM roledetail WHERE idrole = ?"
        result = cursor.execute(query, (idrole,))
        row = result.fetchone()
        role = row[1]
        if (role == 'admin'):
            query = "SELECT * FROM users"
            user_list = []
            table = cursor.execute(query)
            for row in cursor.execute(query):
                if (row[1] != session['username']):
                    user_list.append(row[1])

            query = "SELECT * FROM roledetail"
            role_list = []
            for row in cursor.execute(query):
                role_list.append(row[1])
            return render_template("changeright.html", user_list= user_list, role_list = role_list)
        else:
            return "Tài khoản không phải admin để có thể truy cập trang này !"

    elif request.method == 'POST':
        username = request.form['user_select']
        print(username)
        role = request.form['right_select']
        print(role)
        # get role id
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "SELECT * FROM roledetail WHERE rolename = ?"
        result = cursor.execute(query, (role,))
        row = result.fetchone()
        id_role = row[0]
        #change role of user

        query = "UPDATE users SET role = ? WHERE username = ?"
        cursor.execute(query, (id_role,username))
        connect.commit()
        connect.close()
        return render_template("changeright.html",role = role, username = username, check = 1 )

@app.route('/changepost', methods = ['POST'])
def changepost():
    username = session['username']
    print(username)
    connect = sqlite3.connect('data.db')
    cursor = connect.cursor()
    # kiem tra xem day co phai admin khong
    query = "SELECT * FROM users WHERE username = ?"
    result = cursor.execute(query, (username,))
    row = result.fetchone()
    idrole = row[4]
    query = "SELECT * FROM roledetail WHERE idrole = ?"
    result = cursor.execute(query, (idrole,))
    row = result.fetchone()
    role = row[1]
    print("role người dùng: " + str(role))
    tittle = request.form['tittle']
    linkpost = request.form['linkpost']
    content = request.form['content']
    query = "SELECT * FROM baiviet WHERE linkpost = ?"
    result = cursor.execute(query, (linkpost,))
    row = result.fetchone()
    userpost = row[1]
    print("chủ bài viết là: " + str(userpost))
    print(tittle)

    if (role == "admin" or role == "mod"):
        if (role == "admin"):
            query = "UPDATE baiviet SET content = ? WHERE linkpost = ?"
            cursor.execute(query, (content, linkpost))
            connect.commit()
            connect.close()
            return redirect(url_for('baiviet' ,linkpost=linkpost))
        if (role == "mod"):
            if (username != userpost):
                return "Bạn không phải là chủ bài viết"
            elif (username == userpost):
                query = "UPDATE baiviet SET content = ? WHERE linkpost = ?"
                cursor.execute(query, (content, linkpost))
                connect.commit()
                connect.close()
                return redirect(url_for('baiviet', linkpost=linkpost))
    else:
        return "Bạn không phải là admin lẫn chủ bài viết"


@app.route('/paint', methods = ['POST', 'GET'])
def paint():
    return render_template("paint.html")
app.run(port=9999)