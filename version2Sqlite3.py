import sys
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt,QSize
from PyQt5  import QtCore
from dbconnSqlite import sqlite3DbKlass
from PyQt5.QtWidgets import (QMainWindow,QApplication,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,
                             QFrame,QLabel,QTableWidgetItem,QToolBar,QAction,QWidget,QVBoxLayout,QCheckBox,
                             QMessageBox,QDesktopWidget)


class phonebook(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Contact Book')
        self.display = QDesktopWidget().screenGeometry(-1)
        self.screenWidth = self.display.width()
        self.screenHeight = self.display.height()

        self.setGeometry(200,100,self.screenWidth - 400 ,self.screenHeight - 250)
        self.appIcon = 'res/icons8-contact-details-30.png'
        self.setWindowIcon(QIcon(self.appIcon))

        #store row id which user wants to edit
        self.selectedRecored = 0

        #store all row id which user wants to remove
        self.removArr = []
        
        srch_box = QFrame()
        srch_box_ly = QHBoxLayout()
        srch_box.setLayout(srch_box_ly)

        srchInputFont = QFont()
        srchInputFont.setPixelSize(12)                

        self.srchInput = QLineEdit(srch_box)
        self.srchInput.setPlaceholderText('Search cotact by Name OR Contact no')
        self.srchInput.setFont(srchInputFont)
        self.srchInput.setStyleSheet("height:26px;width:300px;font-size:18;")
        
        self.srchBtn = QPushButton(QIcon("res/icons8-search-30.png"),'Search Contact',srch_box)
        self.srchBtn.clicked.connect(self.searchInContact)
        self.srchBtn.setStyleSheet("height:26px;padding:1px 5px")

        srch_box_ly.addWidget(self.srchInput)
        srch_box_ly.addWidget(self.srchBtn)
                        
        toolbar = QToolBar('kkkk',self)
        self.addToolBar(toolbar)

        addNewAction = QAction(QIcon('res/icons8-add-user-group-man-man-40.png'),'Add New',self)
        addNewAction.triggered.connect(self.addNewActionPerform)

        editAction = QAction(QIcon('res/icons8-registration-40.png'),'Edit Contact',self)
        editAction.triggered.connect(self.editActionPerform)
        
        removeAction = QAction(QIcon('res/icons8-denied-40.png'),'Remove Contact',self)
        removeAction.triggered.connect(self.removeActionPerform)

        aboutME = QAction(QIcon('res/high_priority-48.png'),'About Phonebook',self)
        aboutME.triggered.connect(self.aboutActionPerform)

        toolbar.addAction(addNewAction)
        toolbar.addAction(editAction)
        toolbar.addAction(removeAction)
        toolbar.addAction(aboutME)
        toolbar.addWidget(srch_box)        
        toolbar.setIconSize(QSize(30,30))

        #----------------------------------------------------------------
        #self.setUpGui()
        self.createTbl()
        #----------------------------------------------------------------
       
        #self.setCentralWidget(self.mainFrame)
        self.show()

    

    #====================================================================
    def createTbl(self):
        self.tbl_box = QTableWidget(self)
        
        #set columns
        self.tbl_box.setColumnCount(7)
        
        #set rows
        self.tbl_box.setRowCount(30)
        self.tbl_box.setHorizontalHeaderLabels(['Chk','Name','Contact No','Email','Home','Office','Address'])
        self.tbl_box.verticalHeader().setVisible(False)        

        self.loadData()    

        #Table will fit the screen horizontally 
        self.tbl_box.horizontalHeader().setStretchLastSection(True)
        for i in range(7):
            self.tbl_box.horizontalHeaderItem(i).setTextAlignment(QtCore.Qt.AlignLeft)
        
        self.tbl_box.setColumnWidth(0,5)
        self.tbl_box.setColumnWidth(1,100)
        self.tbl_box.setColumnWidth(2,100)
        self.tbl_box.setColumnWidth(3,100)
        self.tbl_box.setColumnWidth(4,100)
        self.tbl_box.setColumnWidth(5,100)
        self.tbl_box.setColumnWidth(6,100)

        self.tbl_box.setMaximumHeight(600)
        self.setCentralWidget(self.tbl_box)        
    
    #====================================================================
    def loadData(self,loadD=[]):
        self.tbl_box.clearContents()        
        if len(loadD) > 0:            
            rows = loadD                      
        else:            
            db = sqlite3DbKlass()

            rows = db.getAllContacts()                         
        i = 0                    
        for row in rows:              
            chk = QTableWidgetItem()            
            chk.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable)
            chk.setCheckState(QtCore.Qt.Unchecked)            
            chk.setTextAlignment(QtCore.Qt.AlignHCenter)            
            chk.chkId = row[0]

            pname = QTableWidgetItem(row[1])
            pname.setToolTip(row[1])
            
            pcontact = QTableWidgetItem(row[2])
            
            pemail = QTableWidgetItem(row[3])
            pemail.setToolTip(row[3])
            
            phome = QTableWidgetItem(row[4])
            poffice = QTableWidgetItem(row[5])

            paddress = QTableWidgetItem(row[6])
            paddress.setToolTip(row[6])
                        
            self.tbl_box.setItem(i,0,chk)
            self.tbl_box.setItem(i,1,pname)
            self.tbl_box.setItem(i,2,pcontact)
            self.tbl_box.setItem(i,3,pemail)
            self.tbl_box.setItem(i,4,phome)
            self.tbl_box.setItem(i,5,poffice)
            self.tbl_box.setItem(i,6,paddress)
            
            i += 1
        rows = []
        #self.tbl_box.resizeColumnsToContents()
        self.tbl_box.itemClicked.connect(self.bindApply) 
                           

    #====================================================================
    def addNewActionPerform(self):
        a = addContact(self)               
    
    #====================================================================
    def editActionPerform(self):
        if self.selectedRecored == 0:
            self.showMessage(self,'Edit record','please select chk which contact you want to edit','error')
        else:
            ed = editContact(self)

    #====================================================================
    def removeActionPerform(self):
        db = sqlite3DbKlass()
        if len(self.removArr) > 0:
            response = self.showMessage(self,'Remove Contact','Are you sure to remove selected contact?','qustion')
            if response:
                db.removeContact(self.removArr,self)                
        else:
            self.showMessage(self,'Remove Contact','please select chk which contact you want to remove','error')

        self.loadData()
    #====================================================================
    def bindApply(self,chk): 
        self.selectedRecored = chk.chkId if chk.checkState() != 0 else 0

        if chk.checkState() != 0:
            if chk.chkId not in self.removArr:
                self.removArr.append(chk.chkId)
        else:
            temp = []
            for r in self.removArr:
                if r != chk.chkId:
                    temp.append(r)
            self.removArr = None
            self.removArr = temp
            del temp
                

    #====================================================================
    def searchInContact(self):
        srchdata = self.srchInput.text()        
        if len(srchdata) > 3:
            db = sqlite3DbKlass()
            d = db.getSerchContact(srchdata)
            if d != False:                
                self.loadData(d)            
                self.srchInput.clear()
            else:
                self.showMessage(self,'Search Contact','Recored not found','error')
        else:
            self.loadData()

    #====================================================================
    def showMessage(self,pw,boxTitle,msg,msgtype):                
        if msgtype == 'qustion':
            x = QMessageBox.question(pw,boxTitle,msg,QMessageBox.Yes|QMessageBox.No)
            if x == QMessageBox.Yes:
                return True
            else:
                return False
                
        elif msgtype == 'info':
            QMessageBox.information(pw,boxTitle,msg,QMessageBox.Ok)
        elif msgtype == 'warning':
            pass
        elif msgtype == 'error':
            QMessageBox.critical(pw,boxTitle,msg,QMessageBox.Ok)
        else:
            return True

    #====================================================================
    def aboutActionPerform(self):
        aboutP = aboutPhonBook(self)
        return True
#========================================================================================================
#   Add New Contact Class
#   ----------------------
#========================================================================================================

class addContact(QMainWindow):

    def __init__(self, parent, flags=Qt.WindowCloseButtonHint):
        super().__init__(parent=parent, flags=flags)
        self.setWindowTitle("Add New Contact")
        self.setGeometry(300,150,parent.screenWidth // 4,parent.screenHeight-500)        
        self.mainObj = parent
        self.setWindowIcon(QIcon(self.mainObj.appIcon))
        self.buildGui()
        self.show()
 

    def buildGui(self):

        #add contact form
        cn_frm_box_ly = QVBoxLayout()
        cn_frm_box = QFrame(self)
        cn_frm_box.setLayout(cn_frm_box_ly)

        add_btn_group_box = QFrame(cn_frm_box)
        add_btn_group_box_ly = QHBoxLayout()
        add_btn_group_box.setLayout(add_btn_group_box_ly)

        self.cn_name = QLabel('Name',cn_frm_box)
        self.cn_name_txt = QLineEdit('',cn_frm_box)           
        self.cn_name_txt.setStyleSheet("height:25px")

        self.cn_no = QLabel('Contact no')
        self.cn_no_txt = QLineEdit('',cn_frm_box)        
        self.cn_no_txt.setStyleSheet("height:25px")

        self.cn_email = QLabel('email')
        self.cn_email_txt = QLineEdit('',cn_frm_box)
        self.cn_email_txt.setStyleSheet("height:25px")        

        self.cn_home= QLabel('Home')
        self.cn_home_txt = QLineEdit('',cn_frm_box)
        self.cn_home_txt.setStyleSheet("height:25px")

        self.cn_office = QLabel('Office')
        self.cn_office_txt = QLineEdit('',cn_frm_box)
        self.cn_office_txt.setStyleSheet("height:25px")

        self.cn_address = QLabel('address')
        self.cn_address_txt = QLineEdit('',cn_frm_box)
        self.cn_address_txt.setStyleSheet("height:25px")

        self.save_btn = QPushButton('Save',add_btn_group_box)
        self.save_btn.setStyleSheet("height:25px")

        self.save_and_exit_btn = QPushButton('Save and Exit',add_btn_group_box)
        self.save_and_exit_btn.setStyleSheet("height:25px")

        #------------------------------------------

        cn_frm_box_ly.addWidget(self.cn_name)
        cn_frm_box_ly.addWidget(self.cn_name_txt)

        
        cn_frm_box_ly.addWidget(self.cn_no)
        cn_frm_box_ly.addWidget(self.cn_no_txt)

        
        cn_frm_box_ly.addWidget(self.cn_email)
        cn_frm_box_ly.addWidget(self.cn_email_txt)

        
        cn_frm_box_ly.addWidget(self.cn_home)
        cn_frm_box_ly.addWidget(self.cn_home_txt)

        
        cn_frm_box_ly.addWidget(self.cn_office)
        cn_frm_box_ly.addWidget(self.cn_office_txt)

        
        cn_frm_box_ly.addWidget(self.cn_address)
        cn_frm_box_ly.addWidget(self.cn_address_txt)


        add_btn_group_box_ly.addWidget(self.save_btn)
        add_btn_group_box_ly.addWidget(self.save_and_exit_btn)
        cn_frm_box_ly.addWidget(add_btn_group_box)

        
        #------------------------------------------
        # define actions
        self.save_btn.clicked.connect(self.addRecord)    
        self.save_and_exit_btn.clicked.connect(lambda:self.addRecord(True))    

        #------------------------------------------

        self.setCentralWidget(cn_frm_box)

    #====================================================================            
    def addRecord(self,v):        
        #create data packet
        data = (
           self.cn_name_txt.text(),
           self.cn_no_txt.text(),
           self.cn_email_txt.text(),
           self.cn_home_txt.text(),
           self.cn_office_txt.text(),
           self.cn_address_txt.text()
        )

        db = sqlite3DbKlass()
        if db.create_new_record(data, self):
           self.cn_name_txt.setText('')
           self.cn_no_txt.setText('')
           self.cn_email_txt.setText('')
           self.cn_home_txt.setText('')
           self.cn_office_txt.setText('')
           self.cn_address_txt.setText('')           
           self.mainObj.loadData()
        if v:
            self.close()


#========================================================================================================
#   Edit Contact Class
#   ----------------------
#========================================================================================================

class editContact(QMainWindow):

    def __init__(self, parent, flags=Qt.WindowCloseButtonHint):
        super().__init__(parent=parent, flags=flags)
        self.setWindowTitle("Edit Contact")
        self.setGeometry(300,150,parent.screenWidth // 4,parent.screenHeight-500)        
        self.mainObj = parent
        self.setWindowIcon(QIcon(self.mainObj.appIcon))        
        
        self.buildGui()
        self.setDataIntoForm()
        self.show()

    def buildGui(self):
        cn_frm_box_ly = QVBoxLayout()
        cn_frm_box = QFrame(self)
        cn_frm_box.setLayout(cn_frm_box_ly)

        self.cn_name = QLabel('Name',cn_frm_box)
        self.cn_name_txt = QLineEdit('',cn_frm_box)           
        self.cn_name_txt.setStyleSheet("height:25px")

        self.cn_no = QLabel('Contact no')
        self.cn_no_txt = QLineEdit('',cn_frm_box)        
        self.cn_no_txt.setStyleSheet("height:25px")

        self.cn_email = QLabel('email')
        self.cn_email_txt = QLineEdit('',cn_frm_box)
        self.cn_email_txt.setStyleSheet("height:25px")        

        self.cn_home= QLabel('Home')
        self.cn_home_txt = QLineEdit('',cn_frm_box)
        self.cn_home_txt.setStyleSheet("height:25px")

        self.cn_office = QLabel('Office')
        self.cn_office_txt = QLineEdit('',cn_frm_box)
        self.cn_office_txt.setStyleSheet("height:25px")

        self.cn_address = QLabel('address')
        self.cn_address_txt = QLineEdit('',cn_frm_box)
        self.cn_address_txt.setStyleSheet("height:25px")
        
        self.save_changes_btn = QPushButton('Save Changes',cn_frm_box)
        self.save_changes_btn.setStyleSheet("height:25px")

        #------------------------------------------

        cn_frm_box_ly.addWidget(self.cn_name)
        cn_frm_box_ly.addWidget(self.cn_name_txt)

        
        cn_frm_box_ly.addWidget(self.cn_no)
        cn_frm_box_ly.addWidget(self.cn_no_txt)

        
        cn_frm_box_ly.addWidget(self.cn_email)
        cn_frm_box_ly.addWidget(self.cn_email_txt)

        
        cn_frm_box_ly.addWidget(self.cn_home)
        cn_frm_box_ly.addWidget(self.cn_home_txt)

        
        cn_frm_box_ly.addWidget(self.cn_office)
        cn_frm_box_ly.addWidget(self.cn_office_txt)

        
        cn_frm_box_ly.addWidget(self.cn_address)
        cn_frm_box_ly.addWidget(self.cn_address_txt)


        cn_frm_box_ly.addWidget(self.save_changes_btn)

        
        #------------------------------------------
        # define actions
        self.save_changes_btn.clicked.connect(self.editContacts)            

        #------------------------------------------
        self.setCentralWidget(cn_frm_box)

    #----------------------------------------------------------------------
    def setDataIntoForm(self):
        db = sqlite3DbKlass()
        row = db.getContactById(self.mainObj.selectedRecored)
        self.cn_name_txt.setText(row[1])
        self.cn_no_txt.setText(row[2])
        self.cn_email_txt.setText(row[3])
        self.cn_home_txt.setText(row[4])
        self.cn_office_txt.setText(row[5])
        self.cn_address_txt.setText(row[6])
        db.closeConn()
        
    #----------------------------------------------------------------------
    def editContacts(self):
        data = (
           self.cn_name_txt.text(),
           self.cn_no_txt.text(),
           self.cn_email_txt.text(),
           self.cn_home_txt.text(),
           self.cn_office_txt.text(),
           self.cn_address_txt.text(),
           self.mainObj.selectedRecored  
        )

        db = sqlite3DbKlass()
        if db.editContatcData(data, self):
           self.cn_name_txt.setText('')
           self.cn_no_txt.setText('')
           self.cn_email_txt.setText('')
           self.cn_home_txt.setText('')
           self.cn_office_txt.setText('')
           self.cn_address_txt.setText('')                      
           self.mainObj.loadData()
           self.close()
        
    #----------------------------------------------------------------------
    def winCloseAction(self):
        print('edit cotact close')

#========================================================================================================
#   About PhoneBook
#   ----------------------
#========================================================================================================
class aboutPhonBook(QMainWindow):

    def __init__(self, parent, flags=Qt.WindowCloseButtonHint):
        super().__init__(parent=parent, flags=flags)
        self.setWindowTitle("About PhoneBook")
        self.setGeometry(300,150,parent.screenWidth // 2,parent.screenHeight-500)        
        self.mainObj = parent
        self.setWindowIcon(QIcon(self.mainObj.appIcon)) 
        self.buildGui()        
        self.show()

    def buildGui(self):
        self.aboutInforBox = QFrame(self)
        self.aboutInforBox_ly = QVBoxLayout()
        self.aboutInforBox.setLayout(self.aboutInforBox_ly)

        lfont = QFont()
        lfont.setPixelSize(20)
        lfont.setBold(True)
        infoTxtFont = QFont()
        infoTxtFont.setPixelSize(14)        

        self.aboutTitle = QLabel("About PhoneBook-V1.0",self.aboutInforBox)        
        self.aboutTitle.setFont(lfont)

        btxt = "A PhoneBook App is desing and developed by Amit Vadgama. This app is general perpose app.\n"
        btxt += "With the help of this app you can add,edit,remove and serach contacts."
        self.aboutBody = QLabel(btxt,self.aboutInforBox)
        self.aboutBody.setFont(infoTxtFont)

        self.aboutInforBox_ly.addWidget(self.aboutTitle)
        self.aboutInforBox_ly.addWidget(self.aboutBody)
        self.aboutInforBox_ly.setAlignment(Qt.AlignTop)
        
        self.setCentralWidget(self.aboutInforBox)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = phonebook()    
    sys.exit(app.exec_())
