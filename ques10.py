'''
    Date: 7th June, 2018
    Name: Renita Lobo
    Objective: Get answers for a particular subject

'''

# all imports
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os

# initialize the browser
browser = webdriver.Chrome("/home/lobo/Downloads/chromedriver")

# no of links
question_num = 0

# page number
page_num = 1

# page count
page_count = 0

# count
count = 0

# list of all links
links = []

# Get total no of links for a page
def get_link(page_num):
    
    # initialize the browser
    browser = webdriver.Chrome("/home/lobo/Downloads/chromedriver")

    # Open url
    url = "https://www.ques10.com/t/ait(26)/?page=" + str(page_num) + "&sort=update&limit=all%20time&q="
    browser.get(url)

    # get the source code
    source = browser.page_source

    # Now comes Soup
    soup = BeautifulSoup(source, "html.parser")

    # get all links from that div block

    # Step 1: Go to that block 
    post_list = soup.find("div",id="post-list")

    # Step 2: Get all href links (only those links which contain the ans)
    anchor = post_list.find_all("a", href=True)
    for a in anchor:
        count_box_sm = a.parent.parent.find_previous_sibling('div')
        if count_box_sm.find("div", class_="answered"):
            links.append("https://www.ques10.com"+a['href'])

    # This is my code without validating whether it contains answer or not
    # links = []
    # for i in post_list.find_all("a", href=True):
    #     link = i['href']
    #     if link.startswith("/p/"):
    #         links.append("https://www.ques10.com"+link)
              

    browser.close()

    print("Collected all links from page no: ", page_num)

    # Return the list of links
    return links

# Save the data
def save_data(links):
    global count
    count = count + 1

    # initialize the browser
    browser = webdriver.Chrome("/home/lobo/Downloads/chromedriver")

    # Making directory for the page
    os.mkdir("page"+str(count))
    os.chdir("page"+str(count))
    print(os.getcwd())
    for i in links:
        browser.get(i)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')

        main_container = soup.findAll('div', class_="post-body Open clearfix")
        question_container = main_container[0].find('span', itemprop="name")
        second_container = main_container[1].find('span', itemprop = "text")

        # List of image url 
        images = []

        # image count
        imgno = 0

        # Making the directory
        dir_name = question_container.text
        dir_name = dir_name.replace("/"," ")
        os.mkdir(dir_name)
        os.chdir(dir_name)

        # Writing the ans
        with open("ans1.txt", "a+") as f:
            f.write(question_container.text+"\n")

        # Finding the content and saving it
        # Only contains the text part
        for content in second_container.findAll(['p','li','img']):
            # Opening the text file
            with open("ans1.txt","a+") as f:
                # If image url encountered then append to the list
                if content.get('src'):
                    imgno = imgno + 1
                    imgurl = content.get('src')
                    images.append(imgurl)
                    f.write("Fig"+ str(imgno) + "\n")
                else:
                    # Writing the content apart from the text file
                    f.write(content.text+"\n")

        # Downloading the image
        for i in images:
            r = requests.get(i)
            with open("1.png", "wb") as f:
                f.write(r.content)

        # After image and content, change dir
        os.chdir("/home/lobo/Documents/2018_Python3_Projects/ques10/"+"page"+str(count))
        print("Going back one dir...")

    os.chdir("..")
    browser.close()

# Parse Data
def get_data():
    
    global page_count
    page_num = 1
    while page_count > 0: 
        print("Executing for page no: ", page_num)

        # list to save the links
        global links

        # Get no of links
        links = get_link(page_num)
        print("Finished executing get_link for page no: ", page_num)

        # Get the data
        save_data(links)
        print("Finished executing save_data for page no: ", page_num)

        # To move to the next page        
        page_num = page_num + 1

        # Decreasing the page count
        page_count = page_count - 1

        # Initializing the global links 
        links = []
    
    print("Execution completed!")


# Define page count function
def get_page_count():
    print("Executing get_page_count function")

    # Define the main url
    url = "https://www.ques10.com/t/ait(26)/?page=" + str(page_num) + "&sort=update&limit=all%20time&q="

    # Get the total number of pages
    global page_count
    
    # Step 1: Open the browser with the main url 
    browser.get(url)
    source = browser.page_source

    # Step 2: Create soup object
    soup = BeautifulSoup(source, 'html.parser')

    # Step 3: Navigate to the page no at the bottom
    step_link = soup.find("span", class_="step-links")
    page_text = step_link.find("span", class_="current").text

    # Step 4: Get page count
    page_count = int(page_text.split(" ")[-2])

    # Step 5: Close Browser
    browser.close()

    print("Finished executing the function...")

# Function calls
def main():
    print("Executing main function...")
    get_page_count()
    print("Done executing the get page function...")
    print("Executing the get data function...")
    get_data()


main()
