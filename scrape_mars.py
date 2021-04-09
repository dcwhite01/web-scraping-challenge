
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    title, news_p = news(browser)
    data = {
        "title": title,
        "news": news_p,
        "facts": mars_facts(browser),
        "featured_image": featured_image(browser),
        "hemisphere_image_urls": images(browser)
        
    }
    browser.quit
    return(data)
    
def news(browser):

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    bsoup = BeautifulSoup(html, "html.parser")

    article = bsoup.find("div", class_='list_text')
    title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    browser.quit
    return(title, news_p)

def featured_image(browser):
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    bsoup = BeautifulSoup(html, "html.parser")
    image = bsoup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# def featured_image(browser):
#     featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars2.jpg"

def mars_facts(browser):
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    table = pd.read_html(url)
    df = table[1]
    html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)
    browser.quit
    return(html_table)
   
def images(browser):
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    MarsImages_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(MarsImages_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_divs = soup.find_all("div", class_="item")
    hemisphere_image_urls = []
    for hem in range(len(hemisphere_divs)):
        hemisphere = {}
        hem_link = browser.find_by_css("h3")
        hem_link[hem].click()
        downloads = browser.find_by_text("Original")
        hemisphere["image_url"] = downloads["href"]
        title = browser.find_by_css("h2.title").text
        hemisphere["title"] = title
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    browser.quit()
    return(hemisphere_image_urls)


# In[23]:


scrape()


# In[ ]:




