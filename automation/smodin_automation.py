import time, clipboard, platform, os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

class SmodinAutomation:
	def __init__(self, settings):
		self.settings = settings

	def run(self):
		chrome_options = webdriver.ChromeOptions()
		
		# Chrome automation detection prevention
		chrome_options.add_argument("--lang=ko-KR")
		chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		chrome_options.add_argument("--disable-infobars")
		chrome_options.add_argument("--disable-save-password-bubble")
		chrome_options.add_argument("--disable-password-manager-reauthentication")

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
				self.select_options(actions, one_setting)
				self.driver.get('https://app.smodin.io/ko')

		except Exception as e:
			self.settings.add_log("프로그램을 강제 종료 하셨거나 오류가 발생했습니다.", "red")
			print(f"An error occurred during login: {e}")
		finally:
			# time.sleep(500)
			self.settings.add_log("자동화 작업을 종료합니다.", "grey")
			self.driver.quit()

	def login(self, actions):
		self.driver.get('https://app.smodin.io/ko/login')
		
		try:
			main_window = self.driver.current_window_handle
			google_login_button = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div/button'))
			)
			google_login_button.click()
			WebDriverWait(self.driver, 10).until(EC.new_window_is_opened([main_window]))
			all_windows = self.driver.window_handles

			for window in all_windows:
				if window != main_window:
					self.driver.switch_to.window(window)
					break

			id_input = WebDriverWait(self.driver, 10).until(
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

			pw_input = WebDriverWait(self.driver, 60).until(
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
			self.driver.switch_to.window(main_window)

		except Exception as e:
			print(f"An error occurred during the login process: {e}")

	def select_options(self, actions, one_setting):
		rewrite_button = WebDriverWait(self.driver, 60).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/main/div/div/div[2]/div/div/div[3]/div/div/div[1]/a'))
		)
		rewrite_button.click()

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
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[3]'))
					).click()
				case 'AI탐지':
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[5]'))
					).click()
				case 'AI(추가의)':
					WebDriverWait(self.driver, 10).until(
						EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span/span[7]'))
					).click()
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

		with open(one_setting['selected_file'], 'r', encoding='utf-8') as file:
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
			
			result_copy_button = WebDriverWait(self.driver, 120).until(
				EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/main/div/form/div/div[5]/div/div[2]/button[4]'))
			)
			result_copy_button.click()
			self.modify_file_with_template(clipboard.paste(), one_setting, i)
	
	def modify_file_with_template(self, content, one_setting, index):
		splitted_texts = content.split('.')
		chunks = []
		count = 0
		tmp = ''
		for text in splitted_texts:
			tmp += f'{text}.'
			count += 1
			if count % 5 == 0:
				chunks.append(tmp)
				tmp = ''

		with open(rf'{one_setting["template_file"]}', 'r', encoding='utf-8') as template_file:
			template_content = template_file.read()

		first_inquote_idx = template_content.find('<인용구')
		remaining_chunks = chunks.copy()

		search_start_idx = first_inquote_idx + 1
		while remaining_chunks:
			next_inquote_idx = template_content.find('<인용구', search_start_idx)
			if next_inquote_idx == -1:
				break

			chunk = remaining_chunks.pop(0)

			template_content = template_content[:next_inquote_idx] + chunk.strip() + '\n\n' + template_content[next_inquote_idx:]
			search_start_idx = template_content.find('>\n', next_inquote_idx + len(chunk.strip()))

		if remaining_chunks:
			last_placeholder_idx = template_content.rfind('}>')
			if last_placeholder_idx != -1:
				template_content = template_content[:last_placeholder_idx+2] + '\n\n' + '\n\n'.join(remaining_chunks).strip() + template_content[last_placeholder_idx+2:]
			else:
				template_content += '\n\n' + '\n\n'.join(remaining_chunks).strip()

		output_file_name = os.path.basename(rf'{one_setting["selected_file"]}').replace('.txt', f'_{index}.txt')
		print(f'output_file_name = {output_file_name}')
		output_directory = os.path.join(get_script_path(), 'srcs', '결과파일')
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)
		output_file_path = rf'{os.path.join(output_directory, output_file_name)}'

		print(f'output_file_path = {output_file_path}')

		with open(output_file_path, 'w', encoding='utf-8') as modified_file:
			modified_file.write(template_content)
		self.settings.add_log(f"{one_setting['name']} 작업의 자동화 결과물이 {output_file_name}의 이름으로 저장되었습니다.", "green")

@staticmethod
def get_script_path():
	if getattr(sys, 'frozen', False):
		script_path = os.path.dirname(sys.executable)
	else:
		script_path = os.path.dirname(os.path.abspath(__file__))
	return script_path