from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import time
import pyperclip

class SmodinAutomation:
	def __init__(self, settings):
		self.settings = settings

	def run(self):
		self.driver = uc.Chrome()

		# 추가적인 자동화 감지 방지 설정
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
			print(f"An error occurred: {e}")
		finally:
			self.driver.quit()

	
	def login(self):
		self.driver.get('https://app.smodin.io/ko/login')

		google_login_button = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div/button'))
		)
		google_login_button.click()

		# id_input = WebDriverWait(self.driver, 10).until(
		# 	EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'))
		# )
		# id_input.click()

		actions = ActionChains(self.driver)
		time.sleep(100)