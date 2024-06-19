import gui.app
import asyncio

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