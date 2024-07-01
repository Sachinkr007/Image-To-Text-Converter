import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound

def upload_file():
    try:
        aws_mng_con = boto3.session.Session(profile_name='demo_user')
        client = aws_mng_con.client(service_name='textract', region_name='eu-central-1')

        filetypes = [('Image Files', '*.jpg;*.jpeg;*.png;*.bmp;*.tiff')]
        filename = filedialog.askopenfilename(filetypes=filetypes)

        if not filename:
            print("No file selected.")
            return

        img = Image.open(filename)

        # Resize image for display
        img.thumbnail((400, 200))
        img_tk = ImageTk.PhotoImage(img)

        img_label.config(image=img_tk)
        img_label.image = img_tk

        imgbytes = get_image_bytes(filename)
        response = client.detect_document_text(Document={'Bytes': imgbytes})
        extracted_text = ""
        for item in response['Blocks']:
            if item['BlockType'] == 'WORD':
                extracted_text += item['Text'] + " "
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, extracted_text)
        text_display.config(state=tk.DISABLED)

    except ProfileNotFound:
        print("The specified profile could not be found. Please check your AWS credentials and configuration.")
    except NoCredentialsError:
        print("Credentials not available. Please check your AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_image_bytes(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

# Create main window
my_w = tk.Tk()
my_w.geometry("600x500")
my_w.title("AWS Textract")

# Create and pack widgets
l1 = tk.Label(my_w, text="Upload an Image", width=30, font=('times', 18, 'bold'))
l1.pack(pady=10)

b1 = tk.Button(my_w, text='Upload File & See what it has!!', width=30, command=upload_file)
b1.pack(pady=10)

img_label = tk.Label(my_w)
img_label.pack(pady=10)

text_display = tk.Text(my_w, height=10, wrap='word', font=("Helvetica", 12), relief='solid', bd=2, state=tk.DISABLED)
text_display.pack(padx=10, pady=10, fill='both', expand=True)

my_w.mainloop()
