import codecs
import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog as fd
from multiprocessing.pool import ThreadPool


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

with open(out_file, "w", encoding='utf-8') as o_file:
    def fetch_href(a):
        try:
            x = requests.get(a['href'])
            if x.status_code == 200:
                print('found One')
                o_file.write(f"<a href=\"{a['href']}\">{a.text}</a><br>")
            else:
                print('A dead one')
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema):
            print('Excepted 1')
    all_a = soup.find_all('a')
    with ThreadPool(20) as pool:
        pool.map(fetch_href, all_a, chunksize=1)
