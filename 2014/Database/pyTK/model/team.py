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
        self.matches = []           # list holding the matches the team was in
        self.numOff = 0             # the number of matches for which the team played offensively
        self.numDef = 0             # the number of matches for which the team played defensively
        self.numAst = 0             # the number of matches for which the team played assistively
        
        self.autoHadAuto = 0        # the number of matches for which the team had an autonomous mode that did something
        self.autoMobilityBonus = 0  # the number of matches for which the team obtained the mobility bonus
        self.autoGoalieZone = 0     # the number of matches for which the team started in the goalie zone
        self.autoHighScored = []    # list holding the number of scores in the high goal in autonomous (by match)
        self.autoLowScored = []     # list holding the number of scores in the low goal in autonomous (by match)
        self.autoHotScored = []     # list holding the number of scores in a hot goal in autonomous (by match)
        self.autoScoredAuto = 0     # the number of matches for which the team scored in autonomous mode

        self.teleHadTele = 0        # the number of matches for which the robot scored in tele-op mode
        self.teleHighScored = []    # list holding the number of scores in the high goal in tele-op (by match)
        self.teleScoredHigh = 0     # the number of matches for which the team scored in the high goal (search field)
        self.teleLowScored = []     # list holding the number of scores in the high goal in tele-op (by match)
        self.teleTrussScored = []   # list holding the number of successful truss scores in tele-op (by match)
        self.teleScoredTruss = 0    # the number of matches for which the team scored in over the truss (search field)
        self.teleCatchScored = []   # list holding the number of successful catch scores in tele-op (by match)
        self.teleCaught = 0         # the number of matches for which the team caught a ball (search field)
        self.teleAssistScored = []  # list holding the number of successful assist scores in tele-op (by match)
        self.teleScoredTele = 0     # the number of matches for which the team scored (in a goal) in tele-op mode
        self.teleHotSpots = []      # list holding the hots spots for this team (by match)
        self.teleIntakeTimes = []   # list holding the average intake times for this team (by match)
        
        self.postRegFouls = []      # list holding the number of regular fouls for each match
        self.postTechFouls = []     # list holding the number of technical fouls for each match
        self.postHadRegFoul = 0     # the number of matches for which a team incurred a regular foul
        self.postHadTechFoul = 0    # the number of matches for which a team incurred a technical foul
        self.postDisabled = 0       # the number of matches in which a team was disabled
        self.postNoShow = 0         # the number of matches in which a team didn't show up to the field
        self.postHadYellow = 0      # the number of matches for which a team incurred a yellow card
        self.postHadRed = 0         # the number of matches for which a team incurred a red card
        self.postAggressive = 0     # the number of matches for which a team played aggressively

    def get_more_info(self):
        self.autoHotAccuracy = sum(self.autoHotScored)/(sum(self.autoHighScored)+sum(self.autoLowScored)) \
                                if (sum(self.autoHighScored)+sum(self.autoLowScored))>0 else 0
        self.totalTrussScores = sum(self.teleTrussScored)
        self.totalCatchScores = sum(self.teleCatchScored)
        self.totalAssistScores = sum(self.teleAssistScored)
        
    def get_final_info(self):
        self.avgAutoHighScored = sum(self.autoHighScored)/len(self.autoHighScored) if len(self.autoHighScored) else 0
        self.avgAutoLowScored = sum(self.autoLowScored)/len(self.autoLowScored) if len(self.autoLowScored) else 0
        self.avgAutoHotScored = sum(self.autoHotScored)/len(self.autoHotScored) if len(self.autoHotScored) else 0
        self.avgTeleHighScored = sum(self.teleHighScored)/len(self.teleHighScored) if len(self.teleHighScored) else 0
        self.avgTeleLowScored = sum(self.teleLowScored)/len(self.teleLowScored) if len(self.teleLowScored) else 0
        self.avgTeleTrussScored = sum(self.teleTrussScored)/len(self.teleTrussScored) if len(self.teleTrussScored) else 0
        self.avgTeleCatchScored = sum(self.teleCatchScored)/len(self.teleCatchScored) if len(self.teleCatchScored) else 0
        self.avgTeleAssistScored = sum(self.teleAssistScored)/len(self.teleAssistScored) if len(self.teleAssistScored) else 0
        self.avgTeleIntakeTimes = sum(self.teleIntakeTimes)/len(self.teleIntakeTimes) if len(self.teleIntakeTimes) else 0
        self.avgPostRegFoul = sum(self.postRegFouls)/len(self.postRegFouls) if len(self.postRegFouls) else 0
        self.avgPostTechFoul = sum(self.postTechFouls)/len(self.postTechFouls) if len(self.postTechFouls) else 0
        
    def getAttr(self, source):
        return getattr(self, source)

#------------------------------------------------------------------------------
# TeamScores Class
#   -- stores data about a team's scores
#------------------------------------------------------------------------------
class _TeamScores(object):
    """Used to handle scoring data for different teams."""

    def __init__(self):
        self.oScores = []           # list holding offensive scores
        self.dScores = []           # list holding defensive scores
        self.aScores = []           # list holding assistive scores
        self.tScores = []           # list holding total scores
        self.wScores = []           # list holding weighted  scores
        self.woScores = []          # list holding weighted offensive scores
        self.wdScores = []          # list holding weighted defensive scores
        self.waScores = []          # list holding weighted assistive scores
        self.autoScores = []        # list holding auto scores
        self.teleScores = []        # list holding tele scores
        self.foulScores = []        # list holding foul scores

    def get_maxmin_scores(self):
        self.maxOffScore = max(self.oScores)
        self.minOffScore = min(self.oScores)
        self.maxDefScore = max(self.dScores)
        self.minDefScore = min(self.dScores)
        self.maxAstScore = max(self.aScores)
        self.minAstScore = min(self.aScores)
        self.maxTotalScore = max(self.tScores)
        self.minTotalScore = min(self.tScores)
        self.maxWScore = max(self.wScores)
        self.minWScore = min(self.wScores)
        self.maxWOScore = max(self.woScores)
        self.minWOScore = min(self.woScores)
        self.maxWDScore = max(self.wdScores)
        self.minWDScore = min(self.wdScores)
        self.maxWAScore = max(self.waScores)
        self.minWAScore = min(self.waScores)
        self.maxAutoScore = max(self.autoScores)
        self.minAutoScore = min(self.autoScores)
        self.maxTeleScore = max(self.teleScores)
        self.minTeleScore = min(self.teleScores)
        self.maxFoulScore = max(self.foulScores)
        self.minFoulScore = min(self.foulScores)

    def get_avgOff_scores(self, matches=1, offensive=0, auto=0, tele=0):
        self.avgOffScore = sum(self.oScores)/matches if offensive else 0
        self.avgAutoScore = sum(self.autoScores)/auto if auto else 0
        self.avgTeleScore = sum(self.teleScores)/tele if tele else 0
        self.avgFoulScore = sum(self.foulScores)/matches if matches else 0

    def get_avgDefAst_scores(self, matches=1, defensive=0, assistive=0):
        self.avgDefScore = sum(self.dScores)/matches if defensive else 0
        self.avgAstScore = sum(self.aScores)/matches if assistive else 0

    def get_avgWeight_scores(self):
        self.avgTotalScore = sum(self.tScores)/len(self.tScores) if len(self.tScores) else 0
        self.avgWScore = sum(self.wScores)/len(self.wScores) if len(self.wScores) else 0
        self.avgWOScore = sum(self.woScores)/len(self.woScores) if len(self.woScores) else 0
        self.avgWDScore = sum(self.wdScores)/len(self.wdScores) if len(self.wdScores) else 0
        self.avgWAScore = sum(self.waScores)/len(self.waScores) if len(self.waScores) else 0

    def getAttr(self, source):
        return getattr(self, source)
        

#------------------------------------------------------------------------------
# TeamPitInfo Class
#   -- stores data unrelated to performance on the field
#------------------------------------------------------------------------------
class _TeamPitInfo(object):
    """Used to handle information about a teams chassis and other
       non-performance related information."""

    def __init__(self):
        self.robLength = 0          # the length of the robot's chassis
        self.robWidth= 0            # the width  of the robot's chassis
        self.robHeight = 0          # the height of the robot
        self.robWeight = 0          # the weight of the robot
        self.clearance = 0          # the distance to the floor from the bottom of the chassis
        self.wheelSpace = 0         # the spacing between the wheels width-wise
        self.driveSystem = ""       # what type of control the robot uses to drive
                                    # 0 = tank, 1 = arcade, 2 = swerve, 3 = crab, 4 = other
        self.shiftGear = ""         # if the robot has multiple gear drive
                                    # 0 = no, 1 = yes
        self.centerMass = ""        # the center of mass / gravity of the robot
                                    # 0 = low, 1 = mid, 2 = high
        self.driver1 = ""           # the robot's drive team
        self.exp1 = None            # the robot's drive team's experience(in competitions / years)
        self.driver2 = ""           # ''
        self.expe2 = None           # ''
        self.driver3 = ""           # ''
        self.exp3 = None            # ''

    def getAttr(self, source):
        return getattr(self, source)

#------------------------------------------------------------------------------
# TeamRankings class
#   -- place to store ranking lists, for viewing team ranks
#------------------------------------------------------------------------------
class TeamRankings(object):
    """Used to keep track of rankings for each team."""

    off_rank = []
    def_rank = []
    ast_rank = []
    tot_rank = []
    auto_rank = []
    tele_rank = []
    foul_rank = []
    w_rank = []
    wo_rank = []
    wd_rank = []
    wa_rank = []
    
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
        self.PitInfo = _TeamPitInfo()
        self.team_list.append(self)
        self.available.append(self)

        # a few of the final details predefined so as to satisfy predictions with null teams
        self.avgOff = 0
        self.avgDef = 0
        self.avgAst = 0
        self.pOff = 0
        self.pDef = 0
        self.pAst = 0
        
    def get_primary_details(self): # gets the offensive values of Team
        self.Info.get_more_info()
        self.Scores.get_avgOff_scores(len(self.Info.matches),
                                   self.Info.numOff,
                                   self.Info.autoHadAuto, self.Info.teleHadTele)

    def get_secondary_details(self): # gets the defensive and assistive values of the team
        self.Info.get_final_info()
        self.Scores.get_avgDefAst_scores(len(self.Info.matches),
                                         self.Info.numDef, self.Info.numAst)

    def get_tertiary_details(self): # gets the max and min scores, etc. of the team
        self.Scores.get_avgWeight_scores()
        self.Scores.get_maxmin_scores()

    def get_final_details(self): # gets the values to be displayed in the TeamData window
        matches = self.Info.matches
        self.numMatch = len(matches)
        self.pOff = str(int(100*self.Info.numOff)/len(matches)) + "%"
        self.pDef = str(int(100*self.Info.numDef)/len(matches)) + "%"
        self.pAst = str(int(100*self.Info.numAst)/len(matches)) + "%"
        self.avgOff = round(self.Scores.avgOffScore,2)
        self.avgDef = round(self.Scores.avgDefScore,2)
        self.avgAst = round(self.Scores.avgAstScore,2)
        self.avgTotal = round(self.Scores.avgTotalScore,2)
        self.WeightedOff = round(self.Scores.avgWOScore,2)
        self.WeightedDef = round(self.Scores.avgWDScore,2)
        self.WeightedAst = round(self.Scores.avgWAScore,2)
        self.WeightedTotal = round(self.Scores.avgWScore,2)

        self.pHadAuto = str(int(100*self.Info.autoHadAuto)/len(matches)) + "%"
        self.pMobilityBonus = str(int(100*self.Info.autoMobilityBonus)/len(matches)) + "%"
        self.pGoalieZone = str(int(100*self.Info.autoGoalieZone)/len(matches)) + "%"
        self.avgAutoScore = round(self.Scores.avgAutoScore,2)
        self.avgAutoHighScored = round(self.Info.avgAutoHighScored,2)
        self.avgAutoLowScored = round(self.Info.avgAutoLowScored,2)
        self.avgAutoHotScored = round(self.Info.avgAutoHotScored,2)
        self.pHotAccuracy = str(100*round(self.Info.autoHotAccuracy,2)) + "%"

        self.avgTeleScore = round(self.Scores.avgTeleScore,2)
        self.avgTeleIntakeTimes = round(self.Info.avgTeleIntakeTimes,2)
        self.avgTeleHighScored = round(self.Info.avgTeleHighScored,2)
        self.avgTeleLowScored = round(self.Info.avgTeleLowScored,2)  
        self.avgTeleTrussScored = round(self.Info.avgTeleTrussScored,2)
        self.avgTeleCatchScored = round(self.Info.avgTeleCatchScored,2)
        self.avgTeleAssistScored = round(self.Info.avgTeleAssistScored,2)

        self.pDisabled = str(int(100*self.Info.postDisabled)/len(matches)) + "%"
        self.pNoShow  = str(int(100*self.Info.postNoShow)/len(matches)) + "%"
        self.avgPostRegFoul = round(self.Info.avgPostRegFoul,2)
        self.avgPostTechFoul = round(self.Info.avgPostTechFoul,2)
        self.avgFoulScore = round(self.Scores.avgFoulScore,2)
        self.pYellow = str(int(100*self.Info.postHadYellow)/len(matches)) + "%"
        self.pRed = str(int(100*self.Info.postHadRed)/len(matches)) + "%"
        self.pAggressive = str(int(100*self.Info.postAggressive)/len(matches)) + "%"

    def getAttr(self, source):
        return getattr(self, source)
