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

    entryItemTypes = [("avgOff","Offensive Score >= "),("avgDef","Defensive Score >= "),
                        ("avgAst","Assistive Score >= "),("avgTotal","Total Score >= "),
                        ("WeightedOff","Weighted Offensive Score >= "),
                        ("WeightedDef","Weighted Defensive Score >= "),
                        ("WeightedAst","Weighted Assistive Score >= "),
                        ("WeightedTotal","Weighted Total Score >= "),
                        ("avgAutoScore","Auto Score >= "),("avgTeleScore","Tele Score >= "),
                        ("avgFoulScore","Foul Score >= ")]
    
    checkItemTypes = [("numOff","Played Offensive"),("numDef","Played Defensive"),("numAst","Played Assistive"),
                    ("autoHadAuto","Had Autonomous"),("autoScoredAuto","Scored in Autonomous"),
                    ("autoGoalieZone","Started in Goalie Zone"),("autoMobilityBonus","Obtained Mobility Bonus"),
                    ("teleScoredTele","Scored in Tele"),("teleScoredHigh","Scored in High Goal (Tele-Op)"),
                    ("teleScoredTruss","Shot over the Truss"),("teleCaught","Caught a Ball"),
                    ("postDisabled","Never Disabled"),("postNoShow","Always Showed Up"),
                    ("postHadRegFoul","No Regular Fouls"),("postHadTechFoul","No Technical Fouls"),
                    ("postHadYellow","No Yellow Cards"),("postHadRed","No Red Cards")]
                    
    def searchGreater(self, value=None, index=None):
        try:
            self.matchedList = filter(lambda team:team.getAttr(index)>=int(value.get()), self.matchedList)
        except:
             print "Invalid Search Parameter " + str(value.get()) + " for " + str(index)
             value.set(0)

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

    
    Searches = {"avgOff":searchGreater,"avgDef":searchGreater,
                "avgAst":searchGreater,"avgTotal":searchGreater,
                "WeightedOff":searchGreater,"WeightedDef":searchGreater,
                "WeightedAst":searchGreater,"WeightedTotal":searchGreater,
                "avgAutoScore":searchGreater,"avgTeleScore":searchGreater,
                "avgFoulScore":searchGreater,
                "numOff":searchHas,"numDef":searchHas,"numAst":searchHas,
                "autoHadAuto":searchHas,"autoScoredAuto":searchHas,
                "autoGoalieZone":searchHas,"autoMobilityBonus":searchHas,
                "teleScoredTele":searchHas,"teleScoredHigh":searchHas,
                "teleScoredTruss":searchHas,"teleCaught":searchHas,
                "postDisabled":searchNever,"postNoShow":searchNever,
                "postHadRegFoul":searchNever,"postHadTechFoul":searchNever,
                "postHadYellow":searchNever,"postHadRed":searchNever}

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
        
