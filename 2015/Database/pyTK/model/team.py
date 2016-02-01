#------------------------------------------------------------------------------
# team Module
#   -- Keeps track of valuable team information and scorings
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# TeamInfo Class
#   -- Stores performance information
#------------------------------------------------------------------------------
class _TeamInfo(object):
    """Used to handle information for different teams."""

    def __init__(self):
        self.matches = []                   # list holding the matches the team was in
        self.noShow = 0                     # number of matches for which the team didn't show up
        
        self.autoHadAuto = 0                # number of matches for which the team had autonomous
        self.autoTotesToZone = []           # list containing number of totes brought to zone during auto
        self.autoContainersToZone = []      # list containing number of containers brought to zone during auto
        self.autoContainersFromStep = []    # list containing number of containers received from step during auto
        self.autoTotesFromStep = []         # list containing the number of totes taken from the step during auto
        self.autoStackTotalTotes = []       # list containing number of total totes in the auto stack made by this robot
        self.autoEndInZone = 0              # number of matches for which the team ended in the auto zone
        self.autoOther = 0                  # number of matches for which the team did something else in auto

        self.teleStackTotes = []            # list containing the average number of totes in each stack for tele
        self.teleStepStackTotes = []        # list containing the average number of totes in each stepstack for tele
        self.teleStackHeights = []          # list containing the average max height of each stack for tele
        self.teleStepStackHeights = []        # list containing the average max height of each step stack for tele
        self.teleStackContainers = []       # list containing the average number of stacks having containers for each match
        self.teleStackContainerHeights = [] # list containing the average number of container heights for each step match
        self.teleStackLitter = []           # list containing the average number of containers having litter for each match 
        self.teleStackKnockedOver = []      # list containing the average number of knocked over stacks for each stack in tele
        self.teleStepStackKnockedOver = []  # list containing the average number of knocked over stacks for each step stack in tele
        self.teleStacksScored = []          # list containing the number of stacks scored each match
        self.teleStepStacksScored = []      # list containing the number of step stacks scored each match
        self.teleTotesFromChute = []        # list containing the number of totes received from the chute each match
        self.teleLitterFromChute = []       # list containing the number of litter received from the chute each match
        self.teleTotesFromLandfill = []     # list containing the number of totes received from the landfill each match
        self.teleLitterToLandfill = []      # list containing the number of litter pushed to the landfill zone each match

        self.postFouls = []                 # list containing the number of fouls each match
        self.postRedCard = 0                # number of matches for which robot received red card
        self.postYellowCard = 0             # number of matches for which robot received yellow card
        self.postDisabled = 0               # number of matches for which robot was disabled

        self.scoredInTele = 0               # number of matches for which the robot scored in tele-op
        self.scoredInAuto = 0               # number of matches for which the robot scored in auto
        self.hasFoul = 0                    # number of matches for which the robot received a foul

    def get_info(self):
        self.avgAutoTotesToZone = float(sum(self.autoTotesToZone))/float(len(self.autoTotesToZone)) if len(self.autoTotesToZone) else 0
        self.avgAutoContainersToZone = float(sum(self.autoContainersToZone))/float(len(self.autoContainersToZone)) if len(self.autoContainersToZone) else 0
        self.avgAutoContainersFromStep = float(sum(self.autoContainersFromStep))/float(len(self.autoContainersFromStep)) if len(self.autoContainersFromStep) else 0
        self.avgAutoTotesFromStep = float(sum(self.autoTotesFromStep))/float(len(self.autoTotesFromStep)) if len(self.autoTotesFromStep) else 0
        self.avgAutoStackTotalTotes = float(sum(self.autoStackTotalTotes))/float(len(self.autoStackTotalTotes)) if len(self.autoStackTotalTotes) else 0

        self.avgTeleStackTotes = float(sum(self.teleStackTotes))/float(len(self.teleStackTotes)) if len(self.teleStackTotes) else 0
        self.avgTeleStepStackTotes = float(sum(self.teleStepStackTotes))/float(len(self.teleStepStackTotes)) if len(self.teleStepStackTotes) else 0
        self.avgTeleStackHeights = float(sum(self.teleStackHeights))/float(len(self.teleStackHeights)) if len(self.teleStackHeights) else 0
        self.avgTeleStepStackHeights = float(sum(self.teleStepStackHeights))/float(len(self.teleStepStackHeights)) if len(self.teleStepStackHeights) else 0
        self.avgTeleStackContainers = float(sum(self.teleStackContainers))/float(len(self.teleStackContainers)) if len(self.teleStackContainers) else 0
        self.avgTeleStackContainerHeights = float(sum(self.teleStackContainerHeights))/float(len(self.teleStackContainerHeights)) if (self.teleStackContainerHeights) else 0
        self.avgTeleStackLitter = float(sum(self.teleStackLitter))/float(len(self.teleStackLitter)) if len(self.teleStackLitter) else 0
        self.avgTeleStackKnockedOver = float(sum(self.teleStackKnockedOver))/float(len(self.teleStackKnockedOver)) if len(self.teleStackKnockedOver) else 0
        self.avgTeleStepStackKnockedOver = float(sum(self.teleStepStackKnockedOver))/float(len(self.teleStepStackKnockedOver)) if len(self.teleStepStackKnockedOver) else 0
        self.avgTeleStacksScored = float(sum(self.teleStacksScored))/float(len(self.teleStacksScored)) if len(self.teleStacksScored) else 0
        self.avgTeleStepStacksScored = float(sum(self.teleStepStacksScored))/float(len(self.teleStepStacksScored)) if len(self.teleStepStacksScored) else 0
        self.avgTeleTotesFromChute = float(sum(self.teleTotesFromChute))/float(len(self.teleTotesFromChute)) if len(self.teleTotesFromChute) else 0
        self.avgTeleLitterFromChute = float(sum(self.teleLitterFromChute))/float(len(self.teleLitterFromChute)) if len(self.teleLitterFromChute) else 0
        self.avgTeleTotesFromLandfill = float(sum(self.teleTotesFromLandfill))/float(len(self.teleTotesFromLandfill)) if len(self.teleTotesFromLandfill) else 0
        self.avgTeleLitterToLandfill = float(sum(self.teleLitterToLandfill))/float(len(self.teleLitterToLandfill)) if len(self.teleLitterToLandfill) else 0
        
        self.avgPostFoul = sum(self.postFouls)/len(self.postFouls) if len(self.postFouls) else 0
                
    def getAttr(self, source):
        return getattr(self, source)

#------------------------------------------------------------------------------
# TeamScores Class
#   -- stores data about a team's scores
#------------------------------------------------------------------------------
class _TeamScores(object):
    """Used to handle scoring data for different teams."""

    def __init__(self):
        self.oScores = []               # list holding offensive scores
        self.tScores = []               # list holding total scores
        self.autoScores = []            # list holding auto scores
        self.autoStackScores = []       # list holding auto stack scores
        self.autoContainerScores = []   # list holding auto container scores
        self.autoRobotScores = []       # list holding auto robot scores
        self.teleScores = []            # list holding tele scores
        self.teleToteScores = []        # list holding tele totes scores
        self.teleContainerScores = []   # list holding tele container scores
        self.teleLitterScores = []      # list holding tele litter scores
        self.foulScores = []            # list holding foul scores
        
    def get_maxmin_scores(self):
        self.maxOffScore = max(self.oScores)
        self.minOffScore = min(self.oScores)
        self.maxTotalScore = max(self.tScores)
        self.minTotalScore = min(self.tScores)
        self.maxAutoScore = max(self.autoScores)
        self.minAutoScore = min(self.autoScores)
        self.maxAutoStackScore = max(self.autoStackScores)
        self.minAutoStackScore = min(self.autoStackScores)
        self.maxAutoContainerScore = max(self.autoContainerScores)
        self.minAutoContainerScore = min(self.autoContainerScores)
        self.maxAutoRobotScore = max(self.autoRobotScores)
        self.minAutoRobotScore = min(self.autoRobotScores)
        self.maxTeleScore = max(self.teleScores)
        self.minTeleScore = min(self.teleScores)
        self.maxTeleToteScore = max(self.teleToteScores)
        self.minTeleToteScore = min(self.teleToteScores)
        self.maxTeleContainerScore = max(self.teleContainerScores)
        self.minTeleContainerScore = min(self.teleContainerScores)
        self.maxTeleLitterScore = max(self.teleLitterScores)
        self.minTeleLitterScore = min(self.teleLitterScores)
        self.maxFoulScore = max(self.foulScores)
        self.minFoulScore = min(self.foulScores)

    def get_avg_scores(self, matches=1, auto=0):
        self.avgOffScore = sum(self.oScores)/matches if matches else 0
        self.avgAutoScore = sum(self.autoScores)/auto if auto else 0
        self.avgAutoStackScore = sum(self.autoStackScores)/auto if auto else 0
        self.avgAutoContainerScore = sum(self.autoContainerScores)/auto if auto else 0
        self.avgAutoRobotScore = sum(self.autoRobotScores)/auto if auto else 0
        self.avgTeleScore = sum(self.teleScores)/matches if matches else 0
        self.avgTeleToteScore = sum(self.teleToteScores)/matches if matches else 0
        self.avgTeleContainerScore = sum(self.teleContainerScores)/matches if matches else 0
        self.avgTeleLitterScore = sum(self.teleLitterScores)/matches if matches else 0
        self.avgFoulScore = sum(self.foulScores)/matches if matches else 0
        self.avgTotalScore = sum(self.tScores)/matches if matches else 0

    def getAttr(self, source):
        return getattr(self, source)

#------------------------------------------------------------------------------
# TeamRankings class
#   -- place to store ranking lists, for viewing team ranks
#------------------------------------------------------------------------------
class TeamRankings(object):
    """Used to keep track of rankings for each team."""

    off_rank = []
    auto_rank = []
    auto_stack_rank = []
    auto_container_rank = []
    auto_robot_rank = []
    tele_rank = []
    tele_tote_rank = []
    tele_container_rank = []
    tele_litter_rank = []
    foul_rank = []
    tot_rank = []
    
    def __init__(self):
        print
        # no non-static class variables
        # team cannot track its own ranking:
            # rankings are defined by the user
            # rankings are dynamic, constantly changing to user request

    def getAttr(self, source):
        return getattr(self, source)

#------------------------------------------------------------------------------
# Team Class
#   -- stores and recalls team specific data
#------------------------------------------------------------------------------
class Team(object):
    """Store and recall data on a team from here."""

    team_list = []  # list holding all the teams currently loaded in the database
    available = []  # list holding all the teams not currently selected
    wanted = []     # list holding all the teams in our wanted list
    
    def __init__(self, num):
        self.number = num
        self.Info = _TeamInfo()
        self.Scores = _TeamScores()
        self.team_list.append(self)
        self.available.append(self)

        # a few of the final details predefined so as to satisfy predictions with null teams
        self.avgOff = 0
        self.pOff = 0
        
    def get_details(self): # gets all of the information for the team
        self.Info.get_info()
        self.Scores.get_avg_scores(len(self.Info.matches),self.Info.autoHadAuto)
        self.Scores.get_maxmin_scores()

        matches = self.Info.matches
        self.numMatch = len(matches)
        self.pNoShow  = str(int(100*self.Info.noShow)/len(matches)) + "%"
        self.pDisabled = str(int(100*self.Info.postDisabled)/len(matches)) + "%"
        self.avgOff = round(self.Scores.avgOffScore,2)
        self.avgTotal = round(self.Scores.avgTotalScore,2)

        self.pHadAuto = str(int(100*self.Info.autoHadAuto)/len(matches)) + "%"
        self.avgAutoScore = round(self.Scores.avgAutoScore,2)
        self.avgAutoStackScore = round(self.Scores.avgAutoStackScore,2)
        self.avgAutoContainerScore = round(self.Scores.avgAutoContainerScore,2)
        self.avgAutoRobotScore = round(self.Scores.avgAutoRobotScore,2)
        self.avgAutoTotesToZone = round(self.Info.avgAutoTotesToZone,2)
        self.avgAutoContainersToZone = round(self.Info.avgAutoContainersToZone,2)
        self.avgAutoContainersFromStep = round(self.Info.avgAutoContainersFromStep,2)
        self.avgAutoTotesFromStep = round(self.Info.avgAutoTotesFromStep,2)
        self.avgAutoStackTotalTotes = round(self.Info.avgAutoStackTotalTotes,2)
        self.pEndInAuto = str(int(100*self.Info.autoEndInZone)/len(matches)) + "%"
        self.pAutoOther = str(int(100*self.Info.autoOther)/len(matches)) + "%"
        
        self.avgTeleScore = round(self.Scores.avgTeleScore,2)
        self.avgTeleToteScore = round(self.Scores.avgTeleToteScore,2)
        self.avgTeleContainerScore = round(self.Scores.avgTeleContainerScore,2)
        self.avgTeleLitterScore = round(self.Scores.avgTeleLitterScore,2)
        self.avgTeleStackTotes = round(self.Info.avgTeleStackTotes,2)
        self.avgTeleStepStackTotes = round(self.Info.avgTeleStepStackTotes,2)
        self.avgTeleStackHeights = round(self.Info.avgTeleStackHeights,2)
        self.avgTeleStepStackHeights = round(self.Info.avgTeleStepStackHeights,2)
        self.avgTeleStackContainers = round(self.Info.avgTeleStackContainers,2)
        self.avgTeleStackContainerHeights = round(self.Info.avgTeleStackContainerHeights,2)
        self.avgTeleStackLitter = round(self.Info.avgTeleStackLitter,2)
        self.avgTeleStackKnockedOver = round(self.Info.avgTeleStackKnockedOver,2)
        self.avgTeleStepStackKnockedOver = round(self.Info.avgTeleStepStackKnockedOver,2)
        self.avgTeleStacksScored = round(self.Info.avgTeleStacksScored,2)
        self.avgTeleStepStacksScored = round(self.Info.avgTeleStepStacksScored,2)
        self.avgTeleTotesFromChute = round(self.Info.avgTeleTotesFromChute,2)
        self.avgTeleLitterFromChute = round(self.Info.avgTeleLitterFromChute,2)
        self.avgTeleTotesFromLandfill = round(self.Info.avgTeleTotesFromLandfill,2)
        self.avgTeleLitterToLandfill = round(self.Info.avgTeleLitterToLandfill,2)

        self.avgFoulScore = round(self.Scores.avgFoulScore,2)
        self.avgPostFoul = round(self.Info.avgPostFoul,2)
        self.pFoul = str(int(100*self.Info.hasFoul)/len(matches)) + "%"
        self.pYellow = str(int(100*self.Info.postYellowCard)/len(matches)) + "%"
        self.pRed = str(int(100*self.Info.postRedCard)/len(matches)) + "%"

    def getAttr(self, source):
        return getattr(self, source)
