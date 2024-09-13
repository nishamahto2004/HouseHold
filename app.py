from flask import Flask,render_template,request,flash,redirect,url_for,session
from user import UserOperation
from provider import ProviderOperation
from encryption import Encryption
from validation import empty,checkdigit,checkalpha
from datetime import datetime
import razorpay
from voice_search import voiceSearch


app = Flask(__name__) #Flask class object
app.secret_key="sd787834uuhuif89hnfyr8nr7cwn"

client = razorpay.Client(auth=("rzp_test_ncA8cq0QRQXDlq", "oAa0hlEpbvYHrg3Of8G139kE"))


userObj = UserOperation()  # object of class of User Module
providerObj = ProviderOperation()  # object of class of Provider Module
eObj = Encryption() # object Encryption

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_signup',methods=['POST','GET'])
def user_signup():
    if request.method=='GET':
        return render_template('user_signup.html')
    else:
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['email']
        mobile=request.form['mobile']
        state=request.form['state']
        city=request.form['city']
        password=request.form['password']

        #----------- validation--------------
        dataList =[firstName,lastName,email,mobile,password]
        if(empty(dataList)):
            flash("field can't be empty!!")
            return redirect(url_for('user_signup'))
        
        if(checkdigit(mobile)):
            flash("mobile must be number!!")
            return redirect(url_for('user_signup'))
        
        if(checkalpha(firstName) or checkalpha(lastName)):
            flash("Name must be alphabate!!")
            return redirect(url_for('user_signup'))

        password=eObj.convert(password)  # encryption

        userObj.user_signup(firstName,lastName,email,mobile,state,city,password)
        flash("Successfully Registered!! Login Now!!")
        return redirect(url_for('user_login'))

@app.route('/user_login',methods=['POST','GET'])
def user_login():
    if request.method=='GET':
        return render_template('user_login.html')
    else:
        email=request.form['email']
        password=request.form['password']
        #----------- validation--------------
        dataList =[email,password]
        if(empty(dataList)):
            flash("field can't be empty!!")
            return redirect(url_for('user_login'))
        
        password=eObj.convert(password)  # encryption

        status = userObj.user_login(email,password)
        if(status==0):
            flash("invalid email and password!!")
            return redirect(url_for('user_login'))
        else:
            return redirect(url_for('user_dashboard'))

@app.route('/user_logout')
def user_logout():
    session.clear()
    flash("successfully logged out!!")
    return redirect(url_for('user_login'))

@app.route('/user_dashboard',methods=['POST','GET'])
def user_dashboard():
    if 'userEmail' in session:
        if request.method=='GET':
            return render_template('user_dashboard.html')
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))


@app.route('/user_profile',methods=['POST','GET'])
def user_profile():
    if 'userEmail' in session:
        if request.method=='GET':
            record=userObj.user_profile()
            return render_template('user_profile.html',record=record)
        else:
            firstName=request.form['firstName']
            lastName=request.form['lastName']
            mobile=request.form['mobile']
            #--------- validaion--------------
            dataList =[firstName,lastName,mobile]
            if(empty(dataList)):
                flash("field can't be empty!!")
                return redirect(url_for('user_profile'))
        
            if(checkdigit(mobile)):
                flash("mobile must be number!!")
                return redirect(url_for('user_profile'))
        
            if(checkalpha(firstName) or checkalpha(lastName)):
                flash("Name must be alphabate!!")
                return redirect(url_for('user_profile'))
            # --------end validation-------------------
            userObj.user_profile_update(firstName,lastName,mobile)
            flash("Profile updated successfully!!")
            return redirect(url_for('user_profile'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))    

@app.route('/user_delete',methods=['POST','GET'])
def user_delete():
    if 'userEmail' in session:
        if request.method=='GET':
            userObj.user_delete()
            session.clear()
            flash("Account deleted successfully!!See You Soon!!")
            return redirect(url_for('user_signup'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/user_password_change',methods=['POST','GET'])
def user_password_change():
    if 'userEmail' in session:
        if request.method=='GET':
           return render_template('user_password_change.html')
        else:
            oldPassword=request.form['oldPassword']
            newPassword=request.form['newPassword']
            #--------- validaion--------------
            dataList =[oldPassword,newPassword]
            if(empty(dataList)):
                flash("field can't be empty!!")
                return redirect(url_for('user_password_change'))
            
            if(newPassword==oldPassword): #check both are same
                flash("oldpassword and newpassword can't be same!!")
                return redirect(url_for('user_password_change'))
            
            oldPassword=eObj.convert(oldPassword)  # encryption
            newPassword=eObj.convert(newPassword)  # encryption

            status=userObj.checkPassword(oldPassword)
            if(status):
                userObj.user_password_change(newPassword)
                session.clear()
                flash("password change successfully..Login now!!")
                return redirect(url_for('user_login'))
            else:
                flash("your old password invalid.. try again!!")
                return redirect(url_for('user_password_change'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/user_service',methods=['POST','GET'])
def user_service():
    if 'userEmail' in session:
        if request.method=='GET':
            sList=userObj.user_service()
            return render_template('user_service.html',sList=sList)
        else:
            skill=request.form['skill']
            record=userObj.user_service_search(skill)
            sList=userObj.user_service()
            return render_template('user_service.html',sList=sList,record=record)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/user_service_city',methods=['POST','GET'])
def user_service_city():
    if 'userEmail' in session:
        if request.method=='GET':
            sList=userObj.user_service_city()
            return render_template('user_service_city.html',sList=sList)
        else:
            skill=request.form['skill']
            city=request.form['city']
            record=userObj.user_service_city_search(skill,city)
            sList=userObj.user_service_city()
            return render_template('user_service_city.html',sList=sList,record=record)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))
    
@app.route('/user_service_view',methods=['POST','GET'])
def user_service_view():
    if 'userEmail' in session:
        if request.method=='GET':
            providerEmail=request.args.get('providerEmail')
            record=userObj.user_service_view(providerEmail)
            getStar = userObj.user_getStar(providerEmail)
            return render_template('user_service_view.html',record=record,getStar=getStar)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/user_service_book',methods=['POST','GET'])
def user_service_book():
    if 'userEmail' in session:
        if request.method=='POST':
            providerEmail=request.args.get('providerEmail')
            charges=int(request.args.get('charges'))
            bookingDate=request.form['bookDate']
            
            data = { "amount": charges*100, "currency": "INR", "receipt": "xyz" }
            payment = client.order.create(data=data)
            pdata=[charges*100, payment["id"],providerEmail,bookingDate]
            return render_template("payment.html", pdata=pdata)

    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/success', methods=["POST"])
def success():
    if('userEmail' in session):
        if(request.method=='POST'):
            providerEmail=request.args.get('providerEmail')
            bookingDate=request.args.get('bookingDate')
            charges=request.args.get('charges')
            pid=request.form.get("razorpay_payment_id")
            ordid=request.form.get("razorpay_order_id")
            sign=request.form.get("razorpay_signature")
            params={
            'razorpay_order_id': ordid,
            'razorpay_payment_id': pid,
            'razorpay_signature': sign
            }
            final=client.utility.verify_payment_signature(params)
            if final == True:
                userObj.booking(providerEmail,pid,bookingDate,charges)
                flash("Payment Done Successfully!! payment ID is "+str(pid))
                return redirect(url_for('user_service'))
            else:
                flash("Something Went Wrong Please Try Again")
                return redirect(url_for('user_service'))
    else:
        flash("please login to access this page..")
        return redirect(url_for('user_login'))

@app.route('/user_booking_history',methods=['POST','GET'])
def user_booking_history():
    if 'userEmail' in session:
        if request.method=='GET':
            record = userObj.user_booking_history()
            return render_template('user_booking_history.html',record=record)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))

@app.route('/user_voice_search',methods=['POST','GET'])
def user_voice_search():
    if 'userEmail' in session:
        if request.method=='GET':
            skill = voiceSearch()
            record=userObj.user_service_search(skill)
            sList=userObj.user_service()
            if(record):
                return render_template('user_service.html',sList=sList,record=record)
            else:
                flash("This skill is currently not available in your city!!")
                return render_template('user_service.html',sList=sList,record=record)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))
    

@app.route('/user_review',methods=['POST','GET'])
def user_review():
    if 'userEmail' in session:
        if request.method=='GET':
            providerEmail=request.args.get('providerEmail')
            record = userObj.user_review_show(providerEmail)
            return render_template('user_review.html',providerEmail=providerEmail,record=record)
        else:
            providerEmail=request.args.get('providerEmail')
            star = request.form['star']
            comment = request.form['comment']
            userObj.user_review(providerEmail,star,comment)
            flash("review submitted successfully!!")
            return redirect(url_for('user_review',providerEmail=providerEmail))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('user_login'))










#------------------------------------------------------------
#------------------- Provider--------------------------------
#------------------------------------------------------------

@app.route('/provider_signup',methods=['POST','GET'])
def provider_signup():
    if request.method=='GET':
        return render_template('provider_signup.html')
    else:
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['email']
        mobile=request.form['mobile']
        state=request.form['state']
        city=request.form['city']
        address=request.form['address']
        skill=request.form['skill']
        exp=request.form['exp']
        charges=request.form['charges']
        password=request.form['password']
        photo = request.files['photo']

        #----------- validation--------------
        dataList =[firstName,lastName,email,mobile,address,state,city,skill,exp,charges,photo,password]
        if(empty(dataList)):
            flash("field can't be empty!!")
            return redirect(url_for('provider_signup'))
        
        if(checkdigit(mobile)):
            flash("mobile must be number!!")
            return redirect(url_for('provider_signup'))
        
        if(checkalpha(firstName) or checkalpha(lastName)):
            flash("Name must be alphabate!!")
            return redirect(url_for('provider_signup'))

        password=eObj.convert(password)  # encryption
        # ----upload photo--------------------
        p = photo.filename  # retrive photo name with extension
        d = datetime.now() #current date time (import datetime)
        t=int(round(d.timestamp()))
        path = str(t)+'.'+p.split('.')[-1]
        photo.save("static/provider/" + path)  #create provider folder inside static folder
        #---------------------------------------
        providerObj.provider_signup(firstName,lastName,email,mobile,state,city,address,skill,exp,charges,path,password)
        flash("Successfully Registered!! Login Now!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_login',methods=['POST','GET'])
def provider_login():
    if request.method=='GET':
        return render_template('provider_login.html')
    else:
        email=request.form['email']
        password=request.form['password']
        #----------- validation--------------
        dataList =[email,password]
        if(empty(dataList)):
            flash("field can't be empty!!")
            return redirect(url_for('provider_login'))
        
        password=eObj.convert(password)  # encryption

        status = providerObj.provider_login(email,password)
        if(status==0):
            flash("invalid email and password!!")
            return redirect(url_for('provider_login'))
        else:
            return redirect(url_for('provider_dashboard'))

@app.route('/provider_logout')
def provider_logout():
    session.clear()
    flash("successfully logged out!!")
    return redirect(url_for('provider_login'))

@app.route('/provider_dashboard',methods=['POST','GET'])
def provider_dashboard():
    if 'providerEmail' in session:
        if request.method=='GET':
            return render_template('provider_dashboard.html')
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_profile',methods=['POST','GET'])
def provider_profile():
    if 'providerEmail' in session:
        if request.method=='GET':
            record=providerObj.provider_profile()
            return render_template('provider_profile.html',record=record)
        else:
            firstName=request.form['firstName']
            lastName=request.form['lastName']
            mobile=request.form['mobile']
            address=request.form['address']
            skill=request.form['skill']
            exp=request.form['exp']
            charges=request.form['charges']
        
            #--------- validaion--------------
            dataList =[firstName,lastName,mobile,address,skill,exp,charges]
            if(empty(dataList)):
                flash("field can't be empty!!")
                return redirect(url_for('provider_profile'))
        
            if(checkdigit(mobile) or checkdigit(charges) or checkdigit(exp)):
                flash("must be number!!")
                return redirect(url_for('provider_profile'))
        
            if(checkalpha(firstName) or checkalpha(lastName)):
                flash("Name must be alphabate!!")
                return redirect(url_for('provider_profile'))
            # --------end validation-------------------
            providerObj.provider_profile_update(firstName,lastName,mobile,address,skill,exp,charges)
            flash("Profile updated successfully!!")
            return redirect(url_for('provider_profile'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('provider_login'))    

@app.route('/provider_delete',methods=['POST','GET'])
def provider_delete():
    if 'providerEmail' in session:
        if request.method=='GET':
            providerObj.provider_delete()
            session.clear()
            flash("Account deleted successfully!!See You Soon!!")
            return redirect(url_for('provider_signup'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_password_change',methods=['POST','GET'])
def provider_password_change():
    if 'providerEmail' in session:
        if request.method=='GET':
           return render_template('provider_password_change.html')
        else:
            oldPassword=request.form['oldPassword']
            newPassword=request.form['newPassword']
            #--------- validaion--------------
            dataList =[oldPassword,newPassword]
            if(empty(dataList)):
                flash("field can't be empty!!")
                return redirect(url_for('provider_password_change'))
            
            if(newPassword==oldPassword): #check both are same
                flash("oldpassword and newpassword can't be same!!")
                return redirect(url_for('provider_password_change'))
            
            oldPassword=eObj.convert(oldPassword)  # encryption
            newPassword=eObj.convert(newPassword)  # encryption

            status=providerObj.checkPassword(oldPassword)
            if(status):
                providerObj.provider_password_change(newPassword)
                session.clear()
                flash("password change successfully..Login now!!")
                return redirect(url_for('provider_login'))
            else:
                flash("your old password invalid.. try again!!")
                return redirect(url_for('provider_password_change'))
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('provider_login'))

@app.route('/provider_booking_info', methods=['POST','GET'])
def provider_booking_info():
    if 'providerEmail' in session:
        if request.method == 'GET':
            record=providerObj.provider_booking_info()
            return render_template('provider_booking_info.html',record=record)
    else:
        flash('to access this page please login now!!')  
        return redirect(url_for('provider_login'))



# ----------------------providerReview-------------------------------  
@app.route('/provider_review',methods=['POST','GET'])
def provider_review():
    if 'providerEmail' in session:
        if request.method=='GET':
            record = providerObj.provider_review()
            return render_template('provider_review.html',record=record)
    else:
        flash("to access this page please login now!!")
        return redirect(url_for('provider_login'))



if __name__ == '__main__':
    # app.run(debug=True)  # 127.0.0.1:5000
    app.run(host='0.0.0.0',port='5001',debug=True)  # activate server