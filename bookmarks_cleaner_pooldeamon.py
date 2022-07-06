import codecs
import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import filedialog as fd
from concurrent.futures import ThreadPoolExecutor


# For selecting file name
root = tk.Tk()
root.withdraw()

# For identyfing the system - Clear Screen order
os.system('cls' if os.name == 'nt' else 'clear')

in_file = fd.askopenfilename(title='File to clean')

out_file = fd.askopenfilename(title='Target file')

soup = BeautifulSoup(codecs.open(in_file, encoding='utf-8'), "html.parser")
bookmarks_counter = {'goodone':0, 'deadone':0, 'expired':0}
good_bookmarks = []
with open(out_file, "w", encoding='utf-8') as o_file:
    def fetch_href(a):
        try:
            x = requests.get(a['href'], timeout=10)
            if x.status_code == 200:
                good_bookmarks.append(a['href'])
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
        print(bookmarks_counter)
    all_a = set(soup.find_all('a'))
    print(len(all_a))
    with ThreadPoolExecutor(20) as executor:
        futures = [executor.submit(fetch_href, i) for i in all_a]


print(bookmarks_counter)
