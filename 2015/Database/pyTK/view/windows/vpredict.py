#------------------------------------------------------------------------------
# vpredict module
#   -- contains information for displaying the predict window
#------------------------------------------------------------------------------
from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import re

from controller.windows import cpredict

#------------------------------------------------------------------------------
# Predict class
#   -- contains all the functions, etc, for displaying a predict window
#------------------------------------------------------------------------------
class Predict(Frame):
    """Class that handles displaying a predict window to the screen."""

    def predict_alliances(self):
        teams = []
        for i in self.rVals:
            teams.append(i[0])
        for i in self.bVals:
            teams.append(i[0])

        self.outcomeVar.set("Winner - " + self.controller.getComparison(teams) + "%")

    def clear_predict(self):
        self.outcomeVar.set("N/A")
    
    def load_alliance(self, event=None, teams=None, ally=None):
        loadedTeams = self.controller.loadAlliance(alliance=teams)
        
        setState = NORMAL if teams == "Custom" else "readonly"
        if ally == self.rVals:
            i = 0
            for entry in self.rTeamEntries:
                entry.config(state=setState)
                self.rVals[i][0].set(loadedTeams[i])
                self.load_team(teamVals=self.rVals,index=i)
                i+=1
        elif ally == self.bVals:
            i = 0
            for entry in self.bTeamEntries:
                entry.config(state=setState)
                self.bVals[i][0].set(loadedTeams[i])
                self.load_team(teamVals=self.bVals,index=i)
                i+=1

        # eventually will load pre-saved alliances, including the 8 seeded alliances
        
                
        
    def load_team(self, event=None, teamVals=None, index=None):
        team = teamVals[index][0].get()
        if team not in self.controller.available and team != "0":
            tkMessageBox.showinfo("Team Status","That team is not available. Please choose another.")
            teamVals[index][0].set("0")

        self.controller.getInfo(teamVals,index)

        if teamVals[0][0].get() != "0" and teamVals[1][0].get() != "0" and teamVals[2][0].get() != "0":
            data = self.controller.getPrediction(teamVals[0][0],teamVals[1][0],teamVals[2][0])

            if teamVals == self.rVals:
                self.rOffScore.set("Expected Offensive Score: " + str(data[0]))
            elif teamVals == self.bVals:
                self.bOffScore.set("Expected Offensive Score: " + str(data[0]))

        elif teamVals[0][0].get() == "0" or teamVals[1][0].get() == "0" or teamVals[2][0].get() == "0":
            if teamVals == self.rVals:
                self.rOffScore.set("Expected Offensive Score: N/A")
            elif teamVals == self.bVals:
                self.bOffScore.set("Expected Offensive Score: N/A")
            
            
    def create_AllianceOptions(self):
        # create a frame to put the OptionMenu in
        self.rOptionFrame = Frame(self.redAlliance)
        self.rOptionFrame.pack(side=LEFT)

        self.label = Label(self.rOptionFrame,text="Red Alliance:")
        self.label.pack(side=TOP,padx=5,pady=5)

        # create the red alliance OptionMenu
        self.rAllChoiceVar = StringVar(self.rOptionFrame)
        self.rAllChoiceVar.set("Custom")
        self.rAllianceOM = OptionMenu(self.rOptionFrame, self.rAllChoiceVar, *self.controller.allianceOptions,
                                      command=lambda new_value,ally=self.rVals:self.load_alliance(teams=new_value,ally=ally))
        self.rAllianceOM.config(width=15)
        self.rAllianceOM.pack(side=TOP,padx=5,pady=5)
        
        # create a frame to put the OptionMenu in
        self.bOptionFrame = Frame(self.blueAlliance)
        self.bOptionFrame.pack(side=LEFT)

        self.label = Label(self.bOptionFrame,text="Blue Alliance:")
        self.label.pack(side=TOP,padx=5,pady=5)

        # create the blue alliance OptionMenu
        self.bAllChoiceVar = StringVar(self.bOptionFrame)
        self.bAllChoiceVar.set("Custom")
        self.bAllianceOM = OptionMenu(self.bOptionFrame, self.bAllChoiceVar, *self.controller.allianceOptions,
                                      command=lambda new_value,ally=self.bVals:self.load_alliance(teams=new_value,ally=ally))
        self.bAllianceOM.config(width=15)
        self.bAllianceOM.pack(side=TOP,padx=5,pady=5)

        # will eventually allow to save user alliances with custom names

    def create_AllianceTeamEntries(self):
        # Red Alliance
        # create a frame to put the team entries in
        self.rTeams = Frame(self.redAlliance)
        self.rTeams.pack(side=LEFT,padx=5)

        self.label = Label(self.rTeams,text="Team")
        self.label.pack(side=TOP)
        # create the team entries
        for i in xrange(0,3):
            self.EntryVar = StringVar()
            self.EntryVar.set("0")
            self.rVals[i].append(self.EntryVar)
            self.TeamEntry = Entry(self.rTeams,textvariable=self.EntryVar,
                                   width=4,readonlybackground="lightgreen",takefocus=True)
            self.rTeamEntries.append(self.TeamEntry)
            self.TeamEntry.bind("<Return>",
                                lambda event, value=self.rVals,index=i:self.load_team(event,teamVals=value,index=index))
            self.TeamEntry.pack(side=TOP,pady=5)

        # Blue Alliance
        # create a frame to put the team entries in
        self.bTeams = Frame(self.blueAlliance)
        self.bTeams.pack(side=LEFT,padx=5)

        self.label = Label(self.bTeams,text="Team")
        self.label.pack(side=TOP)
        # create the team entries
        for i in xrange(0,3):
            self.EntryVar = StringVar()
            self.EntryVar.set("0")
            self.bVals[i].append(self.EntryVar)
            self.TeamEntry = Entry(self.bTeams,textvariable=self.EntryVar,
                                   width=4,readonlybackground="lightgreen",takefocus=True)
            self.bTeamEntries.append(self.TeamEntry)
            self.TeamEntry.bind("<Return>",
                                lambda event, value=self.bVals,index=i:self.load_team(event,teamVals=value,index=index))
            self.TeamEntry.pack(side=TOP,pady=5)

    def create_AllianceInformation(self):
        # Red Alliance
        for x, y in self.controller.predictIndex:
            self.nextFrame = Frame(self.redAlliance)
            self.nextFrame.pack(side=LEFT,padx=5)

            self.label = Label(self.nextFrame,text=y)
            self.label.pack(side=TOP)
            for i in xrange(0,3):
                self.EntryVar = StringVar()
                self.EntryVar.set("0")
                self.rVals[i].append(self.EntryVar)
                self.InfoEntry = Entry(self.nextFrame,textvariable=self.EntryVar,
                                       width=8,readonlybackground="lightgreen",
                                       state="readonly",takefocus=False)
                self.InfoEntry.pack(side=TOP,pady=5)

        # Blue Alliance
        for x, y in self.controller.predictIndex:
            self.nextFrame = Frame(self.blueAlliance)
            self.nextFrame.pack(side=LEFT,padx=5)

            self.label = Label(self.nextFrame,text=y)
            self.label.pack(side=TOP)
            for i in xrange(0,3):
                self.EntryVar = StringVar()
                self.EntryVar.set("0")
                self.bVals[i].append(self.EntryVar)
                self.InfoEntry = Entry(self.nextFrame,textvariable=self.EntryVar,
                                       width=8,readonlybackground="lightgreen",
                                       state="readonly",takefocus=False)
                self.InfoEntry.pack(side=TOP,pady=5)

    def create_ScoreLabels(self):
        # Red Alliance
        self.rOffScore = StringVar()
        self.rOffScore.set("Expected Offensive Score: N/A")

        self.rOffLabel = Label(self.redPrediction, textvariable=self.rOffScore,anchor=W)
        self.rOffLabel.pack(side=TOP,pady=5)

        # Blue Alliance
        self.bOffScore = StringVar()
        self.bOffScore.set("Expected Offensive Score: N/A")

        self.bOffLabel = Label(self.bluePrediction, textvariable=self.bOffScore,anchor=W)
        self.bOffLabel.pack(side=TOP,pady=5)
        
    def startup(self):
        
        self.redAlliance = Frame(self,relief=RAISED,bd=2)
        self.redAlliance.pack(side=TOP,padx=30,pady=15)

        self.redPrediction = Frame(self)
        self.redPrediction.pack(side=TOP,padx=45,pady=15)
        
        self.blueAlliance = Frame(self,relief=RAISED,bd=2)
        self.blueAlliance.pack(side=TOP,padx=30,pady=15)
        
        self.bluePrediction = Frame(self)
        self.bluePrediction.pack(side=TOP,padx=45,pady=15)

        self.create_AllianceOptions()
        self.create_AllianceTeamEntries()
        self.create_AllianceInformation()
        self.create_ScoreLabels()

        self.predictFrame = Frame(self)
        self.predictFrame.pack(side=BOTTOM)

        self.outcomeVar = StringVar()
        self.outcomeVar.set("N/A")
        self.predictLabel = Label(self.predictFrame,textvariable=self.outcomeVar, font=("Times","18"))
        self.predictLabel.pack(side=LEFT,padx=5,pady=5)
        self.predictButton = Button(self.predictFrame, text="Predict Match Outcome", font=("Times","18"),
                                    command=self.predict_alliances)
        self.predictButton.bind("<Return>",
                                lambda event:self.predict_alliances())
        self.clearButton = Button(self.predictFrame, text="Clear Prediction", font=("Times","18"),
                                  command=self.clear_predict)
        self.clearButton.pack(side=RIGHT,padx=5,pady=5)
        self.predictButton.pack(side=RIGHT,padx=5,pady=5)

    def __init__(self, parent=None, grandParent=None, controller=None):
        self.parent = parent
        self.grandParent = grandParent
        self.controller = controller
        self.rVals = [[],[],[]]
        self.bVals = [[],[],[]]
        self.rTeamEntries = []
        self.bTeamEntries = []

        self.parent.title("Predict")

        Frame.__init__(self,parent)
        self.pack()

        self.startup()
