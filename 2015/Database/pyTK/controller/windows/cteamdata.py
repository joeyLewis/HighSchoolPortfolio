#------------------------------------------------------------------------------
# cteamdata module
#   -- contains the functions and classes for controlling the teamdata window
#------------------------------------------------------------------------------
from Tkinter import *

from model.team import *

#------------------------------------------------------------------------------
# TeamDataController Class
#   -- contains information for setting and getting data and display values
#------------------------------------------------------------------------------
class TeamDataController():
    """Class that handles commands from the teamdata window."""

    # use these to index values to display, use the system: ("key", "term")
    # where key corresponds to a value in team and term labels that value
    dataLabelVals = [("numMatch","Number of Matches: "),
                     ("pNoShow","No Show: "),
                     ("pDisabled","Disabled: "),
                     ("avgOff","Average Offensive Score: "),
                     ("avgTotal","Average Total Score: "),
                     ("pHadAuto","Had Auto Mode: "),
                     ("avgAutoScore","Average Auto Score: "),
                     ("avgAutoStackScore","Average Auto Tote + Stack Set Score: "),
                     ("avgAutoContainerScore","Average Auto Container Set Score: "),
                     ("avgAutoRobotScore","Average Auto Robot Set Score: "),
                     ("avgAutoTotesToZone","Average Number of Auto Totes Brought to Zone: "),
                     ("avgAutoContainersToZone","Average Number of Containers Brought to Zone: "),
                     ("avgAutoContainersFromStep","Average Number of Containers Taken Off the Step in Auto: "),
                     ("avgAutoTotesFromStep","Average Number of Totes Taken From the Step in Auto: "),
                     ("avgAutoStackTotalTotes","Average Number of Totes Contributed to Auto Stack: "),
                     ("pEndInAuto","Ended Autonomous in the Auto Zone: "),
                     ("pAutoOther","Had Other Autonomous: "),
                     ("avgTeleScore","Average Tele Score: "),
                     ("avgTeleToteScore","Average Tele Tote-Stacking Score: "),
                     ("avgTeleContainerScore","Average Tele Container-Stacking Score: "),
                     ("avgTeleLitterScore","Average Tele Litter-Stacking and Pushing Score: "),
                     ("avgTeleStackTotes","Average Number of Totes Stacked per Match: "),
                     ("avgTeleStepStackTotes","Average Number of Step-Stack Totes Stacked per Match: "),
                     ("avgTeleStackHeights","Average Height of Top-Contributed Tote in Stacks: "),
                     ("avgTeleStepStackHeights","Average Height of Top-Contributed Tote in Coop Stacks: "),
                     ("avgTeleStackContainers","Average Number of Containers Stacked per Match: "),
                     ("avgTeleStackContainerHeights","Average Level of Container: "),
                     ("avgTeleStackLitter","Average Litter Scored in Containers: "),
                     ("avgTeleStackKnockedOver","Average Number of Stacks Knocked Over: "),
                     ("avgTeleStepStackKnockedOver","Average Number of Coop-Stacks Knocked Over: "),
                     ("avgTeleStacksScored","Average Number of Stacks Scored: "),
                     ("avgTeleStepStacksScored","Average Number of Coop-Stacks Scored: "),
                     ("avgTeleTotesFromChute","Average Number of Totes Received from Chute: "),
                     ("avgTeleLitterFromChute","Average Number of Litter Received from Chute: "),
                     ("avgTeleTotesFromLandfill","Average Number of Totes Taken from the Landfill: "),
                     ("avgTeleLitterToLandfill","Average Number of Litter Pushed to the Landfill Zone: "),
                     ("avgFoulScore","Average Foul Score: "),
                     ("avgPostFoul","Average Number of Fouls: "),
                     ("pFoul","Matches Received Foul In: "),
                     ("pYellow","Received Yellow Card: "),
                     ("pRed","Received Red Card: ")]

    maxminLabelVals = [("maxOffScore","Maximum Offensive Score: "),("minOffScore","Minimum Offensive Score: "),
                       ("maxTotalScore","Maximum Total Score: "),("minTotalScore","Minimum Total Score: "),
                       ("maxAutoScore","Maximum Auto Score: "),("minAutoScore","Minimum Auto Score: "),
                       ("maxAutoStackScore","Maximum Auto Tote + Stack Set Score: "),("minAutoStackScore","Minimum Auto Tote + Stack Set Score: "),
                       ("maxAutoContainerScore","Maximum Auto Container Set Score: "),("minAutoContainerScore","Minimum Auto Container Set Score: "),
                       ("maxAutoRobotScore","Maximum Auto Robot Set Score: "),("minAutoRobotScore","Minimum Auto Robot Set Score: "),
                       ("maxTeleScore","Maximum Tele Score: "),("minTeleScore","Minimum Tele Score: "),
                       ("maxTeleToteScore","Maximum Tele Tote-Stacking Score"),("minTeleToteScore","Minimum Tele Tote-Stacking Score"),
                       ("maxTeleContainerScore","Maximum Tele Container-Stacking Score: "),("minTeleContainerScore","Minimum Tele Container-Stacking Score: "),
                       ("maxTeleLitterScore","Maximum Tele Litter-Stacking and Pushing Score: "),("minTeleLitterScore","Minimum Tele Litter-Stacking and Pushing Score: "),
                       ("maxFoulScore","Maximum Foul Score: "),("minFoulScore","Minimum Foul Score: ")]

    graphVals = [("avgOff","Scores","oScores"),
                 ("avgTotal","Scores","tScores"),
                 ("avgAutoScore","Scores","autoScores"),
                 ("avgAutoStackScore","Scores","autoStackScores"),
                 ("avgAutoContainerScore","Scores","autoContainerScores"),
                 ("avgAutoRobotScore","Scores","autoRobotScores"),
                 ("avgAutoTotesToZone","Info","autoTotesToZone"),
                 ("avgAutoContainersToZone","Info","autoContainersToZone"),
                 ("avgAutoContainersKnockedOver","Info","autoContainersKnockedOver"),
                 ("avgAutoContainersFromStep","Info","autoContainersKnockedOver"),
                 ("avgAutoTotesFromLandfill","Info","autoTotesFromLandfill"),
                 ("avgAutoTotesFromStep","Info","autoTotesFromStep"),
                 ("avgAutoTotesStacked","Info","autoTotesStacked"),
                 ("avgAutoStackTotalTotes","Info","autoStackTotalTotes"),
                 ("avgTeleScore","Scores","teleScores"),
                 ("avgTeleToteScore","Scores","teleToteScores"),
                 ("avgTeleContainerScore","Scores","teleContainerScores"),
                 ("avgTeleLitterScore","Scores","teleLitterScores"),
                 ("avgTeleStackTotes","Info","teleStackTotes"),
                 ("avgTeleStepStackTotes","Info","teleStepStackTotes"),
                 ("avgTeleStackHeights","Info","teleStackHeights"),
                 ("avgTeleStepStackHeights","Info","teleStepStackHeights"),
                 ("avgTeleStackContainers","Info","teleStackContainers"),
                 ("avgTeleStackContainerHeights","Info","teleStackContainerHeights"),
                 ("avgTeleStackLitter","Info","teleStackLitter"),
                 ("avgTeleStackKnockedOver","Info","teleStackKnockedOver"),
                 ("avgTeleStepStackKnockedOver","Info","teleStepStackKnockedOver"),
                 ("avgTeleStacksScored","Info","teleStacksScored"),
                 ("avgTeleStepStacksScored","Info","teleStepStacksScored"),
                 ("avgTeleTotesFromChute","Info","teleTotesFromChute"),
                 ("avgTeleLitterFromChute","Info","teleLitterFromChute"),
                 ("avgTeleTotesFromLandfill","Info","teleTotesFromLandfill"),
                 ("avgTeleLitterToLandfill","Info","teleLitterToLandfill"),
                 ("avgFoulScore","Scores","foulScores"),
                 ("avgPostFoul","Info","postFouls")]
    
    def __init__(self):
        self.teamNum = 0
        self.entry = None
        self.data = None
        self.image = None

    # gets the team # from self.entry and finds the corresponding team
    # returns true if the team was found and false if not
    def loadData(self):
        try:
            self.teamNum = int(self.entry.get())
        except:
            print "Team value not valid."
            self.teamNum = 0
            
        for team in Team.team_list:
            if team.number == self.teamNum:
                self.data = team
                print "Loading team..."
                return True
            
        print "Team not found."
        return False

    # gets the image file corresponding to self.teamNum and returns it
    # if team is not found: returns nopic.gif
    def get_PhotoImage(self):
        image_name = "Images/" + str(self.teamNum) + ".gif"
        try:
            open(image_name)
        except:
            self.image = PhotoImage(file="Images/nopic.gif")
            return self.image
        
        self.image = PhotoImage(file=image_name)
        return self.image

    def get_GraphData(self, graphType=None):
        index = None
        data = None
        try:
            graphName = self.dataLabelVals[int(graphType[0])][0]  
        except:
            graphName = None

        #find the index and attr name
        for x, y, z in self.graphVals:
            if x == graphName:
                index = y
                data = z
                break # do not continue to iterate through the list
        try:
            currentIndex = self.data.getAttr(index)
            return currentIndex.getAttr(data)
        except:
            print "Cannot find data for that graph."
            return None
