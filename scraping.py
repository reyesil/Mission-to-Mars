# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the Chrome browser in Splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

# ### Latest Mars News

# Visit the Mars NASA news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Parse the HTML
html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# Initial scraping
slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# ### Featured Mars Images

# Visit NASA's Space Images URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Find and click the Full Image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# Find and click the More Info button
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()

# Parse the resulting HTML with BeautifulSoup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the relative image URL
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

# ### Mars Facts

# Scrape Space-Facts front page table
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df

# Convert DataFrame into HTML
df.to_html()

# End the session
browser.quit()