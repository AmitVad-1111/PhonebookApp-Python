import os
import sqlite3
from PyQt5.QtWidgets import QMessageBox

class sqlite3DbKlass:

    BASEPATH = os.path.abspath(os.path.dirname(__name__))

    DbFile = "db/phoneBook.db"

    def __init__(self):

        if not os.path.exists(self.DbFile):
        
            with open(os.path.join(self.BASEPATH,self.DbFile),'w') as fp:
                self.connectToDb()
                try:
                    if self.cursr:
                        
                        self.cursr.execute(""" CREATE TABLE contactBook(
                              uid integer PRIMARY KEY,
                              person_name text NOT NULL,
                              person_no text NOT NULL,
                              person_email text,
                              person_home text,
                              person_office text,
                              person_add text  
                        )""")


                except Exception as e:                
                    print(e)
            
        else:
            self.connectToDb()
            
            

    def connectToDb(self):
        self.con = sqlite3.connect(self.DbFile)    
        self.cursr = self.con.cursor()

    #====================================================================    
    def create_new_record(self,data=(),parentWidget=None):    

        if data[0] == '':
            self.showMessage(parentWidget,'Error','person name required','error')             
        elif data[1] == '':
            self.showMessage(parentWidget,'Error','person phone number required','error')
        elif self.isPhoneNo(data[1]) == False:
            self.showMessage(parentWidget,'Error','Are you kiding me? contact no must be numeric','error')
        else:
            #dbcode goes heres
            qry  = "insert into contactbook"
            qry += "(person_name,person_no,person_email,person_home,person_office,person_add)values(?,?,?,?,?,?)"            
            
            self.cursr.execute(qry,data)

            if self.cursr.lastrowid > 0:
                self.showMessage(parentWidget,'Success','New contact created successfully','info')                
            else:
                self.showMessage(parentWidget,'Error','Something goes wrong','error')   

            self.closeConn()
            return True

    #====================================================================
    def showMessage(self,pw,boxTitle,msg,msgtype):        
        if msgtype == 'qustion':
            pass
        elif msgtype == 'info':
            QMessageBox.information(pw,boxTitle,msg,QMessageBox.Ok)
        elif msgtype == 'warning':
            pass
        elif msgtype == 'error':
            QMessageBox.critical(pw,boxTitle,msg,QMessageBox.Ok)
        else:
            return True

    #====================================================================
    def isPhoneNo(self,num):
        validdata = '0123456789+-()'
        for n in num:
            if n in validdata:
                continue
            else:
                return False
        return True

    #====================================================================
    def getAllContacts(self):
        qry = "select * from contactbook"
        self.cursr.execute(qry)        
        return self.cursr.fetchall() 

    #====================================================================
    def getContactById(self,id):
        qry = "select * from contactbook where uid = %s" %(id)
        self.cursr.execute(qry)        
        r = self.cursr.fetchone() 
        if len(r) > 0:
            return r
        else:
            return -1

    #====================================================================
    def editContatcData(self,data=(),parentWidget=None):
        if data[0] == '':
            self.showMessage(parentWidget,'Error','person name required','error')             
        elif data[1] == '':
            self.showMessage(parentWidget,'Error','person phone number required','error')   
        elif self.isPhoneNo(data[1]) == False:
            self.showMessage(parentWidget,'Error','Are you kiding me? contact no must be numeric','error')
        else:
            #dbcode goes heres
            qry  = "update contactbook set "
            qry += "person_name='%s'"%data[0]
            qry += ", person_no='%s'"%data[1]
            if data[2] != '':
                qry += ", person_email='%s'"%data[2]
            if data[3]:    
                qry += ", person_home='%s'"%data[3]
            if data[4]:        
                qry += ", person_office='%s'"%data[4]
            if data[5]:                    
                qry += ", person_add='%s'"%data[5]

            qry += " where uid = %d"%data[6]
            
            self.cursr.execute(qry)

            if self.cursr.rowcount > 0:
                self.showMessage(parentWidget,'Success','Changes saved successfully','info')                
            else:
                self.showMessage(parentWidget,'Error','Something goes wrong','error')   
            self.closeConn()
            return True     

    #====================================================================
    def removeContact(self,rmvArr,parentWidget=None): 
        if len(rmvArr) == 1:
            qry = f"delete from contactbook where uid = {rmvArr[0]}"
        else:                                                 
            qry = f"delete from contactbook where uid in {tuple(rmvArr)}"      
             
        self.cursr.execute(qry)

        if self.cursr.rowcount > 0:
            self.showMessage(parentWidget,'Success',f'{len(rmvArr)} contact removed successfully','info')                
        else:
            self.showMessage(parentWidget,'Error','Something goes wrong','error') 
        self.closeConn()   

    #====================================================================
    def getSerchContact(self,srchdata):
        qry = f"select * from contactbook where person_name like '%{srchdata}%' or person_no like '%{srchdata}%' "
        self.cursr.execute(qry)        
        srchRes = self.cursr.fetchall() 
        return srchRes if len(srchRes) > 0 else False 

    #====================================================================
    def closeConn(self):
        self.con.commit()
        self.con.close()
