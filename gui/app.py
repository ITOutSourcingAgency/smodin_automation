import threading
import customtkinter
import tkinter as tk
import automation.smodin_automation as sa
from customtkinter import *
import os, json, time, sys, subprocess
from tkinter import filedialog

def set_file_permissions(file_path, user, permissions):
	try:
		subprocess.run(["icacls", file_path, "/grant", f"{user}:({permissions})"], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Failed to set permissions for {file_path}. Error: {e}")

def resource_path(relative_path):
	"""Get the absolute path to the resource, works for dev and for PyInstaller"""
	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, relative_path)

class App(CTk):
	def __init__(self):
		super().__init__()
		self.settings_file = os.path.join(os.path.abspath(os.getcwd()), ".settings.json")
		self.toplevel_window = None

		if os.path.exists(self.settings_file):
			set_file_permissions(self.settings_file, "Everyone", "F")

		self.my_font = CTkFont(family="Helvetica", weight='bold')
		self.geometry('845x575')
		self.title('Smodin Automation')
		self.resizable(False, False)
		self.wm_iconbitmap(resource_path('smodin_img.ico'))
		set_appearance_mode("dark")
		self.create_method()
		self.create_strength()
		self.create_output_language(2)
		self.set_before_file_path()
		self.set_template_file_path()
		self.create_repeat_num_and_name()
		self.create_login_info()
		self.create_result_list()
		self.create_log()
		self.create_submit_button()

		self.add_button.configure(command=self.add_to_list)
	
	def create_method(self):
		self.method_frame = CTkFrame(self)
		self.method_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=5)
		self.method_frame.columnconfigure(0, weight=1)
		self.method_frame.rowconfigure(0, weight=1)

		self.method_label = CTkLabel(self.method_frame, text="방법", font=self.my_font)
		self.method_label.grid(row=0, column=0, padx=10, pady=10)

		self.method = CTkSegmentedButton(self.method_frame, values=['고쳐쓰기', '재창조'], command=self.update_method, height=30)
		self.method.set('고쳐쓰기')
		self.selected_method = 0
		self.method.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_strength(self):
		self.strength_frame = CTkFrame(self)
		self.strength_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=5)
		self.strength_frame.columnconfigure(0, weight=1)
		self.strength_frame.rowconfigure(0, weight=1)

		self.strength_label = CTkLabel(self.strength_frame, text="강도 (현재 강도: 1)", font=self.my_font)
		self.strength_label.grid(row=0, column=0, padx=10, pady=10)

		self.strength = CTkSlider(self.strength_frame, from_=0, to=4, command=self.update_strength_label, height = 27)
		self.strength.set(1)
		self.strength.configure(number_of_steps=4)
		self.strength.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_output_language(self, position):
		self.output_language_frame = CTkFrame(self)
		self.output_language_frame.grid(row=position, column=0, sticky= "nwe", padx=10, pady=5)
		self.output_language_frame.columnconfigure(0, weight=1)
		self.output_language_frame.rowconfigure(0, weight=1)

		self.output_language_label = CTkLabel(self.output_language_frame, text="출력 언어", font=self.my_font)
		self.output_language_label.grid(row=0, column=0, padx=10, pady=10)

		self.output_language = CTkComboBox(self.output_language_frame, values=["Korean", "English"])
		self.output_language.set("Korean")
		self.output_language.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_obj(self):
		self.obj_frame = CTkFrame(self)
		self.obj_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=5)
		self.obj_frame.columnconfigure(0, weight=1)
		self.obj_frame.rowconfigure(0, weight=1)

		self.obj_label = CTkLabel(self.obj_frame, text="목적을 재현", font=self.my_font)
		self.obj_label.grid(row=0, column=0, padx=10, pady=10)

		self.obj = CTkSegmentedButton(self.obj_frame, values=['독창성', 'AI탐지', 'AI(추가의)'])
		self.obj.set('독창성')
		self.obj.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_write_style(self):
		self.write_style_frame = CTkFrame(self)
		self.write_style_frame.grid(row=2, column=0, sticky="nswe", padx=10, pady=5)
		self.write_style_frame.columnconfigure(0, weight=1)
		self.write_style_frame.rowconfigure(0, weight=1)

		self.write_style_label = CTkLabel(self.write_style_frame, text="작문 스타일", font=self.my_font)
		self.write_style_label.grid(row=0, column=0, padx=10, pady=10)

		self.write_style = CTkEntry(self.write_style_frame, width = 200)
		self.write_style.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def update_method(self, value):
		if value == '고쳐쓰기':
			self.destroy_frames()
			self.selected_method = 0
			self.create_strength()
			self.create_output_language(2)
		elif value == '재창조':
			self.destroy_frames()
			self.selected_method = 1
			self.create_output_language(3)
			self.create_obj()
			self.create_write_style()

	def update_strength_label(self, value):
		if value < 1:
			self.strength.set(1)
			value = 1
		self.strength_label.configure(text=f"강도 (현재 강도: {int(value)})")

	def destroy_frames(self):
		for attr_name in ['strength_frame', 'output_language_frame', 'obj_frame', 'write_style_frame']:
			frame = getattr(self, attr_name, None)
			if frame is not None:
				frame.grid_forget()
				frame.destroy()
				setattr(self, attr_name, None)

	def set_before_file_path(self):
		self.file_frame = CTkFrame(self)
		self.file_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=5)
		self.file_frame.columnconfigure(0, weight=1)
		self.file_frame.columnconfigure(1, weight=0)
		self.file_frame.rowconfigure(0, weight=1)

		self.file_label = CTkLabel(self.file_frame, text="수정할 파일 경로", font=self.my_font)
		self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		self.selected_file_entry = CTkEntry(self.file_frame, font=self.my_font, state='readonly', width = 270)
		self.selected_file_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

		self.file_button = CTkButton(self.file_frame, text="파일 선택", command=lambda: self.open_file_dialog(self.selected_file_entry))
		self.file_button.grid(row=0, column=1, padx=10, pady=10)

	def set_template_file_path(self):
		self.template_file_frame = CTkFrame(self)
		self.template_file_frame.grid(row=1, column=1, sticky="ns", padx=10, pady=5)
		self.template_file_frame.columnconfigure(0, weight=1)
		self.template_file_frame.columnconfigure(1, weight=0)
		self.template_file_frame.rowconfigure(0, weight=1)

		self.template_file_label = CTkLabel(self.template_file_frame, text="템플릿 파일 경로", font=self.my_font)
		self.template_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		self.selected_template_file_entry = CTkEntry(self.template_file_frame, font=self.my_font, state='readonly', width = 270)
		self.selected_template_file_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

		self.template_file_button = CTkButton(self.template_file_frame, text="파일 선택", command=lambda: self.open_file_dialog(self.selected_template_file_entry))
		self.template_file_button.grid(row=0, column=1, padx=10, pady=10)

	def open_file_dialog(self, entry):
		file_selected = filedialog.askopenfilename()
		if file_selected:
			entry.configure(state='normal')
			entry.delete(0, 'end')
			entry.insert(0, file_selected)
			entry.configure(state='readonly')

	def create_repeat_num_and_name(self):
		self.repeat_num_frame = CTkFrame(self)
		self.repeat_num_frame.grid(row=2, column=1, sticky="nswe", padx=10, pady=5)
		self.repeat_num_frame.columnconfigure(0, weight=1)
		self.repeat_num_frame.rowconfigure(0, weight=1)

		self.name_label = CTkLabel(self.repeat_num_frame, text="작업 이름", font=self.my_font)
		self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky = 'w')

		self.name = CTkEntry(self.repeat_num_frame, font = self.my_font, width = 70)
		self.name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

		self.repeat_num_label = CTkLabel(self.repeat_num_frame, text="반복 횟수", font=self.my_font)
		self.repeat_num_label.grid(row=1, column=0, padx=10, pady=10, sticky = 'w')

		self.repeat_num = CTkEntry(self.repeat_num_frame, font = self.my_font, width = 70)
		self.repeat_num.grid(row=1, column=1, padx=10, pady=10, sticky="w")

		self.add_button = CTkButton(self.repeat_num_frame, text="등록", width = 100)
		self.add_button.grid(row=0, column=2, rowspan = 2, padx=10, pady=10, sticky = "nsew")

	def create_login_info(self):
		self.login_info_frame = CTkFrame(self)
		self.login_info_frame.grid(row=0, column=2, columnspan = 2, sticky="nswe", padx=10, pady=5)
		self.login_info_frame.columnconfigure(0, weight=1)
		self.login_info_frame.rowconfigure(0, weight=1)

		self.id_label = CTkLabel(self.login_info_frame, text="아이디", font=self.my_font, width = 30)
		self.id_label.grid(row=0, column=0, padx=10, pady=10, sticky = 'w')

		self.id = CTkEntry(self.login_info_frame, font = self.my_font)
		self.id.grid(row=0, column=1, columnspan = 2, padx=10, pady=10, sticky="we")

		self.password_label = CTkLabel(self.login_info_frame, text="비밀번호", font=self.my_font, width = 30)
		self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky = 'w')

		self.pw = CTkEntry(self.login_info_frame, font = self.my_font)
		self.pw.grid(row=1, column=1, columnspan = 2, padx=10, pady=10, sticky="we")

	def create_result_list(self):
		self.result_frame = CTkScrollableFrame(self)
		self.result_frame.grid(row=1, column=2, columnspan=2, rowspan = 2, padx=10, pady=5, sticky = "new")
		
		self.result_frame.configure(width=250)
		self.result_frame.grid_propagate()

		self.result_frame.columnconfigure(0, weight=1)
		self.result_frame.rowconfigure(0, weight=1)

		self.result_list = []

	def add_to_list(self):
		task_frame = CTkFrame(self.result_frame)
		task_frame.grid(sticky="new", padx=10, pady=5)
		task_frame.columnconfigure(0, weight=1)

		name_width = 20
		repeat_num_width = 5

		if self.selected_method == 1:
			if not self.write_style.get().strip():
				self.open_toplevel("작문 스타일을 작성해야 합니다.")
				return
			task_details = {
				"selected_method": 1,
				"obj": self.obj.get()
			}
		else:
			task_details = {
				"strength": self.strength.get()
			}

		if not self.selected_file_entry.get():
			self.open_toplevel("수정할 파일 경로를 선택해주세요.")
			return
		if not self.selected_template_file_entry.get():
			self.open_toplevel("템플릿 파일 경로를 선택해주세요.")
			return
		if not self.name.get():
			self.open_toplevel("작업 이름을 입력해주세요.")
			return
		if not self.repeat_num.get():
			self.open_toplevel("반복 횟수를 입력해주세요.")
			return

		name_display = self.name.get().ljust(name_width)[:name_width]
		repeat_num_display = self.repeat_num.get().rjust(repeat_num_width)[:repeat_num_width]

		task_label = CTkLabel(task_frame, text=f"{name_display} {repeat_num_display}", font=self.my_font)
		task_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

		delete_button = CTkButton(task_frame, text="삭제", command=lambda: self.delete_task(task_frame), width=20)
		delete_button.grid(row=0, column=1, padx=0, pady=5, sticky="e")

		task_details.update({
			"frame": task_frame,
			"output_language": self.output_language.get(),
			"selected_file": self.selected_file_entry.get(),
			"template_file": self.selected_template_file_entry.get(),
			"name": self.name.get(),
			"repeat_num": self.repeat_num.get(),
			"id": self.id.get(),
			"pw": self.pw.get()
		})

		self.result_list.append(task_details)
		for entry in [self.selected_file_entry, self.selected_template_file_entry, self.name, self.repeat_num]:
			self.clear_entry(entry)
		self.render_result_list()
		print(self.result_list)

	def render_result_list(self):
		# Clear existing items
		for widget in self.result_frame.winfo_children():
			widget.destroy()

		for task_details in self.result_list:
			task_frame = CTkFrame(self.result_frame)
			task_frame.grid(sticky="ew", padx=10, pady=5)
			task_frame.columnconfigure(0, weight=1)

			name_width = 20
			repeat_num_width = 5

			name_display = task_details["name"].ljust(name_width)[:name_width]
			repeat_num_display = task_details["repeat_num"].rjust(repeat_num_width)[:repeat_num_width]

			task_label = CTkLabel(task_frame, text=f"{name_display} {repeat_num_display}", font=self.my_font)
			task_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

			delete_button = CTkButton(task_frame, text="삭제", command=lambda tf=task_frame: self.delete_task(tf), width=20)
			delete_button.grid(row=0, column=1, padx=0, pady=5, sticky="e")

			task_details["frame"] = task_frame

	def clear_entry(self, entry):
		tmp_state = entry.cget('state')
		entry.configure(state = 'normal')
		entry.delete(0, 'end')
		if tmp_state == 'readonly':
			entry.configure(state = 'readonly')

	def open_toplevel(self, message="ToplevelWindow"):
		if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
			self.toplevel_window = ToplevelWindow(message, self)  # create window if its None or destroyed
		else:
			self.toplevel_window.focus()  # if window exists focus it

	def create_submit_button(self):
		self.submit_button = CTkButton(self, text="자동화 시작", width = 100, height = 60, command = lambda: self.submit_task())
		self.submit_button.grid(row=4, column=0, padx=10, pady=10, sticky = "sew")
	
	def submit_task(self):
		if len(self.result_list) == 0:
			self.open_toplevel("작업을 등록해주세요.")
		elif not self.id.get() or not self.pw.get():
			self.open_toplevel("로그인 정보를 입력하세요.")
		else:
			self.add_log("자동화를 시작합니다!", "green")
			smodin_auto = sa.SmodinAutomation(self.result_list)
			automation_thread = threading.Thread(target=smodin_auto.run)
			automation_thread.start()
		

	def create_log(self):
		self.log_frame = CTkScrollableFrame(self)
		self.log_frame.grid(row=3, column=1, columnspan=3, rowspan=2, padx=10, pady=10, sticky="nswe")

		self.log_frame.columnconfigure(0, weight=1)
		self.log_frame.rowconfigure(0, weight=1)

		self.log_textbox = tk.Text(self.log_frame, state='disabled', wrap='word', bg = 'black')
		self.log_textbox.grid(row=0, column=0, sticky="nswe")

	def add_log(self, message, color="white"):
		self.log_textbox.configure(state='normal')
		
		unique_tag = f"tag_{len(self.log_textbox.get('1.0', 'end').splitlines())}"
		self.log_textbox.insert('end', message + '\n', unique_tag)
		
		self.log_textbox.tag_configure(unique_tag, foreground=color)
		self.log_textbox.configure(state='disabled')
		self.log_textbox.yview('end')

	def delete_task(self, task_frame):
		for task in self.result_list:
			if task.get("frame") == task_frame:
				self.result_list.remove(task)
				break
		print(self.result_list)
		self.render_result_list()

class ToplevelWindow(customtkinter.CTkToplevel):
	def __init__(self, message, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.geometry("300x80")
		self.title("Warning")
		self.label = CTkLabel(self, text=message)
		self.label.pack(padx=20, pady=20)
		self.parent = parent

		# Center the Toplevel window
		self.update_idletasks()
		self.center_window()

		# Disable parent window
		self.grab_set()

	def center_window(self):
		x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.winfo_width())
		y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.winfo_height() // 2)
		self.geometry(f'+{x}+{y}')