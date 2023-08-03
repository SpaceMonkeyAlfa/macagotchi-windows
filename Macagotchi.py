#imports
import time
import subprocess
import datetime
from datetime import datetime as datetime2
import pygame
import random
import hashlib
import asyncio
import sys
import os
import winwifi
NextScanDelay = 0
#print(dir(winwifi.WinWiFi))
print((winwifi.WinWiFi.scan()[1].ssid))
#winwifi.WinWiFi.get_profiles()
#If packaging, use:
os.chdir(os.getenv('LOCALAPPDATA')+'\macagotchi')
#instead
#os.chdir(str(sys.path[0])+'assets/')
pygame.init()
#Define Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
colour = (184, 230, 229)
GREEN = (0,255,0)
RED = (255,0,0)
#Open Window
width = 350
height = 125
size = (width, height)
img = pygame.transform.scale(pygame.image.load('logo.ico'),(160,100))
pygame.display.set_icon(img)
screen = pygame.display.set_mode(size)
addup = 0
streak = 0
commentary = ""
uniques = []
scanning = False
textColour = WHITE
pygame.display.set_caption("Macagotchi")
typing = False
displayResults = False
scanDelay = 0
wardriving = False
#defines total unique ssids ever found from the address.txt file.
with open('address.txt','r') as f:
        file = f.read()
        values = file.split('\n')
        ssids = len(values)
#defines longest streak from- you guessed it: the longestStreak.txt file.
with open('longestStreak.txt','r') as f:
    file = f.read()
    longestStreak = int(file.split('\n')[0])
#defines name using the stats.txt file
with open('stats.txt','r') as f:
    file = f.read()
    nameText = file.split('\n')[0]
with open('loyalty.txt','r') as f:
    file = f.read()
    values = file.split('\n')
    for d in values:
        if d != "Streak:":
            streak += 1
    if str(datetime.date.today()-datetime.timedelta(days=1)) not in values and str(datetime.date.today()) not in values:
       print("STREAK BROKEN!")
       streak = 0
       print(str(datetime.date.today()))
       with open('loyalty.txt','w') as f:
         streak = 0
         f.write("Streak:")
        #checks how long your macagotchi has been asleep
with open('totalLog.txt','r') as f:
    file = f.read()
    file = file.split('\n')
    
    file = file[len(file)-1]
    print(file)
    file = file.split(',')
    if "".join(file) != "Total Log:":
        lastopened = file[1]
        str_d1 = str(datetime.date.today())
        str_d2 = lastopened
        d1 = datetime2.strptime(str_d1, "%Y-%m-%d")
        d2 = datetime2.strptime(str_d2, "%Y-%m-%d")

        sleepTime = d1 - d2
        sleepTime = sleepTime.days
    else:
        sleepTime = 0
#simple hasher
def ezhash(string):
    hasher = hashlib.sha256()
    hasher.update(string.encode('utf8'))
    return hasher.hexdigest()
            
def findWifi():
    atempts = 0
    found = []
    scanFunc = winwifi.WinWiFi.scan()
    for wifinetwrk in scanFunc:
            found.append(wifinetwrk.ssid)
    """#process runs wifi scan command from the wifi module. shell = True disables wifi.exe from opening a command line window. 
    process = subprocess.Popen(['wifi','scan'],stdout=subprocess.PIPE,shell=True)
    #Running it using the command instead of the library allows me to disable the window
    out, err = process.communicate()
    process.wait()
    output = out.decode()
    output = output.split('\n')
    output = output[4:]
    #This code is responsible for retrieving the ssids
    for x in output:
        if x.startswith('SSID'):
            found.append(x.split(':')[1][1:])"""
    return found
def scan(count):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    uniques = []
    returnList = []
    networks = findWifi()
    count = 0
    print(networks)
#check ssids against last finds and hashes
    for n in networks:
            n = n.replace('\r','')
            print(n)
            with open('address.txt','r') as f:
                file = f.read()
                values = file.split('\n')
                ssids = len(values)   
            if ezhash(n) not in values and n != "":
                with open('address.txt','a') as f:
                        f.write('\n'+str(ezhash(n)))
                        uniques.append(n)
                        count += 1

            
            with open('totalLog.txt','a') as f:
                f.write('\n'+str(ezhash(n)))
                f.write(','+str(datetime.date.today()))
    returnList = [count,uniques]
    return(returnList)

#Setup the pygame window and all of the assets it needs
screen.fill(WHITE)
pygame.display.flip()
carryOn = True
timer = 16200
clock = pygame.time.Clock()
count = 0
happy = pygame.transform.scale(pygame.image.load('awake.jpg'),(150,90))
scanning1 = pygame.transform.scale(pygame.image.load('scanning1.jpg'),(150,90))
scanning2 = pygame.transform.scale(pygame.image.load('scanning2.jpg'),(150,90))
scanning3 = pygame.transform.scale(pygame.image.load('scanning3.jpg'),(150,90))
friendly = pygame.transform.scale(pygame.image.load('friendly.jpg'),(150,90))
normal = pygame.transform.scale(pygame.image.load('happy.jpg'),(150,90))
bored = pygame.transform.scale(pygame.image.load('bored.jpg'),(150,90))
lonely = pygame.transform.scale(pygame.image.load('lonely.jpg'),(150,90))
blink = pygame.transform.scale(pygame.image.load('blink.jpg'),(150,90))
low = pygame.transform.scale(pygame.image.load('0-9.jpg'),(300,100))
medium = pygame.transform.scale(pygame.image.load('10-29.jpg'),(300,100))
high = pygame.transform.scale(pygame.image.load('30-99.jpg'),(300,100))
godtier = pygame.transform.scale(pygame.image.load('100+.jpg'),(300,100))
asleep = pygame.transform.scale(pygame.image.load('asleep.jpg'),(150,90))
awakening = pygame.transform.scale(pygame.image.load('awakening.jpg'),(150,90))
face = asleep
nextface = normal
oldface = normal
finds = 0
actualTime = 0
scanTimes = 0
scanning = False
blinkTime = 0
networksID = 0
displayTime = 0
lastFinds = 0
#Main game loop
while carryOn:

    screen.fill(WHITE)
    for event in pygame.event.get():
    #time.sleep(1)
        if event.type == pygame.QUIT:
            carryOn = False
        #Name modifying
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wardriving = not wardriving
                if scanTimes > 0:
                        timer = 0
            # Check for backspace
            if event.key == pygame.K_F2:
                typing = True
            if event.key == pygame.K_RETURN:
                typing = False
                with open('stats.txt','w') as f:
                    f.write(nameText)

                
            elif event.key == pygame.K_BACKSPACE and typing:
                # get text input from 0 to -1 i.e. end.
                nameText = nameText[:-1]
  

            elif typing and len(nameText) < 21:
                nameText += event.unicode
        #Displays the I've been asleep for x days message
    if actualTime == 60:
        face = awakening
        sleepTime = sleepTime
        if sleepTime > 1:
            commentary = f"I've been asleep for {sleepTime} days."
        else:
            commentary = "Hello hooman!"
            
    if actualTime == 120:
        face = normal
  #Adds a delay to the scan time after scanning 3 times
    if wardriving and scanTimes > 0:
        scanDelay = -16200
    else:
        scanDelay = 0
    if timer == 18000 + scanDelay:
        import winwifi
        displayResults = False
        if longestStreak < streak:
            with open('longestStreak.txt','w') as f:
                f.write(str(streak))
        rng = random.randint(1,4)
        commentary = "Scanning..."
        print("Scanning...")
        scanning = True
        returnedList = scan(0)
        lastFinds = returnedList[0]
        uniques = returnedList[1]
        
        face = scanning1
        finds += lastFinds
        print(uniques)
    elif timer in range(18045 + scanDelay,18050+ scanDelay):
        face = scanning2
    elif timer in range(18090 + scanDelay,18095 + scanDelay):
        face = scanning3
    elif timer in range(18135 + scanDelay,18140 + scanDelay):
        face = scanning2
    elif timer in range(18180 + scanDelay,18185 + scanDelay):
        face = scanning1
    elif timer in range(18225 + scanDelay,18230 + scanDelay):
        face = scanning2
    elif timer in range(18270 + scanDelay,18275 + scanDelay):
        face = scanning3
    elif timer in range(18315 + scanDelay,18320 + scanDelay):
        face = scanning2
    elif timer >= 18360 + scanDelay:
        scanning = False
        timer = 0
        face = nextface
        displayResults = True
        networksID = 0
        with open('address.txt','r') as f:
            file = f.read()
            values = file.split('\n')
            ssids = len(values)
        scanTimes += 1
        
        if lastFinds < 1 and not scanning:
            commentary = f"Zero. But found {finds} already."
    
    if lastFinds > 0 and displayResults:
        timer = 0    
        commentary = f"Found {uniques[networksID]}!"
        displayTime += 1
        if displayTime > 60 and networksID < len(uniques)-1:
            networksID += 1
            displayTime = 0
        elif displayTime > 60 and networksID >= len(uniques)-1:
            if lastFinds > 1:
                commentary = f"Found {lastFinds} new ones!"
            elif lastFinds == 1:
                commentary = f"Found {lastFinds} new one!"       
            displayTime = 0
            displayResults = False


    #super happy face :)    
    if finds > 4 and not scanning:
        
        face = friendly
        nextface = friendly
        with open('loyalty.txt','r') as f:
            file = f.read()
            values = file.split('\n')
        if str(datetime.date.today()) not in values:
            with open('loyalty.txt','a') as f:
                f.write('\n'+str(datetime.date.today()))
                streak += 1
        #happy face
    elif finds > 0 and not scanning:
        face = happy
        nextface = happy
#Hungry face
    elif finds < 1 and scanTimes > 0 and not scanning:
        face = lonely
        nextface = lonely
#Randomised hunger messages

        if rng == 1:
            commentary = "Hungry"
        elif rng == 2:
            commentary = "Feed.. Me"
        elif rng == 3:
            commentary = "Food.."
        elif rng == 4:
            commentary = "Can we go for a walk?"
        #*blink*
    blinkTime += 1
    if blinkTime == 180 and not scanning and face != lonely:
        oldface = face
    if blinkTime > 180 and not scanning and face != lonely:
        face = blink
    if blinkTime > 195 and not scanning and face != lonely:
        face = oldface
        blinkTime = 0
#centers the streak number in the heart
    with open('totalLog.txt','r') as f:
        file = f.read()
        total = len(file.split('\n'))
    if len(str(streak)) > 1:
        adjustmentX = 6
    if len(str(streak)) > 2:
        adjustmentX = 12
    if len(str(streak)) < 2:
        adjustmentX = 0
#defines text and font objects
    message = str(streak)
    
    font = pygame.font.SysFont('Consolas', 20)
    text_surface = font.render(message, False, textColour)
    commentaryText = font.render(commentary, False, BLACK)
    name = font.render(str(nameText), False, (0, 0, 0))
    ssidText = font.render(str(ssids-1), False, (0, 0, 0))
    countText = font.render(str(total+addup-1), False, (0, 0, 0))
    wardrivemode = font.render("w", False, (0,0,0))
    #streak effects
    if longestStreak < 10:
        screen.blit(low, (25,10))
    elif longestStreak < 30:
        screen.blit(medium, (25,10))
    elif longestStreak <= 100:
        screen.blit(high, (25,10))
    elif longestStreak > 100:
        screen.blit(godtier, (25,10))
        textColour = (245, 227, 66)
#render all objects
    screen.blit(face,(0, 20))
    screen.blit(commentaryText,(20, 100) )
   
   
    screen.blit(ssidText, (230,40))
    screen.blit(countText, (230,60))
    screen.blit(text_surface, (176-adjustmentX,50))
    if wardriving:
        screen.blit(wardrivemode, (233,73))
    screen.blit(name, (10, 10))
    timer+=1
    actualTime += 1
    pygame.display.flip()
    clock.tick(60)
    
    
pygame.quit()
#Congratulations! You've read the the entirety of my spagheti code! 
    
