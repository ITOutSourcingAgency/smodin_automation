import threading
import customtkinter
from customtkinter import *
import os, json, time, sys, subprocess
from tkinter import filedialog

def set_file_permissions(file_path, user, permissions):
	"""
	Set permissions for a file using icacls.

	:param file_path: Path to the file.
	:param user: User or group to grant permissions to.
	:param permissions: Permissions to grant (e.g., "R", "W", "F").
	"""
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

		if os.path.exists(self.settings_file):
			set_file_permissions(self.settings_file, "Everyone", "F")

		self.my_font = CTkFont(family="Helvetica", weight='bold')
		self.geometry('845x565')
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
		self.create_result_list()
		self.create_log()

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
		self.method.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_strength(self):
		self.strength_frame = CTkFrame(self)
		self.strength_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
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
		self.output_language_frame.grid(row=position, column=0, sticky= "nwe", padx=10, pady=10)
		self.output_language_frame.columnconfigure(0, weight=1)
		self.output_language_frame.rowconfigure(0, weight=1)

		self.output_language_label = CTkLabel(self.output_language_frame, text="출력 언어", font=self.my_font)
		self.output_language_label.grid(row=0, column=0, padx=10, pady=10)

		self.output_language = CTkComboBox(self.output_language_frame, values=["Korean", "English"])
		self.output_language.set("Korean")
		self.output_language.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_obj(self):
		self.obj_frame = CTkFrame(self)
		self.obj_frame.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
		self.obj_frame.columnconfigure(0, weight=1)
		self.obj_frame.rowconfigure(0, weight=1)

		self.obj_label = CTkLabel(self.obj_frame, text="목적을 재현", font=self.my_font)
		self.obj_label.grid(row=0, column=0, padx=10, pady=10)

		self.obj = CTkSegmentedButton(self.obj_frame, values=['독창성', 'AI탐지', 'AI(추가의)'])
		self.obj.set('독창성')
		self.obj.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def create_write_style(self):
		self.write_style_frame = CTkFrame(self)
		self.write_style_frame.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
		self.write_style_frame.columnconfigure(0, weight=1)
		self.write_style_frame.rowconfigure(0, weight=1)

		self.write_style_label = CTkLabel(self.write_style_frame, text="작문 스타일", font=self.my_font)
		self.write_style_label.grid(row=0, column=0, padx=10, pady=10)

		self.write_style = CTkEntry(self.write_style_frame, width = 200)
		self.write_style.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

	def update_method(self, value):
		if value == '고쳐쓰기':
			self.destroy_frames()
			self.create_strength()
			self.create_output_language(2)
			self.result_list.get('flag')
		elif value == '재창조':
			self.destroy_frames()
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
		self.repeat_num_frame.grid(row=2, column=1, sticky="nswe", padx=10, pady=10)
		self.repeat_num_frame.columnconfigure(0, weight=1)
		self.repeat_num_frame.rowconfigure(0, weight=1)

		self.repeat_num_label = CTkLabel(self.repeat_num_frame, text="반복 횟수", font=self.my_font)
		self.repeat_num_label.grid(row=0, column=0, padx=10, pady=10, sticky = 'w')

		self.repeat_num = CTkEntry(self.repeat_num_frame, font = self.my_font, width = 70)
		self.repeat_num.grid(row=0, column=1, padx=10, pady=5, sticky="w")

		self.name_label = CTkLabel(self.repeat_num_frame, text="작업 이름", font=self.my_font)
		self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky = 'w')

		self.name = CTkEntry(self.repeat_num_frame, font = self.my_font, width = 70)
		self.name.grid(row=1, column=1, padx=10, pady=5, sticky="w")

		self.add_button = CTkButton(self.repeat_num_frame, text="등록", width = 100)
		self.add_button.grid(row=0, column=2, rowspan = 2, padx=10, pady=10, sticky = "nsew")

		
	def create_result_list(self):
		self.result_frame = CTkScrollableFrame(self)
		self.result_frame.grid(row=0, column=2, columnspan=2, rowspan = 3, padx=10, pady=5, sticky = "nsew")
		
		self.result_frame.configure(width=250)
		self.result_frame.grid_propagate()

		self.result_frame.columnconfigure(0, weight=1)
		self.result_frame.rowconfigure(0, weight=1)

		self.result_list = []

	def add_to_list(self):
		repeat_num = self.repeat_num.get()
		name = self.name.get()
		method = self.method.get()
		strength = self.strength.get()
		output_language = self.output_language.get()
		before_file = self.selected_file_entry.get()
		template_file = self.selected_template_file_entry.get()

		task_frame = CTkFrame(self.result_frame)
		task_frame.grid(sticky="ew", padx=10, pady=5)
		task_frame.columnconfigure(0, weight=1)

		name_width = 20
		repeat_num_width = 5

		name_display = name.ljust(name_width)[:name_width]
		repeat_num_display = repeat_num.rjust(repeat_num_width)[:repeat_num_width]

		task_label = CTkLabel(task_frame, text=f"{name_display} {repeat_num_display}", font=self.my_font)
		task_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

		delete_button = CTkButton(task_frame, text="삭제", command=lambda: self.delete_task(task_frame), width = 20)
		delete_button.grid(row=0, column=1, padx=0, pady=5, sticky="e")

		self.result_list.append({
			"frame": task_frame,
			"repeat_num": repeat_num,
			"name": name,
			"method": method,
			"strength": strength,
			"output_language": output_language,
			"before_file": before_file,
			"template_file": template_file
		})

	def create_log(self):
		self.log_frame = CTkScrollableFrame(self)
		self.log_frame.grid(row=3, column=1, columnspan=3, rowspan=2, padx=10, pady=10, sticky="nswe")

		self.log_frame.columnconfigure(0, weight=1)
		self.log_frame.rowconfigure(0, weight=1)

		self.log_textbox = CTkTextbox(self.log_frame, state='disabled')
		self.log_textbox.grid(row=0, column=0, sticky="nswe")

	def delete_task(self, task_frame):
		for task in self.result_list:
			if task["frame"] == task_frame:
				task_frame.grid_forget()
				task_frame.destroy()
				self.result_list.remove(task)
				break