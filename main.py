import gui.app
import asyncio
import logging

# logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), 'error.log'), level=logging.DEBUG)

def main():
	try:
		app = gui.app.App()
		app.mainloop()
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
	try:
		print("main gogogo")
		asyncio.run(main())
		print("main clear")
	except Exception as e:
		print(f"The error = {e}")
		# logging.exception("An error occurred:")
		# input("An error occurred. Press Enter to exit...")