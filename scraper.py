from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
from io import BytesIO

from time import sleep

import os

import getpass

username = '24sdas@student.dasd.org'
password = getpass.getpass()
print(password)

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://snowflake.haesemathematics.com.au/viewer/mathematics-analysis-and-approaches-hl/book/ibhl-aaa-2/1')
print('Opened Page...')

# Login
# To catch <input type="text" id="passwd" />
usernameField = driver.find_element(By.ID, "user_email")
# To catch <input type="text" name="passwd" />
passwordField = driver.find_element(By.ID, "user_password")

usernameField.send_keys(username)
passwordField.send_keys(password)

driver.find_element(By.NAME, "button").click()
print('Logged in...')

# Setup Files
# Remove old files
if os.path.exists('pages'):
    for file in os.listdir('pages'):
        os.remove(os.path.join('pages', file))
else:
    os.makedirs('pages')

# Navigate to new page
def get_page(page):
    print('\nGetting page', page)
    driver.get(f'https://snowflake.haesemathematics.com.au/viewer/mathematics-analysis-and-approaches-hl/book/ibhl-aaa-2/{page}')
    sleep(3)
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    cover = driver.find_element(By.ID, 'cover0')
    location = cover.location
    size = cover.size

    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(f'pages/{page}.png') # saves new cropped image
    print('Saved page', page)

# Read classprep.txt
classprepPages = []
with open('classprep.txt', 'r') as f:
    for line in f:
        if line == '\n':
            continue
        s = line.split(' - ')
        exercise_page = s[0].split('(pg')
        exercise = exercise_page[0].strip(' ')
        page = exercise_page[1].strip('). ')
        if '-' in page:
            page = page.split('-')
            page = [int(i) for i in page]
            page = list(range(page[0], page[1] + 1))
        else:
            page = [int(page)]
        questions = s[1].split(', ')
        classprepPages.append((exercise, page, questions))

# Get pages
pagesRead = []
for _, pages, _ in classprepPages:
    for i in pages:
        if i not in pagesRead:
            get_page(i)
            pagesRead.append(i)

# Close browser
driver.quit()
print('Finished')