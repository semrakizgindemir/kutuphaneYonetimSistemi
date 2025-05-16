import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout,
                             QMessageBox, QListWidget, QHBoxLayout, QMainWindow ,QTableWidget ,QTableWidgetItem,
                             QGridLayout ,QCompleter)

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


INSTITUTION_PASSWORD = "123456"

# Veritabanı oluşturma
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    tc TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tc TEXT UNIQUE,
    ad TEXT,          
    surname TEXT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS kitaplar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kitap_adi TEXT,
    yazar TEXT,
    yayinevi TEXT,
    baski_yili TEXT,
    kategori TEXT,
    stok INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS emanet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullanici_tc TEXT,
    kitap_id INTEGER,
    alis_tarihi TEXT,
    iade_tarihi TEXT,
    teslim_edildi INTEGER DEFAULT 0,
    FOREIGN KEY (kullanici_tc) REFERENCES users(tc),
    FOREIGN KEY (kitap_id) REFERENCES kitaplar(id)
)
""")



conn.commit()
conn.close()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Türü Seçin")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f4f4f4;")

        title_label = QLabel("Giriş Türünü Seçiniz:")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333333; margin-bottom: 30px;")

        self.admin_button = QPushButton("Yönetici Girişi")
        self.user_button = QPushButton("Kullanıcı Girişi")

        for btn in (self.admin_button, self.user_button):
            btn.setMinimumHeight(60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)

        self.admin_button.clicked.connect(self.open_admin_login)
        self.user_button.clicked.connect(self.open_user_login)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(100, 80, 100, 80)
        layout.addWidget(title_label)
        layout.addWidget(self.admin_button)
        layout.addWidget(self.user_button)
        self.setLayout(layout)

    def open_admin_login(self):
        self.admin_window = LoginWindow()
        self.admin_window.show()
        self.close()

    def open_user_login(self):
        self.user_window = UserLoginWindow()
        self.user_window.show()
        self.close()


class UserLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Girişi")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 6px;
            }
        """

        self.tc_label = QLabel("T.C. Kimlik No:")
        self.tc_label.setStyleSheet(label_style)
        self.tc_input = QLineEdit()
        self.tc_input.setStyleSheet(input_style)

        self.password_label = QLabel("Şifre:")
        self.password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Giriş Yap")
        self.register_button = QPushButton("Kayıt Ol")
        self.reset_button = QPushButton("Şifremi Unuttum")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """

        for btn in [self.login_button, self.register_button, self.reset_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
        self.reset_button.clicked.connect(self.reset_password)
        self.back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 70, 120, 70)
        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def login(self):
        tc = self.tc_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE tc = ? AND password = ?", (tc, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.user_panel = UserPanel()
            self.user_panel.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Hatalı T.C. veya şifre!")

    def register(self):
        self.register_window = UserRegisterWindow()
        self.register_window.show()
        self.close()

    def reset_password(self):
        self.reset_window = UserResetPasswordWindow()
        self.reset_window.show()
        self.close()

    def go_back(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()





class UserRegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Kaydı")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(input_style)
        self.tc_input = QLineEdit()
        self.tc_input.setStyleSheet(input_style)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        self.register_button = QPushButton("Kaydet")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [self.register_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)
        for label, input_widget in [
            ("Ad:", self.name_input),
            ("Soyad:", self.surname_input),
            ("T.C. Kimlik No:", self.tc_input),
            ("Kullanıcı Adı:", self.username_input),
            ("Şifre:", self.password_input)
        ]:
            lbl = QLabel(label)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        self.register_button.clicked.connect(self.register_user)
        self.back_button.clicked.connect(self.go_back)

    def register_user(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        tc = self.tc_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if name and surname and tc and username and password:
            try:
                conn = sqlite3.connect("library.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (ad, surname, tc, username, password) VALUES (?, ?, ?, ?, ?)",
                               (name, surname, tc, username, password))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
                self.go_back()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu kullanıcı adı veya T.C. zaten kullanılıyor!")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")

    def go_back(self):
        self.login_window = UserLoginWindow()
        self.login_window.show()
        self.close()



class UserResetPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Sıfırlama")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(input_style)
        self.tc_input = QLineEdit()
        self.tc_input.setStyleSheet(input_style)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet(input_style)

        self.confirm_button = QPushButton("Şifreyi Güncelle")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [self.confirm_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)
        for label, input_widget in [
            ("Ad:", self.name_input),
            ("Soyad:", self.surname_input),
            ("T.C. Kimlik No:", self.tc_input),
            ("Yeni Şifre:", self.new_password_input)
        ]:
            lbl = QLabel(label)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)

        layout.addWidget(self.confirm_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        self.confirm_button.clicked.connect(self.reset_password)
        self.back_button.clicked.connect(self.go_back)

    def reset_password(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        tc = self.tc_input.text()
        new_password = self.new_password_input.text()

        if not all([name, surname, tc, new_password]):
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE tc = ? AND ad = ? AND surname = ?", (tc, name, surname))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE users SET password = ? WHERE tc = ?", (new_password, tc))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Şifre güncellendi!")
            self.go_back()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı!")

    def go_back(self):
        self.login_window = UserLoginWindow()
        self.login_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yönetici Girişi")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        self.login_button = QPushButton("Giriş Yap")
        self.new_admin_button = QPushButton("Yeni Yönetici")
        self.forgot_password_button = QPushButton("Şifremi Unuttum")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [self.login_button, self.new_admin_button, self.forgot_password_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)

        for label_text, input_widget in [
            ("Ad:", self.name_input),
            ("Soyad:", self.surname_input),
            ("Şifre:", self.password_input)
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)

        layout.addWidget(self.login_button)
        layout.addWidget(self.new_admin_button)
        layout.addWidget(self.forgot_password_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.login)
        self.new_admin_button.clicked.connect(self.open_new_admin_window)
        self.forgot_password_button.clicked.connect(self.open_forgot_password_window)
        self.back_button.clicked.connect(self.go_back)

    def login(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM managers WHERE name=? AND surname=? AND password=?", (name, surname, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.select_action_window = SelectActionWindow()
            self.select_action_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı bilgileri yanlış!")

    def open_new_admin_window(self):
        self.new_admin_window = NewAdminWindow()
        self.new_admin_window.previous_window = self
        self.new_admin_window.show()
        self.close()

    def open_forgot_password_window(self):
        self.forgot_password_window = ForgotPasswordWindow()
        self.forgot_password_window.previous_window = self
        self.forgot_password_window.show()
        self.close()

    def go_back(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()



class NewAdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Yönetici Kaydı")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(input_style)
        self.tc_input = QLineEdit()
        self.tc_input.setStyleSheet(input_style)
        self.inst_password_input = QLineEdit()
        self.inst_password_input.setStyleSheet(input_style)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)

        self.save_button = QPushButton("Kaydet")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [self.save_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)

        for label_text, input_widget in [
            ("Ad:", self.name_input),
            ("Soyad:", self.surname_input),
            ("TC:", self.tc_input),
            ("Kurum Şifresi:", self.inst_password_input),
            ("Şifre Belirleyin:", self.password_input)
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)

        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_admin)
        self.back_button.clicked.connect(self.go_back)

    def save_admin(self):
        if self.inst_password_input.text() != INSTITUTION_PASSWORD:
            QMessageBox.warning(self, "Hata", "Kurum şifresi yanlış!")
            return

        name = self.name_input.text()
        surname = self.surname_input.text()
        tc = self.tc_input.text()
        password = self.password_input.text()

        if not (name and surname and tc and password):
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır!")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO managers (name, surname, tc, password) VALUES (?, ?, ?, ?)",
                           (name, surname, tc, password))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Yönetici kaydedildi.")
            self.go_back()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu TC ile zaten bir kullanıcı var!")
        conn.close()

    def go_back(self):
        self.previous_window.show()
        self.close()



class ResetPasswordWindow(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.setWindowTitle("Şifre Sıfırlama Devam")
        self.setGeometry(100, 100, 700, 500)
        self.previous_window = previous_window
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(input_style)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(input_style)
        self.new_password_input = QLineEdit()
        self.new_password_input.setStyleSheet(input_style)

        self.confirm_button = QPushButton("Onayla")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """

        for btn in [self.confirm_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)
        for label_text, input_widget in [
            ("Ad:", self.name_input),
            ("Soyad:", self.surname_input),
            ("Yeni Şifre:", self.new_password_input)
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)

        layout.addWidget(self.confirm_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        self.confirm_button.clicked.connect(self.reset_password)
        self.back_button.clicked.connect(self.go_back)

    def reset_password(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        new_password = self.new_password_input.text()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE managers SET password=? WHERE name=? AND surname=?",
                       (new_password, name, surname))
        conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Başarılı", "Şifre güncellendi.")
            self.previous_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı.")
        conn.close()

    def go_back(self):
        self.previous_window.show()
        self.close()

class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Sıfırlama")
        self.setGeometry(100, 100, 700, 400)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.inst_password_input = QLineEdit()
        self.inst_password_input.setStyleSheet(input_style)

        self.continue_button = QPushButton("Devam Et")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """

        for btn in [self.continue_button, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)

        lbl = QLabel("Kurum Şifresi:")
        lbl.setStyleSheet(label_style)
        layout.addWidget(lbl)
        layout.addWidget(self.inst_password_input)
        layout.addWidget(self.continue_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.continue_button.clicked.connect(self.check_inst_password)
        self.back_button.clicked.connect(self.go_back)

    def check_inst_password(self):
        if self.inst_password_input.text() != INSTITUTION_PASSWORD:
            QMessageBox.warning(self, "Hata", "Kurum şifresi yanlış!")
            return

        self.reset_window = ResetPasswordWindow(self.previous_window)
        self.reset_window.show()
        self.close()

    def go_back(self):
        self.previous_window.show()
        self.close()



class SelectActionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yönetim Paneli")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        title_label = QLabel("Lütfen bir işlem seçiniz:")
        title_label.setStyleSheet("font-size: 18px; color: #333; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)

        self.btn_kitap_islemleri = QPushButton("Kullanıcı Kitap İşlemleri")
        self.btn_kitap_ekleme = QPushButton("Kitap Ekleme")
        self.btn_kitap_cikarma = QPushButton("Kitap Çıkarma")
        self.btn_kitap_arama = QPushButton("Kitap Arama")
        self.btn_kitap_detayi_gorme = QPushButton("Kitap Detayı Görme")
        self.back_button = QPushButton("Çıkış Yap")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 15px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [
            self.btn_kitap_islemleri,
            self.btn_kitap_ekleme,
            self.btn_kitap_cikarma,
            self.btn_kitap_arama,
            self.btn_kitap_detayi_gorme,
            self.back_button
        ]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        self.btn_kitap_islemleri.clicked.connect(self.kitap_islemleri_clicked)
        self.btn_kitap_ekleme.clicked.connect(self.kitap_ekleme_clicked)
        self.btn_kitap_cikarma.clicked.connect(self.kitap_cikarma_clicked)
        self.btn_kitap_arama.clicked.connect(self.kitap_arama_clicked)
        self.btn_kitap_detayi_gorme.clicked.connect(self.kitap_detayi_gorme_clicked)
        self.back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(100, 50, 100, 50)
        layout.addWidget(title_label)
        layout.addWidget(self.btn_kitap_islemleri)
        layout.addWidget(self.btn_kitap_ekleme)
        layout.addWidget(self.btn_kitap_cikarma)
        layout.addWidget(self.btn_kitap_arama)
        layout.addWidget(self.btn_kitap_detayi_gorme)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def kitap_islemleri_clicked(self):
        self.kitap_islem_penceresi = KullaniciKitapIslemleriWindow()
        self.kitap_islem_penceresi.show()

    def kitap_ekleme_clicked(self):
        self.kitap_ekleme_penceresi = KitapEklemePenceresi()
        self.kitap_ekleme_penceresi.show()

    def kitap_cikarma_clicked(self):
        self.kitap_cikarma_penceresi = KitapCikarmaPenceresi()
        self.kitap_cikarma_penceresi.show()

    def kitap_arama_clicked(self):
        self.kitap_arama_penceresi = KitapAramaPenceresi()
        self.kitap_arama_penceresi.show()

    def kitap_detayi_gorme_clicked(self):
        self.kitap_listesi_penceresi = KitapListesiPenceresi()
        self.kitap_listesi_penceresi.show()

    def go_back(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class KullaniciKitapIslemleriWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Kitap İşlemleri")
        self.setGeometry(150, 150, 500, 400)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.btn_kitap_alma = QPushButton("Kullanıcı Kitap Alma")
        self.btn_kitap_iade = QPushButton("Kullanıcı Kitap İadesi")
        self.back_button = QPushButton("Geri Dön")

        button_style = """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """
        for btn in [self.btn_kitap_alma, self.btn_kitap_iade, self.back_button]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet(button_style)

        self.btn_kitap_alma.clicked.connect(self.kitap_alma_clicked)
        self.btn_kitap_iade.clicked.connect(self.kitap_iade_clicked)
        self.back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(100, 60, 100, 60)
        layout.addWidget(self.btn_kitap_alma)
        layout.addWidget(self.btn_kitap_iade)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def kitap_alma_clicked(self):
        self.kitap_alma_penceresi = KitapAlmaWindow()
        self.kitap_alma_penceresi.show()

    def kitap_iade_clicked(self):
        self.kitap_iade_penceresi = KitapIadeWindow()
        self.kitap_iade_penceresi.show()

    def go_back(self):
        self.close()



class KitapAlmaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Alma")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f4f4f4;")

        label_style = "font-size: 16px; color: #333;"
        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.tc_input = QLineEdit()
        self.tc_input.setPlaceholderText("Kullanıcı T.C.")
        self.tc_input.setStyleSheet(input_style)

        self.kitap_input = QLineEdit()
        self.kitap_input.setPlaceholderText("Kitap Adı")
        self.kitap_input.setStyleSheet(input_style)

        kitap_adlari = self.get_kitap_adlari()
        completer = QCompleter(kitap_adlari)
        completer.setCaseSensitivity(False)
        self.kitap_input.setCompleter(completer)

        self.al_button = QPushButton("Kitabı Al")
        self.al_button.setMinimumHeight(50)
        self.al_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        self.al_button.clicked.connect(self.kitap_al)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)
        for label_text, input_widget in [
            ("Kullanıcı T.C.:", self.tc_input),
            ("Kitap İsmi:", self.kitap_input)
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)
            layout.addWidget(input_widget)

        layout.addWidget(self.al_button)
        self.setLayout(layout)

    def get_kitap_adlari(self):
        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT kitap_adi FROM kitaplar")
            kitaplar = cursor.fetchall()
            conn.close()
            return [k[0] for k in kitaplar]
        except Exception as e:
            print("Kitap adları alınamadı:", e)
            return []

    def kitap_al(self):
        tc = self.tc_input.text().strip()
        kitap_adi = self.kitap_input.text().strip().lower()

        if not tc or not kitap_adi:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE tc = ?", (tc,))
        kullanici = cursor.fetchone()

        if not kullanici:
            QMessageBox.warning(self, "Kullanıcı Yok", "Bu TC numarasıyla kayıtlı bir kullanıcı bulunamadı.")
            conn.close()
            return

        cursor.execute("SELECT id, stok FROM kitaplar WHERE lower(kitap_adi) LIKE ?", (kitap_adi + '%',))
        kitap = cursor.fetchone()

        if not kitap:
            QMessageBox.warning(self, "Kitap Yok", "Kitap bulunamadı.")
        else:
            kitap_id, stok = kitap
            if stok > 0:
                cursor.execute("""
                    INSERT INTO emanet (kullanici_tc, kitap_id, alis_tarihi) 
                    VALUES (?, ?, date('now'))
                """, (tc, kitap_id))
                cursor.execute("UPDATE kitaplar SET stok = stok - 1 WHERE id = ?", (kitap_id,))
                conn.commit()
                QMessageBox.information(self, "Başarılı", "Kitap başarıyla alındı.")
            else:
                QMessageBox.warning(self, "Stok Yok", "Kitap stokta bulunmamaktadır.")

        conn.close()

class KitapIadeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap İade")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.tc_input = QLineEdit()
        self.tc_input.setPlaceholderText("Kullanıcı T.C.")
        self.tc_input.setStyleSheet("font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 6px;")
        self.tc_input.returnPressed.connect(self.kitaplari_getir)

        self.kitap_listesi = QListWidget()

        self.iade_button = QPushButton("Seçili Kitabı İade Et")
        self.iade_button.setMinimumHeight(50)
        self.iade_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        self.iade_button.clicked.connect(self.kitap_iade_et)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)
        layout.addWidget(QLabel("Kullanıcı T.C.:"))
        layout.addWidget(self.tc_input)
        layout.addWidget(QLabel("Alınan Kitaplar:"))
        layout.addWidget(self.kitap_listesi)
        layout.addWidget(self.iade_button)

        self.setLayout(layout)

    def kitaplari_getir(self):
        self.kitap_listesi.clear()
        tc = self.tc_input.text().strip()
        if not tc:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir T.C. girin.")
            return

        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT emanet.id, kitaplar.kitap_adi 
                FROM emanet 
                JOIN kitaplar ON emanet.kitap_id = kitaplar.id 
                WHERE emanet.kullanici_tc = ? AND emanet.iade_tarihi IS NULL
            """, (tc,))
            kitaplar = cursor.fetchall()
            conn.close()

            if not kitaplar:
                QMessageBox.information(self, "Bilgi", "İadesi yapılmamış kitap bulunamadı.")

            for emanet_id, kitap_adi in kitaplar:
                item = QListWidgetItem(kitap_adi)
                item.setData(Qt.UserRole, emanet_id)
                self.kitap_listesi.addItem(item)

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Hata: {e}")

    def kitap_iade_et(self):
        secili_item = self.kitap_listesi.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Hata", "Lütfen bir kitap seçin.")
            return

        emanet_id = secili_item.data(Qt.UserRole)

        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT kitap_id FROM emanet WHERE id = ?", (emanet_id,))
            kitap_kaydi = cursor.fetchone()

            if kitap_kaydi:
                kitap_id = kitap_kaydi[0]
                cursor.execute("UPDATE emanet SET iade_tarihi = date('now'), teslim_edildi = 1 WHERE id = ?", (emanet_id,))
                cursor.execute("UPDATE kitaplar SET stok = stok + 1 WHERE id = ?", (kitap_id,))
                conn.commit()
                QMessageBox.information(self, "Başarılı", "Kitap iade edildi.")
                self.kitaplari_getir()
            else:
                QMessageBox.warning(self, "Hata", "Emanet kaydı bulunamadı.")

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Veritabanı Hatası", f"Hata: {e}")
        finally:
            conn.close()




class KitapEklemePenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Ekle")
        self.setGeometry(150, 150, 700, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.kitap_adi_input = QLineEdit()
        self.kitap_adi_input.setPlaceholderText("Kitap Adı")
        self.kitap_adi_input.setStyleSheet(input_style)

        self.yazar_input = QLineEdit()
        self.yazar_input.setPlaceholderText("Yazar Adı")
        self.yazar_input.setStyleSheet(input_style)

        self.yayinevi_input = QLineEdit()
        self.yayinevi_input.setPlaceholderText("Yayınevi")
        self.yayinevi_input.setStyleSheet(input_style)

        self.baski_yili_input = QLineEdit()
        self.baski_yili_input.setPlaceholderText("Baskı Yılı")
        self.baski_yili_input.setStyleSheet(input_style)

        self.kategori_input = QLineEdit()
        self.kategori_input.setPlaceholderText("Kategori")
        self.kategori_input.setStyleSheet(input_style)

        self.stok_input = QLineEdit()
        self.stok_input.setPlaceholderText("Stok Adedi")
        self.stok_input.setStyleSheet(input_style)

        self.kaydet_buton = QPushButton("Kitabı Kaydet")
        self.kaydet_buton.setMinimumHeight(50)
        self.kaydet_buton.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        self.kaydet_buton.clicked.connect(self.kitabi_kaydet)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(120, 50, 120, 50)

        for widget in [
            self.kitap_adi_input,
            self.yazar_input,
            self.yayinevi_input,
            self.baski_yili_input,
            self.kategori_input,
            self.stok_input,
            self.kaydet_buton
        ]:
            layout.addWidget(widget)

        self.setLayout(layout)

    def kitabi_kaydet(self):
        kitap_adi = self.kitap_adi_input.text()
        yazar = self.yazar_input.text()
        yayinevi = self.yayinevi_input.text()
        baski_yili = self.baski_yili_input.text()
        kategori = self.kategori_input.text()
        stok = self.stok_input.text()

        if not all([kitap_adi, yazar, yayinevi, baski_yili, kategori, stok]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            stok = int(stok)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Stok değeri sayısal olmalıdır.")
            return

        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT stok FROM kitaplar WHERE kitap_adi = ? AND yazar = ?", (kitap_adi, yazar))
            sonuc = cursor.fetchone()

            if sonuc:
                mevcut_stok = sonuc[0]
                yeni_stok = mevcut_stok + stok
                cursor.execute("UPDATE kitaplar SET stok = ? WHERE kitap_adi = ? AND yazar = ?", (yeni_stok, kitap_adi, yazar))
                QMessageBox.information(self, "Güncellendi", "Kitap zaten kayıtlıydı, stok miktarı güncellendi.")
            else:
                cursor.execute("""
                    INSERT INTO kitaplar (kitap_adi, yazar, yayinevi, baski_yili, kategori, stok)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (kitap_adi, yazar, yayinevi, baski_yili, kategori, stok))
                QMessageBox.information(self, "Başarılı", "Yeni kitap başarıyla eklendi.")

            conn.commit()
            conn.close()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")




class KitapCikarmaPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Çıkarma")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Kitap adı veya yazar adıyla ara")
        self.arama_input.setStyleSheet(input_style)
        self.arama_input.textChanged.connect(self.kitaplari_listele)

        self.kitap_tablosu = QTableWidget()
        self.kitap_tablosu.setColumnCount(6)
        self.kitap_tablosu.setHorizontalHeaderLabels(["ID", "Adı", "Yazar", "Yayınevi", "Baskı Yılı", "Stok"])
        self.kitap_tablosu.setEditTriggers(QTableWidget.NoEditTriggers)
        self.kitap_tablosu.setSelectionBehavior(QTableWidget.SelectRows)

        self.stok_dus_btn = QPushButton("Stoktan 1 Düş")
        self.stok_dus_btn.setMinimumHeight(50)
        self.stok_dus_btn.setStyleSheet(self.button_style())
        self.stok_dus_btn.clicked.connect(self.stoktan_dus)

        self.kitabi_sil_btn = QPushButton("Kitabı Sil")
        self.kitabi_sil_btn.setMinimumHeight(50)
        self.kitabi_sil_btn.setStyleSheet(self.button_style())
        self.kitabi_sil_btn.clicked.connect(self.kitabi_sil)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.addWidget(self.stok_dus_btn)
        btn_layout.addWidget(self.kitabi_sil_btn)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(80, 50, 80, 50)
        label = QLabel("Arama:")
        label.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(label)
        layout.addWidget(self.arama_input)
        layout.addWidget(self.kitap_tablosu)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.kitaplari_listele()

    def button_style(self):
        return """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """

    def kitaplari_listele(self):
        arama = self.arama_input.text()
        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, kitap_adi, yazar, yayinevi, baski_yili, stok 
            FROM kitaplar 
            WHERE kitap_adi LIKE ? OR yazar LIKE ?
        """, (f"%{arama}%", f"%{arama}%"))
        kitaplar = cursor.fetchall()
        conn.close()

        self.kitap_tablosu.setRowCount(0)
        for row_idx, row_data in enumerate(kitaplar):
            self.kitap_tablosu.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                self.kitap_tablosu.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def get_selected_kitap_id(self):
        selected_items = self.kitap_tablosu.selectedItems()
        if selected_items:
            return int(selected_items[0].text())
        return None

    def stoktan_dus(self):
        kitap_id = self.get_selected_kitap_id()
        if kitap_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kitap seçin.")
            return

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("SELECT stok FROM kitaplar WHERE id = ?", (kitap_id,))
        result = cursor.fetchone()
        if result:
            stok = result[0]
            if stok > 1:
                cursor.execute("UPDATE kitaplar SET stok = stok - 1 WHERE id = ?", (kitap_id,))
                QMessageBox.information(self, "Başarılı", "Stoktan 1 adet düşüldü.")
            else:
                cursor.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id,))
                QMessageBox.information(self, "Silindi", "Stok 1 idi, kitap tamamen silindi.")
            conn.commit()
        conn.close()
        self.kitaplari_listele()

    def kitabi_sil(self):
        kitap_id = self.get_selected_kitap_id()
        if kitap_id is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kitabı seçin.")
            return

        onay = QMessageBox.question(self, "Onay", "Kitap tamamen silinsin mi?",
                                    QMessageBox.Yes | QMessageBox.No)
        if onay == QMessageBox.Yes:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kitaplar WHERE id = ?", (kitap_id,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Silindi", "Kitap başarıyla silindi.")
            self.kitaplari_listele()



class KitapAramaPenceresi(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Arama")
        self.setGeometry(250, 250, 800, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 40, 50, 40)

        input_style = """
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
        """

        label_style = "font-size: 16px; color: #333;"

        arama_layout = QHBoxLayout()
        arama_layout.setSpacing(10)

        self.kitap_adi_input = QLineEdit()
        self.kitap_adi_input.setPlaceholderText("Kitap Adı")
        self.kitap_adi_input.setStyleSheet(input_style)
        self.kitap_adi_input.textChanged.connect(self.kitaplari_listele)

        self.yazar_input = QLineEdit()
        self.yazar_input.setPlaceholderText("Yazar Adı")
        self.yazar_input.setStyleSheet(input_style)
        self.yazar_input.textChanged.connect(self.kitaplari_listele)

        self.kategori_input = QLineEdit()
        self.kategori_input.setPlaceholderText("Kategori")
        self.kategori_input.setStyleSheet(input_style)
        self.kategori_input.textChanged.connect(self.kitaplari_listele)

        self.yayinevi_input = QLineEdit()
        self.yayinevi_input.setPlaceholderText("Yayınevi")
        self.yayinevi_input.setStyleSheet(input_style)
        self.yayinevi_input.textChanged.connect(self.kitaplari_listele)

        for label_text, widget in [
            ("Adı:", self.kitap_adi_input),
            ("Yazar:", self.yazar_input),
            ("Kategori:", self.kategori_input),
            ("Yayınevi:", self.yayinevi_input)
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            arama_layout.addWidget(lbl)
            arama_layout.addWidget(widget)

        self.kitap_tablosu = QTableWidget()
        self.kitap_tablosu.setColumnCount(6)
        self.kitap_tablosu.setHorizontalHeaderLabels(["ID", "Adı", "Yazar", "Yayınevi", "Baskı Yılı", "Kategori"])
        self.kitap_tablosu.setEditTriggers(QTableWidget.NoEditTriggers)
        self.kitap_tablosu.setSelectionBehavior(QTableWidget.SelectRows)

        layout.addLayout(arama_layout)
        layout.addWidget(self.kitap_tablosu)
        self.setLayout(layout)

        self.kitaplari_listele()

    def kitaplari_listele(self):
        kitap_adi = self.kitap_adi_input.text()
        yazar = self.yazar_input.text()
        kategori = self.kategori_input.text()
        yayinevi = self.yayinevi_input.text()

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, kitap_adi, yazar, yayinevi, baski_yili, kategori 
            FROM kitaplar
            WHERE kitap_adi LIKE ?
              AND yazar LIKE ?
              AND kategori LIKE ?
              AND yayinevi LIKE ?
        """, (f"%{kitap_adi}%", f"%{yazar}%", f"%{kategori}%", f"%{yayinevi}%"))
        kitaplar = cursor.fetchall()
        conn.close()

        self.kitap_tablosu.setRowCount(0)
        for row_idx, row_data in enumerate(kitaplar):
            self.kitap_tablosu.insertRow(row_idx)
            for col_idx, item in enumerate(row_data):
                self.kitap_tablosu.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))


class KitapListesiPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kitap Seç")
        self.setGeometry(150, 150, 700, 500)
        self.setStyleSheet("background-color: #f4f4f4;")

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(80, 50, 80, 50)

        self.kitap_listesi = QListWidget()
        self.kitap_listesi.setStyleSheet("font-size: 15px; padding: 10px;")
        self.kitaplari_listele()
        layout.addWidget(self.kitap_listesi)

        detay_gor_button = QPushButton("Seçilen Kitabın Detaylarını Gör")
        detay_gor_button.setMinimumHeight(50)
        detay_gor_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """)
        detay_gor_button.clicked.connect(self.detaylari_goster)
        layout.addWidget(detay_gor_button)

        self.setLayout(layout)

    def kitaplari_listele(self):
        self.kitap_listesi.clear()
        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, kitap_adi, yazar FROM kitaplar")
            kitaplar = cursor.fetchall()
            conn.close()

            for kitap in kitaplar:
                kitap_bilgisi = f"{kitap[1]} - {kitap[2]} (ID: {kitap[0]})"
                item = QListWidgetItem(kitap_bilgisi)
                item.setData(Qt.UserRole, kitap[0])
                self.kitap_listesi.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")

    def detaylari_goster(self):
        secilen_item = self.kitap_listesi.currentItem()
        if secilen_item:
            secilen_kitap_id = secilen_item.data(Qt.UserRole)
            self.detay_penceresi = KitapDetaylariPenceresi(secilen_kitap_id)
            self.detay_penceresi.show()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen detaylarını görmek için bir kitap seçin.")

class KitapDetaylariPenceresi(QWidget):
    def __init__(self, kitap_id):
        super().__init__()
        self.setWindowTitle("Kitap Detayları")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f4f4f4;")
        self.kitap_id = kitap_id
        self.kitap_bilgileri = self.kitabi_yukle()
        if self.kitap_bilgileri:
            self.initUI()
        else:
            QMessageBox.critical(self, "Hata", f"{kitap_id} ID'li kitap bulunamadı.")
            self.close()

    def kitabi_yukle(self):
        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kitaplar WHERE id = ?", (self.kitap_id,))
            kitap = cursor.fetchone()
            conn.close()
            if kitap:
                return {
                    "id": kitap[0],
                    "kitap_adi": kitap[1],
                    "yazar": kitap[2],
                    "yayinevi": kitap[3],
                    "baski_yili": kitap[4],
                    "kategori": kitap[5],
                    "stok": kitap[6]
                }
            else:
                return None
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {str(e)}")
            return None

    def initUI(self):
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 40, 50, 40)
        row = 0

        self.baslik_label = QLabel("<b>Temel Bilgiler</b>")
        self.baslik_label.setStyleSheet("font-size: 18px; color: #333;")
        layout.addWidget(self.baslik_label, row, 0, 1, 2)
        row += 1

        def add_row(label_text, value):
            nonlocal row
            layout.addWidget(QLabel(label_text), row, 0)
            lbl = QLabel(value)
            lbl.setStyleSheet("font-size: 15px;")
            layout.addWidget(lbl, row, 1)
            row += 1

        add_row("Kitap Adı:", self.kitap_bilgileri["kitap_adi"])
        add_row("Yazar:", self.kitap_bilgileri["yazar"])
        add_row("Yayınevi:", self.kitap_bilgileri["yayinevi"] or "-")
        add_row("Baskı Yılı:", self.kitap_bilgileri["baski_yili"] or "-")
        add_row("Kategori:", self.kitap_bilgileri["kategori"] or "-")
        add_row("Stok Adedi:", str(self.kitap_bilgileri["stok"]))

        odunc_adedi = self.odunc_adedi_hesapla()
        add_row("Ödünçteki Adet:", str(odunc_adedi))
        kalan_stok = self.kitap_bilgileri["stok"] - odunc_adedi
        add_row("Kalan Stok:", str(kalan_stok))

        geri_button = QPushButton("Geri")
        geri_button.setMinimumHeight(40)
        geri_button.setStyleSheet("""
            QPushButton {
                background-color: #aaa;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        geri_button.clicked.connect(self.close)
        layout.addWidget(geri_button, row, 0, 1, 2)

        self.setLayout(layout)

    def odunc_adedi_hesapla(self):
        try:
            conn = sqlite3.connect("library.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM emanet WHERE kitap_id = ? AND teslim_edildi = 0", (self.kitap_id,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası (ödünç adedi): {str(e)}")
            return 0



class UserPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Paneli")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f4f4f4;")

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(100, 80, 100, 80)

        title = QLabel("Kullanıcı Paneline Hoş Geldiniz!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        layout.addWidget(title)

        self.kitap_arama_button = QPushButton("Kitap Ara")
        self.kitap_arama_button.setMinimumHeight(50)
        self.kitap_arama_button.setStyleSheet(self.button_style())
        self.kitap_arama_button.clicked.connect(self.kitap_arama_ac)
        layout.addWidget(self.kitap_arama_button)

        self.kitap_detay_button = QPushButton("Kitap Detaylarını Gör")
        self.kitap_detay_button.setMinimumHeight(50)
        self.kitap_detay_button.setStyleSheet(self.button_style())
        self.kitap_detay_button.clicked.connect(self.kitap_detay_ac)
        layout.addWidget(self.kitap_detay_button)

        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setMinimumHeight(50)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #aaa;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #888;
            }
        """)
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def button_style(self):
        return """
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-size: 15px;
                padding: 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
        """

    def kitap_arama_ac(self):
        self.kitap_arama_window = KitapAramaPenceresi()
        self.kitap_arama_window.show()

    def kitap_detay_ac(self):
        self.kitap_detay_window = KitapListesiPenceresi()
        self.kitap_detay_window.show()

    def logout(self):
        self.login_window = UserLoginWindow()
        self.login_window.show()
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())