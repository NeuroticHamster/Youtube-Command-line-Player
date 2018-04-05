from random import randrange
#import vlc
#import sqlalchemy
import time
from bs4 import BeautifulSoup
import requests

from selenium.webdriver.common.keys import Keys


from selenium import webdriver
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from randomsTables import Songinfo, Base
engine = create_engine('sqlite:///music.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()




def playutube(bname=None, element=2):
    if bname == None:
        bname = raw_input('\b' + 'band name? ')
        sname = raw_input('song name? ')
    else:
        sname = ''

    print('\b' + 'Loading your music!')
    ok = '///'
    k = '|'
    dkk = '   |'
    kk = dkk.replace('|', '')
    #ok = k.replace('|', '')


    bandname = bname + sname

    #try:
    try:
        from selenium.webdriver.chrome.options import Options, DesiredCapabilities
        options = Options()
        options.add_argument('log-level=3')
        options.add_argument("--silent")
        options.add_argument('--headless')
        options.add_argument('--hide-scrollbars')
        options.add_argument("--disable-logging")
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        dc = DesiredCapabilities.CHROME

        dc = {"loggingPrefs": {"driver": "OFF", "server": "OFF", "browser": "OFF"}}

        # dc = {"loggingPrefs": {"driver": "OFF", "server": "OFF", "browser": "OFF"}}
        # dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
        driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options, desired_capabilities=dc)

    except:

        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='./geckodriver.exe', firefox_options=options)
        print('firefox')
    print(ok + kk * 3 + k)




    '''except:
        try:
            from selenium.webdriver.chrome.options import Options
            options = Options()

            options.add_argument('--headless')

            options.add_argument('--disable-gpu')  # Last I checked this was necessary.
            driver = webdriver.Chrome('./selenium/webdriver/chromedriver.exe', chrome_options=options)
            print('ok')
        except:
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path='C:\new\Scripts\dist\randoms\selenium\webdriver\firefox\geckodriver.exe', firefox_options=options)'''
    print(ok * 2 + kk * 2 + k)


    driver.get('https://www.youtube.com/results?search_query='+ str(bandname))

    print(ok * 3 + kk + k)
    #time.sleep(2)

    driver.find_elements_by_xpath('//a[@id="video-title"]')[element].click()
    print(ok * 4 + k)
    simArtists = raw_input('\b done loading...Would You like a list of similar artists? yes or no? ')
    #mtitle = driver.find_elements_by_class_name('title')[0]

    #print(mtitle)
    #'style-scope ytd-video-primary-info-renderer'

    if simArtists == 'yes':
        otherbands = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=' + bname + '&api_key=some_api_key')
        sec = otherbands.text
        soup = BeautifulSoup(sec, 'html.parser')
        check = soup.find_all('name')
        a = str(check)
        b = a.replace('<name>', '')
        artList = bname + b.replace('</name>', '')
        print('\b' + artList)

    elif simArtists == 'no':
        artList = ''

    choices(driver, element, bname, artList='')
def choices(driver, element, bname, artList=''):
    closedd = raw_input('\b Press exit, restart, save(save related artists to text doc), random for a random by artist, skip to for next song by artist, or add to add to a playlist: ')


    if str(closedd) == 'exit':

        driver.close()
    elif str(closedd) == 'restart':
        try:
            driver.close()
            playutube()
        except:
            pass
        playutube()
    elif str(closedd) == 'random':
        try:
            driver.close()
        except:
            pass
        element = randrange(1, 10)
        newband = raw_input('random search for band name')
        playutube(newband, element)
    elif str(closedd) == 'save':
        try:
            with open('./' + str(bname) + '.txt', 'w') as w:
                w.write(str(artList))
                choices(driver, element, bname, artList='')
        except:
            choices(driver, element, bname, artList='')
    elif str(closedd) == 'skip':

        print(bname)
        print(element)
        element += 1
        driver.close()

        playutube(bname, element)
    elif str(closedd) == 'add':
        pname = raw_input('name of the new playlist or an existing playlist you want to add music to: )')
        url = driver.current_url
        newentry = Songinfo(artistname=str(bname), playlist=str(pname), link=str(url), songname=str(sname))
        session.add(newentry)
        session.commit()
        '''new_person = Person(songname=str(bname), name='superfuck')
        session.add(new_person)
        session.commit()'''



playutube()
'''allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
#allel.send_keys(Keys.TAB)'''


print('closing')

