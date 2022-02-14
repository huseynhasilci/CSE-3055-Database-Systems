  
from flask import Flask,render_template,flash,request
from wtforms import Form, BooleanField, StringField, PasswordField, validators,TextField,SubmitField,SelectField
from datetime import datetime
import pyodbc 

app = Flask(__name__)
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-E0GAISA;'
                      'Database=RESTAURANT_DATABASE_SYSTEM;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
#cursor.execute('SELECT * FROM RESTAURANT_DATABASE_SYSTEM.dbo.Customers')
#cursor.execute("SELECT * FROM RESTAURANT_DATABASE_SYSTEM.dbo.Customers WHERE FirstName='Kuzey'")
#for row in cursor:
#    print(row)


"""class ReservationForm(Form):
    firstName = StringField("First Name",validators=[validators.Length(min=2,max=50),validators.required()])
    lastName = StringField("Last Name",validators=[validators.Length(min=2,max=50),validators.required()])
    phoneNumber = StringField("Phone Number",validators=[validators.required(),validators.Length(min=11,max=11)])
    email = StringField ("email",validators=[validators.Email(message="Please enter a vaild e-mail.")])
    firstDate = SelectField("firstdate",choices=[("9","09:00"),("10","10:00")])
    secondDate = SelectField("seconddate",choices=[("IX","09:00"),("X","10:00")])"""

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/similation')
def similation():
    return render_template("similation.html")

@app.route("/favorite_product")
def favoriteProduct():
    return render_template("favoriteproduct.html")

@app.route("/survey",methods=["GET","POST"])
def survey():
    
    if request.method=="POST":
        herePhoneNumber = request.form['sphonenumber']
        productRate = request.form['prate']
        waitresRate = request.form['wrate']
        placeRate = request.form['placerate']
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        if(int(productRate)>5 or int(waitresRate)>5 or int(placeRate)>5 or int(productRate)<0 or int(waitresRate)<0 or int(placeRate)<0):
            return render_template("reservation.html")

        phoneNumberTaker = cursor.execute("Select ID  From RESTAURANT_DATABASE_SYSTEM.dbo.Customers Where PhoneNumber='{}'".format(herePhoneNumber)).fetchone()
        reservationIDTaker = cursor.execute("Select ReservationID From RESTAURANT_DATABASE_SYSTEM.dbo.Reservations Where ID={}".format(phoneNumberTaker[0])).fetchone()

        cursor.execute("INSERT INTO RESTAURANT_DATABASE_SYSTEM.dbo.SatisfactionSurveys(ReservationID_,ProductSatisfaction,WaiterSatisfaction,PlaceSatisfaction,Date) VALUES('{}','{}','{}','{}','{}')".format(reservationIDTaker[0],productRate,waitresRate,placeRate,dt_string))


        conn.commit()
    return render_template("survey.html")



@app.route("/reservation",methods=["GET","POST"])
def reservation():
    #form = ReservationForm(request.form)
    if request.method=="POST":
        firstName = request.form['firstName']
        lastName = request.form['secondName']
        phoneNumber = request.form['phoneNumber']
        email = request.form['email']
        massage = request.form['massage']
        numOfPeople= request.form['numOfPeople']
        tableNum=request.form['tableNum']
        
        first = request.form['fDate'] #request.form['fDate']
        first = first.split("T") 
        varFirst = first[0] + " "+ first[1]
        second = request.form['sDate']
        second = second.split("T")
        varSecond = second[0] + " " + second[1]
        
        
        
        
        cursor.execute("INSERT INTO RESTAURANT_DATABASE_SYSTEM.dbo.Customers(Email,FirstName,LastName,PhoneNumber) VALUES('{}','{}','{}','{}')".format(email,firstName,lastName,phoneNumber))
        phoneNumberTaker = cursor.execute("Select ID  From RESTAURANT_DATABASE_SYSTEM.dbo.Customers Where PhoneNumber='{}'".format(phoneNumber)).fetchone() 
        
        cursor.execute("INSERT INTO RESTAURANT_DATABASE_SYSTEM.dbo.Reservations(TableId_,NumberofPeople,MesseagefromCustomer,Date_1,Date_2,ID) VALUES('{}','{}','{}','{}','{}','{}')".format(tableNum,numOfPeople,massage,varFirst,varSecond,phoneNumberTaker[0]))
        
        reservationIDTaker = cursor.execute("Select ReservationID From RESTAURANT_DATABASE_SYSTEM.dbo.Reservations Where ID={}".format(phoneNumberTaker[0])).fetchone()
        
        cursor.execute("INSERT INTO RESTAURANT_DATABASE_SYSTEM.dbo.ReservationCustomerRelation(ReservationID_,ID_,ConformationMail) VALUES('{}','{}','{}')".format(reservationIDTaker[0],phoneNumberTaker[0],email))
        cursor.execute("INSERT INTO RESTAURANT_DATABASE_SYSTEM.dbo.DiscountCoupons(ReservationID_,ID_,DiscountAmount) VALUES('{}','{}','{}')".format(reservationIDTaker[0],phoneNumberTaker[0],int(numOfPeople)*1.5))
 
        conn.commit()
 
    return render_template("reservation.html")

if __name__ == "__main__":
    app.run(debug=True)