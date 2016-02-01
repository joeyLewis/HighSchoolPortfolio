#------------------------------------------------------------------------------
# entry module
#   -- makes sense of the data collected
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Entry class
#   -- Equivalent to a single ms-access entry
#   -- each match has 6 of these entries
#------------------------------------------------------------------------------
class Entry(object):
    """Pull in loaded data and sort it to be later assigned to team values."""

    entries = [] # list holding all the entries, 6 per match
    
    def __init__(self, data):
        # general info
        index = 0
        self.match = int(data[index])
        index +=1
        self.team = int(data[index])
        index +=1
        self.allianceColor = int(data[index])
        index +=1
        
        # autonomous data
        self.autoHotScored = 0.0
        
        self.autoHadAuto = bool(int(data[index]))
        index +=1
        self.autoMobilityBonus = bool(int(data[index]))
        index +=1
        self.autoGoalieZone = bool(int(data[index]))
        index +=1

        self.autoHighScored = float(data[index])
        index +=1
        self.autoHotScored += float(data[index])
        index += 1
        self.autoHotScored += float(data[index])
        index += 1
        self.autoHotScored += float(data[index])
        index += 1

        self.autoLowScored = float(data[index])
        index +=1
        self.autoHotScored += float(data[index])
        index += 1
        self.autoHotScored += float(data[index])
        index += 1
        self.autoHotScored += float(data[index])
        index += 1

        # tele-op data
        self.teleIntakeTimes = []
        self.teleHotSpots = []
        self.teleAssistsGiven = 0
        self.teleAssistsReceived = 0
        self.teleHighScored = 0
        self.teleTrussScored = 0
        self.teleCatchScored = 0

        i = 0
        numIntakes = data[index]
        index += 1
        while (i < numIntakes):
            self.teleIntakeTimes.append(float(data[index]))
            index += 1
            i += 1

        self.teleLowScored = float(data[index])
        index += 1

        i = 0
        numHotSpots = data[index]
        index += 1
        while (i < numHotSpots):
            hotSpot = [int(data[index]),float(data[index+1]),float(data[index+2])]
            self.teleHotSpots.append(hotSpot)
            index += 3
            i += 1

        # post data
        self.postRegFouls = float(data[index])
        index += 1
        self.postTechFouls = float(data[index])
        index += 1

        self.postDisabled = bool(int(data[index]))
        index += 1
        self.postNoShow = bool(int(data[index]))
        index += 1

        self.postYellowCard = bool(int(data[index]))
        index += 1
        self.postRedCard = bool(int(data[index]))
        index += 1

        self.postDefensive = bool(int(data[index]))
        index += 1
        self.postAggressive = bool(int(data[index]))

        for h in self.teleHotSpots:
            if h[0] == 1:
                self.teleTrussScored += 1
            elif h[0] == 2:
                self.teleCatchScored += 1
            elif h[0] == 3:
                self.teleHighScored += 1
            elif h[0] == 4:
                self.teleAssistsGiven += 1
            elif h[0] == 5:
                self.teleAssistsReceived += 1

        self.autoScored = self.autoHighScored + self.autoLowScored
        self.teleScored = self.teleHighScored + self.teleLowScored
        self.teleTCScored = self.teleTrussScored + self.teleCatchScored
        self.teleAssistScored = self.teleAssistsGiven + self.teleAssistsReceived
        self.teleHadTele = True if self.teleScored>0 or self.teleTCScored>0 or self.teleAssistScored>0 else False
        self.entries.append(self)

    def primary_sort(self):
        """Calculates basic scoring and information."""
        self.autoScore = (self.autoHighScored*10
                        + self.autoLowScored*1
                        + self.autoHotScored*5
                        + self.autoScored*5)
        
        self.teleScore = ((self.teleHighScored*10)
                        +(self.teleLowScored*1)
                        +(self.teleTrussScored*10)
                        +(self.teleCatchScored*10)
                        +(self.teleAssistScored*10))

        self.scoredInAuto = True if self.autoScore > 0 else False
        self.scoredInTele = True if self.teleScore > 0 else False
        self.hasRegFoul = True if self.postRegFouls > 0 else False
        self.hasTechFoul = True if self.postTechFouls > 0 else False

        self.offensiveScore = self.autoScore + self.teleScore
        self.foulScore = (20*self.postRegFouls) + (50*self.postTechFouls)

        self.offensive = True if self.offensiveScore > 0 else False
        self.assistive = True if self.teleAssistScored > 0 else False
        self.defensive = self.postDefensive

    def secondary_sort(self, oppOff, allOff, allDef):
        """Calculates defensive and assisstive score values."""
        # result = difference between offensive scores /
        #          the number of defensive players
        self.defensiveScore = (allOff-oppOff) / allDef / 2.0 if self.defensive else 0
        # assistive score this year is really easy: just take the points from assists
        self.assistiveScore = self.teleAssistScored*10
        
    def tertiary_sort(self):
        """Calculates total scores."""
        self.totalScore = (self.offensiveScore + self.defensiveScore +
                           self.assistiveScore - self.foulScore)
        self.totalTAScore = (self.offensiveScore + self.defensiveScore +
                             self.assistiveScore)

#------------------------------------------------------------------------------
# PitEntry class
#   -- stores information about a specific team, robot chassis info, etc.
#   -- does not have to do with performance on the field
#   -- most recent data is from 2012, commenting out any game specific data
#------------------------------------------------------------------------------
class PitEntry(object):
    """Stores data not dealing with performance to be transfered to a team."""

    entries = [] # list holding all the pit entries
    
    def __init__(self,data):
        self.team = data[0]

        self.robLength = data[1]
        self.robWidth = data[2]
        self.robHeight = data[3]
        self.robWieght = data[4]
        self.clearance = data[5]
        self.wheelSpace = data[6]

        ##self.BrdgMech = data[7]
        ##self.SlideBrdg = data[8]
        ##self.balsensor = data[9]
        self.driveSystem = data[7]
        self.shiftGear = data[8]

        self.centerMass = data[9]

        self.driver1 = data[10]
        self.exp1 = data[11]

        self.driver2 = data[12]
        self.exp2 = data[13]

        self.driver3 = data[14]
        self.exp3 = data[15]

        self.entries.append(self)
