from src.libraries.password_manager import PasswordManager
from dotenv import load_dotenv

load_dotenv()
app = PasswordManager()

if __name__ == "__main__":
    try:
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
