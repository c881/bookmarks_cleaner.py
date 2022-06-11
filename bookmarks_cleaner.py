import codecs
import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog as fd

# For selecting file name
root = tk.Tk()
root.withdraw()

# For identyfing the system - Clear Screen order
os.system('cls' if os.name == 'nt' else 'clear')

print('Please select a Bookmarks file to clean: ')
in_file = fd.askopenfilename()

print('Please select a Target file: ')
out_file = fd.askopenfilename()

soup = BeautifulSoup(codecs.open(in_file, encoding='utf-8'), "html.parser")
counter = 1
g_counter = 1
with open(out_file,"w", encoding='utf-8') as o_file:
    for a in soup.find_all('a'):
        print(f"{counter}Found the URL:{a['href']}")
        counter += 1
        try:
            x = requests.get(a['href'])
            if x.status_code < 400:
                print(f"URL still alive")
                o_file.write(f"{g_counter}. <a href=\"{a['href']}\">{a.text}</a><br>")
                g_counter += 1
            else:
                print(f"URL died")
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            print("An exception occurred")
        except requests.exceptions.InvalidSchema:
            print("InvalidSchema")
