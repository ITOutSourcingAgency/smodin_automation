import customtkinter, os, json
from etc.auth import auth
from customtkinter import *

class AuthToplevelView(customtkinter.CTkToplevel):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.geometry("300x300")
		self.title("인증 필요")
		self.parent = parent

		self.label = CTkLabel(self, text="아이디")
		self.label.pack(padx=20, pady=5)
		self.id_entry = CTkEntry(self)
		self.id_entry.pack(padx=20, pady=5)

		self.label = CTkLabel(self, text="비밀번호")
		self.label.pack(padx=20, pady=5)
		self.pw_entry = CTkEntry(self, show="*")
		self.pw_entry.pack(padx=20, pady=5)

		self.warning_label = CTkLabel(self, text="아이디와 비밀번호를 입력해주세요.")
		self.warning_label.pack(padx=20, pady=5)

		self.confirm_button = CTkButton(self, text="확인", command=self.confirm)
		self.confirm_button.pack(padx=20, pady=10)
		
		self.cancel_button = CTkButton(self, text="취소", command=self.cancel)
		self.cancel_button.pack(padx=20, pady=10)

		self.update_idletasks()
		self.center_window()

		self.load_existing_credentials()

		self.grab_set()
		self.protocol("WM_DELETE_WINDOW", self.on_close)

	def load_existing_credentials(self):
			if os.path.exists(self.parent.settings_file):
				with open(self.parent.settings_file, 'r', encoding='UTF-8') as file:
					settings = json.load(file)
					self.id_entry.insert(0, settings.get("auth_id", ""))
					self.pw_entry.insert(0, settings.get("auth_password", ""))

	def confirm(self):
		id = self.id_entry.get()
		password = self.pw_entry.get()
		if auth(id, password):

			if os.path.exists(self.parent.settings_file):
				with open(self.parent.settings_file, 'r', encoding='UTF-8') as file:
					settings = json.load(file)
			else:
				settings = {}

			settings["auth_id"] = id
			settings["auth_password"] = password

			with open(self.parent.settings_file, 'w', encoding='UTF-8') as file:
				json.dump(settings, file, ensure_ascii=False, indent=4)

			self.parent.auth_callback(True)
		else:
			self.warning_label.configure(text="잘못된 아이디 또는 비밀번호입니다.", text_color="red")



	def cancel(self):
		self.parent.auth_callback(False)

	def center_window(self):
		x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.winfo_width() // 2)
		y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
		self.geometry(f'+{x}+{y}')

	def on_close(self):
		self.parent.auth_callback(False)