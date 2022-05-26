from flask import Flask, render_template,request,session,url_for

print('started')

app = Flask(__name__)
# app.secret_key = "very secret key"
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="N#@98wrft45",
    database="sbe2024"
)

mycursor = mydb.cursor()

@app.route('/')
def base():
   print('')
   return render_template('startPage.html')

@app.route('/homePage')
def homePage():
   return render_template('homePage.html')

@app.route('/preSignUp')
def preSignUp():
   return render_template('preSignUp.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        userEmail = request.form['email']
        password = request.form['password']
        mycursor.execute("SELECT * FROM USERS WHERE email = %s AND password = %s",(userEmail,password))
        record = mycursor.fetchone()
        
        if record:
            session['user'] = userEmail
            session['loggedIn'] = True
            return redirect(url_for('homePage'))
        else:
            print(111111)
            return render_template('login.html',msg = True)
    else:
        print(0000000)
        return render_template('login.html',msg = False)
  
@app.route('/signUp')
def signUp():
    if request.method == 'GET':
        return render_template('signUp.html')
    else:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        
        mycursor.execute("INSET INTO USERS (email,password) VALUES (%s,%s)",(email,password))
        mydb.commit()
        
        session['name'] = name
        session['email'] = email
        return redirect(url_for('base'))

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('user',None)
    session.clear()
    # return render_template('Base.html')
    return redirect(url_for('base'))



@app.route('/adddoctor',methods = ['POST','GET'])
def adddoctor():
    
    if request.method == 'POST':

        name = request.form['name1']
        ssn=request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        birth_date = request.form['birth_date']
        degree = request.form['degree']
        Specialization= request.form['specialization']
        salary = request.form['salary']
        sql = """INSERT INTO doctor (name,ssn,sex,email,password,address,birth_date,degree,specialization,salary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        val = (name,ssn,sex,email,password,address,birth_date,degree,Specialization,salary)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('homePage'))
    else:
        print('get')
        return render_template('adddoctor.html')

@app.route('/viewdoctor')
def viewdoctor():
   sql = "SELECT * FROM DOCTOR"
   mycursor.execute(sql)
   result = mycursor.fetchall()
   return render_template('viewdoctor.html',data = result)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/doctors')
def doctors():
    return render_template('doctor.html')
@app.route('/addpatient',methods = ['POST', 'GET'])
def addpatient():
    if request.method == 'POST': ##check if there is post data
        id = request.form['id']
        name = request.form['name']
        ssn = request.form['ssn']
        sex = request.form['sex']
        email = request.form['email']
        userName =  request.form['userName']
        password = request.form['password']
        address = request.form['address']
        birthDate = request.form['birthDate']
        creditCard = request.form['creditCard']
        insuranceNumber = request.form['insuranceNumber']
        maritalStatus = request.form['maritalStatus']
        job = request.form['job']
        age = request.form['Age']

        sql = """INSERT INTO Patient (id, name, ssn, sex, email, userName, password, address, birthDate, creditCard, insuranceNumber, maritalStatus, job, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        val = (id,name,ssn,sex,email,userName,password,address, birthDate, creditCard, insuranceNumber, maritalStatus, job, age)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('base.html')
    else:
        return render_template('addpatient.html')

@app.route('/viewpatient')
def viewpatient():
    mycursor.execute("SELECT * FROM Patient")
    myresult = mycursor.fetchall()
    return render_template('viewpatient.html', data=myresult)


@app.route('/contact_us')
def contact():
    return render_template('contact_us.html')


if __name__ == '__main__':
    app.run(debug = True)
