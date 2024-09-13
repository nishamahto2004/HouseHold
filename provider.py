import mysql.connector as sql
from flask import session

class ProviderOperation:
    def connect(self):
        con = sql.connect(host='127.0.0.1',port='3307',user='root',password='root',database='b6_full_stack')
        return con
    
    def provider_signup(self,firstName,lastName,email,mobile,state,city,address,skill,exp,charges,photo,password):
        con = self.connect()
        cursor = con.cursor()
        sq = "insert into provider(firstName,lastName,email,mobile,state,city,address,skill,exp,charges,photo,password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        record=[firstName,lastName,email,mobile,state,city,address,skill,exp,charges,photo,password]

        cursor.execute(sq,record)
        con.commit() 
        con.close()

    def provider_login(self,email,password):
        con = self.connect()
        cursor = con.cursor()
        sq = "select firstName from provider where email=%s and password=%s"
        record=[email,password]
        cursor.execute(sq,record)
        row=cursor.fetchall()
        con.close()
        if(row):
            session['providerName']=row[0][0]
            session['providerEmail']=email
            return 1
        else:
            return 0
        
    def provider_profile(self):
        con = self.connect()
        cursor = con.cursor()
        sq = "select firstName,lastName,email,mobile,state,city,address,skill,exp,charges from provider where email=%s"
        record=[session['providerEmail']]
        cursor.execute(sq,record)
        row=cursor.fetchall()
        con.close()
        return row
    
    def provider_profile_update(self,firstName,lastName,mobile,address,skill,exp,charges):
        con = self.connect()
        cursor = con.cursor()
        sq = "update provider set firstName=%s,lastName=%s,mobile=%s,address=%s,skill=%s,exp=%s,charges=%s where email=%s"

        record=[firstName,lastName,mobile,address,skill,exp,charges,session['providerEmail']]

        cursor.execute(sq,record)
        con.commit() 
        con.close()
        return
    
    def provider_delete(self):
        con = self.connect()
        cursor = con.cursor()
        sq = "delete from provider where email=%s"
        record=[session['providerEmail']]
        cursor.execute(sq,record)
        con.commit() 
        con.close()
        return

    def checkPassword(self,oldPassword):
        con = self.connect()
        cursor = con.cursor()
        sq = "select * from provider where email=%s and password=%s"
        record=[session['providerEmail'],oldPassword]
        cursor.execute(sq,record)
        row=cursor.fetchall()
        con.close()
        if(row):
            return True
        else:
            return False
        
    def provider_password_change(self,newPassword):
        con = self.connect()
        cursor = con.cursor()
        sq = "update provider set password=%s where email=%s"
        record=[newPassword,session['providerEmail']]
        cursor.execute(sq,record)
        con.commit() 
        con.close()
        return
    
    def provider_booking_info(self):
        con = self.connect()
        cursor = con.cursor()
        sq="select firstName,userEmail,city,mobile,bookingDate,amount from booking b,user u where b.providerEmail=%s and b.userEmail=u.email"
        record=[session['providerEmail']]
        cursor.execute(sq,record)
        row=cursor.fetchall()
        con.close()
        return row


    def provider_review(self):
        con = self.connect()
        cursor = con.cursor()
        sq = "select u.firstName,star,comment from review r, user u where u.email=r.userEmail and providerEmail=%s"
        record=[session[providerEmail]]
        cursor.execute(sq,record)
        row=cursor.fetchall()
        con.close()
        return row    
            