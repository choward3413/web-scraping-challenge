#imoprts
#import dependencies, splinter, BS, and  pandas

from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#scrape all function
def scrape_all():
    print("scrape all was found")
    #set up splinter
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #get informatioin from news page
    news_title, news_paragraph = scrape_news(browser)

    #build dictionary using info from scrapes
    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_img(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "latUpdated": dt.datetime.now()
    }

 
    #stop webdriver
    browser.quit()

    #display output
    return marsData

#scrape through mars news page
def scrape_news(browser):
    #go to mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #delay for page load
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convet browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    #grabs title
    news_title = slide_elem.find('div', class_='content_title').get_text()    
    #grab paragraph
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    #return the title and paragraph
    return news_title, news_p

#scrape through the featured image page
def scrape_feature_img(browser):
    #visit url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #find and click the full image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    #parse resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #find image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    #use base url to find absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    #return image url
    return img_url




#scrape through the facts  page
def scrape_facts_page(browser):
    #visit url
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

     #parse resulting html with soup
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #find facts location
    factsLocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factsLocation.find('table')

    #create empty string
    facts = ""
    #add text to the empty string
    facts +=str(factTable)

    return facts





#sscrape through the hemisphere pages
def scrape_hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url)

    #create list to hold images and titles
    hemisphere_image_urls = []

    #set up loop
    for i in range(4):

        hemisphereInfo = {}


        #fiind elements on each loopto avoid a stale element exemption
        browser.find_by_css('a.product-item img')[i].click()
        
        #find sample image anchor tag and extract href
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"] = sample['href']
        
        
        #get hemisphere title
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
        
        
        #append hemisphere object to list
        hemisphere_image_urls.append(hemisphereInfo)
        
        #navigat backwards
        browser.back()

    #return hemisphere urls with titles
    return hemisphere_image_urls







#scrape_all()
#scrape_news()





#set as a flask app
if __name__ =="__main__":
    print(scrape_all())



