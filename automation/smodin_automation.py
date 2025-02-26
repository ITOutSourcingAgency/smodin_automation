import time, clipboard, platform, os, sys, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager

class TemplateFileNotFoundException(Exception):
    pass

class SmodinAutomation:
	def __init__(self, settings):
		self.settings = settings

	def run(self):
		# driver_path = ChromeDriverManager().install()
		chrome_options = webdriver.ChromeOptions()
		
		# Chrome automation detection prevention
		chrome_options.add_argument("--lang=ko-KR")
		chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		chrome_options.add_argument("--disable-infobars")
		chrome_options.add_argument("--disable-save-password-bubble")
		chrome_options.add_argument("--disable-password-manager-reauthentication")
		# chrome_options.add_argument("--incognito")

		# self.driver = uc.Chrome(options=chrome_options, driver_executable_path=driver_path)
		self.driver = uc.Chrome(options=chrome_options)

		self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
			"source": """
				Object.defineProperty(navigator, 'webdriver', {
					get: () => undefined
				});
			"""
		})

		try:
			actions = ActionChains(self.driver)
			self.settings.add_log("로그인을 진행합니다")
			self.login(actions=actions)

			for one_setting in self.settings.result_list:
				self.settings.add_log(f"{one_setting['name']} 작업의 자동화를 시작합니다.")
				for one_file in one_setting['selected_files']:
					# self.select_options_free(actions, one_setting, one_file)
					self.select_options_paid(actions, one_setting, one_file)
					time.sleep(random.uniform(10, 20))

				self.driver.get('https://app.smodin.io/ko')
		except TemplateFileNotFoundException as e:
			self.settings.add_log(str(e), "red")
		except Exception as e:
			self.settings.add_log("프로그램을 강제 종료 하셨거나 오류가 발생했습니다.", "red")
		finally:
			self.settings.add_log("자동화 작업을 종료합니다.", "grey")
			self.settings.submit_button.configure(state='normal')

			self.driver.quit()

	def login(self, actions):
		max_retries = 5
		retries = 0
		
		while retries < max_retries:
			try:
				self.driver.get('https://app.smodin.io/ko/login')
				main_window = self.driver.current_window_handle
				google_login_button = WebDriverWait(self.driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div/button'))
				)
				print(f"1. Current window handles: {self.driver.window_handles}")
				google_login_button.click()
				print(f"2. Current window handles: {self.driver.window_handles}")
				WebDriverWait(self.driver, 10).until(EC.new_window_is_opened([main_window]))
				all_windows = self.driver.window_handles

				for window in all_windows:
					if window != main_window:
						self.driver.switch_to.window(window)
						break
				login_window_handles = self.get_visible_windows()

				id_input = WebDriverWait(self.driver, timeout=10).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'))
				)
				id_input.click()
				clipboard.copy(self.settings.id.get())
				
				if platform.system() == 'Darwin':  
					actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
				else:
					actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

				id_submit_button = WebDriverWait(self.driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
				)
				id_submit_button.click()

				pw_input = WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'))
				)
				pw_input.click()
				clipboard.copy(self.settings.pw.get())

				if platform.system() == 'Darwin':  
					actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
				else:
					actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

				pw_submit_button = WebDriverWait(self.driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button'))
				)
				pw_submit_button.click()
				print(f"Initial visible window count: {len(login_window_handles)}")
				print(f"3. Current visible window handles: {login_window_handles}")

				if len(login_window_handles) > 1:
					print(f'len = {len(login_window_handles)}')
					start_time = time.time()
					max_wait_time = 300

					while time.time() - start_time < max_wait_time:
						tmp_window_handles = self.driver.window_handles
						print(f'tmp_window_handles = {tmp_window_handles}')
						
						if len(tmp_window_handles) <= 2:
							break
						time.sleep(1)
				time.sleep(2)
				self.driver.switch_to.window(main_window)
				time.sleep(2)

				break  # 성공적으로 로그인하면 루프 종료
				
			except Exception as e:
				self.settings.add_log(f"로그인 도중에 에러가 발생했습니다.", "red")
				retries += 1

				all_windows = self.driver.window_handles
				for window in all_windows:
					if window != main_window:
						self.driver.switch_to.window(window)
						self.driver.close()

				self.driver.switch_to.window(main_window)

				if retries < max_retries:
					self.settings.add_log(f"로그인을 다시 시도합니다.")
				else:
					self.settings.add_log(f"로그인이 지속해서 실패하고 있습니다. 프로그램을 종료하고 다시 실행해주세요.", "blue")


	def get_visible_windows(self):

		visible_windows = []
		original_window = self.driver.current_window_handle

		for handle in self.driver.window_handles:
			try:
				self.driver.switch_to.window(handle)
				time.sleep(1)  # Allow time for the window to load

				if "about:blank" not in self.driver.current_url and self.driver.title.strip():
					visible_windows.append(handle)
			except Exception as e:
				print(f"Error switching to window {handle}: {e}")

		self.driver.switch_to.window(original_window)  # Return to the original window
		return visible_windows



	# def get_visible_windows(self):
	# 	"""
	# 	현재 보이는 창만 필터링하는 함수.
	# 	- `about:blank` 같은 빈 창은 제외
	# 	- 타이틀이 없거나 정상적으로 로드되지 않은 창은 제외
	# 	"""
	# 	visible_windows = []
	# 	for handle in self.driver.window_handles:
	# 		try:
	# 			self.driver.switch_to.window(handle)
	# 			time.sleep(1)
				
	# 			if "about:blank" not in self.driver.current_url and self.driver.title.strip():
	# 				visible_windows.append(handle)
	# 		except Exception as e:
	# 			print(f"Error switching to window {handle}: {e}")

	# 	return visible_windows

	def select_options_paid(self, actions, one_setting, one_file):
		try:
			self.driver.get('https://app.smodin.io/ko/%E1%84%86%E1%85%AE%E1%84%85%E1%85%AD%E1%84%85%E1%85%A9%E1%84%92%E1%85%A1%E1%86%AB%E1%84%80%E1%85%AE%E1%86%A8%E1%84%8B%E1%85%A5%E1%84%85%E1%85%A9%E1%84%90%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%8C%E1%85%A1%E1%84%83%E1%85%A9%E1%86%BC%E1%84%87%E1%85%A5%E1%86%AB%E1%84%8B%E1%85%A7%E1%86%A8')


			if one_setting['selected_method'] == 0:
				WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div/button[1]'))
				).click()
				match one_setting['strength']:
					case 1:
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/span/span[4]'))
						).click()
					case 2:
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/span/span[6]'))
						).click()
					case 3:
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/span/span[8]'))
						).click()
					case 4:
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/span/span[10]'))
						).click()
			else:
				WebDriverWait(self.driver, 20).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/div[1]/div/button[2]'))
				).click()
				
				match one_setting['obj']:
					case '독창성':
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/span/span[4]/span'))
						).click()
					case 'AI탐지':
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/span/span[6]/span'))
						).click()
					case 'AI(추가의)':
						WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/span/span[8]/span'))
						).click()

				if len(one_setting['write_style']) >= 1:
					write_style_input = WebDriverWait(self.driver, 20).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div/input'))
					)
					write_style_input.click()
					clipboard.copy(one_setting['write_style'])
					
					if platform.system() == 'Darwin':  
						actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
					else:
						actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
		except Exception as e:
			print(f"An error occurred: {e}")
		
		text_input = WebDriverWait(self.driver, 20).until(
			EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[3]/div/div/div/div[1]/div/div[2]/div/div/div/textarea[1]'))
		)
		text_input.click()

		with open(one_file, 'r', encoding='utf-8') as file:
			clipboard.copy(file.read())

		if platform.system() == 'Darwin':  
			actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
		else:
			actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

		for i in range(int(one_setting['repeat_num'])):
			rewrite_submit_button = WebDriverWait(self.driver, 60).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[1]/div/div[2]/div[2]/div/div/div/button'))
			)
			rewrite_submit_button.click()
			self.settings.add_log("재창조 버튼 클릭 완료")

			time.sleep(5)
			try:
				print('복사 버튼 누름름')
				# copy_button = WebDriverWait(self.driver, 20).until(
				# 	# EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[5]/div/div[3]/button[4]'))
				# 	EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/form/div/div[5]/div/div[3]/button[4]'))
				# )
				copy_button = WebDriverWait(self.driver, 20).until(
					EC.element_to_be_clickable((
						By.XPATH, "//button[contains(@class, 'MuiButtonBase-root') and contains(@class, 'MuiFab-root')][.//p[text()='복사']]"
					))
				)

				copy_button.click()
				print('파일 처리 시작작')
				self.settings.add_log("파일 처리 시작")
				self.modify_file_with_template(clipboard.paste(), one_setting, i, one_file)
			except TemplateFileNotFoundException:
				raise TemplateFileNotFoundException(f"{os.path.basename(rf'{one_file}')} 파일에 대한 템플릿 파일이 존재하지 않습니다.")
			except Exception as e:
				self.settings.add_log(f"글 변환 실패, 재시도")
				self.select_options_paid(actions, one_setting, one_file)
	
	
	def element_to_be_clickable_or_present(locator1, locator2):
		def _predicate(driver):
			elements1 = driver.find_elements(*locator1)
			if elements1:
				return elements1[0]
			elements2 = driver.find_elements(*locator2)
			if elements2:
				return elements2[0]
			return False
		return _predicate

	def select_options_free(self, actions, one_setting, one_file):
		self.driver.get('https://app.smodin.io/ko/%E1%84%86%E1%85%AE%E1%84%85%E1%85%AD%E1%84%85%E1%85%A9%E1%84%92%E1%85%A1%E1%86%AB%E1%84%80%E1%85%AE%E1%86%A8%E1%84%8B%E1%85%A5%E1%84%85%E1%85%A9%E1%84%90%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3%E1%84%8C%E1%85%A1%E1%84%83%E1%85%A9%E1%86%BC%E1%84%87%E1%85%A5%E1%86%AB%E1%84%8B%E1%85%A7%E1%86%A8')

		if one_setting['selected_method'] == 0:
			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/button[1]'))
			).click()
			match one_setting['strength']:
				case 1:
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/span/span[3]'))
					).click()
				case 2:
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/span/span[5]'))
					).click()
				case 3:
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/span/span[7]'))
					).click()
				case 4:
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/span/span[9]'))
					).click()
		else:
			WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[1]/div/div[2]/div/button[2]'))
			).click()
			match one_setting['obj']:
				case '독창성':
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[4]'))
					).click()
				case 'AI탐지':
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[6]'))
					).click()
				case 'AI(추가의)':
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[8]'))
					).click()
			if len(one_setting['write_style']) >= 1:
				write_style_input = WebDriverWait(self.driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div/input'))
				)
				write_style_input.click()
				clipboard.copy(one_setting['write_style'])
				
				if platform.system() == 'Darwin':  
					actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
				else:
					actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
		
		text_input = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[3]/div/div/div/div[2]/div/div/div/textarea[1]'))
		)
		text_input.click()

		with open(one_file, 'r', encoding='utf-8') as file:
			clipboard.copy(file.read())

		if platform.system() == 'Darwin':  
			actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
		else:
			actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

		for i in range(int(one_setting['repeat_num'])):
			rewrite_submit_button = WebDriverWait(self.driver, 60).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[2]/div/div/button'))
			)
			rewrite_submit_button.click()
			self.settings.add_log("재창조 버튼 클릭 완료")

			try:
				WebDriverWait(self.driver, 40).until(
					EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[5]/div/div[2]/button[4]'))
				).click()
				self.settings.add_log("파일 처리 시작")
				self.modify_file_with_template(clipboard.paste(), one_setting, i, one_file)

			except Exception as e:
				self.settings.add_log(f"글 변환 실패")
				self.select_options_free(actions, one_setting, one_file)
	def modify_file_with_template(self, content, one_setting, index, one_file):
		splitted_texts = content.split('.')
		total_sentences = len(splitted_texts) - 1
		template_content = ''

		try:
			try:
				if '.txt' not in os.path.basename(rf'{one_setting["template_folder"]}'):
					matched_template_file = os.path.join(rf'{one_setting["template_folder"]}', os.path.basename(rf'{one_file}'))
					with open(rf'{matched_template_file}', 'r', encoding='utf-8') as template_file:
						template_content = template_file.read()
						print(f"Template loaded from file: {matched_template_file}")
				else:
					with open(rf'{one_setting["template_folder"]}', 'r', encoding='utf-8') as template_file:
						template_content = template_file.read()
						print(f"Template loaded from folder: {one_setting['template_folder']}")
			except FileNotFoundError as e:
				print(f"Template file not found: {e}")
				raise TemplateFileNotFoundException()

			inquote_count = template_content.count('<인용구')
			print(f"Number of <인용구> placeholders: {inquote_count}")

			sentences_per_chunk = total_sentences // inquote_count
			print(f"Sentences per chunk: {sentences_per_chunk}")

			chunks = []
			tmp = ''
			count = 0
			for text in splitted_texts:
				if len(text.strip()) == 0:
					continue
				tmp += f'{text}.'
				count += 1
				if count % sentences_per_chunk == 0:
					chunks.append(tmp.strip())
					tmp = ''

			if tmp:
				chunks.append(tmp.strip())

			print(f"Generated chunks: {chunks}")

			first_inquote_idx = template_content.find('<인용구')
			remaining_chunks = chunks.copy()
			search_start_idx = first_inquote_idx + 1
			while remaining_chunks and search_start_idx < len(template_content):
				next_inquote_idx = template_content.find('<인용구', search_start_idx)
				if next_inquote_idx == -1:
					break

				chunk = remaining_chunks.pop(0)
				print(f"Inserting chunk at position {next_inquote_idx}: {chunk}")
				template_content = template_content[:next_inquote_idx] + chunk + '\n\n' + template_content[next_inquote_idx:]
				search_start_idx = template_content.find('>\n', next_inquote_idx + len(chunk))

			if remaining_chunks:
				last_placeholder_idx = max(template_content.rfind('<인용구'), template_content.rfind('}>\n<랜덤슬라이드'))
				if last_placeholder_idx != -1:
					last_placeholder_idx += 3
					end_of_last_inquote_idx = template_content.find('>', last_placeholder_idx) + 1
					next_line_start_idx = end_of_last_inquote_idx
					while next_line_start_idx < len(template_content) and template_content[next_line_start_idx] in ['\n', ' ']:
						next_line_start_idx += 1

					insertion_idx = next_line_start_idx
					print(f"Inserting remaining chunks at position {insertion_idx}: {remaining_chunks}")
					template_content = template_content[:insertion_idx] + '\n\n'.join(remaining_chunks).strip() + '\n\n' + template_content[insertion_idx:]
				else:
					print("Appending remaining chunks at the end of the template")
					template_content += '\n\n' + '\n\n'.join(remaining_chunks).strip()

			tmp_index = ''
			if index == 0:
				tmp_index = '.txt'
			else:
				tmp_index = f'_{index}.txt'

			output_origin_file_name = os.path.basename(rf'{one_file}').replace('.txt', tmp_index)
			output_origin_directory = os.path.join(get_script_path(), 'srcs', '결과원본파일')
			if not os.path.exists(output_origin_directory):
				os.makedirs(output_origin_directory)
				print(f"Created directory: {output_origin_directory}")
			output_origin_file_path = rf'{os.path.join(output_origin_directory, output_origin_file_name)}'

			with open(output_origin_file_path, 'w', encoding='utf-8') as modified_origin_file:
				modified_origin_file.write(content)
				print(f"Saved original file content to: {output_origin_file_path}")

			self.settings.add_log(f"{one_setting['name']} 작업의 자동화 결과물의 원본이 {output_origin_file_name}의 이름으로 저장되었습니다.", "green")

			output_file_name = os.path.basename(rf'{one_file}').replace('.txt', tmp_index)
			output_directory = os.path.join(get_script_path(), 'srcs', '결과파일')
			if not os.path.exists(output_directory):
				os.makedirs(output_directory)
				print(f"Created directory: {output_directory}")
			output_file_path = rf'{os.path.join(output_directory, output_file_name)}'

			with open(output_file_path, mode='w', encoding='utf-8') as modified_file:
				modified_file.write(template_content)
				print(f"Saved modified content to: {output_file_path}")

			self.settings.add_log(f"{one_setting['name']} 작업의 자동화 결과물이 {output_file_name}의 이름으로 저장되었습니다.", "green")

		except Exception as e:
			print(f"An error occurred: {e}")
			raise



@staticmethod
def get_script_path():
	if getattr(sys, 'frozen', False):
		script_path = os.path.dirname(sys.executable)
	else:
		script_path = os.path.dirname(os.path.abspath(__file__))
	return script_path