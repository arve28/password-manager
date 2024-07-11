import json
import random
import re
import sys
import bcrypt
import customtkinter
import colorsys
from cryptography.fernet import Fernet
from dotenv import load_dotenv, dotenv_values
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph

SECOND = 1000
MINUTE = 60000


def resource_path(relative_path):
    """https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file"""
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(hashed_password: str, provided_password: str) -> bool:
    # Verify the provided password against the hashed password
    return bcrypt.checkpw(provided_password.encode("utf-8"), hashed_password.encode("utf-8"))


def center_window(root: customtkinter.CTk, width: int, height: int):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window
    root.geometry(f"{width}x{height}+{x}+{y}")


def adjust_brightness(hex_color, factor=.9) -> str:
    # Convert hex to RGB
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Convert RGB to HLS
    hue, lightness, saturation = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # Adjust the lightness
    adjusted_lightness = lightness * factor

    # Convert HLS back to RGB
    r, g, b = colorsys.hls_to_rgb(hue, adjusted_lightness, saturation)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    # Convert RGB back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


def load_config():
    with open(resource_path("config\\config.json"), "r") as f:
        return json.load(f)


def update_config(data):
    with open(resource_path("config\\config.json"), "w") as f:
        json.dump(data, f, indent=2)


def generate_key() -> str:
    """Generates cipher key"""
    return Fernet.generate_key().decode()


# Function to encrypt a string
def encrypt(data: str, key: str) -> str:
    """Encrypts data."""
    cipher_suite = Fernet(key)
    encoded_data = data.encode("utf-8")
    encrypted_data = cipher_suite.encrypt(encoded_data)
    return encrypted_data.decode("utf-8")


# Function to decrypt a string
def decrypt(encrypted_data: str, key: str) -> str:
    """Decrypts data."""
    cipher_suite = Fernet(key)
    decoded_encrypted_data = encrypted_data.encode("utf-8")
    decrypted_data = cipher_suite.decrypt(decoded_encrypted_data)
    return decrypted_data.decode("utf-8")


# Function to write a new key-value pair to the .env file
def add_env_key(key: str, value: str):
    # Read the existing .env file
    env_file_path = resource_path(".env")
    env_values = dotenv_values(env_file_path)

    # Check if the key already exists
    if key not in env_values:
        with open(env_file_path, "a") as env_file:
            env_file.write(f"\n{key}={value}")

        load_dotenv(override=True)


def generate_password() -> str:
    letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    symbols = ('!', '#', '$', '%', '&', '(', ')', '*', '+')

    nr_letters = random.randint(10, 12)
    nr_symbols = random.randint(4, 6)
    nr_numbers = random.randint(4, 6)

    password = [random.choice(letters) for _ in range(nr_letters)]
    password.extend([random.choice(symbols) for _ in range(nr_symbols)])
    password.extend([random.choice(numbers) for _ in range(nr_numbers)])

    random.shuffle(password)
    password = "".join(password)
    return password


def generate_pdf(filename, data, title, user_password):
    # Set up encryption
    encryption = StandardEncryption(userPassword=user_password, canPrint=1)

    # Create the document with encryption
    c = canvas.Canvas(filename, pagesize=A4, encrypt=encryption)

    # Set up the styles
    styles = getSampleStyleSheet()
    style_title = styles['Title']

    # Title
    title_paragraph = Paragraph(title, style_title)
    title_paragraph.wrapOn(c, A4[0] - 2 * inch, A4[1] - 2 * inch)
    title_paragraph.drawOn(c, inch, A4[1] - 1.5 * inch)

    # Calculate the number of tables needed
    rows_per_table = 25
    number_of_tables = (len(data) + rows_per_table - 1) // rows_per_table

    for table_index in range(number_of_tables):
        # Calculate the start and end row indices for the current table
        start_row = table_index * rows_per_table
        end_row = min(start_row + rows_per_table, len(data))

        # Create the table with the current subset of rows
        table_data = data[start_row:end_row]
        table = Table(table_data)

        # Style the table
        style = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Bottom padding to add space below text
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Calculate table position for centering on the x-axis
        table_width, table_height = table.wrap(0, 0)
        x_position = (A4[0] - table_width) / 2
        y_position = A4[1] - table_height - (2 * inch if table_index == 0 else inch)  # Adjust y_position for the title

        # Add the table to the elements
        table.drawOn(c, x_position, y_position)

        # If it's not the last table, create a new page
        if table_index < number_of_tables - 1:
            c.showPage()

    # Save the PDF
    c.save()


def delete_file(filename):
    """Delete the specified file."""
    try:
        os.remove(filename)
        print(f"File {filename} has been deleted successfully.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except PermissionError:
        print(f"Permission denied: unable to delete {filename}.")
    except Exception as e:
        print(f"An error occurred while trying to delete {filename}: {e}")
