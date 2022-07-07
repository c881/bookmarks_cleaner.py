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

in_file = fd.askopenfilename(title='File to clean')

out_file = fd.askopenfilename(title='Target file')

soup = BeautifulSoup(codecs.open(in_file, encoding='utf-8'), "html.parser")
bookmarks_counter = {'goodone':0, 'deadone':0, 'expired':0}
with open(out_file, "w", encoding='utf-8') as o_file:
    def fetch_href(a):
        try:
            x = requests.get(a['href'],timeout=15)
            if x.status_code == 200:
                bookmarks_counter['goodone'] += 1
                o_file.write(f"<a href=\"{a['href']}\" target=\"_blank\">{bookmarks_counter['goodone']}. {a.text}</a><br>")
                print('.', end='')
            else:
                bookmarks_counter['deadone'] += 1
                print('\n')
        except (requests.exceptions.Timeout, requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError, requests.exceptions.InvalidSchema):
            bookmarks_counter['expired'] += 1
            print('\t')
    all_a = soup.find_all('a')
    print(len(all_a))
    with ThreadPool(20) as pool:
        pool.map(fetch_href, all_a, chunksize=1)


print(bookmarks_counter)
