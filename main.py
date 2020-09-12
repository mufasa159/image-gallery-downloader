"""
Image Gallery Downloader || By Muhfasul Alam
Originally created on September 11th, 2020
"""

# Importing all the necessary modules
import requests
from bs4 import BeautifulSoup
import re
import ssl
import shutil
import random
# import wget

# Not quite sure what this line does, but it fixed the error I was getting. #stackoverflow
ssl._create_default_https_context = ssl._create_unverified_context

# Copy and paste the url of the page in `url` variable.
url = ""

"""
You can leave the `folder` variable blank if you want. If not, make sure the folder name matches the actual folder.
Do not put directory path here. Only put the folder name.
"""
folder = ""

# Getting all the html texts from the page
html = requests.get(url)
bs = BeautifulSoup(html.text, 'html.parser')

"""
Finds all the links and matches the ones with .jpg. Then saves it to `images` list.
You can change the elements and/or file extension to catch whatever type of images you're trying to download.
"""
images = bs.find_all('a', {'href': re.compile('.jpg')})

# List of letters for image renaming purpose
letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def download_image(image):
    """
    Generates a random 4 letters word and adds to the filename to avoid file replacing with the same name.
    Without the `x` any existing file with the same name will automatically be replaced by the new downloaded image.
    """
    x = str(random.choice(letter) + random.choice(letter) + random.choice(letter) + random.choice(letter))

    """
    Variable 'id' takes the folder name and adds it before the original image name. 
    Feel free to change it based on how you want the downloaded images to be named
    """
    id = folder.replace(" ", "") + "-" + x

    # Name of the downloaded image
    realname = id + "-" + image['href'].split('/')[-1]

    """
    This is the path of the image (including the image itself).
    You can change the location of where you want the file to save.
    """
    path = "/Users/username/Downloads/" + folder + "/" + realname

    """
    Some websites block wget requests, so I used shutil module for downloading.
    But wget makes the code simple and small. If you want to use wget, then uncomment the following line.
    Also, don't forget to uncomment its import on top.
    """
    # file = wget.download(image['href'], path)

    """
    If you chose to use wget module for downloading, then comment out everything below this line until the `for` loop.
    """
    r = requests.get((image['href']), stream=True)

    """
    Sometimes BeautifulSoup catches url without domain name (https://www.website.com) in the link, which gives an error.
    If that happens comment out the line above and uncomment the following line. 
    Make sure you use appropriate link in place of `https://` based on the given error.
    """
    # r = requests.get(("https://" + image['href']), stream=True)

    # If the request to the image url is successful, it will download the image.
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


# It will go through all the specific type of image links it found in the page and download each one of them.
for i in range(0, len(images)):
    download_image(images[i])
