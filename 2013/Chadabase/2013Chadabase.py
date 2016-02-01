# Database program - gets DS information and gives statistics
# 0.0
# To Do:
# Work on Getting the Teams and Ranking to work
#          Improve Framerate on Alliance Selection Tab
#imports
import math
import pygame
import tkFileDialog     #For open and save dialogs
import tkSimpleDialog   #Simple input
import pickle
import os
import csv # For using access filetype .csv
from Tkinter import *
from statlib import stats #to get prob(z-score), use stats.lzprob(z)
pygame.init()


# Main variables
running = True
TeamCalc = False  #Whether or not the data was calculated (if it hasn't been, you can't view team data)
PitCalc  = False  #whether or not the pitdata was calculated
HEIGHT = 700
WIDTH = 1200
x0 = 160  # initial x-coordinate for the TAB
y0 = 65  # initial y-coordinate for the TAB
bgcolor = (0,51,0)
txcolor = (255,223,0)

Reload = False

root = Tk()
root.withdraw()

#screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("ultimAteAscent Chadabase_0.4")
tab = 0     # The tab displayed:
            # 0 - blank
            # 1 - Team
            # 2 - Pit
            # 3 - Ranking
            # 4 - Rank2 (possible)
            # 5 - Search
            # 6 - Compare (Alliances)
            # 7 - Choose (During Actual Alliance Selection[Function: Alliance_Selection()])
last = 0    #used for measuring fps
curfile = ""    #Current data file

# Stored Data
TeamEntries = []                                    # All the TeamEntries; 6 entries per match (1 per team)
#PitEntries = []                                     # All the PitEntries; 1 pitentry per term, to enter the bot shape info
Teams = []                                          # All of the teams and their data (see 'Team' class)
Matches = []                                        # All of the match data.
overal_score = 0                                    # Overall score for all matches
tb_buttons = []                                     #task bar button
t1_tboxes = []                                      #tab 1(Team) textboxes
t1_pic = None
teamnumber = 0
t1_update = True                                    #update team 2; preset to true so tboxes are drawn the first time
t1_surface = pygame.Surface((WIDTH-160,HEIGHT-65))  # surface for the second tab (to improve framerate)
t1_lreg = 0                                         # linear regression graph

#t2_tboxes = []
#t2_update = True
#t2_surface = pygame.Surface((WIDTH-160,HEIGHT-65))

t3_scrolls = []                                     #tab 3 (ranking) scrollers
t3_buttons = []                                     # rank buttons for scrolling

t4_scrolls = []                                    # hopefully only need 1 raking tab, but just in case
t4_buttons = []

Searches = {}
t5_stuff = []                                       #tab 5(Search) textboxes and radio boxes
t5_scroll = 0                                       #tab 5's scroller; create later before main loop
t5_wscroll = 0                                      #tab 5's scroller for teams we want on our alliance
t5_tempbut = []                                     # Temporary buttons
t5_temprad = []                                     # Temporary radio buttons
t5_wbut = []                                        # Temporary buttons for wanted teams
t5_wrad = []                                        # Temporary radio buttons for wanted teams
update_wanted = False                               # Whether or not to update the wanted teams in tab 5
t5_update = False                                   # Whether or not tab 5's data needs to be updated
t5_redraw = False                                   # Whether or not to redraw tab 4's scroller (so that radio buttons can become unchecked
t5_wbmov = []                                       # List for buttons that move wanted rank +/- 1
t5_buttons = []                                     #tab 5's buttons

t6_surface = pygame.Surface((WIDTH-160,HEIGHT-65))  #surface for the fifth tab (to improve framerate)
t6_update = True                                       # Whether or not to update tab 6
t6_tboxes = []                                      # tab 6 (comparison) textboxes

t7_tboxes = []                                      #All the text boxes for tab 7
t7_scroll = []                                      #Scroller for tab 7 (shows wanted teams [only those that have not been selected])
t7_buttons = []                                     # buttons for tab 7
t7_update = True                                    # whether or not to update tab 7 (alliance selection)
t7_surface = pygame.Surface((WIDTH-160,HEIGHT-65))
available_teams = []                                #Teams that are available for alliance selection
wanted = []                                         # List of teams we want on our alliance

r1o = r1d = r1a = r1th = r1ah = r1hs = r1ab = r1bo = r1md = r1tt = r1tp = r1ha = r1as = r1po = r1pd = r1pa = r1t = r1ts = 0
r2o = r2d = r2a = r2th = r2ah = r2hs = r2ab = r2bo = r2md = r2tt = r2tp = r2ha = r2as = r2po = r2pd = r2pa = r2t = r2ts = 0
r3o = r3d = r3a = r3th = r3ah = r3hs = r3ab = r3bo = r3md = r3tt = r3tp = r3ha = r3as = r3po = r3pd = r3pa = r3t = r3ts = 0
b1o = b1d = b1a = b1th = b1ah = b1hs = b1ab = b1bo = b1md = b1tt = b1tp = b1ha = b1as = b1po = b1pd = b1pa = b1t = b1ts = 0
b2o = b2d = b2a = b2th = b2ah = b2hs = b2ab = b2bo = b2md = b2tt = b2tp = b2ha = b2as = b2po = b2pd = b2pa = b2t = b2ts = 0
b3o = b3d = b3a = b3th = b3ah = b3hs = b3ab = b3bo = b3md = b3tt = b3tp = b3ha = b3as = b3po = b3pd = b3pa = b3t = b3ts = 0


r1 = r2 = r3 = b1 = b2 = b3 = 0
r1t = r2t = r3t = b1t = b2t = b3t = 0               #average total scores
r1ts = r2ts = r3ts = b1ts = b2ts = b3ts = 0         #total scores for each team

tabnum = 0
accessinfo = ""                                     #a file that can be opened in access will be created for editing purposes

#ranking info
off_rank = []
def_rank = []
ast_rank = []
tot_rank = []

auto_rank = []
tel_rank = []
pyr_rank = []

team_list = []                                      #Made global so that button and radio objects can be created in search tab
old_list = []                                       #Old team list; compare to team_list to see if update needed

#----------------------------------------------------------------------------------------------------
# Linear Regression class
# -- Gives you information on a linear regression, and can return a graph
#----------------------------------------------------------------------------------------------------
class lreg():
    def __init__(self,datax=[],datay=[],a=0,b=0,r=0):
        #Make all of the numbers floats
        self.x = []
        self.y = []
        for num in datax:
            self.x.append(long(num))
        for num in datay:
            self.y.append(long(num))
        self.b = 0 #slope
        self.a = 0 #constant
        self.r2 = 0 #coefficient of determination
    def get_ab(self):
        n = float(len(self.x))
        self.xy = []
        self.x2 = []
        self.y2 = []
        i = 0
        while i < len(self.x):
            self.xy.append(self.x[i]*self.y[i])
            self.x2.append(self.x[i]**2)
            self.y2.append(self.y[i]**2)
            i += 1
        try:
            self.b = (n*sum(self.xy)-sum(self.x)*sum(self.y))/(n*sum(self.x2)-sum(self.x)**2)
        except:
            self.b = 100000000000000000000000
        self.a = (sum(self.y)/float(len(self.y))) - self.b*(sum(self.x)/len(self.x))
        #Get r2
        hmy2 = []
        ymh2= []
        i = 0
        try:
            while i < len(self.y):
                hy = self.x[i]*self.b+self.a
                hmy2.append((hy-(sum(self.y)/len(self.y)))**2)
                ymh2.append((self.y[i]-(sum(self.y)/len(self.y)))**2)
                i += 1
            self.r2 = sum(hmy2)/sum(ymh2)
        except:
            self.r2 = "N\A"
    def get_image(self,sx,sy,bgcolor,txcolor,stx=20,sty=20):
        self.surface = pygame.Surface((sx,sy))
        self.surface.fill(bgcolor)
        self.tx = [] # x coordinates modified to fit
        self.ty = [] # y coordinates modified to fit
        maxy = 0
        for y in self.y:
            if y > maxy: maxy = y
        xmod = (sx-2*stx)/float(len(self.x))
        # Always start at x=0
        for point in self.x:
            self.tx.append(xmod*point+stx)
        # Start at y=0
        if maxy != 0: ymod = (sy-2*sty)/float(maxy)
        else: ymod = sy-2*sty
        for point in self.y:
            self.ty.append(ymod*point+sty)
        # Remember that the image is flipped.
        x1 = stx
        x2 = sx-stx
        y1 = sty
        y2 = sy-sty
        #Draw axes
        pygame.draw.line(self.surface,(0,0,0),(x1,y1),(x2,y1),1)
        pygame.draw.line(self.surface,(0,0,0),(x1,y1),(x1,y2),1)
        #Draw numbers at end of axes to indicate max value of each axis
        xmax = 0
        ymax = 0
        for num in self.x:
            if num > xmax: xmax = num
        for num in self.y:
            if num > ymax: ymax = num
        # Draw points on graph
        i = 0
        while i < len(self.tx):
            pygame.draw.circle(self.surface,(255,0,0),(int(self.tx[i]),int(self.ty[i])),(int((sx+sy)/100)))
            i += 1
        i = 1
        #pygame.draw.line(screen,(0,0,0),(302,65),(302,HEIGHT),1)
        while i < len(self.tx):
            pygame.draw.line(self.surface,(0,0,0),(self.tx[i-1],self.ty[i-1]),(self.tx[i],self.ty[i]))
            i += 1
        # Draw the line of best fit
        #self.tx.append(xmod*point+stx)
        #self.ty.append(ymod*point+sty)
        p1 = (x1,self.a*ymod+sty) # B = slope
        p2 = (len(self.x)*xmod+stx,(self.b*len(self.x)+self.a)*ymod+sty)
        pygame.draw.line(self.surface,(0,0,255),(stx,self.a*ymod+sty),(len(self.x)*xmod+stx,(self.b*len(self.x)+self.a)*ymod+sty))
        #Flip and add text
        newsurface = pygame.transform.flip(self.surface,0,1)
        font = pygame.font.Font(None,stx)
        text = font.render(str(ymax),True,txcolor,bgcolor)
        newsurface.blit(text,(0,.5*stx))
        text = font.render(str(xmax),True,txcolor,bgcolor)
        newsurface.blit(text,(sx-.5*stx,sy-stx))
        text = font.render("r^2="+str(self.r2),True,txcolor,bgcolor)
        newsurface.blit(text,(0,sy-stx))
        return newsurface
#----------------------------------------------------------------------------------------------------
# Scroller Class
#----------------------------------------------------------------------------------------------------
class scroller():
    def __init__(self,surface,maxheight=100,x=0,y=0,t="test"):
        self.type = t
        self.x=x
        self.y=y
        self.surface=surface
        self.maxh=maxheight
        self.currenty=0 #Scroll distance
        self.maxy = pygame.Surface.get_height(self.surface)-self.maxh
        self.speed = 1.5*self.maxy/self.maxh
    def draw(self,screen):
        self.width = pygame.Surface.get_width(self.surface)
        screen.blit(self.surface,(self.x,self.y),[0,self.currenty,self.width,self.maxh])
    def update(self,direction):
        if direction == 1 and self.currenty >= self.speed: #Scroll up
            self.currenty -= self.speed
        if direction == 0 and self.currenty + self.speed <= self.maxy:#scroll down
            self.currenty += self.speed

#----------------------------------------------------------------------------------------------------
# Radio Button Class
#----------------------------------------------------------------------------------------------------
class radio():
    def __init__(self,t="t",x=0,y=0,caption="Test:",flip=0,fs=50,check=0,teamnum=0):
        global bgcolor
        global txcolor
        self.x=x
        self.y=y
        self.type=t
        self.caption=caption
        self.flip=flip  #1 = text shows up on right of button
        self.size=fs
        font=pygame.font.Font(None,self.size)
        self.text = font.render(self.caption,True,txcolor,bgcolor)
        self.w = pygame.Surface.get_width(self.text)
        self.check=bool(check)
        self.teamnum = teamnum #Only used in the search tab; has no other use
    def draw(self,screen):
        if self.check:
            if self.flip: # Button to left
                pygame.draw.circle(screen,(0,0,0),(self.x+int(.5*self.size),self.y+int(.4*self.size)),
                                   int(.25*self.size),0)
                screen.blit(self.text,(self.x+self.size,self.y))
            else: # button to right
                screen.blit(self.text,(self.x,self.y))
                pygame.draw.circle(screen,(0,0,0),(self.x+self.w+int(.5*self.size),self.y+int(.4*self.size)),
                                   int(.25*self.size),0)
        else:
            if self.flip: # button to left
                pygame.draw.circle(screen,(0,0,0),(self.x+int(.5*self.size),self.y+int(.4*self.size)),
                                   int(.25*self.size),int(.1*self.size))
                screen.blit(self.text,(self.x+self.size,self.y))
            else:   # button to right
                screen.blit(self.text,(self.x,self.y))
                pygame.draw.circle(screen,(0,0,0),(self.x+self.w+int(.5*self.size),self.y+int(.4*self.size)),
                                   int(.25*self.size),int(.1*self.size))
    def click(self):
        self.check = not self.check

#----------------------------------------------------------------------------------------------------
# Textbox Class
#----------------------------------------------------------------------------------------------------
class textbox():
    def __init__(self,t="t",x=0,y=0,w=100,caption="Test:",fs=50,thickness = 1,clickable=0,val=0):
        global bgcolor
        global txcolor
        self.x=x
        self.y=y
        self.w=w
        self.type = t
        self.click = clickable
        self.caption = caption
        self.size = fs
        self.value = val
        self.th = thickness
        self.type = t
        font= pygame.font.Font(None,self.size)
        self.text= font.render(self.caption,True,txcolor,bgcolor)
        self.cw = pygame.Surface.get_width(self.text)
        self.ch = pygame.Surface.get_height(self.text)
        if self.click == 1:
            self.color = (0,255,0)
        else:
            self.color = bgcolor
    def draw(self,screen):
        global txcolor
        global bgcolor
        #draw caption
        screen.blit(self.text,(self.x+.5*self.th,self.y+.5*self.th))
        #draw textbox
        pygame.draw.rect(screen, self.color, (self.x+self.cw+.5*self.th,
                                              self.y+.5*self.th,self.w+.5*self.th,self.size+.5*self.th-10),
                         self.th)
        f2 = pygame.font.Font(None,self.size-self.th) #Account for thickness in rectangle
        intxt = f2.render(str(self.value),True,txcolor,bgcolor)
        screen.blit(intxt,(self.x+self.cw+self.th,self.y+self.th))
    def clicked(self):
        global root
        global screen
        global WIDTH
        global HEIGHT
        global teamnumber
        if self.click == 1: #Is clickable
            root.focus()
            newval = tkSimpleDialog.askstring("New Value","_",parent=root,initialvalue=0)
            root.withdraw()
            if newval == "": newval = 0
            self.value = newval
            teamnumber = newval
    def update(self,surface):
        print "updating"

#----------------------------------------------------------------------------------------------------
# Button Class
#----------------------------------------------------------------------------------------------------
class button():
    def __init__(self,t="none",x=0,y=0,w=0,h=0,text="Press Me",font=50,thickness = 1,static=1):
        global bgcolor
        global txcolor
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.text = text
        self.size = font
        self.type = t
        self.static=1
        self.th = thickness
        font = pygame.font.Font(None,self.size)
        self.text= font.render(self.text,True,txcolor,bgcolor)
        self.w = pygame.Surface.get_width(self.text) if w==0 else w
        self.h = pygame.Surface.get_height(self.text) if h==0 else h

    def draw(self,screen):
        screen.blit(self.text,(self.x+.5*self.th,self.y+.5*self.th))
        pygame.draw.rect(screen, (255,0,0), (self.x,self.y,self.w+.5*self.th,self.h+.5*self.th),self.th)
    def click(self):
        global TeamEntries
        global tab
        global root
        global screen
        global curfile
        if self.type == "s": # save
            print "Saving"
            try:
                root.focus()
                filename = tkFileDialog.asksaveasfilename(parent=root)
                root.withdraw()
                filename = str(filename)
                data = pickle.dumps(TeamEntries)
                dfile = open(filename,"w")
                dfile.write(data)
                dfile.close()
                curfile = filename
                pygame.display.set_caption("Database -- " + filename)
                output_data()
                save_csv()
            except:
                print "save failed"
        elif self.type == "t":              # view team data
            tab = 1
        #elif self.type == "ps":             # view pit data
        #    tab = 2
        elif self.type == "r":              # View rankings
            tab = 3
        elif self.type == "r2":             # view rank2
            tab = 4
        elif self.type == "se":             # Search
            tab = 5
        elif self.type == "co":             # Compare Alliances
            tab = 6
        elif self.type == "ch":             # Choose Alliances
            tab = 7
        elif self.type == "i": #import data
            TeamDataImported = False
            try:
                import_data()
                TeamDataImported = True
            except:
                print "Could Not Import TeamData"
                
            if TeamDataImported: calculate()
##        elif self.type == "ip":
##            #if TeamCalc == True:
##            PitDataImported = False
##            try:
##                import_data2()
##                PitDataImported = True
##            except:  print "Could Not Import PitData"
##            if PitDataImported: calculate2()
        elif self.type == "o": #open
            print "opening"
            try:
                root.focus()
                filename = tkFileDialog.askopenfilename(parent=root)
                root.withdraw()
                filename = str(filename)
                dfile = open(filename,"r")
                data = pickle.load(dfile)
                print "data loaded"
                TeamEntries = data
                global Teams
                global Matches
                Teams = []
                Matches = []
                print str(TeamEntries)
                calculate()
                pygame.display.set_caption("Database -- " + filename)
            except:
                print "error opening"

#----------------------------------------------------------------------------------------------------
# Picture Class
#----------------------------------------------------------------------------------------------------
class Picture():
    def __init__ (self,x=0,y=0,val=0):
        self.x = x
        self.y = y
        self.number = val
        self.gifname = str(val) + ".gif"
        self.img = pygame.image.load(self.gifname)
    def draw(self,surface,val=0):
        try:
            self.number = val
            self.gifname = str(val) + ".gif"
            self.img = pygame.image.load(self.gifname)
        except:
            self.number = 0
            self.gifname = str(self.number) + ".gif"
            self.img = pygame.image.load(self.gifname)
        surface.blit(self.img,(self.x,self.y))

#----------------------------------------------------------------------------------------------------
# Entry Class
#   -- Equivalent to a single ms-access entry
#   -- Each amtch has 6 of these entries
#----------------------------------------------------------------------------------------------------
class Entry():
    # 1 per team per match
    def __init__(self,data):
        self.Match = data[0]                                        #The number of the match
        self.Team = data[1]                                         #The team number
        self.AllianceColor = data[2]                                #The color for the match

        self.StartInAutoZone = bool(data[3])                           #if robot starts completely in Autonomous Zone
        self.autoDiscs = float(data[4])                                  #number of discs picked up in auto
        self.autoTopP = float(data[5])                                  #number of scores in the Top
        self.autoMidP = float(data[6])                                    #number of scores in the Middle
        self.autoLowP = float(data[7])                                    #number of scores in the Low
        self.Other = bool(data[8])                                        #if robot had a different strategy during autonomous

        self.disabledCount = float(data[9])                                #number times robot was disabled during Tele-Op
        self.ScoreFromNotZone = bool(data[10])                           #if robot scores from beyond the auto zone
        self.teleFloorDiscs = float(data[11])                              #number of discs picked up off the floor
        self.teleStationDiscs = float(data[12])                            #number of discs picked up off the ground
        self.telePyrP = float(data[13])                                   #number of scores in the pyramid
        self.teleTopP = float(data[14])                                    #number of scores in the top
        self.teleMidP = float(data[15])                                   #number of scores in the mid
        self.teleLowP = float(data[16])                                    #number of scores in the low

        self.ScoresWhileOnPyr = bool(data[17])                            #if robot scored points while climbing
        self.SupportsAnotherBot = bool(data[18])                          #if robot supported another bot while climbing
        self.HangLevel = float(data[19] + 1)                               #level robot got to, whether it was successfuly or not
        self.HangSuccess = bool(data[20])                                 #if robot was actually successful at climbing

        self.Defensive = bool(data[21])                                   #if robot played defensively
        self.Assistive = bool(data[22])                                   #if robot played assistively
        self.Technical = float(data[23])                                   #number of technical fouls incurred
        self.Regular = float(data[24])                                     #number of regular fouls incurred
        self.YellowPenalty = bool(data[25])                               #if a yellow_card was received
        self.RedPenalty = bool(data[26])                                  #if a red_card was received

        self.disabled = True if self.disabledCount>0 else False                         #is robot was disabled at all during match
        self.DiscsScored = self.telePyrP + self.teleTopP + self.teleMidP + self.teleLowP#number of discs scored during match
        self.AutoDiscsScored = self.autoTopP + self.autoMidP + self.autoLowP            #number of discs scored during autonomous
        self.DiscsPU = self.teleFloorDiscs + self.teleStationDiscs                      #number of discs picked up during match

    def primary_sort(self):
        # Gets the match offensive score, whether the robot was offensive, etc.
        self.autoScore = (2*self.autoLowP) + (4*self.autoMidP) + (6*self.autoTopP)
        self.teleScore = self.teleLowP + (2*self.teleMidP) + (3*self.teleTopP) + (5*self.telePyrP)

        self.ScoreInAuto = True if self.autoScore > 0 else False
        self.ScoreInTele = True if self.teleScore > 0 else False
        self.HasTechFoul = True if self.Technical > 0 else False
        self.HasRegFoul = True if self.Regular > 0 else False

        self.hangScore = (10*self.HangLevel) if self.HangSuccess else 0
        self.AttemptedHangScore = (10*self.HangLevel)

        self.offensiveScore = self.autoScore + self.teleScore + self.hangScore
        self.teleautoScore = self.autoScore + self.teleScore
        self.foulScore = (3*self.Regular) + (20*self.Technical)

        # If the robot was offensive during the match
        self.isOffensive = True if self.offensiveScore > 0 else False

    def secondary_sort(self,oppAvg,oppOff,allAvg,allOff,allDef,allAst):
        self.defScore = (allOff - oppOff - (allAvg - oppAvg)) / allDef if self.Defensive else 0     # keep messing with this until it comes up with
        self.astScore = (allAvg + allOff - oppAvg - oppOff) / allAst / 6 if self.Assistive else 0 # reasonable values instead of just crap
    def tertiary_sort(self):
        self.totalScore = self.defScore + self.astScore + self.offensiveScore - self.foulScore
        self.totaltaScore = self.defScore + self.astScore + self.teleautoScore

#----------------------------------------------------------------------------------------------------
# Entry2 Class
# -- Gets the robot chasis type
#----------------------------------------------------------------------------------------------------
##class entry2():
##    def __init__(self,data):
##        self.team = data[0]
##
##        self.roblength = data[1]
##        self.robwidth = data[2]
##        self.robheigth = data[3]
##        self.robwieght = data[4]
##        self.clearance = data[5]
##        self.spacing = data[6]
##
##        self.BrdgMech = data[7]
##        self.SlideBrdg = data[8]
##        self.balsensor = data[9]
##        self.DriSys = data[10]
##        self.ShiftGear = data[11]
##
##        self.CenMass = data[12]
##
##        self.Drive1 = data[13]
##        self.exp1 = data[14]
##
##        self.Drive2 = data[15]
##        self.exp2 = data[16]
##
##        self.Drive3 = data[17]
##        self.exp3 = data[18]
##
#----------------------------------------------------------------------------------------------------
# Team Class
#   --Stores team data
#----------------------------------------------------------------------------------------------------
class Team():
    def __init__(self,num):
        self.number = num
        self.matches = []           # list holding all the matches the team is in
        self.oScores = []           # list holding all of the Elimination offensive scores
        self.dScores = []           # list holding all of the defensive scores
        self.aScores = []           # list holding all of the assistive scores
        self.tScores = []           # list holding all of the Elimination total scores
        self.wScores = []           # list holding all of the weighted scores
        self.woScores = []          # list holding all of the weighted offensive scores
        self.wdScores = []          # list holding all of the weighted defensive scores
        self.waScores = []          # list holding all of the weighted assistive scores
        self.taScores = []          # list holding the sum of tele and hybd scores for all the matches
        self.hangLevel = []         # list holding the level of hang for each match
        self.hangSuccess = []       # list holding success of hanging for each match
        self.hangScores = []        # list holding the hangScores for each match
        self.timesHanged = 0        # the number of matches for which the team hanged successfully
        self.attemptedHang = 0      # the number of matches for which the team attempted to hang
        self.SupportsBot = []       # list holding whether the robot supported another robot for climbing
        self.ScoredOnPyr = []       # list holding whether the robot scored while on the pyramid
        self.numOff = 0             # the number of matches for which the team was offensive
        self.numDef = 0             # the number of matches for which the team was defensive
        self.numAst = 0             # the number of matches for which the team was assistive

        self.hadAuto = 0            # the number of matches for which the team had an autonomous that did something
        self.StartedInAuto = 0      # the number of matches for which the team started in the AutoZone
        self.OtherAutoStrat = 0     # the number of matches for which the team had another strategy (other than offense) in Auto
        self.autoDiscsScored = []   #discs scored in auto for each match
        self.autoDiscsPU = []       # list holding the number of discs picked up during auto each match
        self.autoTopP = []          # list holding the number of discs scored in the top in auto for each match
        self.autoMidP = []          # list holding the number of discs scored in the middle in auto for each match
        self.autoLowP = []          # list holding the number of discs scored in the low in auto for each match
        self.autoScores = []        # list holding the the auto scores for each match
        self.scoredAuto = 0         # the number of matches for which the team scored in auto

        self.hadTele = 0            # the number of matches for which the robot scored in tele-op
        self.disabledState = []     # list holding the disabled state for each match
        self.disabled = 0           # the number of matches for which the robot was disabled
        self.disabledCount = 0      # the number of times the robot was disabled total
        self.teleFloorDiscsPU = []  # discs picked up from floor for each match
        self.teleStationDiscsPU = []# discs picked up from loading station for each match
        self.DiscsPU = []           # list holding the number of discs picked up total for each match (in tele)
        self.teleDiscsScored = []   # discs scored in tele for each match
        self.teleScores = []        # list holding the tele scores for each match
        self.telePyrP = []          # list holding the discs scored in the pyramid
        self.teleTopP = []          # list holding the discs scored in the top
        self.teleMidP = []          # list holding the discs scored in the middle
        self.teleLowP = []          # list holding the discs scored in the bottom

        self.avgRegFoul = []        # list holding the number of regular fouls for each match
        self.avgTechFoul = []       # list holding the number of technical fouls for each match
        self.hadRegFoul = 0         # the number of matches for which the team incurred regular fouls
        self.hadTechFoul = 0        # the number of matches for which the team incurred technical fouls
        self.hadYellow = 0          # the number of matches for which the team received a yellow card
        self.hadRed = 0             # the number of matches for which the team received a red card
        self.Defensive = 0          # the number of matches for which the team was defensive
        self.Assistive = 0          # the number of matches for which the team was assistive

        self.off_rank = 0           #ranks among all teams
        self.def_rank = 0
        self.ast_rank = 0
        self.tot_rank = 0
        self.auto_rank = 0
        self.tel_rank = 0
        self.pyr_rank = 0

        #self.robotlen = 0
        #self.robotwid = 0
        #self.robotheg = 0
        #self.robotwig = 0
        #self.floorclear = ""
        #self.wheelspace = ""
        #self.BridgeMechanics = ""
        #self.SldBridge = ""
        #self.ballsen = ""
        #self.ShiftGear = ""
        #self.DriveSystem = ""
        #self.CenterMass = ""
        #self.Driver1 = ""
        #self.experince1 = None
        #self.Driver2 = ""
        #self.experince2 = None
        #self.Driver3 = ""
        #self.experince3 = None

    def get_avg_Off(self):
        self.avgTeleAutoOff = sum(self.taScores)/len(self.matches) if self.numOff > 0 else 0
        self.avgOff = sum(self.oScores)/len(self.matches) if self.numOff > 0 else 0

    def get_avg_DefAst(self):
        self.avgDef = sum(self.dScores)/len(self.matches) if self.numDef > 0 else 0
        self.avgAst = sum(self.aScores)/len(self.matches) if self.numAst > 0 else 0

    def get_avg_Hang(self):
        self.timesHanged = float(sum(self.hangSuccess))
        for var in self.hangSuccess:
            if var == 0:
                self.attemptedHang += 1
                
        self.hangsSucctoAtt = self.timesHanged/self.attemptedHang if self.attemptedHang else 0
        self.avgHangScore = sum(self.hangScores)/self.timesHanged if self.timesHanged else 0

        self.TotalSupportsBot = float(sum(self.SupportsBot))
        self.TotalScoredOnPyr = float(sum(self.ScoredOnPyr))

    def get_avg_AutoTele(self):
        self.avgAuto = sum(self.autoScores)/self.hadAuto if self.hadAuto else 0
        self.avgTele = sum(self.teleScores)/self.hadTele if self.hadTele else 0
        self.discsPUtoScored = sum(self.DiscsPU)/sum(self.teleDiscsScored) if sum(self.teleDiscsScored)>0 else 0

    def getAttribute(self, source):
        dataSource = getattr(self, source)
        return dataSource

#----------------------------------------------------------------------------------------------------
# Match Class
#   -- Stores all match data
#----------------------------------------------------------------------------------------------------
class Match():
    def __init__(self,num):
        self.number = num   # Match Number
        self.teams = []     # The teams in the match
        self.team0 = []     # the teams in the first alliance
        self.team1 = []     # the teams in the second alliance
        self.all0 = []      # The teams in the first alliance
        self.all1 = []      # The teams in the second alliance
        self.off0 = 0       # The total offensive score for the first alliance
        self.off1 = 0       # The total offensive score for the second alliance
        self.noff0 = 0      # The nunber of offensive teams for the first alliance
        self.noff1 = 0      # The number of offensive teams for the second alliance
        self.THangScore0 = 0# the score of first alliance for each match from the pyramid
        self.THangScore1 = 0# the score of second alliance for each match from the pyramid
        self.defense0 = 0   # The number of defensive teams in the first alliance
        self.assist0 = 0    # The number of assistive teams in the first alliance
        self.defense1 = 0   # The number of defensive teams in the second alliance
        self.assist1 = 0    # The number of assistive teams in the second alliance
        self.avgSum0 = 0    # The total of the average offensive scores for the first alliance
        self.avgSum1 = 0    # The total of the average offensive scores for the second alliance
        self.taavgSum0 = 0  # The average sum of the first alliance's auto and tele score
        self.taavgSum1 = 0  # The average sum of the second alliance's auto and tele score
        self.def0 = 0       # Total defensive score for first alliance
        self.def1 = 0       # Total defensive score for the second alliance
        self.ast0 = 0       # Total assistive score for the first alliance
        self.ast1 = 0       # Total assistive score for the second alliance
    def get_total(self):
        self.total0 = self.off0 + self.THangScore0 #+self.def0                  #Total score for first alliance
        self.total1 = self.off1 + self.THangScore1 #+ self.def1                 #Total score for second alliance
        self.overall = self.total0 + self.total1                                # Total match score


#----------------------------------------------------------------------------------------------------
# Output Data Function
# -- outputs access-importable text file with all information
#----------------------------------------------------------------------------------------------------
def output_data():
    global TeamEntries
    global curfile
    #if data file exists, destroy it
    try:
        os.delete(curfile+"_access.txt")
    except:
        print ""
    #open file for writing
    filetosave = open(curfile+"_access.txt","w")
    print "File Opened"
    n = 0
    outstring = ""
    while n < len(TeamEntries):
        outstring = ""
        for element in TeamEntries[n].stored_data:
            outstring += str(element) + ","
        oustring = outstring.strip(",")     #remove unnecessary last ","
        oustring += "\r\n" #new line at end
        filetosave.write(outstring)
        n += 1
    print "loop ended"
    filetosave.close()

def save_csv():
    global TeamEntries
    global curfile
    rows = []
    for entry in aEntries:
        rows.append(entry.stored_data)
    try:
        os.delete(curfile+"_access.txt")
    except:
        writer = csv.writer(open(curfile+"_access.txt","wb"))
        writer.writerows(rows)
    print writer
#----------------------------------------------------------------------------------------------------
# Import Data Function
#----------------------------------------------------------------------------------------------------
def import_data():
    global TeamEntries
    global TeamCalc
    global old_file
    global Reload
    #TeamCalc = False
    if not TeamCalc:
        if Reload:
            oldFile = open("old_file.txt","r")
            Filename = oldFile.read()
            new_data = open(Filename,"r")
            print "file opened"
            
        else:
            filename = tkFileDialog.askopenfilename()
            filename = str(filename)
            print "file selected"
            filename = os.path.basename(filename)
            print filename
            new_data = open(filename,"r")
            print "file opened"

            oldFile = open("old_file.txt","w")
            oldFile.write(filename)
            
        # Clean out the data except for TeamEntries.  This way, data won't count multiple teams during
        # calculations
        global Teams
        global Matches
        Teams = []
        Matches = []
        # Now that the file is loaded, you need to parse it
        print "Parsing Data"
        for line in new_data:
            TeamEntries.append(parse_data(line))
        print "--Data parsed"

    #except:
    #    print "error"
#----------------------------------------------------------------------------------------------------
# Import Data2 Function
#----------------------------------------------------------------------------------------------------
##def import_data2():
##    global PitEntries
##    global PitCalc
##    global Teams
##    PitCalc = False
##    if not PitCalc:
##        filename = tkFileDialog.askopenfilename()
##        filename = str(filename)
##        print "file selected"
##        filename = os.path.basename(filename)
##        print filename
##        new_data = open(filename,"r")
##        print "file opened"
##
##        print "Prasing Data 2"
##        p=0
##        for line in new_data:
##            p +=1
##            entries2.append(parse_data2(line))
##            print "p"
##            print p
##        print "hi"
##        print "--Data 2 parsed"
#----------------------------------------------------------------------------------------------------
# Parse Data Function - Takes each line in the file and transfers it to an entry
#----------------------------------------------------------------------------------------------------
def parse_data(info):
    data = []
    i = 0
    new = ""
    while i < 27:
        for character in info:
            if character != "," and character != "\n":
                new += str(character)
            else:
                data.append(int(new))
                new = ""
                i += 1
                if i >= 27: break
                
    return Entry(data)

##def parse_data2(info):
##    data = []
##    i = 0
##    next = ""
##    while i < 19:
##        for character in info:
##            if character != "," and character != "\n":
##                next += str(character)
##            else:
##                data.append(int(next))
##                next = ""
##                i += 1
##                print "i"
##                print i
##                if i >= 19: break
##    return entry2(data)
#----------------------------------------------------------------------------------------------------
# Calculate Function - Calculates data for statistical analysis.
#                    - Both overall and team data created
#----------------------------------------------------------------------------------------------------
def calculate():
    global TeamEntries
    global Teams
    global TeamCalc
    global available_teams
    # Get offensive scores, whether the team was defensive this match, and whether they were defensive.
    for entry in TeamEntries:
        entry.primary_sort()
    # Create team data
    for entry in TeamEntries:
        done = False
        for t in Teams:
            if t.number == entry.Team:
                t.matches.append(entry.Match)
                t.oScores.append(entry.offensiveScore)
                t.taScores.append(entry.teleautoScore)
                t.numOff += int(entry.isOffensive)
                t.numDef += int(entry.Defensive)
                t.numAst += int(entry.Assistive)

                t.hangLevel.append(entry.HangLevel)
                t.hangSuccess.append(entry.HangSuccess)
                t.hangScores.append(entry.hangScore)
                t.SupportsBot.append(entry.SupportsAnotherBot)
                t.ScoredOnPyr.append(entry.ScoresWhileOnPyr)

                t.hadAuto = t.hadAuto + 1 if (entry.ScoreInAuto or entry.Other) else t.hadAuto
                t.StartedInAuto += int(entry.StartInAutoZone)
                t.OtherAutoStrat += int(entry.Other)
                t.autoDiscsScored.append(entry.AutoDiscsScored)
                t.autoDiscsPU.append(entry.autoDiscs)
                t.autoTopP.append(entry.autoTopP)
                t.autoMidP.append(entry.autoMidP)
                t.autoLowP.append(entry.autoLowP)
                t.autoScores.append(entry.autoScore)
                t.scoredAuto += int(entry.ScoreInAuto)

                t.hadTele += int(entry.ScoreInTele)
                t.disabledState.append(entry.disabled)
                t.disabled += int(entry.disabled)
                t.disabledCount += entry.disabledCount
                t.teleFloorDiscsPU.append(entry.teleFloorDiscs)
                t.teleStationDiscsPU.append(entry.teleStationDiscs)
                t.DiscsPU.append(entry.DiscsPU)
                t.teleDiscsScored.append(entry.DiscsScored)
                t.teleScores.append(entry.teleScore)
                t.telePyrP.append(entry.telePyrP)
                t.teleTopP.append(entry.teleTopP)
                t.teleMidP.append(entry.teleMidP)
                t.teleLowP.append(entry.teleLowP)

                t.avgRegFoul.append(entry.Regular)
                t.avgTechFoul.append(entry.Technical)
                t.hadRegFoul += int(entry.HasRegFoul)
                t.hadTechFoul += int(entry.HasTechFoul)
                t.hadYellow += int(entry.YellowPenalty)
                t.hadRed += int(entry.RedPenalty)
                t.Defensive += int(entry.Defensive)
                t.Assistive += int(entry.Assistive)

                done = True
        if done == False:
            Teams.append(Team(entry.Team))
            print "Added team#" + str(entry.Team)

            Teams[len(Teams)-1].matches.append(entry.Match)
            Teams[len(Teams)-1].oScores.append(entry.offensiveScore)
            Teams[len(Teams)-1].taScores.append(entry.teleautoScore)
            Teams[len(Teams)-1].numOff += int(entry.isOffensive)
            Teams[len(Teams)-1].numDef += int(entry.Defensive)
            Teams[len(Teams)-1].numAst += int(entry.Assistive)

            Teams[len(Teams)-1].hangLevel.append(entry.HangLevel)
            Teams[len(Teams)-1].hangSuccess.append(entry.HangSuccess)
            Teams[len(Teams)-1].hangScores.append(entry.hangScore)
            Teams[len(Teams)-1].SupportsBot.append(entry.SupportsAnotherBot)
            Teams[len(Teams)-1].ScoredOnPyr.append(entry.ScoresWhileOnPyr)

            Teams[len(Teams)-1].hadAuto = Teams[len(Teams)-1].hadAuto + 1 if (entry.ScoreInAuto or entry.Other) else Teams[len(Teams)-1].hadAuto
            Teams[len(Teams)-1].StartedInAuto += int(entry.StartInAutoZone)
            Teams[len(Teams)-1].OtherAutoStrat += int(entry.Other)
            Teams[len(Teams)-1].autoDiscsScored.append(entry.AutoDiscsScored)
            Teams[len(Teams)-1].autoDiscsPU.append(entry.autoDiscs)
            Teams[len(Teams)-1].autoTopP.append(entry.autoTopP)
            Teams[len(Teams)-1].autoMidP.append(entry.autoMidP)
            Teams[len(Teams)-1].autoLowP.append(entry.autoLowP)
            Teams[len(Teams)-1].autoScores.append(entry.autoScore)
            Teams[len(Teams)-1].scoredAuto += int(entry.ScoreInAuto)

            Teams[len(Teams)-1].hadTele += int(entry.ScoreInTele)
            Teams[len(Teams)-1].disabledState.append(entry.disabledCount)
            Teams[len(Teams)-1].disabled += int(entry.disabled)
            Teams[len(Teams)-1].disabledCount += entry.disabledCount
            Teams[len(Teams)-1].teleFloorDiscsPU.append(entry.teleFloorDiscs)
            Teams[len(Teams)-1].teleStationDiscsPU.append(entry.teleStationDiscs)
            Teams[len(Teams)-1].DiscsPU.append(entry.DiscsPU)
            Teams[len(Teams)-1].teleDiscsScored.append(entry.DiscsScored)
            Teams[len(Teams)-1].teleScores.append(entry.teleScore)
            Teams[len(Teams)-1].telePyrP.append(entry.telePyrP)
            Teams[len(Teams)-1].teleTopP.append(entry.teleTopP)
            Teams[len(Teams)-1].teleMidP.append(entry.teleMidP)
            Teams[len(Teams)-1].teleLowP.append(entry.teleLowP)

            Teams[len(Teams)-1].avgRegFoul.append(entry.Regular)
            Teams[len(Teams)-1].avgTechFoul.append(entry.Technical)
            Teams[len(Teams)-1].hadRegFoul += int(entry.HasRegFoul)
            Teams[len(Teams)-1].hadTechFoul += int(entry.HasTechFoul)
            Teams[len(Teams)-1].hadYellow += int(entry.YellowPenalty)
            Teams[len(Teams)-1].hadRed += int(entry.RedPenalty)
            Teams[len(Teams)-1].Defensive += int(entry.Defensive)
            Teams[len(Teams)-1].Assistive += int(entry.Assistive)

    TeamCalc = True
    # Get average Bridge, Tele and Auto, and Offensive Scores
    for team in Teams:
        team.get_avg_Hang()
        team.get_avg_AutoTele()
        team.get_avg_Off()

    # Get match data
    for entry in TeamEntries:
        done = False
        for match in Matches:
            if match.number == entry.Match:
                match.teams.append(entry.Team)
                if entry.AllianceColor == 0:
                    match.all0.append(entry.Team)
                    match.off0 += entry.teleautoScore
                    match.noff0 += int(entry.isOffensive)
                    match.defense0 += int(entry.Defensive)
                    match.assist0 += int(entry.Assistive)
                    match.THangScore0 += entry.hangScore
                    match.team0.append(entry.Team)
                    if entry.isOffensive:
                        for team in Teams:
                            if team.number == entry.Team:
                                match.taavgSum0 += team.avgTeleAutoOff
                                
                elif entry.AllianceColor == 1:
                    match.all1.append(entry.Team)
                    match.off1 += entry.teleautoScore
                    match.noff1 += int(entry.isOffensive)
                    match.defense1 += int(entry.Defensive)
                    match.assist1 += int(entry.Assistive)
                    match.THangScore1 += entry.hangScore
                    match.team1.append(entry.Team)
                    if entry.isOffensive:
                        for team in Teams:
                            if team.number == entry.Team:
                                match.taavgSum1 += team.avgTeleAutoOff
                done = True
        if done == False:
            Matches.append(Match(entry.Match))
            print "Added match#" + str(entry.Match)
            Matches[len(Matches)-1].teams.append(entry.Team)
            if entry.AllianceColor == 0:
                Matches[len(Matches)-1].all0.append(entry.Team)
                Matches[len(Matches)-1].off0 += entry.teleautoScore
                Matches[len(Matches)-1].noff0 += int(entry.isOffensive)
                Matches[len(Matches)-1].defense0 += int(entry.Defensive)
                Matches[len(Matches)-1].assist0 += int(entry.Assistive)
                Matches[len(Matches)-1].THangScore0 += entry.hangScore
                Matches[len(Matches)-1].team0.append(entry.Team)
                if entry.isOffensive == 1:
                    for team in Teams:
                        if team.number == entry.Team:
                            Matches[len(Matches)-1].taavgSum0 += team.avgTeleAutoOff

            elif entry.AllianceColor == 1:
                Matches[len(Matches)-1].all1.append(entry.Team)
                Matches[len(Matches)-1].off1 += entry.teleautoScore
                Matches[len(Matches)-1].noff1 += int(entry.isOffensive)
                Matches[len(Matches)-1].defense1 += int(entry.Defensive)
                Matches[len(Matches)-1].assist1 += int(entry.Assistive)
                Matches[len(Matches)-1].THangScore1 += entry.hangScore
                Matches[len(Matches)-1].team1.append(entry.Team)
                if entry.isOffensive == 1:
                    for team in Teams:
                        if team.number == entry.Team:
                            Matches[len(Matches)-1].taavgSum1 += team.avgTeleAutoOff

    # Get defensive scores for each entry
    for entry in TeamEntries:
        entry.defScore = 0
        entry.astScore = 0
        if entry.Defensive or entry.Assistive:
            for match in Matches:
                if match.number == entry.Match:
                    if entry.AllianceColor == 0:
                        taavgOff = match.taavgSum1
                        oppOff = match.off1
                        allAvgta = match.taavgSum0
                        allOff = match.off0
                        allDefense = match.defense0
                        allAssist = match.assist0
                    if entry.AllianceColor == 1:
                        taavgOff = match.taavgSum0
                        oppOff = match.off0
                        allAvgta = match.taavgSum1
                        allOff = match.off1
                        allDefense = match.defense1
                        allAssist = match.assist1
            entry.secondary_sort(taavgOff,oppOff,allAvgta,allOff,allDefense,allAssist)

        # get total score
        entry.tertiary_sort()

    # Get average defensive scores
    for entry in TeamEntries:
        for team in Teams:
            if team.number == entry.Team:
                team.dScores.append(entry.defScore)
                team.aScores.append(entry.astScore)
    for team in Teams:
        team.get_avg_DefAst()

    # Get match defensive scores
    for entry in TeamEntries:
        for match in Matches:
            if entry.Match == match.number:
                if entry.AllianceColor == 0:
                    match.def0 += (entry.defScore)
                    match.ast0 += (entry.astScore)
                elif entry.AllianceColor == 1:
                    match.def1 += (entry.defScore)
                    match.ast1 += (entry.astScore)

    # Get match total scores
    for match in Matches:
        match.get_total()

    # Get match weighted scores
    overall_score = 0
    for match in Matches:
        overall_score += match.overall

    # weight = (S[m]/(S[w]-S[l])) * S[t]
    for entry in TeamEntries:
        for match in Matches:
            if entry.Match == match.number:
                tempweight = 0
                if (match.total0-match.total1) != 0:
                    entry.wScore = ((match.total0 + match.total1)*entry.totalScore)/100
                    entry.woScore = ((match.total0 + match.total1)*entry.offensiveScore)/100
                    entry.wdScore = ((match.total0 + match.total1)*entry.defScore)/100
                    entry.waScore = ((match.total0 + match.total1)*entry.astScore)/100
                else:
                    entry.wScore = ((match.total0 + match.total1)*entry.totalScore)
                    entry.woScore = ((match.total0 + match.total1)*entry.offensiveScore)
                    entry.wdScore = ((match.total0 + match.total1)*entry.defScore)
                    entry.waScore = ((match.total0 + match.total1)*entry.astScore)
    # Get team average weighted and total scores
    for team in Teams:
        counter = 0
        for entry in TeamEntries:
            if team.number == entry.Team:
                counter += 1
                team.wScores.append(entry.wScore)
                team.tScores.append(entry.totalScore)
                team.woScores.append(entry.woScore)
                team.wdScores.append(entry.wdScore)
                team.waScores.append(entry.waScore)
        team.avg_wScore = sum(team.wScores)/len(team.wScores)
        team.avg_tScore = sum(team.tScores)/len(team.tScores)

        # Only take average weighted score for matches in which the team particpated
        team.avg_woScore = sum(team.woScores)/len(team.woScores) if len(team.woScores)>0 else 0
        team.avg_wdScore = sum(team.wdScores)/len(team.wdScores) if len(team.wdScores)>0 else 0
        team.avg_waScore = sum(team.waScores)/len(team.waScores) if len(team.waScores)>0 else 0
        team.avg_autoScore = sum(team.autoScores)/len(team.autoScores) if len(team.autoScores)>0 else "N/A"
        team.avg_autoDiscsPU = sum(team.autoDiscsPU)/len(team.autoDiscsPU) if len(team.autoDiscsPU) else 0
        team.avg_autoTopP = sum(team.autoTopP)/team.hadAuto if team.hadAuto else 0
        team.avg_autoMidP = sum(team.autoMidP)/team.hadAuto if team.hadAuto else 0
        team.avg_autoLowP = sum(team.autoLowP)/team.hadAuto if team.hadAuto else 0
        team.avg_DiscsPU = sum(team.DiscsPU)/len(team.DiscsPU) if len(team.DiscsPU)>0 else 0
        team.avg_FloorDiscsPU = sum(team.teleFloorDiscsPU)/len(team.teleFloorDiscsPU) if len(team.teleFloorDiscsPU)>0 else 0
        team.avg_StationDiscsPU = sum(team.teleStationDiscsPU)/len(team.teleStationDiscsPU) if len(team.teleStationDiscsPU)>0 else 0
        team.avg_DiscsScored = sum(team.teleDiscsScored)/len(team.teleDiscsScored) if len(team.teleDiscsScored)>0 else 0
        team.avg_telePyrP = sum(team.telePyrP)/team.hadTele if team.hadTele else 0
        team.avg_teleTopP = sum(team.teleTopP)/team.hadTele if team.hadTele else 0
        team.avg_teleMidP = sum(team.teleMidP)/team.hadTele if team.hadTele else 0
        team.avg_teleLowP = sum(team.teleLowP)/team.hadTele if team.hadTele else 0

    global off_rank, def_rank, ast_rank, tot_rank, auto_rank, tel_rank, pyr_rank
    off_rank = []
    def_rank = []
    ast_rank = []
    tot_rank = []

    auto_rank = []
    tel_rank = []
    pyr_rank = []
    for team in Teams:
        if team.numOff>0: off_rank.append([team.avgOff,team.number])
        if team.numDef>0: def_rank.append([team.avgDef,team.number])
        if team.numAst>0: ast_rank.append([team.avgAst,team.number])
        tot_rank.append([team.avg_tScore,team.number])

        if team.hadAuto>0: auto_rank.append([team.avgAuto,team.number])
        if team.hadTele>0: tel_rank.append([team.avgTele,team.number,team.discsPUtoScored])
        if team.timesHanged>0: pyr_rank.append([team.avgHangScore,team.number])

    # sort them
    off_rank.sort(reverse=True)
    def_rank.sort(reverse=True)
    ast_rank.sort(reverse=True)
    tot_rank.sort(reverse=True)

    auto_rank.sort(reverse=True)
    tel_rank.sort(reverse=True)
    pyr_rank.sort(reverse=True)

    # add all Teams to available teams list
    available_teams = []
    offr = 0
    defr = 0
    astr = 0
    totr = 0

    autor = 0
    telr = 0
    pyrr = 0
    for rank in off_rank:
        offr += 1
        for team in Teams:
            if team.number == rank[1]: team.off_rank = offr
    for rank in def_rank:
        defr += 1
        for team in Teams:
            if team.number == rank[1]: team.def_rank = defr
    for rank in ast_rank:
        astr += 1
        for team in Teams:
            if team.number == rank[1]: team.ast_rank = astr
    for rank in tot_rank:
        totr += 1
        for team in Teams:
            if team.number == rank[1]: team.tot_rank = totr
    for rank in auto_rank:
        autor += 1
        for team in Teams:
            if team.number == rank[1]: team.auto_rank = autor
    for rank in tel_rank:
        telr += 1
        for team in Teams:
            if team.number == rank[1]: team.tel_rank = telr
    for rank in pyr_rank:
        pyrr +=1
        for team in Teams:
            if team.number == rank[1]: team.pyr_rank = pyrr
    for team in Teams:
        available_teams.append(team.number)


#----------------------------------------------------------------------------------------------------
# Calculate Function - Calculates data for statistical analysis from data2.
#----------------------------------------------------------------------------------------------------
##def calculate2():
##
##
##    global entries2
##    global Teams
##    global PitCalc
##    for entry in entries2:
##        done = False
##        for team in Teams:
##            if team.number == entry.Team:
##
##               #do a bunch of crap
##
##                done == True
##        if done == False:
##            Teams.append(Team(entry.Team))
##            print "Added team#" + str(entry.Team)
##
##               #do another whole bunch of crap
##
##    PitCalc = True
##
##
##
#----------------------------------------------------------------------------------------------------
# Team Data Function
#   -- Allows the user to access data for specific teams
#----------------------------------------------------------------------------------------------------
def team_data():
    global Teams
    global t1_tboxes
    global tabnum     # the number of the team currently being viewed
    global mpos
    global t1_pic
    global t1_update
    global t1_surface
    global teamdata
    #run = True
    # reference --------- pygame.draw.rect(screen,(0,0,0),(160,65,200,50),1)
    # Get the team numbers
    tnums = []
    for team in Teams:
        tnums.append(team.number)
    tnums.sort()
    if len(tnums) > 0 and tabnum == 0:    #only for first time
        tnum = tnums[0]
    #else: tabnum = 0
    for textbox in t1_tboxes:
        if textbox.type == "tnum":
            if textbox.value is not None:
                try:
                    if int(textbox.value) == 0: textbox.value = tabnum #if value is 0, make it the current team number
                    elif int(textbox.value) != tabnum: #If the number has changed, then do updates
                        if int(textbox.value) in tnums:
                            tabnum = int(textbox.value)
                            t1_update = True
                        else:
                            tabnum = tnums[0] if len(tnums)>0 else 0 #if the number is not found, reset to the first team in the list
                except:
                    #Not actually a number
                    print "Error: non-numerical characters inserted for team number"
            else: textbox.value = tabnum
            textbox.value = tabnum
    # Update values based on tabnum
        #-- start by getting team data from beginning
    if t1_update:
        print "Update in tab 2 requested"
        teamdata = 0
        for team in Teams:
            if team.number == tabnum: teamdata = team
        if teamdata != 0:
            for textbox in t1_tboxes:
                if textbox.type == "numMatch": textbox.value = len(teamdata.matches)
                elif textbox.type == "pOff": textbox.value = str(int(100*teamdata.numOff/len(teamdata.matches))) + "%"
                elif textbox.type == "pDef": textbox.value = str(int(100*teamdata.numDef/len(teamdata.matches))) + "%"
                elif textbox.type == "pAst": textbox.value = str(int(100*teamdata.numAst/len(teamdata.matches))) + "%"
                elif textbox.type == "avgOff": textbox.value = round(teamdata.avgOff,2)
                elif textbox.type == "avgDef": textbox.value = round(teamdata.avgDef,2)
                elif textbox.type == "avgAst": textbox.value = round(teamdata.avgAst,2)
                elif textbox.type == "avgTotal": textbox.value = round(teamdata.avg_tScore,2)
                elif textbox.type == "WeightedOff": textbox.value = round(teamdata.avg_woScore,2)
                elif textbox.type == "WeightedDef": textbox.value = round(teamdata.avg_wdScore,2)
                elif textbox.type == "WeightedAst": textbox.value = round(teamdata.avg_waScore,2)

                elif textbox.type == "pHadAuto": textbox.value = str(int(100*teamdata.hadAuto/len(teamdata.matches))) + "%"
                elif textbox.type == "pStartInZone": textbox.value = str(int(100*teamdata.StartedInAuto)/len(teamdata.matches)) + "%"
                elif textbox.type == "pOtherStrat": textbox.value = str(int(100*teamdata.OtherAutoStrat)/len(teamdata.matches)) + "%"
                elif textbox.type == "avgAutoScore": textbox.value = str(round(teamdata.avgAuto,2))
                elif textbox.type == "avgAutoTopP": textbox.value = str(round(teamdata.avg_autoTopP,2))
                elif textbox.type == "avgAutoMidP": textbox.value = str(round(teamdata.avg_autoMidP,2))
                elif textbox.type == "avgAutoLowP": textbox.value = str(round(teamdata.avg_autoLowP,2))

                elif textbox.type == "pWasDisabled": textbox.value = str(int(100*teamdata.disabled)/len(teamdata.matches)) + "%"
                elif textbox.type == "avgDisabled": textbox.value = str(round(float(sum(teamdata.disabledState)/len(teamdata.disabledState)),2))
                elif textbox.type == "totalDisabled": textbox.value = str(round(teamdata.disabledCount,2))
                elif textbox.type == "avgTotalPickUp": textbox.value = str(round(teamdata.avg_DiscsPU,2))
                elif textbox.type == "avgFloorPickUp": textbox.value = str(round(teamdata.avg_FloorDiscsPU,2))
                elif textbox.type == "avgStationPickUp": textbox.value = str(round(teamdata.avg_StationDiscsPU,2))
                elif textbox.type == "rPickUpScored": textbox.value = str(round(teamdata.discsPUtoScored,2)) + " : 1"
                elif textbox.type == "avgTeleScore": textbox.value = str(round(teamdata.avgTele,2))
                elif textbox.type == "avgTelePyrP": textbox.value = str(round(teamdata.avg_telePyrP,2))
                elif textbox.type == "avgTeleTopP": textbox.value = str(round(teamdata.avg_teleTopP,2))
                elif textbox.type == "avgTeleMidP": textbox.value = str(round(teamdata.avg_teleMidP,2))
                elif textbox.type == "avgTeleLowP": textbox.value = str(round(teamdata.avg_teleLowP,2))

                elif textbox.type == "avgHangScore": textbox.value = str(round(teamdata.avgHangScore,2))
                elif textbox.type == "rHangSuccToAtt": textbox.value = str(round(teamdata.hangsSucctoAtt,2)) + " : 1"
                elif textbox.type == "pHanged": textbox.value = str(int(100*teamdata.timesHanged)/len(teamdata.matches)) + "%"
                elif textbox.type == "avgSupportBot": textbox.value = str(round(sum(teamdata.SupportsBot)/len(teamdata.SupportsBot),2))
                elif textbox.type == "avgScoredOnPyr": textbox.value = str(round(sum(teamdata.ScoredOnPyr)/len(teamdata.ScoredOnPyr),2))

                elif textbox.type == "avgRegFoul": textbox.value = str(round(sum(teamdata.avgRegFoul)/len(teamdata.avgRegFoul),2))
                elif textbox.type == "avgTechFoul": textbox.value = str(round(sum(teamdata.avgTechFoul)/len(teamdata.avgTechFoul),2))
                elif textbox.type == "pDefensive": textbox.value = str(int(100*teamdata.Defensive/len(teamdata.matches))) + "%"
                elif textbox.type == "pAssistive": textbox.value = str(int(100*teamdata.Assistive/len(teamdata.matches))) + "%"
                elif textbox.type == "pYellow": textbox.value = str(int(100*teamdata.hadYellow/len(teamdata.matches))) + "%"
                elif textbox.type == "pRed": textbox.value = str(int(100*teamdata.hadRed/len(teamdata.matches))) + "%"

                elif textbox.type == "rankOff": textbox.value = str(teamdata.off_rank)
                elif textbox.type == "rankDef": textbox.value = str(teamdata.def_rank)
                elif textbox.type == "rankAst": textbox.value = str(teamdata.ast_rank)
                elif textbox.type == "rankTot": textbox.value = str(teamdata.tot_rank)

    # Draw Them
    if t1_update:
        t1_surface.fill(bgcolor)
        for textbox in t1_tboxes:
            textbox.draw(t1_surface)
        t1_pic.draw(t1_surface,val=teamnumber)
        t1_update = False
    screen.blit(t1_surface,(160,65))
    # See if a textbox needs to be drawn
    # -- This only occurs if the mouse is hovering over the textbox
    for tbox in t1_tboxes:
        x = tbox.x+tbox.cw+(.5*tbox.th)+160
        y = tbox.y+.5*tbox.th+65
        if x<=cmpos[0]<=x+tbox.w+.5*tbox.th \
            and y<=cmpos[1]<=y+tbox.size+.5*tbox.th-10 and teamdata != 0:

            #this is for displaying the linear regression graphs.  needs to be updated still
            if tbox.type=="avgOff":
                # Get information for offensive score
                i = 0
                lx = []
                ly = []
                print teamdata.oScores
                while i <len(teamdata.oScores):
                    lx.append(i+1)
                    ly.append(teamdata.oScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgDef" and teamdata.numDef>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.dScores
                while i <len(teamdata.dScores):
                    lx.append(i+1)
                    ly.append(teamdata.dScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgAst" and teamdata.numAst>0:
                # Get information for assistive score
                i = 0
                lx = []
                ly = []
                print teamdata.aScores
                while i <len(teamdata.aScores):
                    lx.append(i+1)
                    ly.append(teamdata.aScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgTotal" and teamdata.numDef+teamdata.numOff+teamdata.numAst>0:
                # Get information for total score
                i = 0
                lx = []
                ly = []
                print teamdata.tScores
                while i <len(teamdata.tScores):
                    lx.append(i+1)
                    ly.append(teamdata.tScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgRegFoul" and teamdata.hadRegFoul>0:
                # Get information for total score
                i = 0
                lx = []
                ly = []
                print teamdata.avgRegFoul
                while i <len(teamdata.avgRegFoul):
                    lx.append(i+1)
                    ly.append(teamdata.avgRegFoul[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgTechFoul" and teamdata.hadTechFoul>0:
                # Get information for total score
                i = 0
                lx = []
                ly = []
                print teamdata.avgTechFoul
                while i <len(teamdata.avgTechFoul):
                    lx.append(i+1)
                    ly.append(teamdata.avgTechFoul[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgAutoScore" and teamdata.hadAuto>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.autoScores
                while i <len(teamdata.autoScores):
                    lx.append(i+1)
                    ly.append(teamdata.autoScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgAutoTopP" and teamdata.hadAuto>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.autoTopP
                while i <len(teamdata.autoTopP):
                    lx.append(i+1)
                    ly.append(teamdata.autoTopP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgAutoMidP" and teamdata.hadAuto>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.autoMidP
                while i <len(teamdata.autoMidP):
                    lx.append(i+1)
                    ly.append(teamdata.autoMidP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgAutoLowP" and teamdata.hadAuto>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.autoLowP
                while i <len(teamdata.autoLowP):
                    lx.append(i+1)
                    ly.append(teamdata.autoLowP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgDisabled" and teamdata.disabled>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.disabledState
                while i <len(teamdata.disabledState):
                    lx.append(i+1)
                    ly.append(teamdata.disabledState[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
##            elif tbox.type=="avgTotalPickUp" and sum(teamdata.teleDiscsPU)>0:
##                # Get information for defensive score
##                i = 0
##                lx = []
##                ly = []
##                print teamdata.teleDiscsPU
##                while i <len(teamdata.teleDiscsPU):
##                    lx.append(i+1)
##                    ly.append(teamdata.teleDiscsPU[i])
##                    i += 1
##                display = lreg(lx,ly)
##                display.get_ab()
##                draw = display.get_image(300,300,(255,255,255),(0,0,0))
##                screen.blit(draw,(x+tbox.w+.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgFloorPickUp" and sum(teamdata.teleFloorDiscsPU)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleFloorDiscsPU
                while i <len(teamdata.teleFloorDiscsPU):
                    lx.append(i+1)
                    ly.append(teamdata.teleFloorDiscsPU[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgStationPickUp" and sum(teamdata.teleStationDiscsPU)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleStationDiscsPU
                while i <len(teamdata.teleStationDiscsPU):
                    lx.append(i+1)
                    ly.append(teamdata.teleStationDiscsPU[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-4*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10))
            elif tbox.type=="avgTeleScore" and teamdata.hadTele>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleScores
                while i <len(teamdata.teleScores):
                    lx.append(i+1)
                    ly.append(teamdata.teleScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgTeleLowP" and sum(teamdata.teleLowP)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleLowP
                while i <len(teamdata.teleLowP):
                    lx.append(i+1)
                    ly.append(teamdata.teleLowP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgTeleMidP" and sum(teamdata.teleMidP)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleMidP
                while i <len(teamdata.teleMidP):
                    lx.append(i+1)
                    ly.append(teamdata.teleMidP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgTeleTopP" and sum(teamdata.teleTopP)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.teleTopP
                while i <len(teamdata.teleTopP):
                    lx.append(i+1)
                    ly.append(teamdata.teleTopP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgTelePyrP" and sum(teamdata.telePyrP)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.telePyrP
                while i <len(teamdata.telePyrP):
                    lx.append(i+1)
                    ly.append(teamdata.telePyrP[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgHangScore" and teamdata.timesHanged>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.hangScores
                while i <len(teamdata.hangScores):
                    lx.append(i+1)
                    ly.append(teamdata.hangScores[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgSupportBot" and sum(teamdata.SupportsBot)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.SupportsBot
                while i <len(teamdata.SupportsBot):
                    lx.append(i+1)
                    ly.append(teamdata.SupportsBot[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-8*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))
            elif tbox.type=="avgScoredOnPyr" and sum(teamdata.ScoredOnPyr)>0:
                # Get information for defensive score
                i = 0
                lx = []
                ly = []
                print teamdata.ScoredOnPyr
                while i <len(teamdata.ScoredOnPyr):
                    lx.append(i+1)
                    ly.append(teamdata.ScoredOnPyr[i])
                    i += 1
                display = lreg(lx,ly)
                display.get_ab()
                draw = display.get_image(300,300,(255,255,255),(0,0,0))
                screen.blit(draw,(x-2*tbox.w-.5*tbox.th,y+tbox.size+.5*tbox.th-10-325))

    # See if any changes are requested from clicks
    for textbox in t1_tboxes:
        x = textbox.x+textbox.cw+textbox.th+160
        y = textbox.y+.5*textbox.th+65
        if x+textbox.w+.5*textbox.th>=mpos[0]>=x \
           and y+textbox.size+.5*textbox.th-10>=mpos[1]>=y:
           # click event
           textbox.clicked()


##def team_pitdata():
##    global Teams
##    global t7_tboxes
##    global tabnum     # the number of the team currently being viewed
##    global mpos
##    global t7_update
##    global t7_surface
##    global teamdata
##    tnums = []
##    for team in Teams:
##        tnums.append(team.number)
##    tnums.sort()
##    if len(tnums) > 0 and tabnum == 0:    #only for first time
##        tnum = tnums[0]
##    for textbox in t7_tboxes:
##        if textbox.type == "tnum":
##            if textbox.value is not None:
##                try:
##                    if int(textbox.value) == 0: textbox.value = tabnum #if value is 0, make it the current team number
##                    elif int(textbox.value) != tabnum: #If the number has changed, then do updates
##                        if int(textbox.value) in tnums:
##                            tabnum = int(textbox.value)
##                            t7_update = 1
##                        else:
##                            if len(tnums)>0: tabnum = tnums[0] #if the number is not found, reset to the first team in the list
##                            else: tabnum = 0
##                except:
##                    #Not actually a number
##                    print "Error: non-numerical characters inserted for team number"
##            else: textbox.value = tabnum
##            textbox.value = tabnum
##    if t7_update == 1:
##        print "Update in tab 2 requested"
##        teamdata = 0
##        for team in Teams:
##            if team.number == tabnum: teamdata = team
##        if teamdata != 0:
##            for textbox in t7_tboxes:
##                # textbox.type == "
##                if textbox.type == "rbln": textbox.value = teamdata.robotlen
##                elif textbox.type == "rbwd": textbox.value = teamdata.robotwid
##                elif textbox.type == "rbhg": textbox.value = teamdata.robotheg
##                elif textbox.type == "rbwg": textbox.value = teamdata.robotwig
##                elif textbox.type == "frcr": textbox.value = teamdata.floorclear
##                elif textbox.type == "wlsc": textbox.value = teamdata.wheelspace
##                elif textbox.type == "bgmc": textbox.value = teamdata.BridgeMechanics
##                elif textbox.type == "sdbg": textbox.value = teamdata.SldBridge
##                elif textbox.type == "blsn": textbox.value = teamdata.ballsen
##                elif textbox.type == "sggr": textbox.value = teamdata.ShiftGear
##                elif textbox.type == "dvsy": textbox.value = teamdata.DriveSystem
##                elif textbox.type == "cnms": textbox.value = teamdata.CenterMass
##                elif textbox.type == "dri1": textbox.value = teamdata.Driver1
##                elif textbox.type == "exp1": textbox.value = teamdata.experince1
##                elif textbox.type == "dri2": textbox.value = teamdata.Driver2
##                elif textbox.type == "exp2": textbox.value = teamdata.experince2
##                elif textbox.type == "dri3": textbox.value = teamdata.Driver3
##                elif textbox.type == "exp3": textbox.value = teamdata.experince3
##    if t7_update == 1:
##        t7_surface.fill(bgcolor)
##        for textbox in t7_tboxes:
##            textbox.draw(t7_surface)
##        t7_update = 0
##    screen.blit(t7_surface,(160,65))
##    # linear regresssion/otherstuff
##    for textbox in t7_tboxes:
##        x = textbox.x+textbox.cw+textbox.th+160
##        y = textbox.y+.5*textbox.th+65
##        if x+textbox.w+.5*textbox.th>=mpos[0]>=x \
##           and y+textbox.size+.5*textbox.th-10>=mpos[1]>=y:
##           # click event
##           textbox.clicked()

#----------------------------------------------------------------------------------------------------
# Ratings Functions
#   -- Delivers team ratings based upon user preferences
#----------------------------------------------------------------------------------------------------
def ratings():
    global Teams
    global screen
    global HEIGHT
    global bgcolor
    global txcolor
    global t3_scrolls
    global t3_buttons
    global off_rank, def_rank, ast_rank, tot_rank
    run = False

    # Draw Average Offensive Score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Offensive Score",True,txcolor,bgcolor)
    screen.blit(text,(160,65))
    # Draw Avg Off
    font = pygame.font.Font(None,20)
    x = 0
    y = 0
    n = 0
    t3_scrolls[0].surface.fill(bgcolor)
    for rank in off_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t3_scrolls[0].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.off_rank = n
    t3_scrolls[0].draw(screen)
    pygame.draw.line(screen,(0,0,0),(365,65),(365,HEIGHT),1)

    # Draw Average Defensive Score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Defensive Score",True,txcolor,bgcolor)
    screen.blit(text,(370,65))
    # Draw Avg Def
    x = 0
    y = 0
    n=0
    t3_scrolls[1].surface.fill(bgcolor)
    for rank in def_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t3_scrolls[1].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.def_rank = n
    t3_scrolls[1].draw(screen)
    pygame.draw.line(screen,(0,0,0),(575,65),(575,HEIGHT),1)

    # Draw Average Assistive score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Assistive Score",True,txcolor,bgcolor)
    screen.blit(text,(580,65))
    # Draw Avg Ast
    x = 0
    y = 0
    n=0
    t3_scrolls[2].surface.fill(bgcolor)
    for rank in ast_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t3_scrolls[2].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.ast_rank = n
    t3_scrolls[2].draw(screen)
    pygame.draw.line(screen,(0,0,0),(785,65),(785,HEIGHT),1)

    # Draw Average total score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Total Score",True,txcolor,bgcolor)
    screen.blit(text,(790,65))
    x = 0
    y = 0
    n=0
    t3_scrolls[3].surface.fill(bgcolor)
    for rank in tot_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t3_scrolls[3].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.tot_rank = n
    t3_scrolls[3].draw(screen)
    # Draw Average Weighted Score
    #pygame.draw.line(sceen,(0,0,0),(600,65),(600,HEIGHT),1)
    #font = pygame.font.Font(None,20)
    #text = font.render("Avg Total Score(W)",True,txcolor,bgcolor)
    #screen.blit(text,(602,65))
    #team_wei = []   # Uses (avg_weighted,team_number) as the format
    #for team in teams:
    #    team_wei.append([team.avg_wscore,team.number])
    #team_wei.sort(reverse = True)
    #x = 602
    #y = 85
    #n=0
    #for rank in team_wei:
    #   n += 1
    #   text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(rank[0]),True,txcolor,bgcolor)
    #   screen.blit(text,(x,y))
    #   y += 20
    # Get Weighted Offensive Scores
    #pygame.draw.line(screen,(0,0,0),(740,65),(740,HEIGHT),1)
    #font = pygame.font.Font(None,20)
    #text = font.render("Avg Offensive Score(W)",True,txcolor,bgcolor)
    #screen.blit(text,(742,65))
    #team_weo = []
    #for team in teams:
    #    if team.noff > 0:
    #        team_weo.append([team.avg_woscore,team.number])
    #team_weo.sort(reverse = True)
    #x = 742
    #y = 85
    #n = 0
    #for rank in team_weo:
    #    n += 1
    #    text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(rank[0]),True,txcolor,bgcolor)
    #    screen.blit(text,(x,y))
    #    y += 20
    # Get Weighted Defensive Scores
    #pygame.draw.line(screen,(0,0,0),(910,65),(910,HEIGHT),1)
    #font = pygame.font.Font(None,20)
    #text = font.render("Avg Defensive Score(W)",True,txcolor,bgcolor)
    #screen.blit(text,(912,65))
    #team_wed = []
    #for team in teams:
    #    if team.ndef > 0:
    #        team_wed.append([team.avg_wdscore,team.number])
    #team_wed.sort(reverse = True)
    #x = 912
    #y = 85
    #n=0
    #for rank in team_wed:
    #    n += 1
    #    text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(rank[0]),True,txcolor,bgcolor)
    #    screen.blit(text,(x,y))
    #    y += 20
    for button in t3_buttons:
        button.draw(screen)
    for button in t3_buttons:
        if mbut[0] == 1:
            if button.x<=cmpos[0]<=button.x+button.w and button.y<=cmpos[1]<=button.y+button.h:
                if button.type == "offup":
                    t3_scrolls[0].update(True)
                elif button.type == "offdo":
                    t3_scrolls[0].update(False)
                elif button.type == "defup":
                    t3_scrolls[1].update(True)
                elif button.type == "defdo":
                    t3_scrolls[1].update(False)
                elif button.type == "astup":
                    t3_scrolls[2].update(True)
                elif button.type == "astdo":
                    t3_scrolls[2].update(False)
                elif button.type == "totup":
                    t3_scrolls[3].update(True)
                elif button.type == "totdo":
                    t3_scrolls[3].update(False)

def ratings2():
    global Teams
    global screen
    global HEIGHT
    global bgcolor
    global txcolor
    global t4_scrolls
    global t4_buttons
    global auto_rank, tel_rank, pyr_rank
    run = False

    # Draw Average Auto Score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Auto Score",True,txcolor,bgcolor)
    screen.blit(text,(160,65))
    # Draw Avg hyb
    font = pygame.font.Font(None,20)
    x = 0
    y = 0
    n = 0
    t4_scrolls[0].surface.fill(bgcolor)
    for rank in auto_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t4_scrolls[0].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.auto_rank = n
    t4_scrolls[0].draw(screen)
    pygame.draw.line(screen,(0,0,0),(365,65),(365,HEIGHT),1)

    # Draw Average Tele Score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Tele Score",True,txcolor,bgcolor)
    screen.blit(text,(370,65))
    # Draw Avg Tel
    x = 0
    y = 0
    n=0
    t4_scrolls[1].surface.fill(bgcolor)
    for rank in tel_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t4_scrolls[1].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.yrl_rank = n
    t4_scrolls[1].draw(screen)
    pygame.draw.line(screen,(0,0,0),(575,65),(575,HEIGHT),1)

    # Draw Average Bridge score
    font = pygame.font.Font(None,20)
    text = font.render("Avg Hang Score",True,txcolor,bgcolor)
    screen.blit(text,(580,65))
    # Draw Avg Ast
    x = 0
    y = 0
    n=0
    t4_scrolls[2].surface.fill(bgcolor)
    for rank in pyr_rank:
        n += 1
        text = font.render("#"+str(n)+"--Team "+str(rank[1])+": " + str(round(rank[0],2)),True,txcolor,bgcolor)
        t4_scrolls[2].surface.blit(text,(x,y))
        y += 20
        for team in Teams:
            if team.number == rank[1]: team.pyr_rank = n
    t4_scrolls[2].draw(screen)
    #pygame.draw.line(screen,(0,0,0),(785,65),(785,HEIGHT),1)

    for button in t4_buttons:
        button.draw(screen)
    for button in t4_buttons:
        if mbut[0] == 1:
            if button.x<=cmpos[0]<=button.x+button.w and button.y<=cmpos[1]<=button.y+button.h:
                if button.type == "autoup":
                    t4_scrolls[0].update(True)
                elif button.type == "autodo":
                    t4_scrolls[0].update(False)
                elif button.type == "teleup":
                    t4_scrolls[1].update(True)
                elif button.type == "teledo":
                    t4_scrolls[1].update(False)
                elif button.type == "pyrup":
                    t4_scrolls[2].update(True)
                elif button.type == "pyrdo":
                    t4_scrolls[2].update(False)

#----------------------------------------------------------------------------------------------------
# Search Sub Functions and Definition of Search Dictionary
#  -- used in looking for specifics from the search tab
#----------------------------------------------------------------------------------------------------

def searchGreater(item):
    global team_list
    try:
        team_list = filter(lambda team:team[1].getAttribute(item.type)>=int(item.value), team_list)

    except:
        item.value = 0

def searchHas(item):
    global team_list
    try:
        if item.check == 1:
            team_list = filter(lambda team:team[1].getAttribute(item.type)>=1, team_list)

    except:
        item.check = 0

def searchNever(item):
    global team_list
    try:
        if item.check == 1:
            team_list = filter(lambda team:team[1].getAttribute(item.type) == 0, team_list)

    except:
        item.check = 0

Searches = {"avgOff":searchGreater, "avgDef":searchGreater, "avgAst":searchGreater, "numOff":searchHas, "numDef":searchHas, "numAst":searchHas, \
            "scoredAuto":searchHas, "StartedInAuto":searchHas, "OtherAutoStrat":searchHas, \
            "timesHanged":searchHas, "avgHangScore":searchGreater, \
            "TotalSupportsBot":searchHas, "TotalScoredOnPyr":searchHas, "disabledCount":searchNever, \
            "hadRegFoul":searchNever, "hadTechFoul":searchNever, "hadYellow":searchNever, "hadRed":searchNever}

#----------------------------------------------------------------------------------------------------
# Search
#----------------------------------------------------------------------------------------------------
def search():
    global screen
    global t5_stuff
    global tabnum
    global teams
    global mpos
    global t5_scroll
    global t5_tempbut
    global t5_temprad
    global team_list
    global t5_buttons
    global t5_update
    global old_list
    global Searches
    global tabnum
    global t1_tboxes
    global t1_update
    global tab
    global wanted
    global update_wanted
    global t5_wscroll
    global t5_wbut
    global t5_wrad
    global t5_redraw
    global t5_wbmov
    global available_teams
    global t7_update

    # Add title text for each scroller
    font = pygame.font.Font(None,20)
    text = font.render(" Matches: ",True,txcolor,bgcolor)
    screen.blit(text,(510,65))
    text = font.render(" Alliance Wanted List: ",True,txcolor,bgcolor)
    screen.blit(text,(625,65))
    # Add tempbut and temprad to scroller image; only change if update needed
    if t5_update == 1 or t5_redraw == 1:
        t5_scroll.surface = pygame.Surface((180,2000)) # Reset surface
        t5_scroll.surface.fill(bgcolor)
        for b in t5_tempbut:
            b.draw(t5_scroll.surface)
        for r in t5_temprad:
            r.draw(t5_scroll.surface)
        t5_update = 0
    #Draw the scroller image
    t5_scroll.draw(screen)

    # Add wbut and wrad to wscroll image; only change if update needed
    if update_wanted:
        t5_wscroll.surface = pygame.Surface((180,2000)) # Reset surface
        t5_wscroll.surface.fill(bgcolor)
        for b in t5_wbut:
            b.draw(t5_wscroll.surface)
        for r in t5_wrad:
            r.draw(t5_wscroll.surface)
        for bu in t5_wbmov:
            bu.draw(t5_wscroll.surface)
        update_wanted = 0
    #Draw the scroller image
    t5_wscroll.draw(screen)

    #Draw buttons
    for but in t5_buttons:
        but.draw(screen)

    #Detect button clicks
    nx = mpos[0] - t5_wscroll.x
    ny = mpos[1] - t5_wscroll.y + t5_wscroll.currenty 
    for but in t5_wbmov:
        if but.x<=nx<=but.x+but.w and but.y<=ny<=but.y+but.h and \
           but.y+but.h<t5_scroll.currenty+t5_scroll.maxh and but.y>t5_scroll.currenty:
            number = ""
            t = ""
            counter = 0
            while counter < len(but.type):
                try:
                    int(but.type[counter]) #Only if it is a number will try continue
                    number += but.type[counter]
                except:
                    t += but.type[counter]
                counter += 1
            if t== "up": # move the rank of the team up; the rank of the team above it down
                for te in wanted:
                    if te[1][0] == int(number): # Is the team
                        rank = te[0]
                        print "Our rank was:" + str(rank)
                for te in wanted:
                    # First, move the rank of the other team down; prevents errors
                    if te[0] == rank+1: # Is the rank the team is a/b to replace
                        te[0] = rank
                for te in wanted:
                    if te[1][0] == int(number):
                        te[0] += 1
                        print "Our rank is now" + str(te[0])
                update_wanted = 1
            if t=="do":
                for te in wanted:
                    if te[1][0] == int(number): # Is the team
                        rank = te[0]
                        print "Our rank was:" + str(rank)
                for te in wanted:
                    # First, move the rank of the other team down; prevents errors
                    if te[0] == rank-1: # Is the rank the team is a/b to replace
                        te[0] = rank
                for te in wanted:
                    if te[1][0] == int(number):
                        te[0] -= 1
                        print "Our rank is now:" + str(te[0])
                update_wanted = 1
            
    for but in t5_buttons:
        if mbut[0] == 1:
            if but.x<=cmpos[0]<=but.x+but.w and but.y<=cmpos[1]<=but.y+but.h:
                if but.type == "tlup":
                    t5_scroll.update(1)
                elif but.type == "tldo":
                    t5_scroll.update(0)
                elif but.type == "wlup":
                    t5_wscroll.update(1)
                elif but.type == "wldo":
                    t5_wscroll.update(0)
    nx = mpos[0] - t5_scroll.x
    ny = mpos[1] - t5_scroll.y + t5_scroll.currenty
    for but in t5_tempbut:
        if but.x<=nx<=but.x+but.w and but.y<=ny<=but.y+but.h and but.y+but.h<t5_scroll.currenty+t5_scroll.maxh and but.y>t5_scroll.currenty:
            # Open team data in other tab
            for textbox in t1_tboxes:
                if textbox.type == "tnum":
                    textbox.value = but.type
            tabnum = int(but.type)
            t1_update = 1
            tab = 1
    for rad in t5_temprad:
        if rad.flip:   #button to left:
            if rad.x+.75*rad.size>=nx>=rad.x+.25*rad.size and \
               rad.y+.75*rad.size>=ny>=rad.y+.25*rad.size: # Clicked
                if rad.check == 0: 
                    for t in team_list:
                        if t[0] == rad.teamnum: #Add team to wanted list
                            wanted.append([len(wanted)+1,t])
                            t7_update = 1
                    rad.click()
                    rad.draw(t5_scroll.surface)
                    update_wanted = 1
                    t5_redraw = 1
                else: # Already Selected; now, deselect and remove from wanted list
                    for t in team_list:
                        if t[0] == rad.teamnum:
                            i = 0
                            while i < len(wanted):
                                if wanted[i][1][0] == rad.teamnum:
                                    del wanted[i]
                                    i -= 1
                                i += 1
                    rad.click()
                    rad.draw(t5_scroll.surface)
                    update_wanted = 1
                    t5_redraw = 1
        else: #Button to right
            if rad.x+item.w+.75*rad.size>=nx>=rad.x+item.w+.25*rad.size and \
               rad.y+.75*rad.size>=ny>=rad.y+.25*rad.size:
                if rad.check == 0: 
                    for t in team_list:
                        if t[0] == rad.teamnum: #Add team to wanted list
                            wanted.append([len(wanted)+1,t])
                    rad.click()
                    rad.draw(t5_scroll.surface)
                    update_wanted = 1
                    t5_redraw = 1
                else: # Already Selected; now, deselct and remove from wanted list
                    for t in team_list:
                        if t[0] == rad.teamnum:
                            i = 0
                            while i < len(wanted):
                                if wanted[i][1][0] == rad.teamnum:
                                    del wanted[i]
                                    i -= 1
                                i += 1
                    rad.click()
                    rad.draw(t5_scroll.surface)
                    update_wanted = 1
                    t5_redraw = 1
    
    #click events
    for item in t5_stuff:   
        try:#uses this for radio buttons
            if item.flip:   #button to left:
                if item.x+.75*item.size>=mpos[0]>=item.x+.25*item.size and \
                   item.y+.75*item.size>=mpos[1]>=item.y+.25*item.size:
                    item.click()
            else:
                if item.x+item.w+.75*item.size>=mpos[0]>=item.x+item.w+.25*item.size and \
                   item.y+.75*item.size>=mpos[1]>=item.y+.25*item.size:
                    item.click()
        except:#uses this for textboxes
            # See if any changes are requested from clicks
            x = item.x+item.cw+item.th
            y = item.y+.5*item.th
            if x+item.w+.5*item.th>=mpos[0]>=x \
               and y+item.size+.5*item.th-10>=mpos[1]>=y:
               # click event
               item.clicked()
    #draw
    for item in t5_stuff:
        item.draw(screen)
    pygame.draw.line(screen,(0,0,0),(500,65),(500,HEIGHT),5)
    pygame.draw.line(screen,(0,0,0),(620,65),(620,HEIGHT),5)

    # Do Search
    old_list = []
    for t in team_list:
        old_list.append(t[0])
    old_list.sort()
    team_list = []
    for team in Teams:
        team_list.append([team.number,team])
    if len(team_list) > 0:
        for item in t5_stuff:
            if item.type in Searches:
                Searches[item.type](item)

    team_list.sort()
    nlist = []
    for t in team_list:
        nlist.append(t[0])
    nlist.sort()
    if nlist != old_list:
        t5_update = 1

    # Deal with the wanted scroller(t5_wscroll)
    if update_wanted:
        t5_wbut = []
        #t5_wrad = []
        t5_wbmov = []
        y = 5
        wanted.sort()
        n = 0
        if len(wanted)>0:
            while n < len(wanted):
                n += 1
                wanted[n-1][0] = n
        for t in wanted:
            t5_wbut.append(button(x=0,y=y,thickness=1,text=str(t[1][0]),font=30,w=50,t=str(t[1][0])))
            #t5_wrad.append(radio(x=55,y=y,caption=[],flip=1,t=str(t[1][0]),fs=30,teamnum=t[1][0]))
            t5_wbmov.append(button(x=55,y=y,thickness=1,text="<",font=30,w=30,t=str(t[1][0])+"up"))
            t5_wbmov.append(button(x=80,y=y,thickness=1,text="  >",font=30,w=30,t=str(t[1][0])+"do"))
            y += 30
#----------------------------------------------------------------------------------------------------
# Compare Alliance Function
#   - Given two alliances, tells who is more likely to win
#     and why.
# x=160,y = 145
#----------------------------------------------------------------------------------------------------
def compare():
    global t6_surface
    global t6_update
    global t6_tboxes

    global Teams
    #only changed locally
    global r1, r2, r3, b1, b2, b3
    global r1o, r1d, r1a, r1th, r1ah, r1hs, r1ab, r1bo, r1md, r1tt, r1tp, r1ha, r1as, r1po, r1pd, r1pa, r1t, r1ts
    global r2o, r2d, r2a, r2th, r2ah, r2hs, r2ab, r2bo, r2md, r2tt, r2tp, r2ha, r2as, r2po, r2pd, r2pa, r2t, r2ts
    global r3o, r3d, r3a, r3th, r3ah, r3hs, r3ab, r3bo, r3md, r3tt, r3tp, r3ha, r3as, r3po, r3pd, r3pa, r3t, r3ts
    global b1o, b1d, b1a, b1th, b1ah, b1hs, b1ab, b1bo, b1md, b1tt, b1tp, b1ha, b1as, b1po, b1pd, b1pa, b1t, b1ts
    global b2o, b2d, b2a, b2th, b2ah, b2hs, b2ab, b2bo, b2md, b2tt, b2tp, b2ha, b2as, b2po, b2pd, b2pa, b2t, b2ts
    global b3o, b3d, b3a, b3th, b3ah, b3hs, b3ab, b3bo, b3md, b3tt, b3tp, b3ha, b3as, b3po, b3pd, b3pa, b3t, b3ts

    #Draw the surface
    if t6_update:
        t6_surface.fill((bgcolor)) # Clear out old stuff
        font = pygame.font.Font(None,30)
        text = font.render(" Red Alliance: ",True,txcolor,bgcolor)
        t6_surface.blit(text,(0,70))
        text = font.render("Blue Alliance: ",True,txcolor,bgcolor)
        t6_surface.blit(text,(0,220))
        font = pygame.font.Font(None,12)
        text = font.render("Team",True,txcolor,bgcolor)
        t6_surface.blit(text,(140,20))
        text = font.render("Offense",True,txcolor,bgcolor)
        t6_surface.blit(text,(175,20))
        text = font.render("Defense",True,txcolor,bgcolor)
        t6_surface.blit(text,(215,20))
        text = font.render("Assist",True,txcolor,bgcolor)
        t6_surface.blit(text,(255,20))
        text = font.render("%HangSucc/Attempted",True,txcolor,bgcolor)
        t6_surface.blit(text,(295,20))
        text = font.render("HangScore",True,txcolor,bgcolor)
        t6_surface.blit(text,(430,20))
        text = font.render("AvgDiscScore",True,txcolor,bgcolor)
        t6_surface.blit(text,(500,20))
        text = font.render("Low",True,txcolor,bgcolor)
        t6_surface.blit(text,(610,20))
        text = font.render("Mid",True,txcolor,bgcolor)
        t6_surface.blit(text,(640,20))
        text = font.render("Top",True,txcolor,bgcolor)
        t6_surface.blit(text,(670,20))
        text = font.render("Pyr",True,txcolor,bgcolor)
        t6_surface.blit(text,(700,20))
        text = font.render("%HadAuto",True,txcolor,bgcolor)
        t6_surface.blit(text,(730,20))
        text = font.render("AvgAutoScore",True,txcolor,bgcolor)
        t6_surface.blit(text,(790,20))
        for textbox in t6_tboxes:
            textbox.draw(t6_surface)
        # if three teams on an alliance are selected, show their expected values
        if r1!=0 and r2!=0 and r3!=0:
            font = pygame.font.Font(None,20)
            text = font.render("Expected Offensive Score:" + str((r1o*r1po)+(r2o*r2po)+(r3o*r3po)),
                               True,txcolor,bgcolor)
            t6_surface.blit(text,(100,130))
            text = font.render("Expected Defensive Score:" + str((r1d*r1pd)+(r2d*r2pd)+(r3d*r3pd)),
                               True,txcolor,bgcolor)
            t6_surface.blit(text,(100,150))
            text= font.render("Expected Assistive Score:" + str((r1a*r1pa)+(r2a*r2pa)+(r3a*r3pa)),
                              True,txcolor,bgcolor)
            t6_surface.blit(text,(100,170))
        if b1!=0 and b2!=0 and b3!=0:
            font = pygame.font.Font(None,20)
            text = font.render("Expected Offensive Score:" + str((b1o*b1po)+(b2o*b2po)+(b3o*b3po)),
                               True,txcolor,bgcolor)
            t6_surface.blit(text,(100,300))
            text = font.render("Expected Defensive Score:" + str((b1d*b1pd)+(b2d*b2pd)+(b3d*b3pd)),
                               True,txcolor,bgcolor)
            t6_surface.blit(text,(100,320))
            text = font.render("Expected Assistive Score:" + str((b1a*b1pa)+(b2a*b2pa)+(b3a*b3pa)),
                               True,txcolor,bgcolor)
            t6_surface.blit(text,(100,340))
        if r1!=0 and r2!=0 and r3!=0 and b1!=0 and b2!=0 and b3!=0:
            # get standard deviations
            print "Calculating Probability"
            dr1 = [] #Differences from mean squared
            dr2 = []
            dr3 = []
            db1 = []
            db2 = []
            db3 = []
            for score in r1ts:
                dr1.append(((score-r1t)**2)/len(r1ts))
            for score in r2ts:
                dr2.append(((score-r2t)**2)/len(r2ts))
            for score in r3ts:
                dr3.append(((score-r3t)**2)/len(r3ts))
            for score in b1ts:
                db1.append(((score-b1t)**2)/len(b1ts))
            for score in b2ts:
                db2.append(((score-b2t)**2)/len(b2ts))
            for score in b3ts:
                db3.append(((score-b3t)**2)/len(b3ts))
            r1st = math.sqrt(sum(dr1))
            r2st = math.sqrt(sum(dr2))
            r3st = math.sqrt(sum(dr3))
            b1st = math.sqrt(sum(db1))
            b2st = math.sqrt(sum(db2))
            b3st = math.sqrt(sum(db3))
            mur = (float(1)/3)*(r1t+r2t+r3t)
            mub = (float(1)/3)*(b1t+b2t+b3t)
            rst = math.sqrt((float(1)/float(9))*(r1st**2+r2st**2+r3st**2))
            bst = math.sqrt((float(1)/float(9))*(b1st**2+b2st**2+b3st**2))
            if mur > mub:
                zval = (mur-mub)/math.sqrt((rst**2)+(bst**2)) if math.sqrt((rst**2)+(bst**2)) > 0 else 0
                perr = stats.lzprob(zval)
                font = pygame.font.Font(None,30)
                text = font.render("Winner: Red Alliance, " + str(100*perr) + "%",True,
                                   txcolor,bgcolor)
                t6_surface.blit(text,(100,400))
            else:
                zval = (mub-mur)/math.sqrt((rst**2)+(bst**2)) if math.sqrt((rst**2)+(bst**2)) > 0 else 0
                perr = stats.lzprob(zval)
                font = pygame.font.Font(None,30)
                text = font.render("Winner: Blue Alliance, " + str(100*1-perr) + "%",True,
                                   txcolor,bgcolor)
                t6_surface.blit(text,(100,400))

        t6_update = 0
   # Draw the main surface
    screen.blit(t6_surface,(160,65))


    #Check for changes
    for item in t6_tboxes:
        x = item.x+item.cw+item.th+160
        y = item.y+.5*item.th+65
        if x+item.w+.5*item.th>=mpos[0]>=x \
            and y+item.size+.5*item.th-10>=mpos[1]>=y:
            # click event
            item.clicked()
            exists = 0
            for team in Teams:
                if str(team.number) == str(item.value): # Team exists
                    exists = 1
                    if item.type == "rtn1": r1 = item.value
                    if item.type == "rtn2": r2 = item.value
                    if item.type == "rtn3": r3 = item.value
                    if item.type == "btn1": b1 = item.value
                    if item.type == "btn2": b2 = item.value
                    if item.type == "btn3": b3 = item.value
            if exists != 1: item.value = 0
            t6_update = 1
    # Get the team names
    r1 = 0
    r2 = 0
    r3 = 0
    b1 = 0
    b2 = 0
    b3 = 0
    for tbox in t6_tboxes:
        if tbox.type == "rt1n":
            try:
                r1 = int(tbox.value)
            except:
                "Invalid value"
        elif tbox.type == "rt2n":
            try:
                r2 = int(tbox.value)
            except:
                "Invalid value"
        elif tbox.type == "rt3n":
            try:
                r3 = int(tbox.value)
            except:
                "Invalid value"
        elif tbox.type == "bt1n":
            try:
                b1 = int(tbox.value)
            except:
                "Invalid value"
        elif tbox.type == "bt2n":
            try:
                b2 = int(tbox.value)
            except:
                "Invalid value"
        elif tbox.type == "bt3n":
            try:
                b3 = int(tbox.value)
            except:
                "Invalid value"

    #reset variables
    ##r1o = r1d = r1a = r1th = r1ah = r1hs = r1ab = r1bo = r1md = r1tt = r1tp = r1ha = r1as = r1po = r1pd = r1pa = r1t = r1ts = 0
    ##r2o = r2d = r2a = r2th = r2ah = r2hs = r2ab = r2bo = r2md = r2tt = r2tp = r2ha = r2as = r2po = r2pd = r2pa = r2t = r2ts = 0
    ##r3o = r3d = r3a = r3th = r3ah = r3hs = r3ab = r3bo = r3md = r3tt = r3tp = r3ha = r3as = r3po = r3pd = r3pa = r3t = r3ts = 0
    ##b1o = b1d = b1a = b1th = b1ah = b1hs = b1ab = b1bo = b1md = b1tt = b1tp = b1ha = b1as = b1po = b1pd = b1pa = b1t = b1ts = 0
    ##b2o = b2d = b2a = b2th = b2ah = b2hs = b2ab = b2bo = b2md = b2tt = b2tp = b2ha = b2as = b2po = b2pd = b2pa = b2t = b2ts = 0
    ##b3o = b3d = b3a = b3th = b3ah = b3hs = b3ab = b3bo = b3md = b3tt = b3tp = b3ha = b3as = b3po = b3pd = b3pa = b3t = b3ts = 0



    # Set variables based upon team number input
    for team in Teams:
        if team.number == r1:
            r1o = round(team.avgOff,1)
            r1d = round(team.avgDef,1)
            r1a = round(team.avgAst,1)
            r1th = int(100*team.timesHanged/len(team.matches))
            r1ah = int(100*team.attemptedHang/len(team.matches))
            r1hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
            r1ab = round(team.avg_DiscsScored,1)
	    r1bo = round(team.avg_teleLowP,1)
	    r1md = round(team.avg_teleMidP,1)
	    r1tt = round(team.avg_teleTopP,1)
            r1tp = round(team.avg_telePyrP,1)
	    r1ha = int(100*team.hadAuto/len(team.matches))
            r1as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            r1po = round(float(team.numOff)/len(team.matches),2)
            r1pd = round(float(team.numDef)/len(team.matches),2)
            r1pa = round(float(team.numAst)/len(team.matches),2)
            r1t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            r1ts = team.teleScores
        elif team.number == r2:
            r2o = round(team.avgOff,1)
            r2d = round(team.avgDef,1)
            r2a = round(team.avgAst,1)
            r2th = int(100*team.timesHanged/len(team.matches))
            r2ah = int(100*team.attemptedHang/len(team.matches))
            r2hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
	    r2ab = round(team.avg_DiscsScored,1)
	    r2bo = round(team.avg_teleLowP,1)
	    r2md = round(team.avg_teleMidP,1)
	    r2tt = round(team.avg_teleTopP,1)
            r2tp = round(team.avg_telePyrP,1)
	    r2ha = int(100*team.hadAuto/len(team.matches))
            r2as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            r2po = round(float(team.numOff)/len(team.matches),2)
            r2pd = round(float(team.numDef)/len(team.matches),2)
            r2pa = round(float(team.numAst)/len(team.matches),2)
            r2t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            r2ts = team.teleScores
        elif team.number == r3:
            r3o = round(team.avgOff,1)
            r3d = round(team.avgDef,1)
            r3a = round(team.avgAst,1)
            r3th = int(100*team.timesHanged/len(team.matches))
            r3ah = int(100*team.attemptedHang/len(team.matches))
            r3hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
	    r3ab = round(team.avg_DiscsScored,1)
	    r3bo = round(team.avg_teleLowP,1)
	    r3md = round(team.avg_teleMidP,1)
	    r3tt = round(team.avg_teleTopP,1)
            r3tp = round(team.avg_telePyrP,1)
	    r3ha = int(100*team.hadAuto/len(team.matches))
            r3as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            r3po = round(float(team.numOff)/len(team.matches),2)
            r3pd = round(float(team.numDef)/len(team.matches),2)
            r3pa = round(float(team.numAst)/len(team.matches),2)
            r3t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            r3ts = team.teleScores
        elif team.number == b1:
            b1o = round(team.avgOff,1)
            b1d = round(team.avgDef,1)
            b1a = round(team.avgAst,1)
            b1th = int(100*team.timesHanged/len(team.matches))
            b1ah = int(100*team.attemptedHang/len(team.matches))
            b1hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
	    b1ab = round(team.avg_DiscsScored,1)
	    b1bo = round(team.avg_teleLowP,1)
	    b1md = round(team.avg_teleMidP,1)
	    b1tt = round(team.avg_teleTopP,1)
            b1tp = round(team.avg_telePyrP,1)
	    b1ha = int(100*team.hadAuto/len(team.matches))
            b1as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            b1po = round(float(team.numOff)/len(team.matches),2)
            b1pd = round(float(team.numDef)/len(team.matches),2)
            b1pa = round(float(team.numAst)/len(team.matches),2)
            b1t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            b1ts = team.teleScores
        elif team.number == b2:
            b2o = round(team.avgOff,1)
            b2d = round(team.avgDef,1)
            b2a = round(team.avgAst,1)
            b2th = int(100*team.timesHanged/len(team.matches))
            b2ah = int(100*team.attemptedHang/len(team.matches))
            b2hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
	    b2ab = round(team.avg_DiscsScored,1)
	    b2bo = round(team.avg_teleLowP,1)
	    b2md = round(team.avg_teleMidP,1)
	    b2tt = round(team.avg_teleTopP,1)
            b2tp = round(team.avg_telePyrP,1)
	    b2ha = int(100*team.hadAuto/len(team.matches))
            b2as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            b2po = round(float(team.numOff)/len(team.matches),2)
            b2pd = round(float(team.numDef)/len(team.matches),2)
            b2pa = round(float(team.numAst)/len(team.matches),2)
            b2t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            b2ts = team.teleScores
        elif team.number == b3:
            b3o = round(team.avgOff,1)
            b3d = round(team.avgDef,1)
            b3a = round(team.avgAst,1)
            b3th = int(100*team.timesHanged/len(team.matches))
            b3ah = int(100*team.attemptedHang/len(team.matches))
            b3hs = int(sum(team.hangScores)/len(team.hangScores)) if team.timesHanged>0 else "N\A"
	    b3ab = round(team.avg_DiscsScored,1)
	    b3bo = round(team.avg_teleLowP,1)
	    b3md = round(team.avg_teleMidP,1)
	    b3tt = round(team.avg_teleTopP,1)
            b3tp = round(team.avg_telePyrP,1)
	    b3ha = int(100*team.hadAuto/len(team.matches))
            b3as = round(float(sum(team.autoScores)/len(team.autoScores)),2)
            b3po = round(float(team.numOff)/len(team.matches),2)
            b3pd = round(float(team.numDef)/len(team.matches),2)
            b3pa = round(float(team.numAst)/len(team.matches),2)
            b3t = round(float(sum(team.teleScores))/len(team.teleScores),2)
            b3ts = team.teleScores

    for tbox in t6_tboxes:
        if tbox.type == "r1o": tbox.value = r1o
        elif tbox.type == "r1d": tbox.value = r1d
        elif tbox.type == "r1a": tbox.value = r1a
        elif tbox.type == "r1th": tbox.value = r1th
        elif tbox.type == "r1ah": tbox.value = r1ah
        elif tbox.type == "r1hs": tbox.value = r1hs
        elif tbox.type == "r1ab": tbox.value = r1ab
        elif tbox.type == "r1bo": tbox.value = r1bo
        elif tbox.type == "r1md": tbox.value = r1md
        elif tbox.type == "r1tt": tbox.value = r1tt
        elif tbox.type == "r1tp": tbox.value = r1tp
        elif tbox.type == "r1ha": tbox.value = r1ha
        elif tbox.type == "r1as": tbox.value = r1as
        elif tbox.type == "r1po": tbox.value = r1po
        elif tbox.type == "r1pd": tbox.value = r1pd
        elif tbox.type == "r1pa": tbox.value = r1pa
        elif tbox.type == "r1t": tbox.value = r1t
        elif tbox.type == "r1ts": tbox.value = r1ts

        if tbox.type == "r2o": tbox.value = r2o
        elif tbox.type == "r2d": tbox.value = r2d
        elif tbox.type == "r2a": tbox.value = r2a
        elif tbox.type == "r2th": tbox.value = r2th
        elif tbox.type == "r2ah": tbox.value = r2ah
        elif tbox.type == "r2hs": tbox.value = r2hs
        elif tbox.type == "r2ab": tbox.value = r2ab
        elif tbox.type == "r2bo": tbox.value = r2bo
        elif tbox.type == "r2md": tbox.value = r2md
        elif tbox.type == "r2tt": tbox.value = r2tt
        elif tbox.type == "r2tp": tbox.value = r2tp
        elif tbox.type == "r2ha": tbox.value = r2ha
        elif tbox.type == "r2as": tbox.value = r2as
        elif tbox.type == "r2po": tbox.value = r2po
        elif tbox.type == "r2pd": tbox.value = r2pd
        elif tbox.type == "r2pa": tbox.value = r2pa
        elif tbox.type == "r2t": tbox.value = r2t
        elif tbox.type == "r2ts": tbox.value = r2ts

        if tbox.type == "r3o": tbox.value = r3o
        elif tbox.type == "r3d": tbox.value = r3d
        elif tbox.type == "r3a": tbox.value = r3a
        elif tbox.type == "r3th": tbox.value = r3th
        elif tbox.type == "r3ah": tbox.value = r3ah
        elif tbox.type == "r3hs": tbox.value = r3hs
        elif tbox.type == "r3ab": tbox.value = r3ab
        elif tbox.type == "r3bo": tbox.value = r3bo
        elif tbox.type == "r3md": tbox.value = r3md
        elif tbox.type == "r3tt": tbox.value = r3tt
        elif tbox.type == "r3tp": tbox.value = r3tp
        elif tbox.type == "r3ha": tbox.value = r3ha
        elif tbox.type == "r3as": tbox.value = r3as
        elif tbox.type == "r3po": tbox.value = r3po
        elif tbox.type == "r3pd": tbox.value = r3pd
        elif tbox.type == "r3pa": tbox.value = r3pa
        elif tbox.type == "r3t": tbox.value = r3t
        elif tbox.type == "r3ts": tbox.value = r3ts

        if tbox.type == "b1o": tbox.value = b1o
        elif tbox.type == "b1d": tbox.value = b1d
        elif tbox.type == "b1a": tbox.value = b1a
        elif tbox.type == "b1th": tbox.value = b1th
        elif tbox.type == "b1ah": tbox.value = b1ah
        elif tbox.type == "b1hs": tbox.value = b1hs
        elif tbox.type == "b1ab": tbox.value = b1ab
        elif tbox.type == "b1bo": tbox.value = b1bo
        elif tbox.type == "b1md": tbox.value = b1md
        elif tbox.type == "b1tt": tbox.value = b1tt
        elif tbox.type == "b1tp": tbox.value = b1tp
        elif tbox.type == "b1ha": tbox.value = b1ha
        elif tbox.type == "b1as": tbox.value = b1as
        elif tbox.type == "b1po": tbox.value = b1po
        elif tbox.type == "b1pd": tbox.value = b1pd
        elif tbox.type == "b1pa": tbox.value = b1pa
        elif tbox.type == "b1t": tbox.value = b1t
        elif tbox.type == "b1ts": tbox.value = b1ts

        if tbox.type == "b2o": tbox.value = b2o
        elif tbox.type == "b2d": tbox.value = b2d
        elif tbox.type == "b2a": tbox.value = b2a
        elif tbox.type == "b2th": tbox.value = b2th
        elif tbox.type == "b2ah": tbox.value = b2ah
        elif tbox.type == "b2hs": tbox.value = b2hs
        elif tbox.type == "b2ab": tbox.value = b2ab
        elif tbox.type == "b2bo": tbox.value = b2bo
        elif tbox.type == "b2md": tbox.value = b2md
        elif tbox.type == "b2tt": tbox.value = b2tt
        elif tbox.type == "b2tp": tbox.value = b2tp
        elif tbox.type == "b2ha": tbox.value = b2ha
        elif tbox.type == "b2as": tbox.value = b2as
        elif tbox.type == "b2po": tbox.value = b2po
        elif tbox.type == "b2pd": tbox.value = b2pd
        elif tbox.type == "b2pa": tbox.value = b2pa
        elif tbox.type == "b2t": tbox.value = b2t
        elif tbox.type == "b2ts": tbox.value = b2ts

        if tbox.type == "b3o": tbox.value = b3o
        elif tbox.type == "b3d": tbox.value = b3d
        elif tbox.type == "b3a": tbox.value = b3a
        elif tbox.type == "b3th": tbox.value = b3th
        elif tbox.type == "b3ah": tbox.value = b3ah
        elif tbox.type == "b3hs": tbox.value = b3hs
        elif tbox.type == "b3ab": tbox.value = b3ab
        elif tbox.type == "b3bo": tbox.value = b3bo
        elif tbox.type == "b3md": tbox.value = b3md
        elif tbox.type == "b3tt": tbox.value = b3tt
        elif tbox.type == "b3tp": tbox.value = b3tp
        elif tbox.type == "b3ha": tbox.value = b3ha
        elif tbox.type == "b3as": tbox.value = b3as
        elif tbox.type == "b3po": tbox.value = b3po
        elif tbox.type == "b3pd": tbox.value = b3pd
        elif tbox.type == "b3pa": tbox.value = b3pa
        elif tbox.type == "b3t": tbox.value = b3t
        elif tbox.type == "b3ts": tbox.value = b3ts

#----------------------------------------------------------------------------------------------------
# Alliance Selection
#----------------------------------------------------------------------------------------------------
def alliance_selection():
    global available_teams
    global wanted
    global t7_scroll
    global t7_tboxes
    global t7_update
    global t7_surface
    global screen

    screen.blit(t7_surface,(160,65))
    # Draw the team numbers on the scroller
    if t7_update:
        t7_surface.fill(bgcolor)
        for tb in t7_tboxes:
            tb.draw(t7_surface)
        x = 0
        y = 5
        t7_scroll.surface.fill(bgcolor)
        draw_list = []
        for te in wanted:
            for tea in available_teams:
                if int(te[1][0]) == int(tea):
                    draw_list.append(tea)
        #print "Draw list: " + str(draw_list)
        font = pygame.font.Font(None,20)
        for tm in draw_list:
            text = font.render("Team "+str(tm)+"",True,txcolor,bgcolor)
            t7_scroll.surface.blit(text,(x,y))
            y += 30
        t7_scroll.draw(t7_surface)

        # Start coordinates: (160,65)
        x=0
        y=5
        n = 1
        font = pygame.font.Font(None,40)
        #text = font.render(" Matches: ",True,txcolor,bgcolor)
        #t7_surface.blit(text,(510,65))
        while n < 9:
            text = font.render(str(n)+":",True,txcolor,bgcolor)
            t7_surface.blit(text,(x,y))
            y += 40
            n += 1
        t7_update = True

        # Draw the scroller buttons
        for but in t7_buttons:
            but.draw(t7_surface)

    # Scroller button click detection
    for but in t7_buttons:
        if mbut[0] == 1:
            if but.x<=cmpos[0]<=but.x+but.w and but.y<=cmpos[1]<=but.y+but.h:
                if but.type == "tlup":
                    t7_scroll.update(True)
                    t7_update = True
                elif but.type == "tldo":
                   t7_scroll.update(False)
                   t7_update = True

    # Textbox click detection (also, check to see if that team can be selected
    for tb in t7_tboxes:
        if tb.x+160<=mpos[0]<=tb.x+160+tb.w and tb.y+65<=mpos[1]<=tb.y+65+tb.size:
            tb.clicked()
            try: int(tb.value)
            except: tb.value = 0
            t7_update = True
            n = 0
            while n < len(available_teams):
                if str(tb.value) == str(available_teams[n]):
                    del available_teams[n] # So this team can no longer be chosen
                    break
                n += 1
            #if in_there != 1: textbox.value = 0 # Commented out b/c a user error would require a restart of the database

#----------------------------------------------------------------------------------------------------
# Main Loop
#----------------------------------------------------------------------------------------------------
#Main  Buttons
tb_buttons.append(button(x=6,y=6,thickness=4,text="New",t="n"))
tb_buttons.append(button(x=81,y=6,thickness=4,text="Open",t="o"))
tb_buttons.append(button(x=176,y=6,thickness=4,text="Save",t="s"))
tb_buttons.append(button(x=263,y=6,thickness=4,text="Import Data",t="i"))
#tb_buttons.append(button(x=457,y=6,thickness=4,text="Import Pit Data",t="ip"))
#tb_buttons.append(button(x=6,y=65,thickness=4,text="Matches",t="m"))
tb_buttons.append(button(x=6,y=100,thickness=4,text= "  Teams  ",t="t"))
#tb_buttons.append(button(x=6,y=135,thickness=4,text="   Pit   ",t="ps"))
tb_buttons.append(button(x=6,y=170,thickness=4,text= "Ranking",t="r"))
tb_buttons.append(button(x=6,y=205,thickness=4,text= "  Rank2  ",t="r2"))
tb_buttons.append(button(x=6,y=240,thickness=4,text= " Search ",t="se"))
tb_buttons.append(button(x=6,y=275,thickness=4,text= "Compare",t="co"))
tb_buttons.append(button(x=6,y=310,thickness=4,text= " Choose ",t="ch"))

#tab1 text boxes *top left = 160,65
t1_tboxes.append(textbox(x=0,y=0,thickness=1,caption="Team:",t="tnum",clickable=1))
t1_tboxes.append(textbox(x=0,y=35,thickness=1,caption="Matches:",t="numMatch",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=70,thickness=1,caption="Played Offensive:",t="pOff",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=90,thickness=1,caption="Played Defensive:",t="pDef",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=110,thickness=1,caption="Played Assistive:",t="pAst",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=140,thickness=1,caption="Avg Offensive Score:",t="avgOff",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=160,thickness=1,caption="Avg Defensive Score:",t="avgDef",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=180,thickness=1,caption="Avg Assistive Score:",t="avgAst",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=200,thickness=1,caption="Avg Total Score:",t="avgTotal",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=240,thickness=1,caption="Avg Weighted Off Score:",t="weightedOff",fs=25,w=50))
t1_tboxes.append(textbox(x=0,y=260,thickness=1,caption="Avg Weighted Def Score:",t="weightedDef",fs=25,w=50))
t1_tboxes.append(textbox(x=0,y=280,thickness=1,caption="Avg Weighted Ast Score:",t="weightedAst",fs=25,w=50))
t1_tboxes.append(textbox(x=0,y=320,thickness=1,caption="Offensive Rank:",t="rankOff",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=340,thickness=1,caption="Defensive Rank:",t="rankDef",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=360,thickness=1,caption="Assistive Rank:",t="rankAst",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=380,thickness=1,caption="Total Rank:",t="rankTot",fs=25,w=40))
#other ranks
t1_pic = Picture(x=700,y=0)

t1_tboxes.append(textbox(x=400,y=20,thickness=1,caption="Had Auto Mode:",t="pHadAuto",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=45,thickness=1,caption="Started in Auto Zone:",t="pStartInZone",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=65,thickness=1,caption="Other Auto:",t="pOtherStrat",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=110,thickness=1,caption="Average Auto Score:",t="avgAutoScore",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=130,thickness=1,caption="Average Auto Scored in Low:",t="avgAutoLowP",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=150,thickness=1,caption="Average Auto Scored in Mid:",t="avgAutoMidP",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=170,thickness=1,caption="Average Auto Scored in Top:",t="avgAutoTopP",fs=25,w=40))

t1_tboxes.append(textbox(x=400,y=205,thickness=1,caption="Matches/Disabled Percentage:",t="pWasDisabled",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=225,thickness=1,caption="Average Times Disabled per Match:",t="avgDisabled",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=245,thickness=1,caption="Number of Times Disabled:",t="totalDisabled",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=265,thickness=1,caption="Discs Picked Up to Discs Scored:",t="rPickUpScored",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=285,thickness=1,caption="Average Discs Picked up from Floor:",t="avgFloorPickUp",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=305,thickness=1,caption="Average Discs Picked up from Station:",t="avgStationPickUp",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=325,thickness=1,caption="Average Tele Score:",t="avgTeleScore",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=345,thickness=1,caption="Average Scored in Low:",t="avgTeleLowP",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=365,thickness=1,caption="Average Scored in Mid:",t="avgTeleMidP",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=385,thickness=1,caption="Average Scored in Top:",t="avgTeleTopP",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=405,thickness=1,caption="Average Scored in Pyramid:",t="avgTelePyrP",fs=25,w=40))

t1_tboxes.append(textbox(x=400,y=445,thickness=1,caption="Average Hang Score:",t="avgHangScore",fs=24,w=40))
t1_tboxes.append(textbox(x=400,y=465,thickness=1,caption="Successful Hangs to Attempts:",t="rHangSuccToAtt",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=485,thickness=1,caption="Robot Hung from Pyramid:",t="pHanged",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=505,thickness=1,caption="Average Supports of Another Bot while Hanging:",t="avgSupportBot",fs=25,w=40))
t1_tboxes.append(textbox(x=400,y=525,thickness=1,caption="Average Disc Scores while Hanging:",t="avgScoredOnPyr",fs=25,w=40))

t1_tboxes.append(textbox(x=0,y=425,thickness=1,caption="Average number of Regular Fouls:",t="avgRegFoul",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=445,thickness=1,caption="Average number of Technical Fouls:",t="avgTechFoul",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=465,thickness=1,caption="Defensive:",t="pDefensive",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=485,thickness=1,caption="Assistive:",t="pAssistive",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=505,thickness=1,caption="Received Yellow Card:",t="pYellow",fs=25,w=40))
t1_tboxes.append(textbox(x=0,y=525,thickness=1,caption="Received Red Card:",t="pRed",fs=25,w=40))

#tab2 stuff
##t2_tboxes.append(textbox(x=0,y=0,thickness=1,caption="Team:",t="tnum",clickable=1))
##t2_tboxes.append(textbox(x=0,y=40,thickness=1,caption="Robot Length:",t="rbln",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=60,thickness=1,caption="Robot Width:",t="rbwd",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=80,thickness=1,caption="Robot Heigth:",t="rbhg",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=100,thickness=1,caption="Robot Wieght:",t="rbwg",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=120,thickness=1,caption="Floor Clearance to Frame:",t="frcr",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=140,thickness=1,caption="Spacing between the wheels:",t="wlsc",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=160,thickness=1,caption="Ability to lower bridge:",t="bgmc",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=180,thickness=1,caption="Traction on Bridge:",t="sdbg",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=200,thickness=1,caption="Has a sensor for balance:",t="blsn",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=220,thickness=1,caption="Has gear shifting system:",t="sggr",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=260,thickness=1,caption="Type of Drive System:",t="dvsy",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=280,thickness=1,caption="Center of Mass:",t="cnms",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=300,thickness=1,caption="Do they have a Drive Team:",t="dri1",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=320,thickness=1,caption="How many years have they played:",t="exp1",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=360,thickness=1,caption="Do they have a second Drive team:",t="dri2",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=380,thickness=1,caption="How many years have they played:",t="exp2",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=420,thickness=1,caption="Do they have a third  Drive team:",t="dri3",fs=30,w=50))
##t2_tboxes.append(textbox(x=0,y=440,thickness=1,caption="How many years have they played:",t="exp3",fs=30,w=50))

#tab3 stuff
t3_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=160,y=105,t="")) #Offensive Score Scroller
t3_buttons.append(button(x=160,y=85,thickness=1,text="",t="offup",w=200,h=20)) #scroll offensive score up
t3_buttons.append(button(x=160,y=605,thickness=1,text="",t="offdo",w=200,h=20)) #scroll offensive score down
t3_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=370,y=105,t="")) #Defensive Score Scroller
t3_buttons.append(button(x=370,y=85,thickness=1,text="",t="defup",w=200,h=20))#scroll defensive score up
t3_buttons.append(button(x=370,y=605,thickness=1,text="",t="defdo",w=200,h=20))#scroll defensive score down
t3_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=580,y=105,t="")) #Assistive Score Scroller
t3_buttons.append(button(x=580,y=85,thickness=1,text="",t="astup",w=200,h=20))#scroll assistive score up
t3_buttons.append(button(x=580,y=605,thickness=1,text="",t="astdo",w=200,h=20))#scroll assistive score down
t3_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=790,y=105,t="")) #Total Score Scroller
t3_buttons.append(button(x=790,y=85,thickness=1,text="",t="totup",w=200,h=20))#scroll total score up
t3_buttons.append(button(x=790,y=605,thickness=1,text="",t="totdo",w=200,h=20))#scroll total score down

#tab4 stuff
t4_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=160,y=105,t="")) #Offensive Score Scroller
t4_buttons.append(button(x=160,y=85,thickness=1,text="",t="autoup",w=200,h=20)) #scroll offensive score up
t4_buttons.append(button(x=160,y=605,thickness=1,text="",t="autodo",w=200,h=20)) #scroll offensive score down
t4_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=370,y=105,t="")) #Defensive Score Scroller
t4_buttons.append(button(x=370,y=85,thickness=1,text="",t="teleup",w=200,h=20))#scroll defensive score up
t4_buttons.append(button(x=370,y=605,thickness=1,text="",t="teledo",w=200,h=20))#scroll defensive score down
t4_scrolls.append(scroller(pygame.Surface((200,2000)),maxheight=500,x=580,y=105,t="")) #Assistive Score Scroller
t4_buttons.append(button(x=580,y=85,thickness=1,text="",t="pyrup",w=200,h=20))#scroll assistive score up
t4_buttons.append(button(x=580,y=605,thickness=1,text="",t="pyrdo",w=200,h=20))#scroll assistive score down

#tab5 stuff
t5_stuff.append(textbox(x=160,y=65,thickness=1,caption="Offensive Score >= ",clickable=1,val=-30,fs=30,w=50,t="avgOff"))
t5_stuff.append(textbox(x=160,y=95,thickness=1,caption="Defensive Score >= ",clickable=1,val=-30,fs=30,w=50,t="avgDef"))
t5_stuff.append(textbox(x=160,y=125,thickness =1,caption="Assistive Score >= ",clickable=1,val=-30,fs=30,w=50,t="avgAst"))
t5_stuff.append(radio(x=160,y=155,fs=30,caption="Played Offensive",t="numOff"))
t5_stuff.append(radio(x=160,y=185,fs=30,caption="Played Defensive",t="numDef"))
t5_stuff.append(radio(x=160,y=215,fs=30,caption="Played Assistive",t="numAst"))
t5_stuff.append(radio(x=160,y=245,fs=30,caption="Scored in Auto",t="scoredAuto"))
t5_stuff.append(radio(x=160,y=275,fs=30,caption="Started in the Auto Zone",t="StartedInAuto"))
t5_stuff.append(radio(x=160,y=305,fs=30,caption="Other Strategy in Auto",t="OtherAutoStrat"))
t5_stuff.append(radio(x=160,y=335,fs=30,caption="Hung from a Pyramid",t="timesHanged"))
t5_stuff.append(textbox(x=160,y=365,thickness =1,caption="Hang Score >= ",clickable=1,val=-30,fs=30,w=50,t="avgHangScore"))
t5_stuff.append(radio(x=160,y=395,fs=30,caption="Supported Bot While Hanging",t="TotalSupportsBot"))
t5_stuff.append(radio(x=160,y=425,fs=30,caption="Scored Discs While Hanging",t="TotalScoredOnPyr"))
t5_stuff.append(radio(x=160,y=455,fs=30,caption="Never Disabled",t="disabledCount"))
t5_stuff.append(radio(x=160,y=485,fs=30,caption="No Regular Fouls",t="hadRegFoul"))
t5_stuff.append(radio(x=160,y=515,fs=30,caption="No Technical Fouls",t="hadTechFoul"))
t5_stuff.append(radio(x=160,y=545,fs=30,caption="No Yellow Cards",t="hadYellow"))
t5_stuff.append(radio(x=160,y=575,fs=30,caption="No Red Cards",t="hadRed"))
#tab 5's scroller
t5_scroll = scroller(pygame.Surface((100,2000)),maxheight=400,x=510,y=105,t="")
t5_wscroll = scroller(pygame.Surface((110,2000)),maxheight=400,x=630,y=105,t="")
#tab 5 buttons
t5_buttons.append(button(x=510,y=84,thickness=1,text="",t="tlup",w=100,h=20))
t5_buttons.append(button(x=510,y=510,thickness=1,text="",t="tldo",w=100,h=20))
t5_buttons.append(button(x=630,y=84,thickness=1,text="",t="wlup",w=110,h=20))
t5_buttons.append(button(x=630,y=510,thickness=1,text="",t="wldo",w=110,h=20))

# Tab 6 stuff
t6_tboxes.append(textbox(x=140,y=40,thickness=1,caption="",clickable=1,fs=20,w=30,t="rt1n"))            #Red alliance, team 1's number
t6_tboxes.append(textbox(x=140,y=70,thickness=1,caption="",clickable=1,fs=20,w=30,t="rt2n"))            #Red alliamce, team 2's number
t6_tboxes.append(textbox(x=140,y=100,thickness=1,caption="",clickable=1,fs=20,w=30,t="rt3n"))           #Red alliance, team 3's number
t6_tboxes.append(textbox(x=175,y=40,thickness=1,caption="",fs=20,w=50,t="r1o"))                         #Red alliance, team 1's offensive score
t6_tboxes.append(textbox(x=175,y=70,thickness=1,caption="",fs=20,w=50,t="r2o"))                         #Red alliance, team 2's offensive score
t6_tboxes.append(textbox(x=175,y=100,thickness=1,caption="",fs=20,w=50,t="r3o"))                        #Red alliance, team 3's offensive score
t6_tboxes.append(textbox(x=215,y=40,thickness=1,caption="",fs=20,w=50,t="r1d"))                         #Red alliance, team 1's defensive score
t6_tboxes.append(textbox(x=215,y=70,thickness=1,caption="",fs=20,w=50,t="r2d"))                         #Red alliance, team 2's defensive score
t6_tboxes.append(textbox(x=215,y=100,thickness=1,caption="",fs=20,w=50,t="r3d"))                        #Red alliance, team 3's defensive score
t6_tboxes.append(textbox(x=255,y=40,thickness=1,caption="",fs=20,w=50,t="r1a"))                         #Red alliance, team 1's assistive score
t6_tboxes.append(textbox(x=255,y=70,thickness=1,caption="",fs=20,w=50,t="r2a"))                         #Red alliance, team 2's assistive score
t6_tboxes.append(textbox(x=255,y=100,thickness=1,caption="",fs=20,w=50,t="r3a"))                        #Red alliance, team 3's assistive score
t6_tboxes.append(textbox(x=305,y=40,thickness=1,caption="",fs=20,w=50,t="r1th"))                        #Red alliance, team 1 times hanged
t6_tboxes.append(textbox(x=305,y=70,thickness=1,caption="",fs=20,w=50,t="r2th"))                        #Red alliance, team 2 " "
t6_tboxes.append(textbox(x=305,y=100,thickness=1,caption="",fs=20,w=50,t="r3th"))                       #Red alliance, team 3 " "
t6_tboxes.append(textbox(x=365,y=40,thickness=1,caption="",fs=20,w=50,t="r1ah"))                        #Red alliance, team 1 attempted hanging
t6_tboxes.append(textbox(x=365,y=70,thickness=1,caption="",fs=20,w=50,t="r2ah"))                        #Red alliance, team 2 " "
t6_tboxes.append(textbox(x=365,y=100,thickness=1,caption="",fs=20,w=50,t="r3ah"))                       #Red alliance, team 3 " "
t6_tboxes.append(textbox(x=450,y=40,thickness=1,caption="",fs=20,w=50,t="r1hs"))                        #Red alliance, team 1 hang score
t6_tboxes.append(textbox(x=450,y=70,thickness=1,caption="",fs=20,w=50,t="r2ha"))                        #Red alliance, team 2 hang score
t6_tboxes.append(textbox(x=450,y=100,thickness=1,caption="",fs=20,w=50,t="r3ha"))                       #Red alliance, team 3 hang score
t6_tboxes.append(textbox(x=525,y=40,thickness=1,caption="",fs=20,w=50,t="r1ab"))                        #Red alliance, team 1 Average discs scored
t6_tboxes.append(textbox(x=525,y=70,thickness=1,caption="",fs=20,w=50,t="r2ab"))                        #Red alliance, team 2 Average discs scored
t6_tboxes.append(textbox(x=525,y=100,thickness=1,caption="",fs=20,w=50,t="r3ab"))                       #Red alliance, team 3 Average discs scored
t6_tboxes.append(textbox(x=610,y=40,thickness=1,caption="",fs=20,w=50,t="r1bo"))                        #Red alliance, team 1 Average discs bottom
t6_tboxes.append(textbox(x=610,y=70,thickness=1,caption="",fs=20,w=50,t="r2bo"))                        #Red alliance, team 2 Average discs bottom
t6_tboxes.append(textbox(x=610,y=100,thickness=1,caption="",fs=20,w=50,t="r3bo"))                       #Red alliance, team 3 Average discs bottom
t6_tboxes.append(textbox(x=640,y=40,thickness=1,caption="",fs=20,w=50,t="r1md"))                        #Red alliance, team 1 Average discs middle
t6_tboxes.append(textbox(x=640,y=70,thickness=1,caption="",fs=20,w=50,t="r2md"))                        #Red alliance, team 2 Average discs middle
t6_tboxes.append(textbox(x=640,y=100,thickness=1,caption="",fs=20,w=50,t="r3md"))                       #Red alliance, team 3 Average discs middle
t6_tboxes.append(textbox(x=670,y=40,thickness=1,caption="",fs=20,w=50,t="r1tt"))                        #Red alliance, team 1 Average discs top
t6_tboxes.append(textbox(x=670,y=70,thickness=1,caption="",fs=20,w=50,t="r2tt"))                        #Red alliance, team 2 Average discs top
t6_tboxes.append(textbox(x=670,y=100,thickness=1,caption="",fs=20,w=50,t="r3tt"))                       #Red alliance, team 3 Average discs top
t6_tboxes.append(textbox(x=700,y=40,thickness=1,caption="",fs=20,w=50,t="r1tp"))                        #Red alliance, team 1 Average discs pyramid
t6_tboxes.append(textbox(x=700,y=70,thickness=1,caption="",fs=20,w=50,t="r2tp"))                        #Red alliance, team 2 Average discs pyramid
t6_tboxes.append(textbox(x=700,y=100,thickness=1,caption="",fs=20,w=50,t="r3tp"))                       #Red alliance, team 3 Average discs pyramid
t6_tboxes.append(textbox(x=750,y=40,thickness=1,caption="",fs=20,w=50,t="r1ha"))                        #Red alliance, team 1 had auto
t6_tboxes.append(textbox(x=750,y=70,thickness=1,caption="",fs=20,w=50,t="r2ha"))                        #Red alliance, team 2 had auto
t6_tboxes.append(textbox(x=750,y=100,thickness=1,caption="",fs=20,w=50,t="r3ha"))                       #Red alliance, team 3 had auto
t6_tboxes.append(textbox(x=810,y=40,thickness=1,caption="",fs=20,w=50,t="r1as"))                        #Red alliance, team 1 auto score
t6_tboxes.append(textbox(x=810,y=70,thickness=1,caption="",fs=20,w=50,t="r2as"))                        #Red alliance, team 2 auto score
t6_tboxes.append(textbox(x=810,y=100,thickness=1,caption="",fs=20,w=50,t="r3as"))                       #Red alliance, team 3 auto score
t6_tboxes.append(textbox(x=140,y=200,thickness=1,caption="",clickable=1,fs=20,w=30,t="bt1n"))           #Blue alliance, team 1's number
t6_tboxes.append(textbox(x=140,y=230,thickness=1,caption="",clickable=1,fs=20,w=30,t="bt2n"))           #blue alliamce, team 2's number
t6_tboxes.append(textbox(x=140,y=260,thickness=1,caption="",clickable=1,fs=20,w=30,t="bt3n"))           #blue alliance, team 3's number
t6_tboxes.append(textbox(x=175,y=200,thickness=1,caption="",fs=20,w=50,t="b1o"))                        #blue alliance, team 1's offensive score
t6_tboxes.append(textbox(x=175,y=230,thickness=1,caption="",fs=20,w=50,t="b2o"))                        #blue alliance, team 2's offensive score
t6_tboxes.append(textbox(x=175,y=260,thickness=1,caption="",fs=20,w=50,t="b3o"))                        #blue alliance, team 3's offensive score
t6_tboxes.append(textbox(x=215,y=200,thickness=1,caption="",fs=20,w=50,t="b1d"))                        #blue alliance, team 1's defensive score
t6_tboxes.append(textbox(x=215,y=230,thickness=1,caption="",fs=20,w=50,t="b2d"))                        #blue alliance, team 2's defensive score
t6_tboxes.append(textbox(x=215,y=260,thickness=1,caption="",fs=20,w=50,t="b3d"))                        #blue alliance, team 3's defensive score
t6_tboxes.append(textbox(x=255,y=200,thickness=1,caption="",fs=20,w=50,t="b1a"))                        #blue alliance, team 1's assistive score
t6_tboxes.append(textbox(x=255,y=230,thickness=1,caption="",fs=20,w=50,t="b2a"))                        #blue alliance, team 2's assistive score
t6_tboxes.append(textbox(x=255,y=260,thickness=1,caption="",fs=20,w=50,t="b3a"))                        #blue alliance, team 3's assistive score
t6_tboxes.append(textbox(x=305,y=200,thickness=1,caption="",fs=20,w=50,t="b1th"))                       #blue alliance, team 1 balanced bridge
t6_tboxes.append(textbox(x=305,y=230,thickness=1,caption="",fs=20,w=50,t="b2th"))                       #blue alliance, team 2 balanced bridge
t6_tboxes.append(textbox(x=305,y=260,thickness=1,caption="",fs=20,w=50,t="b3th"))                       #blue alliance, team 3 balanced bridge
t6_tboxes.append(textbox(x=365,y=200,thickness=1,caption="",fs=20,w=50,t="b1ah"))                       #blue alliance, team 1 balanced team bridge
t6_tboxes.append(textbox(x=365,y=230,thickness=1,caption="",fs=20,w=50,t="b2ah"))                       #blue alliance, team 2 balanced team bridge
t6_tboxes.append(textbox(x=365,y=260,thickness=1,caption="",fs=20,w=50,t="b3ah"))                       #blue alliance, team 3 balanced team bridge
t6_tboxes.append(textbox(x=450,y=200,thickness=1,caption="",fs=20,w=50,t="b1hs"))                       #blue alliance, team 1 bridge score
t6_tboxes.append(textbox(x=450,y=230,thickness=1,caption="",fs=20,w=50,t="b2hs"))                       #blue alliance, team 2 bridge score
t6_tboxes.append(textbox(x=450,y=260,thickness=1,caption="",fs=20,w=50,t="b3hs"))                       #blue alliance, team 3 bridge score
t6_tboxes.append(textbox(x=525,y=200,thickness=1,caption="",fs=20,w=50,t="b1ab"))                       #blue alliance, team 1 Average discs scored
t6_tboxes.append(textbox(x=525,y=230,thickness=1,caption="",fs=20,w=50,t="b2ab"))                       #blue alliance, team 2 Average discs scored
t6_tboxes.append(textbox(x=525,y=260,thickness=1,caption="",fs=20,w=50,t="b3ab"))                       #blue alliance, team 3 Average discs scored
t6_tboxes.append(textbox(x=610,y=200,thickness=1,caption="",fs=20,w=50,t="b1bo"))                       #blue alliance, team 1 Average discs bottom
t6_tboxes.append(textbox(x=610,y=230,thickness=1,caption="",fs=20,w=50,t="b2bo"))                       #blue alliance, team 2 Average discs bottom
t6_tboxes.append(textbox(x=610,y=260,thickness=1,caption="",fs=20,w=50,t="b3bo"))                       #blue alliance, team 3 Average discs bottom
t6_tboxes.append(textbox(x=640,y=200,thickness=1,caption="",fs=20,w=50,t="b1md"))                       #blue alliance, team 1 Average discs middle
t6_tboxes.append(textbox(x=640,y=230,thickness=1,caption="",fs=20,w=50,t="b2md"))                       #blue alliance, team 2 Average discs middle
t6_tboxes.append(textbox(x=640,y=260,thickness=1,caption="",fs=20,w=50,t="b3md"))                       #blue alliance, team 3 Average discs middle
t6_tboxes.append(textbox(x=670,y=200,thickness=1,caption="",fs=20,w=50,t="b1tt"))                       #blue alliance, team 1 Average discs top
t6_tboxes.append(textbox(x=670,y=230,thickness=1,caption="",fs=20,w=50,t="b2tt"))                       #blue alliance, team 2 Average discs top
t6_tboxes.append(textbox(x=670,y=260,thickness=1,caption="",fs=20,w=50,t="b3tt"))                       #blue alliance, team 3 Average discs top
t6_tboxes.append(textbox(x=700,y=200,thickness=1,caption="",fs=20,w=50,t="b1tp"))                       #blue alliance, team 1 Average discs pyramid
t6_tboxes.append(textbox(x=700,y=230,thickness=1,caption="",fs=20,w=50,t="b2tp"))                       #blue alliance, team 2 Average discs pyramid
t6_tboxes.append(textbox(x=700,y=260,thickness=1,caption="",fs=20,w=50,t="b3tp"))                       #blue alliance, team 3 Average discs pyramid
t6_tboxes.append(textbox(x=750,y=200,thickness=1,caption="",fs=20,w=50,t="b1ha"))                       #blue alliance, team 1 had auto
t6_tboxes.append(textbox(x=750,y=230,thickness=1,caption="",fs=20,w=50,t="b2ha"))                       #blue alliance, team 2 had auto
t6_tboxes.append(textbox(x=750,y=260,thickness=1,caption="",fs=20,w=50,t="b3ha"))                       #blue alliance, team 3 had auto
t6_tboxes.append(textbox(x=810,y=200,thickness=1,caption="",fs=20,w=50,t="b1as"))                       #blue alliance, team 1 auto score
t6_tboxes.append(textbox(x=810,y=230,thickness=1,caption="",fs=20,w=50,t="b2as"))                       #blue alliance, team 2 auto score
t6_tboxes.append(textbox(x=810,y=260,thickness=1,caption="",fs=20,w=50,t="b3as"))                       #blue alliance, team 3 auto score

# Tab 7 stuff
t7_tboxes.append(textbox(x=100,y=5,thickness=1,caption="",fs=40,w=50,t="a1t1",clickable=1)) # alliance 1, team 1
t7_tboxes.append(textbox(x=165,y=5,thickness=1,caption="",fs=40,w=50,t="a1t2",clickable=1)) # alliance 1, team 2
t7_tboxes.append(textbox(x=230,y=5,thickness=1,caption="",fs=40,w=50,t="a1t3",clickable=1)) # alliance 1, team 3
t7_tboxes.append(textbox(x=100,y=45,thickness=1,caption="",fs=40,w=50,t="a2t1",clickable=1)) # alliance 2, team 1
t7_tboxes.append(textbox(x=165,y=45,thickness=1,caption="",fs=40,w=50,t="a2t2",clickable=1)) # alliance 2, team 2
t7_tboxes.append(textbox(x=230,y=45,thickness=1,caption="",fs=40,w=50,t="a2t3",clickable=1)) # alliance 2, team 3
t7_tboxes.append(textbox(x=100,y=85,thickness=1,caption="",fs=40,w=50,t="a3t1",clickable=1)) # alliance 3, team 1
t7_tboxes.append(textbox(x=165,y=85,thickness=1,caption="",fs=40,w=50,t="a3t2",clickable=1)) # alliance 3, team 2
t7_tboxes.append(textbox(x=230,y=85,thickness=1,caption="",fs=40,w=50,t="a3t3",clickable=1)) # alliance 3, team 3
t7_tboxes.append(textbox(x=100,y=125,thickness=1,caption="",fs=40,w=50,t="a4t1",clickable=1)) # alliance 4, team 1
t7_tboxes.append(textbox(x=165,y=125,thickness=1,caption="",fs=40,w=50,t="a4t2",clickable=1)) # alliance 4, team 2
t7_tboxes.append(textbox(x=230,y=125,thickness=1,caption="",fs=40,w=50,t="a4t3",clickable=1)) # alliance 4, team 3
t7_tboxes.append(textbox(x=100,y=165,thickness=1,caption="",fs=40,w=50,t="a1t1",clickable=1)) # alliance 5, team 1
t7_tboxes.append(textbox(x=165,y=165,thickness=1,caption="",fs=40,w=50,t="a1t2",clickable=1)) # alliance 5, team 2
t7_tboxes.append(textbox(x=230,y=165,thickness=1,caption="",fs=40,w=50,t="a1t3",clickable=1)) # alliance 5, team 3
t7_tboxes.append(textbox(x=100,y=205,thickness=1,caption="",fs=40,w=50,t="a2t1",clickable=1)) # alliance 6, team 1
t7_tboxes.append(textbox(x=165,y=205,thickness=1,caption="",fs=40,w=50,t="a2t2",clickable=1)) # alliance 6, team 2
t7_tboxes.append(textbox(x=230,y=205,thickness=1,caption="",fs=40,w=50,t="a2t3",clickable=1)) # alliance 6, team 3
t7_tboxes.append(textbox(x=100,y=245,thickness=1,caption="",fs=40,w=50,t="a3t1",clickable=1)) # alliance 7, team 1
t7_tboxes.append(textbox(x=165,y=245,thickness=1,caption="",fs=40,w=50,t="a3t2",clickable=1)) # alliance 7, team 2
t7_tboxes.append(textbox(x=230,y=245,thickness=1,caption="",fs=40,w=50,t="a3t3",clickable=1)) # alliance 7, team 3
t7_tboxes.append(textbox(x=100,y=285,thickness=1,caption="",fs=40,w=50,t="a4t1",clickable=1)) # alliance 8, team 1
t7_tboxes.append(textbox(x=165,y=285,thickness=1,caption="",fs=40,w=50,t="a4t2",clickable=1)) # alliance 8, team 2
t7_tboxes.append(textbox(x=230,y=285,thickness=1,caption="",fs=40,w=50,t="a4t3",clickable=1)) # alliance 8, team 3
t7_scroll = scroller(pygame.Surface((100,2000)),maxheight=500,x=410,y=25,t="")
t7_buttons.append(button(x=410,y=4,thickness=1,text="",t="tlup",w=100,h=20))
t7_buttons.append(button(x=410,y=530,thickness=1,text="",t="tldo",w=100,h=20))

#If want to import data from last session
root.focus()
newval = tkSimpleDialog.askstring("Prompt","Reload Previous Data? (y / n)",parent=root,initialvalue="y")
root.withdraw()
if newval == "y":
    Reload = True
    for but in tb_buttons:
        if but.type == "i":
            but.click()
    Reload = False

screen.fill(bgcolor)

#draw top bar
pygame.draw.rect(screen, (0,0,0), (2,2,1276,46),5)
pygame.draw.rect(screen, (0,0,0), (2,50,1276,10),5)
for but in tb_buttons:
    if but.static == 1:
        but.draw(screen)
#draw side bar
pygame.draw.rect(screen, (0,0,0), (2,60,155,1000),5)

while running:
    mpos = (-1,-1)  #reset
    cmpos = pygame.mouse.get_pos() #current mouse position
    mbut = pygame.mouse.get_pressed() #which buttons are pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print "quit has been pressed"
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:    #Click on buttons
            mpos = pygame.mouse.get_pos()
            for but in tb_buttons:
                if mpos[0]>=but.x and mpos[0]<=but.x+but.w and mpos[1]>=but.y and mpos[1]<=but.y+but.h:
                    but.click()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        running = False
        print "ESC has been pressed"
            
    # draw the tab
    screen.fill(bgcolor,[x0,y0,WIDTH-x0,HEIGHT-y0])#Fill in case of update
    if tab == 1:    #Team Data
        team_data()
    #elif tab == 2:
        #team_pitdata()
    elif tab == 3:  #Rank data
        ratings()
    elif tab == 4:
        ratings2()
    elif tab == 5:  #Search Tab
        search()
        # Present list of teams that meet criteria on right, if needed to update
        if t5_update:
            y = 5
            team_list.sort()
            t5_tempbut = []
            t5_temprad = []
            for t in team_list:
                #add the buttons to the list
                t5_tempbut.append(button(x=0,y=y,thickness=1,text=str(t[0]),font=30,w=50,t=str(t[0])))
                t5_temprad.append(radio(x=55,y=y,caption=[],flip = 1,t=str(t[0]),fs=30,teamnum=t[0]))
                y += 30
    elif tab == 6:  #Alliance Comparison Tab
        compare()
    elif tab == 7: #Alliance Selection tab
        alliance_selection()

    pygame.display.flip()
    new = pygame.time.get_ticks()
    if (new-last)!= 0:
        print str(1000/(new-last))
    last = new
