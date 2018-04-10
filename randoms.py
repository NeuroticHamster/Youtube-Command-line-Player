from random import randrange
#import vlc
#import sqlalchemy
import time
from bs4 import BeautifulSoup
import requests
#from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium import webdriver


import os
import sys

#--- add to tables imports


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#from randomsTables import Address, Base, Person
from randomsTables import Songinfo, Base

#------- adding to database


#engine = create_engine('sqlite:///sqlalchemy_example.db')
engine = create_engine('sqlite:///music.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Person in the person table
'''new_person = Person(name='new person2')
session.add(new_person)
session.commit()'''

# Insert an Address in the address table
'''new_address = Address(post_code='00000', person=new_person)
session.add(new_address)
session.commit()'''

#----

#from sqlalchemy_declarative import Person, Base, Address



# Make a query to find all Persons in the database
'''session.query(Person).all()
print(Person)'''
'''try:
    allit = session.query(Songinfo.artistname).all()
    #print(allit)

except:
    pass'''
'''with engine.connect() as c:
    user = c.execute("SELECT * FROM Songinfo WHERE playlist == ?",('kiss'))
    #user = Songinfo.filter(Songinfo.playlist == 'kiss')
    for use in user:
        print(use)'''


#object
#at
#0x2ee3a10 >]

# Return the first Person from all Persons in the database
#person = session.query(Person).first()
#print(person.name)
#len(person)

#new = session.query(Person.name).all()
#print(new)
#u'new person'

# Find all Address whose person field is pointing to the person object
#session.query(Address).filter(Address.person == person).all()
#print(Address)
#object
#at
#0x2ee3cd0 >]

# Retrieve one Address whose person field is point to the person object
#session.query(Address).filter(Address.person == person).one()
#print(Address)
#object
#at
#0x2ee3cd0 >
#address = session.query(Address).filter(Address.person == person).one()
#print(address.post_code)
#u'00000'
#-----
ok = '///'
k = '|'
dkk = '   |'
kk = dkk.replace('|', '')

def playutube(bname=None, element=2):
    playvalues = session.query(Songinfo.playlist).all()
    print('type in a playlist name to open previous playlist, type info to see playlists:')

    if bname == None:
        bname = raw_input('\b' + 'band name? ')

        if bname in str(playvalues):

                # print(item)

            print('its there')
            sname = 'redirect'
        elif str(bname) == 'info':
            newlist = []
            for item in playvalues:
                if item not in newlist:
                    newlist.append(item)
                    #print(item)
            for item in newlist:
                for item2 in item:
                    print(item2)
            #print(newlist)
                # print(item)

            playutube()
            return
        else:
            sname = raw_input('song name? ')



    else:
        sname = ''

    print('\b' + 'Loading your music!')

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
    if sname == 'redirect':
        with engine.connect() as c:
            lvalue = c.execute('SELECT link FROM Songinfo WHERE playlist == ?', (str(bname)))
            #print(lvalue)
            newlist = []
            for item in lvalue:
                #print(item)
                for it in item:
                    newlist.append(it)

        playplaylist(bname, driver, newlist)
        return
    else:
        pass

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
        otherbands = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist=' + bname + '&api_key='your api key here')
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
        #exit()
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
        pname = raw_input('name of the new playlist or an existing playlist you want to add music to. Try not to give the playlist the same name as the band:  )')
        url = driver.current_url
        newentry = Songinfo(artistname=str(bname), playlist=str(pname), link=str(url))
        session.add(newentry)
        session.commit()
        choices(driver, element, bname, artList)
        '''new_person = Person(songname=str(bname), name='superfuck')
        session.add(new_person)
        session.commit()'''
    else:
        driver.close()
        exit()

def playplaylist(bname, driver,newlist, element=0):
    #river.get()
    print(ok * 3 + kk + k)
    # time.sleep(2)
    driver.get(newlist[element])
    #print(newlist[element])
    #time.sleep(15)
    #driver.close()
    print(ok * 4 + k)
    length = len(newlist) - 1
    nav = raw_input('type next or back to navigate the playlist. Type restart to exit playlist menu. Type exit to close application.')
    if str(nav) == 'restart':
        driver.close()
        playutube()
    elif str(nav) == 'next' and element < length or str(nav) == 'next' and element > 0:
        element += 1
        playplaylist(bname, driver, newlist, element)
    elif str(nav) == 'exit':
        driver.close()
        exit()
    else:
        print("that's the last item in the playlist or you made a typo")
        playplaylist(bname, driver, newlist, element)







playutube()
'''allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
allel.send_keys(Keys.TAB)
#allel.send_keys(Keys.TAB)'''

#driver.get("https://open.spotify.com/track/0JRWjTvlxTThEY8lc3Fjhr")
#driver.get("https://www.youtube.com/watch?v=VsaxPaJSf24&list=PLngz5HPZ6rjBs0sOGLnDlf1_lCC93mgID")
print('closing')
'''
#url = 'http://prem1.rockradio.com:80/bluesrock?9555ae7caa92404c73cade1d'
url = "https://www.youtube.com/watch?v=VsaxPaJSf24&list=PLngz5HPZ6rjBs0sOGLnDlf1_lCC93mgID"
# define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

# Define VLC player
player = instance.media_player_new()

# Define VLC media
media = instance.media_new(url)

# Set player media
player.set_media(media)

# Play the media
player.play()
time.sleep(20)
'''
