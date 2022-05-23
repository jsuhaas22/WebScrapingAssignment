#NOTE: Since I do not have PostgreSQL installed and cannot install it, I am outputting the information
# that I parse on to the console. Just to have some output for me and evaluators to examine

from selenium import webdriver
import requests
import os
import time 

#initializing the web driver
driver = webdriver.Chrome()
driver.get('https://www.ranker.com/crowdranked-list/the-most-influential-people-of-all-time?ref=list_item_rl&rlf=GRID')

#the main list view on the page holding each influential person's entry
item_main = driver.find_element_by_class_name('blogView_main__332IP')

#Wait for page to be loaded. This only waits till Socrates, though it can be made to wait longer 
#but that would mean waiting more
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

#each influential person is a list object, so getting them all by their tag name
item_list = item_main.find_elements_by_tag_name('li')

#printing number of items scraped, simply.
print(len(item_list))

print("===========OUTPUT============\n")

for item in item_list:
    #we only want to save info on influential people, not ads
    try:
        name = item.find_element_by_class_name('Title_title__2P7ae').text #person's name
        birth = item.find_element_by_class_name('blogItem_properties__3kQW0').text #person's date and place of birth
        
        #image sources defined in 2 ways, so trying them both:
        try:
            image = requests.get(item.find_element_by_tag_name('img').get_attribute('src')).content
        except:    
            image = requests.get(item.find_element_by_tag_name('img').get_attribute('data-src')).content
        
        #printing the name, birth and *type* of image object to have an output
        print(name)
        print(birth)
        print(type(image))

        #saving image in files
        try:
            f = open(os.path.join(".", 'jpg' + '_'  + name), 'wb')
            f.write(image)
            f.close()
        except Exception as e:
            print("Exception: " + e)
    #if ads are encountered, they should not be saved
    except:
        print("Encountered an ad")

print("\n===========OUTPUT============")
