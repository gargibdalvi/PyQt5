from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,QVBoxLayout, QGraphicsDropShadowEffect, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from home.c2w_home import C2W_UserProfileForm 
from google.cloud import firestore
import json
from dbConfig import db

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
    
        self.outerWidgetLogin = QWidget()
        self.outerWidgetLogin.setStyleSheet("background:#f9f9fc;max-height:600px; max-width:400px; border-radius:15px; margin-left:160px")

        pixmap = QPixmap(".\\assets\\images\\logo.jpg")

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.setGeometry(0, 0, 10,10)
        self.image_label.setAlignment(Qt.AlignHCenter)
        self.image_label.setStyleSheet("margin-bottom:20px; margin-top:10px")

        shadow = QGraphicsDropShadowEffect(self.outerWidgetLogin)
        shadow.setColor(QColor(63, 63, 63, 180))
        shadow.setBlurRadius(20) # Set blur radius
        shadow.setXOffset(5) # Set horizontal offset
        shadow.setYOffset(5) # Set vertical offset
        self.outerWidgetLogin.setGraphicsEffect(shadow)

        outer_layout = QVBoxLayout(self.outerWidgetLogin)

        self.heading = QLabel("Core2web")
        self.heading.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.heading.setStyleSheet("font-size:25px; font-weight:500; margin-top:20px; height:60px; font-family:Poppins")
        self.pageHeading=QLabel("Login")
        self.pageHeading.setAlignment(Qt.AlignCenter)
        self.pageHeading.setStyleSheet("width:350px; font-size:30px; color:qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #013565, stop:1 #057be7);")
        self.userEmailLabel = QLineEdit()
        self.userEmailLabel.setPlaceholderText("Enter Mobile No")
        self.userEmailLabel.setStyleSheet("border:1px solid #918a8ae8; max-width:300px; padding-left:20px; font-size:15px; margin-top:40px")
        self.userPassLabel = QLineEdit()
        self.userPassLabel.setPlaceholderText("Enter Password")
        self.userPassLabel.setEchoMode(QLineEdit.Password)
        self.userPassLabel.setStyleSheet("border:1px solid #918a8ae8; max-width:300px; padding-left:20px; font-size:15px; margin-top:40px")
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submit)
        self.submitBtn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #013565, stop:1 #057be7);width:350px; font-size:20px; color:#ffffff; margin-top:50px")

        self.submitBtn.enterEvent = self.on_enter_btn
        self.submitBtn.leaveEvent = self.on_leave_btn

        self.inputFeildHolder = QVBoxLayout()
        self.inputFeildHolder.addWidget(self.userEmailLabel)
        self.inputFeildHolder.addWidget(self.userPassLabel)
        self.inputFeildHolder.addWidget(self.submitBtn)

        outer_layout.addWidget(self.image_label)
        outer_layout.addWidget(self.pageHeading)
        outer_layout.addLayout(self.inputFeildHolder)
        self.formLayout = QVBoxLayout()
        outer_layout.addLayout(self.formLayout)
        outer_layout.setAlignment(Qt.AlignHCenter)
        outer_layout.addStretch(1)

        self.layout.addWidget(self.outerWidgetLogin)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #013565, stop:1 #057be7); min-height:40px;")
        self.setLayout(self.layout)

    def on_enter(self, event):
        self.userForgot.setStyleSheet("color: blue; margin-bottom:20px")
    def on_leave(self,event):
        self.userForgot.setStyleSheet("color: black; margin-bottom:20px")
    def on_enter_btn(self,event):
        self.submitBtn.setStyleSheet("background: qlineargradient(x1:0, y1:0,x2:1, y2:0, stop:0 #013565, stop:1 #1ae7c3);width:350px; font-size:20px;color:#ffffff; margin-top:50px")
    def on_leave_btn(self,event):
        self.submitBtn.setStyleSheet("background: qlineargradient(x1:0, y1:0,x2:1, y2:0, stop:0 #013565, stop:1 #057be7);width:350px; font-size:20px;color:#ffffff; margin-top:50px")

    def submit(self):
        mobileNo = self.userEmailLabel.text()
        password = self.userPassLabel.text()

        if not mobileNo.isdigit() or len(mobileNo) != 10:
            QMessageBox.critical(self, "Error", "Please enter a valid 10-digit mobile number.")
            return

        user_profiles_ref = db.collection('c2w_admin')

        user_profiles = user_profiles_ref.stream()
        for user_profile in user_profiles:
            user_data = user_profile.to_dict()
            if(user_data['mobileNo']==mobileNo and user_data['password']==password):

                self.setStyleSheet("background:white")
                self.layout.removeWidget(self.outerWidgetLogin)
                self.home = C2W_UserProfileForm(self.layout, LoginWindow)
                
                break
            else:
                QMessageBox.critical(self, "Error", "Invalid Credential")