from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd





def scrape_mars_hw():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=True)

    news_title, news_content = scrape_info(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_content": news_content,
        "mars_image": mars_image(browser),
        "mars_table": mars_table(),
        "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def scrape_info(browser):

    # Establish the link in chrome; a brower object
    http = 'https://mars.nasa.gov/news/'
    browser.visit(http)

    # Use the code from class activities that parse the information retreived from the web; use. the beautiful soup to create an object
    webpage = browser.html
    mars_news_nasa = soup(webpage, 'html.parser')

    try: 
        #after inspecting the nasa webpage, the news were listed uner div class = grid_layout, ul class = item_list, li class = slide
        each_news = mars_news_nasa.select_one('ul.item_list li.slide')

        # Now get the title text from the class content_title
        news_title = each_news.find("div", class_='content_title').get_text()
        # Now get the news contents from the class article_teaser_body
        news_content = each_news.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_content


    #####################################################
def mars_image(browser):
    # Visit URL from the homework instructions, however, the full image on the webpage is "FEATURED IMAGE NASA Spacecraft Tracks Argentine Flooding"，so I double check the url and found the correct one
    http2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(http2)

    # The full image on this page is on the top, it is not about mars. To find a image for mars, need to click on the full image icon, which has id = full_image
    image_full = browser.find_by_id('full_image')
    image_full.click()

    # The more info button is under div class "buttons" -> a class = button
    button_more_info = browser.links.find_by_partial_text('more info')
    button_more_info.click()

    # Now interpretate the contents from this webpage 
    webpage = browser.html
    image_webpage = soup(webpage, 'html.parser')

    try:
        url_mars_image = image_webpage.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
    
    complete_url = f'https://www.jpl.nasa.gov'+ url_mars_image

    return complete_url


    #####################################################
def mars_table():
    try: 
        mars = pd.read_html('http://space-facts.com/mars/')
        mars_table = mars[0]
    except BaseException:
        return None

    mars_table.columns=['Parameter', 'Values']
    mars_table_html = mars_table.to_html()

    return mars_table_html


    #####################################################
def hemispheres(browser):
    http3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(http3)

    # create an empty list to store future https
    https_list = []
    links = browser.find_by_css("a.itemLink h3")

    for i in range(len(links)):
        temp = {} # this is to create an object to hold the values for https_list
        
        browser.find_by_css("a.itemLink h3")[i].click() # find the corresponding link and click on it
        
        graph_sample = browser.links.find_by_text('Sample').first # find the jpg graph 
        temp['img_url'] = graph_sample['href'] # store the link
        temp['title'] = browser.find_by_css("h2.title").text # store the title
        https_list.append(temp)
        browser.back() # this is new technique to go back for the next item
    
    return https_list

    

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_mars_hw())
