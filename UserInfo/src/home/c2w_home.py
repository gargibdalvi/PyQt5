from PyQt5.QtWidgets import QLabel, QDateEdit, QLineEdit, QPushButton,QVBoxLayout, QFormLayout, QFileDialog, QRadioButton, QWidget, QMessageBox,QSplitter
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from info.c2w_Info import C2W_Info
from dbConfig import db

class C2W_UserProfileForm(QWidget):
    def __init__(self, main_widget, outerWidgetLogin):
        super().__init__()
        self.main_widget=main_widget
        self.outerWidgetLogin = outerWidgetLogin
        self.c2w_init_ui(main_widget)

    def c2w_init_ui(self, main_widget):

        header_label = QLabel('User Info Form')
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet('background-color: #003A6B; color: white;padding: 10px; font-size: 22px; max-height:40px')

        self.backbtn = QPushButton("About us")
        self.backbtn.clicked.connect(lambda : self.c2w_about_us())
        self.backbtn.setStyleSheet("background: qlineargradient(x1:0, y1:0,x2:1, y2:0, stop:0 #013565, stop:1 #057be7);max-width:100px; font-size:20px;color:#ffffff; margin-top:10px")

        self.c2w_first_name_edit = QLineEdit()
        self.c2w_last_name_edit = QLineEdit()
        self.c2w_mobile_no_edit = QLineEdit()
        self.c2w_college_name_edit = QLineEdit()
        self.c2w_date_of_birth = QDateEdit()
        self.c2w_age = QLineEdit()
        self.c2w_profile_photo_label = QLabel('No file selected')
        self.c2w_gender_radio_male = QRadioButton('Male')
        self.c2w_gender_radio_female = QRadioButton('Female')
        self.c2w_height_edit = QLineEdit()

        self.c2w_gender_radio_male.setFont(QFont('Arial', 12))
        self.c2w_gender_radio_female.setFont(QFont('Arial', 12))
        self.c2w_height_edit.setFont(QFont('Arial', 12))
        self.c2w_age.setFont(QFont('Arial', 12))

        self.c2w_date_of_birth.setDateRange(self.c2w_date_of_birth.minimumDate(),self.c2w_date_of_birth.maximumDate())
        
        self.c2w_image_label = QLabel()
        self.c2w_image_label.setAlignment(Qt.AlignCenter)
        self.c2w_image_label.setFixedSize(200, 200)
        self.c2w_image_label.hide()
    
        self.c2w_submit_button = QPushButton('Save')
        self.c2w_view_record = QPushButton("View All Records")
        
        self.c2w_output_label = QLabel()
        self.c2w_output_label.setStyleSheet('font-size: 14px; margin-top:10px;')
    
        self.c2w_age_label = QLabel('Enter Age:')

        self.c2w_age_label.setFont(QFont('Arial', 12))
        self.c2w_gender_label = QLabel('Gender:')
        self.c2w_gender_label.setFont(QFont('Arial', 12))
        self.c2w_height_label = QLabel("Height(cm):")
        self.c2w_height_label.setFont(QFont('Arial', 12))
        
        form_layout = QFormLayout()
        form_layout.addRow('Enter First Name:', self.c2w_first_name_edit)
        form_layout.addRow('Enter Last Name:', self.c2w_last_name_edit)
        form_layout.addRow('Enter Mobile No:', self.c2w_mobile_no_edit)
        form_layout.addRow('Enter College Name:', self.c2w_college_name_edit)
        form_layout.addRow('Enter DOB:', self.c2w_date_of_birth)
        form_layout.addRow(self.c2w_age_label,self.c2w_age)
        form_layout.addRow(self.c2w_gender_label, self.c2w_gender_radio_male)
        form_layout.addRow('', self.c2w_gender_radio_female)
        form_layout.addRow(self.c2w_height_label, self.c2w_height_edit)
        form_layout.setContentsMargins(0, 20, 0, 0)
        form_layout.setVerticalSpacing(20)
       
        for i in range(10):
            item = form_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                font = widget.font()
                font.setPointSize(12)
                widget.setFont(font)
   
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.c2w_submit_button)
        button_layout.addWidget(self.c2w_view_record)
        button_layout.setContentsMargins(0, 200, 0, 0)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(header_label)
        left_layout.addWidget(self.backbtn)
        left_layout.addLayout(form_layout)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.c2w_output_label)
        
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(QWidget())

        self.splitter.setSizes([self.width() // 2, self.width() // 2])
        self.splitter.setStyleSheet("QSplitter::handle {background:lightgray;}")
        self.splitter.widget(0).setLayout(left_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter)
        main_widget.addLayout(self.main_layout)
        
        self.c2w_submit_button.clicked.connect(lambda : self.c2w_submit_form())
        self.c2w_view_record.clicked.connect(lambda : self.c2w_fetch_records())
        
    def c2w_submit_form(self):
    
        if not self.c2w_first_name_edit.text() or not self.c2w_last_name_edit.text() or not self.c2w_mobile_no_edit.text():
            QMessageBox.critical(self, "Error", "Please fill in all required fields.")

            return
    
        mobile_no = self.c2w_mobile_no_edit.text()
        if not mobile_no.isdigit() or len(mobile_no) != 10:
            QMessageBox.critical(self, "Error", "Please enter a valid 10-digit mobile number.")
            return
    
        first_name = self.c2w_first_name_edit.text()
        last_name = self.c2w_last_name_edit.text()
        gender = 'Male' if self.c2w_gender_radio_male.isChecked() else 'Female'
        height = self.c2w_height_edit.text()
        college_name = self.c2w_college_name_edit.text()
        dob = self.c2w_date_of_birth.text()
        age = self.c2w_age.text()
       
        output_text = f"Name: {first_name} {last_name}\n" \
                        f"Mobile No: {mobile_no}\n" \
                        f"College Name: "\
                        f"Date Of Birth: "\
                        f"Age: "\
                        f"Gender: {gender}\n" \
                        f"Height: {height} cm"
    
        user_profiles_ref = db.collection('user_profiles')
        
        user_profile = {
            'first_name': first_name,
            'last_name': last_name,
            'mobile_no': mobile_no,
            'college_name' : college_name,
            'dob': dob,
            'age':age,
            'gender': gender,
            'height': height
        }
        
        new_user_ref = user_profiles_ref.add(user_profile)
        
        user_id = new_user_ref[1].id
        
        success_message = f"Form submitted successfully.\n\n" \
                            f"Firestore User ID: {user_id}\n" \
                            f"{output_text}"

        QMessageBox.information(self, "Success", success_message)

    def c2w_fetch_records(self):
        self.main_layout.removeWidget(self.splitter)
        obj = C2W_Info(self.main_layout, C2W_UserProfileForm)
    def c2w_about_us(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://www.core2web.in/about-us"))