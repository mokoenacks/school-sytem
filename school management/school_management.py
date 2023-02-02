import mysql.connector as mysql
from datetime import datetime

# use try
# security and data intergrity
#simpler methods are needed
#set up mysql
try:
    db = mysql.connect(host="localhost",user="root",password="Sandile1342#",database="school")
    command_handler=db.cursor(buffered=True)

#function



#student login
    def auth_student():
        print("Student login")
        print("")
        username=input(str("Username : "))
        password= input(str("Password : "))
        quary_vals=(username,password,"student")
        command_handler.execute("SELECT * FROM users WHERE username= %s AND password=%s AND priviledge=%s ",quary_vals)
        if command_handler.rowcount <= 0:
            print("invalid login details")
        else:
            student_console(username)
       
       

    #student UI
    def student_console(username):
        while 1:

            print("")
            print("Student menu")
            print("")
            print("1. View register ")
            print("2. Download register")
            print("3. logout")

            user_opt=input(str("Options : "))
            if user_opt=="1":
                username=(str(username),)
                command_handler.execute("SELECT username,date,status FROM attendents WHERE username= %s ",username)
                records = command_handler.fetchall()
                print("Displaying register")
                for record in records:
                    print(record)
                  
            elif user_opt=="2":
                #download register in pdf format
                print("Downloading register")
                username=(str(username),)
                command_handler.execute("SELECT username,date,status FROM attendents WHERE username= %s ",username)
                records = command_handler.fetchall()
                print("Displaying register")
                for record in records:
                    with open("C:/Users/Clement/Downloads/register.txt","w") as f:
                        f.write(str(records)+"\n")
                    f.close()
                print("All records saved")


            elif user_opt=="3":

                logout = input(str("are you sure want to log out ? \n y or n :"))

                if logout =="y":
                    print("goodbye")
                    break;
                elif logout=="n":
                    continue
                else:
                    print("invalid input")
            else:
                print("invalid option")



    #teacher login
    def auth_teacher():
        print("Teacher's login")
        print("")
        username=input(str("Username : "))
        password = input(str("Password : "))
        quary_vals=(username,password);
        command_handler.execute("SELECT * FROM users WHERE username=%s AND password= %s AND priviledge='teacher' ",quary_vals)
        if command_handler.rowcount <= 0:
             print("credentials invalid")
        
        else:
             print("Welcome "+ username)
             teacher_console()
          

     #teacher UI 
    def teacher_console():
        while 1: 
            print("") 
            print("Teacher's menu")
            print("1 .Mark student attendence")
            print("2 .update student attendence")
            print("3. view student register")
            print("4. Logout")
        
            user_opt= input(str("Option : "))
    #student Mark registry
            if user_opt=="1":
                print("")
                print("MARK STUDENT REGISTER")
                command_handler.execute("SELECT username FROM users WHERE priviledge = 'student'")
                records= command_handler.fetchall()
                date = input(str("Date : DD/MM/YYYY : "))
                #should be current dates everyday
                for record in records:
                    record=str(record).replace("'","")
                    record=str(record).replace(",","")
                    record=str(record).replace("(","")
                    record=str(record).replace(")","")
                    #present | Absent | Late
                    status = input(str("Status for "+ str(record)+ "P/A/L :"))
                    if status=="p" or status=="P":
                        status="Present"
                    elif status=="a" or status=="A":
                        status="Absent"
                    elif status=="l" or status=="L":
                        status="Late"
                    else:
                        print("invalid option")# my biggest problem
                        status = input(str("Status for "+ str(record)+ "P/A/L :"))

                    quary_vals = (str(record),date,status)
                    command_handler.execute("INSERT INTO attendents (username,date,status) VALUES (%s,%s,%s)",quary_vals)
                    db.commit()
                    print(record +"marked as "+ status)
            #adding an update section

            elif user_opt=="2":
                print("")
                print("Update student status")

                name= input(str("Enter the name of the student: "))
                dates= input(str("Enter the date DD/MM/YYYY: "))

                newStatus= input(str("Enter new status(P/A/L) :"))           
                if newStatus=="p" or newStatus=="P":
                        newStatus="Present"
                elif newStatus=="a" or newStatus=="A":
                        newStatus="Absent"
                elif newStatus=="l" or newStatus=="L":
                       newStatus="Late"
                else:
                     print("invalid option")# my biggest problem
                     newStatus = input(str("Status for "+ str(record)+ "P/A/L :"))

                quary_vals=(newStatus,name,dates)

                command_handler.execute("UPDATE attendents SET status=%s WHERE username=%s AND date=%s ",quary_vals)
                db.commit()
                print(name + " updated status is "+ newStatus)

            elif user_opt=="3":
                print("")
                print("Viewing all student registered")
                command_handler.execute("SELECT username ,date,status FROM attendents  ")
                records=command_handler.fetchall()
                print("Displaying all registers")
                for record in records:
                    print(record)
#log out
            elif user_opt=="4":
                logout = input(str("are you sure want to log out ? \n y or n :"))

                if logout =="y":
                    print("goodbye")
                    break;
                elif logout=="n":
                    continue
                else:
                    print("invalid input")
            else:
                print("invalid option")







    def admin_console():
        while 1: #admin UI
            print("")
            print("welcome Admin")
            print("")
            print("Admin menu")
            print("1 .Register new student")
            print("2. Register new teacher")
            print("3. Delete existing student")
            print("4. Delete existing teacher")
            print("5. Logout")

            user_opt = input(str("Option :"))
            #register a student
            if user_opt=="1":
                print("Register new student")
                username=input(str("Student username : "))
                password=input(str("Student password : "))
                query_vals=(username,password)
                command_handler.execute("INSERT INTO users (username,password,priviledge) VALUES (%s,%s,'student' )",query_vals)
                db.commit()
                print(username + " has been registered as a new student")
    #register a teacher
            elif user_opt=="2":

                 print("Register new teacher")
                 username=input(str("Teacher username : "))
                 password=input(str("Teacher password : "))
                 query_vals=(username,password)
                 command_handler.execute("INSERT INTO users (username,password,priviledge) VALUES (%s,%s,'teacher' )",query_vals)
                 db.commit()
                 print(username + " has been registered as a teacher")
          

    #delete student
            elif user_opt=="3":
                 print("Delete student account")
                 username=input(str("Student username : "))
                 query_vals=(username,'student')
                 command_handler.execute("DELETE FROM  users WHERE username= %s  AND priviledge = %s ",query_vals)
                 db.commit()
                 if command_handler.rowcount < 1:
                    print("user not found")
                 else:        
                    print(username + " has been deleted ")
    #delete teacher
            elif user_opt=="4":
                print("Delete teacher account")
                username=input(str("Teacher username : "))
                query_vals=(username,'teacher')
                command_handler.execute("DELETE FROM  users WHERE username= %s  AND priviledge = %s ",query_vals)
                db.commit()
                print(username + " has been deleted ")
                if command_handler.rowcount < 1:
                    print("user not found")
                else:        
                    print(username + " has been deleted ")
    #log out
            elif user_opt=="5":
                logout = input(str("are you sure want to log out ? \n y or n :"))

                if logout =="y":
                    print("goodbye")
                    break;
                elif logout=="n":
                    continue
                else:
                    print("invalid input")
            else:
                print("invalid option")






    def auth_admin():
        print("")
        print("Admin login")
        print("")
        username= input(str("Username : "))
        password= input(str("Password : "))
    
        if username== "admin":
            if password=="school":
                admin_console()
            else:
                print("incorrect password")
        else:
            print("incorrect details")

    #UI

    def main():
        while 1:
            print("welcome to the school of codes")
            print("")
            print("1. Log in as a student")
            print("2. Log in as a teacher")
            print("3. Log in as admin")
            print("4. exit ")

            user_opt=input(str("Option : "))

            if user_opt=="1":
                print("student login")
                auth_student()
            elif user_opt=="2":
                print("Teacher login")
                auth_teacher()
            elif user_opt=="3":
                print("Admin login")
                auth_admin()
            elif user_opt=="4":
                print("Exit system?")
                exit=input(str("are you sure? \n y or n :"))

                if exit=="y":
                    print("goodbye")
                    break
                else:
                    continue
            else:
                print("No valid input")

    main()

except:
    print("Failed to connect to database")
  