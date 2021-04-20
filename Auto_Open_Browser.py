#!/usr/bin/env python
# coding: utf-8

# ## Auto Open Web Pages 
# ***

# In[2]:


# what variables are we going to need
# how are we going to do it?

# open up a series of web pages
# we need a list of URLs that we will open
# open a wweb page
# open up a series of tabs

import webbrowser

socialUrls = ["https://www.linkedin.com/feed/" , "https://mail.google.com/mail/u/0/#inbox" , "https://www.peacocktv.com/watch/home"]
techUrls = ["https://plotly.com/python/ml-regression/" , "https://www.coursera.org/learn/what-is-datascience/lecture/QcFwx/the-many-paths-to-data-science"]
def open_tabs(url_list):
    for element in url_list:
         webbrowser.open_new_tab(element)

def main():
   # webbrowser.open("www.youtube.com" , new = 2, autoraise = True)
    open_tabs(socialUrls)
    open_tabs(techUrls)
    
main()

