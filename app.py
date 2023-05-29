#Import necessary libraries
import sqlite3 #db insert delete

from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#import base64

import smtplib #importing the module
import pandas as pd  # read excel file 
import os #read file



#data=pd.read_excel("report/s1/3_Mathemetics.xlsx")
#print(data)

#------------------------------------------------------------------------------------------------------------------------------------------------------
def send_email(reciever_email,s,temp):


    sender_add='apmaas.g1@gmail.com' #storing the sender's mail id
    receiver_add=reciever_email 
    password='kyhyvsxpclfhstoa' #storing the password to log in

     #creating the SMTP server object by giving SMPT server address and port number
    smtp_server=smtplib.SMTP("smtp.gmail.com",587)
    smtp_server.ehlo() #setting the ESMTP protocol

    smtp_server.starttls() #setting up to TLS connection
    smtp_server.ehlo() #calling the ehlo() again as encryption happens on calling startttls()

    smtp_server.login(sender_add,password) #logging into out email id

    msg_to_be_sent ="reciever_email\n"+s+" "+temp

    #sending the mail by specifying the from and to address and the message 
    smtp_server.sendmail(sender_add,receiver_add,msg_to_be_sent)
    print('Successfully the mail is sent') #priting a message on sending the mail

    smtp_server.quit()#terminating the server


grade_points = {"A+":4.0,"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"E":0.0} 
#-------------------------------------------------------------------------------------------------------------------------------------------

def get_gpa(index_no,path):
    print(path.split("/"))
    path_e = path.split("/")
    email=pd.read_excel("Emails/"+path_e[0]+"/"+path_e[1]+"/"+"emails.xlsx")
    names = os.listdir("report/"+path)
    sum_sem_point_tot = sum_sem_credit_tot = 0
    gpa = 0
    result_list = []
    for s in names: #semester
        semi = os.listdir("report/"+path+s+"/") 
        sem_credit_tot = 0
        sem_point_tot = 0
        sgpa = 0
        subject_grade_credit=[]

        for credit_no in semi:
            
            data=pd.read_excel("report/"+path+s+"/"+credit_no)
            data = data.loc[data['Unnamed: 0'] == index_no]  

            temp = str(data["Unnamed: 1"]).split()[1]
            if temp =="E(ESA)" or temp =="AB(ESA)" or temp =="E(CA)" or temp =="E(CA&ESA)" or temp =="AB(CA)&E(ESA)"  or temp =="E(CA)&AB(ESA)" or temp == "AB(CA&ESA)":
                email_user = email.loc[email['Unnamed: 0'] == index_no]
                reciever_email = str(email_user["UserPrincipalName"]).split()[1]
                print(reciever_email)
                subject_grade_credit.append((credit_no,temp,"no"))
                send_email(reciever_email=reciever_email,s=credit_no,temp=temp)
                continue
            
            unit_credit = grade_points[str(data["Unnamed: 1"]).split()[1]]*int(credit_no[0])
            sem_credit_tot = sem_credit_tot + int(credit_no[0])
            sem_point_tot = sem_point_tot + unit_credit
            #print(str(data["Unnamed: 1"]).split()[1])
            sgpa = sem_point_tot/sem_credit_tot

            subject_grade_credit.append((credit_no,temp,unit_credit)) # single semester 
        #print(s,sem_point_tot,sem_credit_tot,sgpa)
        gpa = gpa+sgpa
        
        sum_sem_point_tot = sum_sem_point_tot+sem_point_tot
        sum_sem_credit_tot = sum_sem_credit_tot + sem_credit_tot
        
        result_list.append([s,subject_grade_credit,sem_point_tot,sem_credit_tot,sgpa]) # holle  semester sgp = -1
    result_list.append(gpa/len(names))
    result_list.append(sum_sem_credit_tot)
    result_list.append(sum_sem_point_tot)
    return result_list
#------------------------------------------------------------------------------------

# Create flask instance
app = Flask(__name__)



global result_n

@app.route("/userdata")
def userdata():
    return render_template('userdata.html')



@app.route('/suggest',  methods = ['GET','POST'])
def suggest():
    next_sem_subjects = []
    next_sem_credits = 0

    def input_next_semester_subjects(next_sem_subjects,next_sem_credits,result_n):
        next_sem_subjects = next_sem_subjects
        next_sem_credits = next_sem_credits
        global suggest_r,message
        suggest_r = message = ""
        next_sem_credits_sum = next_sem_credits
        print("Sum of subject credits in the next semester:", next_sem_credits_sum)

        current_gpa = result_n[-3]

        if current_gpa >= 3.3 and current_gpa <= 3.69:
            NextSemGPA = 3.7
        elif current_gpa >= 3.0 and current_gpa <= 3.29:
            NextSemGPA = 3.3
        elif current_gpa < 3.0:
            NextSemGPA = 3.0
        else:
            NextSemGPA = 0
            print("You are already in FIrst Class Keep it up!")
            suggest_r = "A"
            message = "To Achive this GPA you need to work hard next semensters too"
        print("NextSemGPA:", NextSemGPA)

        total_sem_credit_tot = result_n[-2]
        total_sem_point_tot = result_n[-3]

        print("total_sem_credit_tot",total_sem_credit_tot)
        print("total_sem_point_tot",total_sem_point_tot)

        target_points = ((NextSemGPA * (total_sem_credit_tot + next_sem_credits_sum)) - total_sem_point_tot)/next_sem_credits_sum

        if target_points > 4.0:
            for i in range(num_subjects):
                print(next_sem_subjects[i] , "A")
            suggest_r = "A"
            message = "To Achive this GPA you need to work hard next semensters too"
            print("To Achive this GPA you need to work hard next semensters too")
        elif 4.0 >= target_points > 3.7:
            for i in range(num_subjects):

                suggest_r = "A"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "A")
        elif 3.7 >= target_points > 3.3:
            for i in range(num_subjects):
           
                suggest_r = "A-"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "A-")
        elif 3.3 >= target_points > 3.0:
            for i in range(num_subjects):
                
                suggest_r = "B+"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "B+")
        elif 3.0 >= target_points > 2.7:
            for i in range(num_subjects):
                suggest_r = "B"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "B")
        elif 2.7 >= target_points > 2.3:
            for i in range(num_subjects):
                suggest_r = "B-"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "B-")
        elif 2.3 >= target_points > 2.0:
            for i in range(num_subjects):
                suggest_r = "C+"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "C+")
        elif 2.0 >= target_points > 1.7:
            for i in range(num_subjects):
                suggest_r = "C"
                message = "To Achive this GPA you need to work hard next semensters too"
                print(next_sem_subjects[i] , "C")
        
        return next_sem_subjects, next_sem_credits, NextSemGPA, target_points,suggest_r,message

    
    s1 = request.form.get('s1')
    next_sem_subjects.append(s1)
    c1 = request.form.get('c1')
    next_sem_credits = next_sem_credits + int(c1)

    s1 = request.form.get('s2')
    next_sem_subjects.append(s1)
    c1 = request.form.get('c2')
    next_sem_credits = next_sem_credits + int(c1)

    s1 = request.form.get('s3')
    next_sem_subjects.append(s1)
    c1 = request.form.get('c3')
    next_sem_credits = next_sem_credits + int(c1)
    
    s1 = request.form.get('s4')
    next_sem_subjects.append(s1)
    c1 = request.form.get('c4')
    next_sem_credits = next_sem_credits + int(c1)

    s1 = request.form.get('s5')
    next_sem_subjects.append(s1)
    c1 = request.form.get('c5')
    next_sem_credits = next_sem_credits + int(c1)
    
    next_sem_subjects, next_sem_credits, NextSemGPA, target_points, suggest_r_v , message_n_v = input_next_semester_subjects(next_sem_subjects,next_sem_credits,result_n)
    
    print(next_sem_subjects, next_sem_credits, NextSemGPA, target_points,suggest_r_v)

 
    
    return render_template('sugestion_display.html',next_sem_subjects_v = next_sem_subjects , suggest_r = suggest_r_v , message_n = message_n_v)





#----------------------------------------------------------------------------------------------------------------------------------------------------
#database connection
    
con = sqlite3.connect("user.db")
print("database connected successfully")
global email,index #bcz home peytu again profile warakita details display ahum

email=index=""





 
#this method for login page
@app.route("/loginpage", methods = ['GET','POST'])
def loginpage():
     return render_template('Sigin_SignOut.html')

# this method for registration page
@app.route("/registerpage", methods = ['GET','POST'])
def registerpage():
     return render_template('Sigin_SignOut.html')    

#this method for landing page
@app.route("/", methods = ['GET','POST'])
def landingpage():
     return render_template('Landingpage.html')

#this method for main_Window page
@app.route("/main_Window", methods = ['GET','POST'])
def main_Window():
     return render_template('main_Window.html')


#this method for teams page
@app.route("/teams", methods = ['GET','POST'])
def teams():
     return render_template('teams.html')



#this method for profileCard page
@app.route("/profileCard", methods = ['GET','POST'])
def profileCard():
     
     cursor = con.execute("select * from user where email = '"+email+"'")
     for row in cursor:
          print(row)
          
     return render_template("profileCard.html",name=row[1],index=row[0],
                                 Department=row[4],Currentbatch=row[5],email=row[2])

#this method for aboutPage page
@app.route("/aboutPage", methods = ['GET','POST'])
def aboutPage():
     return render_template('aboutPage.html')

# this method for contact page
@app.route("/contactPage", methods = ['GET','POST'])
def contactPage():
     return render_template('contactPage.html')


# this method for semester result out page
@app.route("/Results", methods = ['GET','POST'])
def Results():
     return render_template('Results.html') 



#------------------------------------------------------------------------------------------------------------------------------------------------------

# this method for semester result page
@app.route("/semesterResults_disply1", methods = ['GET','POST'])
def semesterResults_disply1():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
   
    result = result[0]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply2", methods = ['GET','POST'])
def semesterResults_disply2():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[1])
    result = result[1]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])#class: spesific semster



@app.route("/semesterResults_disply3", methods = ['GET','POST'])
def semesterResults_disply3():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[2])
    result = result[2]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply4", methods = ['GET','POST'])
def semesterResults_disply4():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[3])
    result = result[3]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply5", methods = ['GET','POST'])
def semesterResults_disply5():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[4])
    result = result[4]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply6", methods = ['GET','POST'])
def semesterResults_disply6():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[5])
    result = result[5]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply7", methods = ['GET','POST'])
def semesterResults_disply7():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[6])
    result = result[6]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])

@app.route("/semesterResults_disply8", methods = ['GET','POST'])
def semesterResults_disply8():
    global result_n
    cursor = con.execute("select * from user where email = '"+email+"'")
    for row in cursor:
        print(row)
    result = get_gpa(index_no =index,path=row[6] + "/" + row[5] + "/" + row[4] + "/" )
    r = result
    print(result[7])
    result = result[7]
    result_n = r

    print("tot points:",result_n[-1],"total credit",result_n[-2],"GPA:",result_n[-3])
    return render_template('semesterResults_disply.html',results=result[1],Semester=result[0],
                            credit=r[-1],Class=result[-1])




















# method for get the user login details from the login form
@app.route("/login", methods = ['GET','POST'])
def login():
     count = 0
     if request.method == 'POST':
       # get the user name from login form
        global index,email
        email = request.form.get('email') # get input values from form inputs using there name attribute
        password = request.form.get('password')
        cursor = con.execute("select * from user where email = '"+email+"' and password='"+password+"'")
        for row in cursor:
          count = count + 1
        if count>0:
          cursor = con.execute("select * from user where email = '"+email+"'")
          for row in cursor:
              print(row)
              
              index=row[0]
              email=row[2]
          return render_template("profileCard.html",name=row[1],index=row[0],
                                 Department=row[4],Currentbatch=row[5],email=row[2])

        else:

          return render_template("Sigin_SignOut.html")
      

# method for get the user register details from the register form
@app.route("/register", methods = ['GET','POST'])
def register():
     count = 0
     if request.method == 'POST':
       # get the user name from login form 

        global index,email
        index = request.form.get('index') # get input values from form inputs using there name attribute
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        Department = request.form.get('Department')
        Currentbatch = request.form.get('Currentbatch')
        faculty = request.form.get('faculty')

        try: # pila wandhal fulla astop  awum
            
          con.execute("insert into user values('"+index+"','"+username+"','"+email+"','"
                      +password+"','"+Department+"','"+Currentbatch+"','"+faculty+"')")
          con.commit() # must


          cursor = con.execute("select * from user where email = '"+email+"'")
          for row in cursor:
              print(row)
          
          return render_template("profileCard.html",name=row[1],index=row[0],
                                 Department=row[4],Currentbatch=row[5],email=row[2])
        except:
          return render_template("Sigin_SignOut.html")


      
# For local system & cloud
if __name__ == "__main__":   
    app.run(threaded=False,port=7000) 
    
    
