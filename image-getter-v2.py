"""
This version does not create subfolders in the image directory
"""

import os
import requests
import zipfile

import os
from pexels_api import API
import zipfile

PEXELS_API_KEY = "E9YgGcXpWtkSkpn6J1EeGY7b3AD8MJvJYy1DOsjwk36V3T5GSSqadyz9"
RANDOM_WORD_URL = "https://random-word-api.herokuapp.com/word?lang=en"

def getWord() -> str:
    try:
        response = requests.get(RANDOM_WORD_URL)
    except ConnectionError:
        print("Connection error")
    if response.status_code == 200:
        # try:
        word = response.json()[0] # Should account for JSONDecodeError
        # except JSONDecodeError:
        #    print("JSON Decode Error") 
    return word

def add_to_zip(zip_path, image_path):
    # Open zip file in append (write?) mode
    with zipfile.ZipFile(zip_path, 'a') as zip_file:
        # Add image to zip file
        zip_file.write(image_path, os.path.basename(image_path))


def getImages(word):
    api = API(PEXELS_API_KEY)
    api.search(word) #, page=1, results_per_page=2)

    while True:
        photos = api.get_entries() # Sometimes 
        if (api.total_results == 0):
            getImages(getWord())
        else:
            for photo in photos:
                url = photo.original
                data = requests.get(url).content
                image_name = f"{word}-{str(photo.id)}-{str(photo.width)}-{str(photo.height)}.jpg"
                try:
                    zipfile.ZipFile('images.zip', mode='w').write(data) 
                except ValueError:
                    print("Embedded null character in path...")

                # Use chatgpt to figure out how to add one file at a time to a zip file in Python


                

                save_dir = f"resources//pexels_imgs/"
                # zip_path = 'images.zip'
                # image_path = image_name
                # The zip file is automatically created
                # add_to_zip(zip_path=zip_path, image_path=image_path)
                # with zipfile.ZipFile(zip_path, 'w') as zip_file:
                #     if not os.path.exists(image_path):
                #         os.makedirs(image_path)
                #     zip_file.write(image_path, os.path.basename(image_path))

                # How to write a single file to a zip file? (In order to write multiple 
                # files one a time to the zip file?)

                # if not os.path.exists(save_dir):
                #     os.makedirs(save_dir)

                # with open(f"{save_dir}//{image_name}", "wb") as f:
                #     f.write(data)
                #     f.close()

            if not api.has_next_page:
                print("Last page: ", api.page)
                break
            else:
                api.search_next_page()
                print("Last page reached. Searching next page...")

getImages(getWord())
      
# # Example usage 
# zip_path = 'images.zip'
# image_paths = [] # Append each image to this list with a for loop
# for image_path in image_paths:
#     add_to_zip(zip_path=zip_path, image_path=image_path)



