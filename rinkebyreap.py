#!/usr/bin/env python

import os
import time
import json
import twitter
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def tweet_addr():
    statuses=api.GetUserTimeline(screen_name=uname)
    status=api.PostUpdate(msg)
    data=str(status)
    json_obj=json.dumps(data)
    
    with open('tweet.json','w') as f:
        f.write(json_obj)

    with open('tweet.json','r') as f:
        data = f.read()

    d=json.loads(data)
    y=json.loads(d)
    tweet_id=(y['id'])
    url='https://twitter.com/{}/status/{}'
    tweet_url=url.format(uname,tweet_id)
    return tweet_url,tweet_id

def reap(tweet_url):
    driver=webdriver.Chrome('./chromedriver')
    driver.get('https://faucet.rinkeby.io/')
    elem=driver.find_element_by_xpath('//*[@id="url"]')
    elem.clear()
    string=tweet_url.split('/')
    for s in string:
        elem.send_keys(s)
        elem.send_keys('/')
        time.sleep(0.25)
    elem.send_keys(Keys.BACKSPACE)
    # elem.send_keys(tweet_url)
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/button')
    elem.click()
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/ul/li[3]/a') 
    elem.click()
    time.sleep(5)
    driver.close()

def phantom_reap(tweet_url):
    chrome_options=Options()
    chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--window-size=1920x1080')
    chrome_driver='./chromedriver'
    driver=webdriver.Chrome(chrome_options=chrome_options,executable_path=chrome_driver)
    driver.get('https://faucet.rinkeby.io/')
    elem=driver.find_element_by_xpath('//*[@id="url"]')
    elem.clear()
    elem.send_keys(tweet_url)
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/button')
    elem.click()
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/ul/li[3]/a') 
    elem.click()
    time.sleep(5)
    driver.close()

def destroy_tweet(tweet_id):
    destro=api.DestroyStatus(tweet_id)

if __name__ == '__main__':
    usage='''\n%(prog)s [-p phantom]\nexample:\n./reaper.py -p'''
    parser=argparse.ArgumentParser(usage=usage)
    parser.add_argument('-p','--phantom',action='store_true',help='run phantom browser',dest='phantom')
    args=parser.parse_args()

    phantom=args.phantom

    uname=raw_input('Enter Twitter username: ')
    msg=raw_input('Enter wallet address: ')

    api=twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    if phantom:
        tweet_url,tweet_id=tweet_addr()
        phantom_reap(tweet_url)
        time.sleep(3)
        destroy_tweet(tweet_id)
    else:
        tweet_url,tweet_id=tweet_addr()
        reap(tweet_url)
        time.sleep(3)
        destroy_tweet(tweet_id)

