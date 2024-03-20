import pymysql
import time
import os
from werkzeug.utils  import secure_filename



from flask import Flask,render_template,request,redirect,url_for,session
from mylib import check_photo,create_connection
app=Flask(__name__)

app.config["UPLOAD_FOLDER"]='./static/photos'

app.secret_key="super secret key"

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email=request.form["T1"]
        Password=request.form["T2"]
        con=pymysql.connect(host="localhost",port=3306,user="root",db="saqib",passwd="",autocommit=True)
        s1="select*from logindata where email='"+email+"' AND Password='"+Password+"'"

        cur=con.cursor()

        cur.execute(s1)
        a=cur.rowcount

        if(a==1):
            data=cur.fetchone()
            ut=data[2]
            session["email"]=email
            session["usertype"]=ut
            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif(ut=="medical"):
                return redirect(url_for("medical_home"))
            elif(ut=="hospital"):
                return redirect(url_for("hospital_home"))
            else:
                return render_template("login.html",msg="user type does not exist")
        else:
            return render_template("login.html",msg="either roll_no or password is incorrect")
    else:
        return render_template("login.html")

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="POST":
        medicine_name=request.form['T1']
        sql="select * from search_medicine where medicine_name LIKE '%"+medicine_name+"%'"
        cur=create_connection()
        cur.execute(sql)
        a=cur.rowcount
        if(a>0):
            data=cur.fetchall()
            return render_template('search.html',data=data,nm=medicine_name)
        else:
            return render_template('search.html',msg='no medicine found')
    else:
        return render_template("search.html")


@app.route("/admin_home")
def admin_home():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]

        if(ut=="admin"):
            photo=check_photo(email)
            return render_template("admin_home.html",e1=email,photo=photo)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/hospital_home")
def hospital_home():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]

        if(ut=="hospital"):
            return render_template("hospital_home.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/adminphoto",methods=["GET","POST"])
def adminphoto():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                file=request.files["F1"]
                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time())) + '.' + file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"

                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template("photoupload_admin.html",result="success")
                        else:

                            return render_template("photoupload_admin.html",result="failure")
                    except:
                        return render_template("photouload_admin.html",result="duplicate")
            else:
                return redirect(url_for("admin_home"))
        else:
             return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/change_adminphoto")
def change_adminphoto():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            photo=check_photo(email)
            cur=create_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+photo)
                return render_template("change_adminphoto.html",data="success")
            else:
                return render_template("change_adminphoto.html",data="failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_home")
def medical_home():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="medical"):
            photo=check_photo(email)
            return render_template("medical_home.html",e1=email,photo=photo)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medicalphoto",methods=["GET","POST"])
def medicalphoto():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="medical"):
            if(request.method=="POST"):
                file=request.files["F1"]

                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time())) + "." + file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"

                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save((os.path.join(app.config["UPLOAD_FOLDER"],filename)))
                            return render_template("photoupload_medical.html",result="success")
                        else:
                            return render_template("photoupload_medical.html",result="failure")
                    except:
                        return render_template("photoupload_medical.html",result="duplicate")
            else:
                return redirect(url_for("medical_home"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/change_medicalphoto",methods=["GET","POST"])
def change_medicalphoto():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="medical"):
            photo=check_photo(email)
            cur=create_connection()
            sql="delete from photodata where email='"+email+"' "
            cur=create_connection()
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/"+photo)
                return render_template("change_medicalphoto.html",data="success")
            else:
                return render_template("change_medicalphoto.html",data="failure")
        else:
            redirect(url_for("auth_error"))
    else:
        redirect(url_for("auth_error"))




@app.route("/logout")
def logout():
    if("uertype" in session):
        session.pop("usertype",None)
        session.pop("email",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("welcome"))

@app.route("/auth_error")
def auth_error():
    return render_template("auth_error.html")

@app.route("/medical_reg",methods=["GET","POST"])
def medical_reg():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":
            if(request.method=="POST"):

                    Name=request.form["T1"]
                    owner = request.form["T2"]
                    l_no= request.form["T3"]
                    address = request.form["T4"]
                    contact = request.form["T5"]
                    email = request.form["T6"]
                    Password = request.form["T7"]
                    confirm_password=request.form["T8"]
                    usertype="admin"
                    photo="no"

                    msg=""
                    if(Password!=confirm_password):
                        msg="password not match with cpassword"

                    else:
                        try:
                            sn=pymysql.Connect(host="localhost",user="root",db="saqib",password="",autocommit=True,port=3306)
                            s1="insert into medicaldata values('"+Name+"','"+owner+"','"+l_no+"','"+address+"','"+contact+"','"+email+"')"
                            s2="insert into logindata values('"+email+"','"+Password+"','"+usertype+"')"



                            cur=sn.cursor()
                            cur.execute(s1)
                            a=cur.rowcount

                            cur.execute(s2)
                            b=cur.rowcount

                            if(a==1 and b==1):
                                msg="save data and save created"
                            elif(a==1):
                                msg="only save data "
                            elif(b==1):
                                msg="only create"
                            else:
                                msg="no save data and no save create"


                        except pymysql.err.OperationalError:
                            msg='email already hai'
                        return render_template("medical_registration.html", vgt=msg)
            else:
                return render_template("medical_registration.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/hospital_reg",methods=["GET","POST"])
def hospital_reg():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":
            if(request.method=="POST"):

                    hospital_name=request.form["T1"]
                    contact = request.form["T2"]
                    address= request.form["T3"]
                    email = request.form["T4"]
                    Password = request.form["T5"]
                    confirm_password=request.form["T6"]
                    usertype="hospital"
                    photo="no"

                    msg=""
                    if(Password!=confirm_password):
                        msg="password not match with cpassword"

                    else:
                        try:
                            sn=pymysql.Connect(host="localhost",user="root",db="saqib",password="",autocommit=True,port=3306)
                            s1="insert into hospitaldata values('"+hospital_name+"','"+contact+"','"+address+"','"+email+"')"
                            s2="insert into logindata values('"+email+"','"+Password+"','"+usertype+"')"



                            cur=sn.cursor()
                            cur.execute(s1)
                            a=cur.rowcount

                            cur.execute(s2)
                            b=cur.rowcount

                            if(a==1 and b==1):
                                msg="save data and save created"
                            elif(a==1):
                                msg="only save data "
                            elif(b==1):
                                msg="only create"
                            else:
                                msg="no save data and no save create"


                        except pymysql.err.OperationalError:
                            msg='email already hai'
                        return render_template("hospital_reg.html", vgt=msg)
            else:
                return render_template("hospital_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/show_medical")
def show_medical():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            sn=pymysql.connect(host="localhost",user="root",db="saqib",port=3306,autocommit=True,password="")
            sql="select * from medicaldata"

            cur=sn.cursor()
            cur.execute(sql)
            a=cur.rowcount

            if(a>0):
                data=cur.fetchall()
                a=[]
                for d in data:
                    ee=d[5]
                    photo=check_photo(ee)
                    b=[d[0],d[1],d[2],d[3],d[4],ee,photo]
                    a.append(b)

                return render_template("show_medical.html",vgt=a)
            else:
                return render_template("show_medical.html",msg="no found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_medical1")
def show_medical1():

            sn=pymysql.connect(host="localhost",user="root",db="saqib",port=3306,autocommit=True,password="")
            sql="select * from medicaldata"

            cur=sn.cursor()
            cur.execute(sql)
            a=cur.rowcount

            if(a>0):
                data=cur.fetchall()
                a=[]
                for d in data:
                    ee=d[5]
                    photo=check_photo(ee)
                    b=[d[0],d[1],d[2],d[3],d[4],ee,photo]
                    a.append(b)

                return render_template("show_medical1.html",vgt=a)
            else:
                return render_template("show_medical1.html",msg="no found")


@app.route("/medical_photo",methods=["GET","POST"])
def medical_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            file=request.files["F1"]
            e1=request.form["H1"]
            if(file):
                path=os.path.basename(file.filename)
                file_ext=os.path.splitext(path)[1][1:]
                filename=str(int(time.time())) + "."+file_ext
                filename=secure_filename(filename)

                cur=create_connection()
                s1="insert into photodata values('"+e1+"','"+filename+"')"
                try:
                    cur.execute(s1)
                    n=cur.rowcount
                    if(n==1):
                        file.save(os.path.join("./static/photos",filename))
                        return render_template("medical_photo.html",result="success")
                    else:
                        return render_template("medical_photo.html",result="failure")
                except:
                    return render_template("medical_photo.html",result="duplicate")
            else:
                render_template("show_data.html")
        else:
            redirect(url_for("auth_error"))
    else:
        redirect(url_for("auth_error"))

@app.route("/change_medical_photo",methods=["GET","POST"])
def change_medical_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            if(request.method=="POST"):
                email=request.form["H1"]
                photo=request.form["H2"]
                cur=create_connection()
                s1="update photodata set photo='no' where email='"+email+"' "
                s2="delete from photodata where email='"+email+"'"
                cur.execute(s1)
                n=cur.rowcount

                cur.execute(s2)
                b=cur.rowcount
                if(n>0 and b>0):
                    os.remove("./static/photos/"+photo)
                    return render_template("change_medical_photo.html",result="success")
                else:
                    return render_template("change_medical_photo.html",result="failure")
            else:
                return render_template("show_data.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



@app.route("/edit_medical",methods=["GET","POST"])
def edit_medical():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":

            if(request.method=="POST"):
                email=request.form["H1"]
                sn=pymysql.connect(host="localhost",password="",port=3306,user="root",db="saqib",autocommit=True)
                con="select * from medicaldata where email='"+email+"' "

                cur=sn.cursor()
                cur.execute(con)
                b=cur.rowcount

                if(b>0):
                    data=cur.fetchone()
                    return render_template("edit_medical.html",vgt=data)
                else:
                    return render_template("edit_medical.html",msg="no data found")
            else:
                return redirect(url_for("show_data"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/edit_medical_1",methods=["GET","POST"])
def edit_medical_1():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":
            if(request.method=="POST"):
                Name = request.form["T1"]
                owner = request.form["T2"]
                l_no = request.form["T3"]
                address = request.form["T4"]
                contact = request.form["T5"]
                email=request.form["T6"]

                sn = pymysql.connect(host="localhost", password="", port=3306, user="root", db="saqib", autocommit=True)
                con="update medicaldata set Name='"+Name+"',owner='"+owner+"',l_no='"+l_no+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"
                print(con)
                cur=sn.cursor()

                cur.execute(con)
                c=cur.rowcount

                if(c>0):
                    return render_template("edit_medical_1.html",msg="data change and save")
                else:
                    return render_template("edit_medical_1.html",msg="data change are not save")
            else:
                return redirect(url_for("show_data"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medical",methods=["GET","POST"])
def delete_medical():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":
            if(request.method=="POST"):
                email=request.form["H1"]
                sn=pymysql.connect(host="localhost",password="",port=3306,user="root",db="saqib",autocommit=True)
                con="select * from medicaldata where email='"+email+"' "

                cur=sn.cursor()
                cur.execute(con)
                b=cur.rowcount

                if(b>0):
                    data=cur.fetchone()
                    return render_template("delete_medical.html",vgt=data)
                else:
                    return render_template("delete_medical.html",msg="no data found")
            else:
                return redirect(url_for("show_data"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/delete_medical_1",methods=["GET","POST"])
def delete_medical_1():
    if "usertype" in session:
        usertype=session["usertype"]
        email=session["email"]
        if usertype=="admin":
            if(request.method=="POST"):
                Name = request.form["T1"]
                owner = request.form["T2"]
                l_no = request.form["T3"]
                address = request.form["T4"]
                contact = request.form["T5"]
                email=request.form["T6"]

                sn = pymysql.connect(host="localhost", password="", port=3306, user="root", db="saqib", autocommit=True)
                con="delete from medicaldata   where email='"+email+"'"
                con2="delete from logindata where email='"+email+"'"
                print(con)
                cur=sn.cursor()

                cur.execute(con)
                c=cur.rowcount

                cur.execute(con2)
                d=cur.rowcount

                if(c>0 and d>0):
                    return render_template("delete_medical_1.html",msg="data change and save")
                else:
                    return render_template("delete_medical_1.html",msg="data change are not save")
            else:
                return redirect(url_for("show_data"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/changepass_admin", methods=["GET","POST"])
def change_password():
    if ("usertype" in session):
        ut = session["usertype"]
        E1 =session["email"]
        if (ut == "admin"):
            if (request.method == "POST"):
                old_password = request.form["T1"]
                new_password = request.form["T2"]
                confirm_password = request.form["T3"]

                msg = ""
                if (confirm_password != new_password):
                    msg = "passowrd does not match with confirm password"
                else:
                    sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root",autocommit=True)

                    sql = "update logindata set password='" + new_password + "' where email='" + E1+"' AND password='" + old_password + "' "
                    cur=sn.cursor()
                    cur.execute(sql)
                    n=cur.rowcount

                    if(n==1):
                        msg="password change"
                    else:
                        msg="Invalid password"


                    return render_template("changepass_admin.html",msg=msg)

            else:
                return render_template("changepass_admin.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/changepass_medical", methods=["GET","POST"])
def changepass_medical():
    if ("usertype" in session):
        ut = session["usertype"]
        E2 = session["email"]
        if (ut == "medical"):
            if(request.method=="POST"):
                old_password = request.form["T1"]
                new_password = request.form["T2"]
                confirm_password = request.form["T3"]

                msg = ""
                if (confirm_password != new_password):
                    msg = "passowrd does not match with confirm password"
                else:
                    sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root",autocommit=True)

                    sql = "update logindata set password='" + new_password + "' where email='"+E2+"' AND password='"+old_password+"' "

                    cur = sn.cursor()
                    cur.execute(sql)
                    n = cur.rowcount

                    if (n == 1):
                        msg = "password change"
                    else:
                        msg = "Invalid password"

                    return render_template("changepass_medical.html",msg=msg)
            else:
                 return render_template("changepass_medical.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_profile",methods=["GET","POST"])
def admin_profile():
    if ("usertype" in session):
        ut = session["usertype"]
        email = session["email"]
        if (ut == "admin"):
            if(request.method=="POST"):
                Name=request.form["T1"]
                owner=request.form["T2"]
                l_no=request.form["T3"]
                address = request.form["T4"]
                contact = request.form["T5"]
                sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root", autocommit=True)
                sql="update medicaldata set Name='"+Name+"',owner='"+owner+"',l_no='"+l_no+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"

                cur=sn.cursor()
                cur.execute(sql)
                a=cur.rowcount
                if(a>0):
                    return render_template("admin_profile.html",msg="data save")
                else:
                    return render_template("admin_profile.html",msg="not data save")
            else:
                sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root", autocommit=True)
                sql1="select * from medicaldata where email='"+email+"'"
                cur=sn.cursor()
                cur.execute(sql1)
                a=cur.rowcount
                if(a==1):
                    data=cur.fetchone()
                    return render_template("admin_profile.html",vgt=data)
                else:
                    return render_template("admin_profile.html",msg="no profile")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medical_profile",methods=["GET","POST"])
def medical_profile():
    if ("usertype" in session):
        ut = session["usertype"]
        email = session["email"]
        if (ut == "medical"):
            if(request.method=="POST"):
                Name=request.form["T1"]
                owner=request.form["T2"]
                l_no=request.form["T3"]
                address = request.form["T4"]
                contact = request.form["T5"]
                sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root", autocommit=True)
                sql="update medicaldata set Name='"+Name+"',owner='"+owner+"',l_no='"+l_no+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"

                cur=sn.cursor()
                cur.execute(sql)
                a=cur.rowcount
                if(a>0):
                    return render_template("medical_profile.html",msg="data save")
                else:
                    return render_template("medical_profile.html",msg="not data save")
            else:
                sn = pymysql.connect(host="localhost", db="saqib", port=3306, passwd="", user="root", autocommit=True)
                sql1="select * from medicaldata where email='"+email+"'"
                cur=sn.cursor()
                cur.execute(sql1)
                a=cur.rowcount
                if(a==1):
                    data=cur.fetchone()
                    return render_template("medical_profile.html",vgt=data)
                else:
                    return render_template("medical_profile.html",msg="no profile")

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/medicine_add",methods=["GET","POST"])
def medicine_add():
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method=="POST"):
                medicine_name = request.form["T2"]
                company_name = request.form["T3"]
                lno_med = request.form["T4"]
                typeof_medicine = request.form["T5"]
                price = request.form["T6"]
                sn=pymysql.connect(host="localhost",db="saqib",passwd="",port=3306,user="root",autocommit=True)
                sql="insert into medicinedata values(0,'"+medicine_name+"','"+company_name+"','"+lno_med+"','"+typeof_medicine+"','"+price+"' ,'"+e1+"')"
                cur=sn.cursor()
                cur.execute(sql)
                a=cur.rowcount
                if(a==1):
                    msg="data save"
                else:
                    msg="not data save"
                return render_template("medicine_add.html",vgt=msg)
            else:
                return render_template("medicine_add.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/show_medicine")
def show_medicine():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="medical"):
            sn = pymysql.connect(host="localhost", user="root", db="saqib", port=3306, autocommit=True, password="")
            sql = "select * from medicinedata"

            cur = sn.cursor()
            cur.execute(sql)
            a = cur.rowcount

            if (a > 0):
                data = cur.fetchall()
                return render_template("show_medicine.html", vgt=data)
            else:
                return render_template("show_medicine.html", msg="no found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine", methods=["GET","POST"])
def edit_medicine():
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method=="POST"):
                medicine_id=request.form["H1"]
                sn = pymysql.connect(host="localhost", password="", port=3306, user="root", db="saqib", autocommit=True)
                con = "select * from medicinedata where medicine_id='" + medicine_id + "' "

                cur = sn.cursor()
                cur.execute(con)
                b = cur.rowcount

                if (b > 0):
                    data = cur.fetchone()
                    return render_template("edit_medicine.html", vgt=data)
                else:
                    return render_template("edit_medicine.html", msg="no data found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/edit_medicine_1",methods=["GET","POST"])
def edit_medicine_1():
    if("usertype" in session):
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if (request.method == "POST"):
                medicine_name = request.form["T1"]
                company_name = request.form["T2"]
                lno_med = request.form["T3"]
                typeof_medicine = request.form["T4"]
                price = request.form["T5"]


                sn = pymysql.connect(host="localhost", password="", port=3306, user="root", db="saqib", autocommit=True)
                con = "update medicinedata set medicine_name='" + medicine_name + "',company_name='" + company_name + "',lno_med='" + lno_med + "',typeof_medicine='" + typeof_medicine + "',price='" + price + "' where medicine_email='" + e1 + "'"
                print(con)
                cur = sn.cursor()

                cur.execute(con)
                c = cur.rowcount

                if (c > 0):
                    return render_template("edit_medicine_1.html", msg="data change and save")
                else:
                    return render_template("edit_medicine_1.html", msg="data change are not save")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/delete_medicine",methods=["GET","POST"])
def delete_medicine():
    if('usertype' in session):
        ut=session['usertype']
        e1=session['email']
        if(ut=='medical'):
            if(request.method=="POST"):
                medicine_id=request.form["H1"]

                cn=pymysql.connect(host="localhost",db="saqib",user="root",port=3306,passwd="",autocommit=True)

                sql="select * from medicinedata where medicine_id='"+medicine_id+"'"

                cur=cn.cursor()
                cur.execute(sql)
                a=cur.rowcount
                if(a>0):
                    data=cur.fetchone()
                    return render_template("delete_medicine.html",vgt=data)
                else:
                    return render_template("delete_medicine.html",msg="No data Found")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/delete_medicine_1",methods=["GET","POST"])
def delete_medicine_1():
    if('usertype' in session):
        ut=session['usertype']
        e1=session['email']
        if(ut=='medical'):
            if(request.method=="POST"):
                medicine_id=request.form["T1"]
                medicine_name=request.form["T2"]
                company_name=request.form["T3"]
                lno_med=request.form["T4"]
                typeof_medicine=request.form["T5"]
                price=request.form["T6"]

                cn=pymysql.connect(host="localhost",user="root",port=3306,db="saqib",passwd="",autocommit=True)

                sql="delete from medicinedata where medicine_id='"+medicine_id+"'"

                cur=cn.cursor()
                cur.execute(sql)
                a=cur.rowcount
                if(a>0):
                    return render_template("delete_medicine_1.html",msg="Data changes are saved successfully")
                else:
                    return render_template("delete_medicine_1.html",msg="Data changes are not saved successfully")
            else:
                return redirect(url_for("show_medicine"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


if __name__=="__main__":
    app.run(debug=True)