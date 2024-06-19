import time, clipboard, platform
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
			self.login()
		except Exception as e:
			print(f"An error occurred during login: {e}")
		finally:
			time.sleep(500)
			self.driver.quit()

	def login(self):
		self.driver.get('https://app.smodin.io/ko/login')
		actions = ActionChains(self.driver)
		
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

			pw_input = WebDriverWait(self.driver, 10).until(
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
