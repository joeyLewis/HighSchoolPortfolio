#------------------------------------------------------------------------------
# csearch module
#   -- contains data and information for controlling the search window
#------------------------------------------------------------------------------
from Tkinter import *

from model import team

#------------------------------------------------------------------------------
# SearchController class
#   -- contains functions, lists, data, etc, for handling the search window
#------------------------------------------------------------------------------
class SearchController():
    """Class that handles commands from the search window."""

    entryItemGenAuto = [("avgOff","Offensive Score >= "),
                        ("avgTotal","Total Score >= "),
                        ("avgAutoScore","Auto Score >= "),
                        ("avgAutoStackScore","Auto Tote-Stack Set Score >= "),
                        ("avgAutoContainerScore","Auto Container Set Score >= "),
                        ("avgAutoRobotScore","Auto Robot Set Score >= "),
                        ("avgAutoTotesToZone","Auto Totes Brought to Zone >= "),
                        ("avgAutoContainersToZone","Auto Containers Brought to Zone >= "),
                        ("avgAutoContainersFromStep","Auto Containers Taken From Step >= "),
                        ("avgAutoTotesFromStep","Auto Totes Taken From Step >= "),
                        ("avgAutoStackTotalTotes","Auto Totes Contribued to Stack >= ")]

    entryItemTelePost = [("avgTeleScore","Tele Score >= "),
                         ("avgTeleToteScore","Tele Tote Score >= "),
                         ("avgTeleContainerScore","Tele Container Score >= "),
                         ("avgTeleLitterScore","Tele Litter Score >= "),
                         ("avgTeleStackTotes","Number of Totes Stacked per Match >= "),
                         ("avgTeleStepStackTotes","Number of Coop-Totes Stacked per Match >= "),
                         ("avgTeleStackHeights","Highest Tote Avg >= "),
                         ("avgTeleStepStackHeights","Highest Coop-Tote Avg >= "),
                         ("avgTeleStackContainers","Number of Containers Stacked per Match >= "),
                         ("avgTeleStackContainerHeights","Container Stack Level Avg >= "),
                         ("avgTeleStackLitter","Number of Litter Scored per Match >= "),
                         ("avgTeleStackKnockedOver","Number of Stacks Knocked Over <= "),
                         ("avgTeleStepStackKnockedOver","Number of Coop-Stacks Knocked Over <= "),
                         ("avgTeleStacksScored","Number of Stacks Scored per Match >= "),
                         ("avgTeleStepStacksScored","Number of Coop-Stacks Scored per Match >= "),
                         ("avgTeleTotesFromChute","Number of Totes Received from Chute per Match >= "),
                         ("avgTeleLitterFromChite","Number of Litter Received from Chute per Match >= "),
                         ("avgTeleTotesFromLandfill","Number of Totes Taken From Landfill per Match >= "),
                         ("avgTeleLitterToLandfill","Number of Litter Pushed to Landfill per Match >= "),
                         ("avgFoulScore","Foul Score <= ")]
    
    checkItemTypes = [("autoHadAuto","Had Autonomous"),
                      ("scoredInAuto","Scored in Autonomous"),
                      ("autoEndInZone","Ended Auto in Auto Zone"),
                      ("autoOther","Had Other Autonomous"),
                      ("scoredInTele","Scored in Tele"),
                      ("postNoShow","Always Showed Up"),
                      ("postDisabled","Never Disabled"),
                      ("hasFoul","No Fouls"),
                      ("postYellowCard","No Yellow Cards"),
                      ("postRedCard","No Red Cards")]
                    
    def searchGreater(self, value=None, index=None):
        try:
            self.matchedList = filter(lambda team:team.getAttr(index)>=int(value.get()), self.matchedList)
        except:
             print "Invalid Search Parameter " + str(value.get()) + " for " + str(index)
             value.set(0)

    def searchLess(self, value=None, index=None):
        try:
            self.matchedList = filter(lambda team:team.getAttr(index)<=int(value.get()), self.matchedList)
        except:
             print "Invalid Search Parameter " + str(value.get()) + " for " + str(index)
             value.set(999)

    def searchHas(self, value=None, index=None):
        try:
            if value.get() == 1:
                self.matchedList = filter(lambda team:team.Info.getAttr(index) >= 1, self.matchedList)
        except:
            value.set(0)

    def searchNever(self, value=None, index=None):
        try:
            if value.get() == 1:
                self.matchedList = filter(lambda team:team.Info.getAttr(index) == 0, self.matchedList)
        except:
            value.set(0)

    
    Searches = {"avgOff":searchGreater,
                "avgTotal":searchGreater,
                "avgAutoScore":searchGreater,
                "avgAutoStackScore":searchGreater,
                "avgAutoContainerScore":searchGreater,
                "avgAutoRobotScore":searchGreater,
                "avgAutoTotesToZone":searchGreater,
                "avgAutoContainersToZone":searchGreater,
                "avgAutoContainersFromStep":searchGreater,
                "avgAutoTotesFromStep":searchGreater,
                "avgAutoStackTotalTotes":searchGreater,
                "autoHadAuto":searchHas,
                "scoredInAuto":searchHas,
                "autoEndInZone":searchHas,
                "autoOther":searchHas,
                "avgTeleScore":searchGreater,
                "avgTeleToteScore":searchGreater,
                "avgTeleContainerScore":searchGreater,
                "avgTeleLitterScore":searchGreater,
                "avgTeleStackTotes":searchGreater,
                "avgTeleStepStackTotes":searchGreater,
                "avgTeleStackHeights":searchGreater,
                "avgTeleStepStackHeights":searchGreater,
                "avgTeleStackContainers":searchGreater,
                "avgTeleStackContainerHeights":searchGreater,
                "avgTeleStackLitter":searchGreater,
                "avgTeleStackKnockedOver":searchLess,
                "avgTeleStepStackKnockedOver":searchLess,
                "avgTeleStacksScored":searchGreater,
                "avgTeleStepStacksScored":searchGreater,
                "avgTeleTotesFromChute":searchGreater,
                "avgTeleLitterFromChute":searchGreater,
                "avgTeleTotesFromLandfill":searchGreater,
                "avgTeleLitterToLandfill":searchGreater,
                "scoredInTele":searchHas,
                "avgFoulScore":searchLess,
                "postDisabled":searchNever,
                "noShow":searchNever,
                "hasFoul":searchNever,
                "postHadYellow":searchNever,
                "postHadRed":searchNever}

    def search(self):
        self.matchedList = team.Team.team_list

        for index, value in self.searchVariables:
            if index in self.Searches:
                self.Searches[index](self,value,index)

    def addWanted(self,number=None):
        for t in team.Team.team_list:
            if t.number == int(number) and t not in team.Team.wanted:
                team.Team.wanted.append(t)
                break

        self.wantedList = team.Team.wanted

    def subWanted(self,number=None):
        for t in team.Team.wanted:
            if t.number == int(number):
                team.Team.wanted.remove(t)
                break

        self.wantedList = team.Team.wanted

    def sortWanted(self,rList=None):
        newList = []
        for item in rList:
            for t in team.Team.team_list:
                if t.number == int(item):
                    newList.append(t)
                    break
                    
        team.Team.wanted = newList
        self.wantedList = team.Team.wanted
        
    def __init__(self):
        self.matchedList = team.Team.team_list
        self.searchVariables = []
        self.wantedList = team.Team.wanted
        
