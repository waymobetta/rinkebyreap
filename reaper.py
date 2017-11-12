#!/usr/bin/env python

import os
import sys
import time
import json
import argparse

os.system('clear')

try:
    import requests
except:
    sys.exit('[!] Requests library not found. Please install before proceeding: pip install requests\n')
try:
    import twitter
except:
    sys.exit('[!] Twitter library not found. Please install before proceeding: pip install python-twitter\n')
try:
    from termcolor import cprint
except:
    sys.exit('[!] Termcolor library not found. Please install before proceeding: pip install termcolor\n')
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
except:
    sys.exit('[!] Selenium library not found. Please install before proceeding: pip install selenium\n')

def check_bal():
    api_key=os.environ['ETHERSCAN_API_KEY']
    url='https://rinkeby.etherscan.io/api?module=account&action=balance&address={}&tag=latest&apikey={}'.format(addr,api_key)
    r=requests.get(url)
    data=r.json()
    bal=int(data['result'])
    wei=1000000000000000000 
    eth=bal/wei
    return eth

def tweet_wallet():
    statuses=api.GetUserTimeline(screen_name=uname)
    status=api.PostUpdate('Rinkeby wallet: ' + addr)
    data=str(status)
    json_obj=json.dumps(data)
    
    with open('tweet.json','w') as f:
        f.write(json_obj)

    with open('tweet.json','r') as f:
        data = f.read()

    d=json.loads(data)
    y=json.loads(d)
    tweet_id=(y['id'])
    tweet_url='https://twitter.com/{}/status/{}'.format(uname,tweet_id)
    return tweet_url,tweet_id

def reap(tweet_url):
    driver=webdriver.Chrome('./chromedriver')
    driver.get('https://faucet.rinkeby.io/')
    elem=driver.find_element_by_xpath('//*[@id="url"]')
    elem.clear()
    elem.send_keys(tweet_url)
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/button')
    elem.click()
    elem=driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/span/ul/li[3]/a') 
    elem.click()
    time.sleep(3)
    driver.close()

def phantom_reap(tweet_url):
    chrome_options=Options()
    chrome_options.add_argument('--phantom')
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
    time.sleep(3)
    driver.close()

def destroy_tweet(tweet_id):
    api.DestroyStatus(tweet_id)

def version():
    if sys.version_info[0] < 3:
        uname=raw_input('Enter Twitter username: ')
        addr=raw_input('Enter wallet address: ')
        return uname,addr
    else:
        uname=input('Enter Twitter username: ')
        addr=input('Enter wallet address: ')
        return uname,addr

if __name__ == '__main__':
    usage='''%(prog)s [-p phantom] [-d destroy]\n\nexample:\n./reaper.py -p -d'''
    parser=argparse.ArgumentParser(usage=usage)
    parser.add_argument('-p','--phantom',action='store_true',help='run phantom browser',dest='phantom')
    parser.add_argument('-d','--destroy',action='store_true',help='destroy tweet',dest='destroy')
    args=parser.parse_args()
    
    phantom=args.phantom
    destroy=args.destroy

    uname,addr=version()
    print('\n==============================================\n')

    api=twitter.Api(
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
            access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
 
    if phantom:
        cprint('- Running as phantom -','yellow')
        print('\n')

        tweet_url,tweet_id=tweet_wallet()
        cprint('[+] Generating authentication tweet..','cyan')
        cprint('[*] Done','green')
        cprint('[+] Requesting funds from faucet..','cyan')
        phantom_reap(tweet_url)
        eth=check_bal() 
        cprint('[*] Balance: {} Ether'.format(eth),'yellow')
        funded=(eth-1) + 18
        while eth < funded:
            cprint('[!] Captcha discovered!','red')
            cprint('[+] Retrying..','cyan')
            phantom_reap(tweet_url)
            time.sleep(1)
        time.sleep(1)
        cprint('[*] Done','green')
        cprint('[*] Balance: {} Ether'.format(eth),'yellow')
        if destroy:
            destroy_tweet(tweet_id)
            cprint('[*] Tweet destroyed','green')
    else:
        tweet_url,tweet_id=tweet_wallet()
        cprint('[+] Generating authentication tweet..','cyan')
        cprint('[*] Done','green')
        cprint('[+] Requesting funds from faucet..','cyan')
        reap(tweet_url)
        eth=check_bal()
        cprint('[*] Balance: {} Ether'.format(eth),'yellow')
        funded=(eth-1) + 18
        while eth < funded:
            cprint('[!] Captcha discovered!','red')
            cprint('[+] Retrying..','cyan')
            reap(tweet_url)
            time.sleep(1)
        time.sleep(1)
        cprint('[*] Done','green')
        cprint('[*] Balance: {} Ether'.format(eth),'yellow')
        if destroy:
            destroy_tweet(tweet_id) 
            cprint('[*] Tweet destroyed','green')

