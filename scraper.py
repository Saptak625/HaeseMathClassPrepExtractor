from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
from io import BytesIO

from time import sleep
import os
import sys
import getpass

def scrape(classprepPages):
    username = input('Enter username: ')
    password = getpass.getpass()
    print(password)

    # Setup Selenium
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get('https://snowflake.haesemathematics.com.au/viewer/mathematics-analysis-and-approaches-hl/book/ibhl-aaa-2/1')
    print('Opened Page...')

    # Login
    # To catch <input type="text" id="passwd" />
    usernameField = driver.find_element(By.ID, "user_email")
    # To catch <input type="text" name="passwd" />
    passwordField = driver.find_element(By.ID, "user_password")

    usernameField.send_keys(username)
    passwordField.send_keys(password)

    try:
        driver.find_element(By.NAME, "button").click()

        if driver.current_url != 'https://snowflake.haesemathematics.com.au/viewer/mathematics-analysis-and-approaches-hl/book/ibhl-aaa-2/1':
            raise Exception('Login Failed: Invalid email or password.')
        print('Logged in...')
    except Exception as e:
        print(e)
        sys.exit()

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

    # Get pages
    pagesRead = []
    for _, pages, _ in classprepPages:
        for i in pages:
            if i not in pagesRead:
                get_page(i)
                pagesRead.append(i)

    # Close browser
    driver.quit()
    print('Finished Scraping')