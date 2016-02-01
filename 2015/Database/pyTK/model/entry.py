#------------------------------------------------------------------------------
# entry module
#   -- makes sense of the data collected
#------------------------------------------------------------------------------
from stack import *

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
        index += 1
        self.team = int(data[index])
        index += 1
        self.allianceColor = int(data[index])
        index += 1
        self.noShow = bool(int(data[index]))
        index += 1
        
        # autonomous data
        self.autoStack = []
        self.autoHadAuto = bool(int(data[index]))
        index += 1
        self.autoTotesToZone = float(data[index])
        index += 1
        self.autoContainersToZone = float(data[index])
        index += 1
        self.autoContainersFromStep = float(data[index])
        index += 1
        self.autoTotesFromStep = float(data[index])
        index += 1

        #auto stack data
        i = 0
        while (i < 3):
            self.autoStack.append(bool(int(data[index])))
            index += 1
            i += 1

        self.autoEndInZone = bool(int(data[index]))
        index += 1
        self.autoOther = bool(int(data[index]))
        index += 1

        # tele-op data
        self.teleStacks = []
        self.teleStepStacks = []

        numStacks = int(data[index])
        index += 1
        
        i = 0
        while (i < numStacks):
            stackdata = []
            stackdata.append(float(data[index]))
            index += 1
            stackdata.append(float(data[index]))
            index += 1

            j = 0
            while(j < 6):
                stackdata.append(bool(int(data[index])))
                index += 1
                j += 1

            stackdata.append(bool(int(data[index])))
            index += 1
            stackdata.append(float(data[index]))
            index += 1
            stackdata.append(bool(int(data[index])))
            index += 1
            stackdata.append(bool(int(data[index])))
            index += 1
                            
            self.teleStacks.append(Stack(stackdata))
            i += 1

        numStepStacks = int(data[index])
        index += 1
        
        i = 0
        while (i < numStepStacks):
            ssdata = []
            ssdata.append(float(data[index]))
            index += 1
            ssdata.append(float(data[index]))
            index += 1

            j = 0
            while (j < 6):
                ssdata.append(bool(int(data[index])))
                index += 1
                j += 1

            ssdata.append(bool(int(data[index])))
            index += 1

            self.teleStepStacks.append(StepStack(ssdata))
            i += 1

        self.teleTotesFromChute = float(data[index])
        index += 1
        self.teleLitterFromChute = float(data[index])
        index += 1
        self.teleTotesFromLandfill = float(data[index])
        index += 1
        self.teleLitterToLandfill = float(data[index])
        index += 1

        # post data
        self.postFouls = float(data[index])
        index += 1
        self.postRedCard = bool(int(data[index]))
        index += 1
        self.postYellowCard = bool(int(data[index]))
        index += 1
        self.postDisabled = bool(int(data[index]))

        # more general data
        self.teleStackTotes = []
        self.teleStepStackTotes = []
        self.teleStackHeights = []
        self.teleStepStackHeights = []
        self.teleStackContainers = []
        self.teleStackContainerHeights = []
        self.teleStackLitter = []
        self.teleStackKnockedOver = []
        self.teleStepStackKnockedOver = []
        self.autoStackTotalTotes = 0

        self.teleStacksScored = len(self.teleStacks)
        self.teleStepStacksScored = len(self.teleStepStacks)

        self.entries.append(self)

    def sort(self):
        """Calculates basic scoring and information."""

        for s in self.teleStacks:
            self.teleStackTotes.append(float(s.totalTotes))
            self.teleStackHeights.append(float(s.highestTote))
            self.teleStackContainers.append(float(int(s.container)))
            self.teleStackContainerHeights.append(float(s.containerHeight))
            self.teleStackLitter.append(float(int(s.litter)))
            self.teleStackKnockedOver.append(float(int(s.knockedOver)))

        for s in self.teleStepStacks:
            self.teleStepStackTotes.append(float(s.totalTotes))
            self.teleStepStackHeights.append(float(s.highestTote))
            self.teleStepStackKnockedOver.append(float(int(s.knockedOver)))
            
        self.avgTeleStackTotes = float(sum(self.teleStackTotes))/float(len(self.teleStackTotes)) if len(self.teleStackTotes) else 0
        self.avgTeleStepStackTotes = float(sum(self.teleStepStackTotes))/float(len(self.teleStepStackTotes)) if len(self.teleStepStackTotes) else 0
        self.avgTeleStackHeights = float(sum(self.teleStackHeights))/float(len(self.teleStackHeights)) if len(self.teleStackHeights) else 0
        self.avgTeleStepStackHeights = float(sum(self.teleStepStackHeights))/float(len(self.teleStepStackHeights)) if len(self.teleStepStackHeights) else 0
        self.avgTeleStackContainers = float(sum(self.teleStackContainers))
        self.avgTeleStackContainerHeights = float(sum(self.teleStackContainerHeights))/float(len(self.teleStackContainerHeights)) if len(self.teleStackContainerHeights) else 0
        self.avgTeleStackLitter = float(sum(self.teleStackLitter))/float(len(self.teleStackLitter)) if len(self.teleStackLitter) else 0
        self.avgTeleStackKnockedOver = float(sum(self.teleStackKnockedOver))/float(len(self.teleStackKnockedOver)) if len(self.teleStackKnockedOver) else 0
        self.avgTeleStepStackKnockedOver = float(sum(self.teleStepStackKnockedOver))/float(len(self.teleStepStackKnockedOver)) if len(self.teleStepStackKnockedOver) else 0

        i = 0
        while (i < len(self.autoStack)):
            self.autoStackTotalTotes += 1 if self.autoStack[i] else 0
            i += 1
        
        self.autoStackScore = 20 if self.autoStackTotalTotes == 3 else self.autoTotesToZone*2
        self.autoContainerScore = 8 if self.autoContainersToZone >= 3 else float(self.autoContainersToZone)*float(8.0/3.0)
        self.autoRobotScore = float(4.0/3.0) if self.autoEndInZone else 0
        
        self.autoScore = (self.autoStackScore + self.autoContainerScore + self.autoRobotScore)

        self.teleToteScore = float(sum(self.teleStackTotes))*float(2)
        self.teleContainerScore = 0
        i = 0
        while (i < len(self.teleStackContainers)):
            self.teleContainerScore += float(4*(int(self.teleStackContainers[i])*self.teleStackContainerHeights[i])) \
                                       if self.teleStackContainerHeights[i]>0 else float(4*(int(self.teleStackContainers[i])*self.teleStackTotes[i]))
            i += 1
        self.teleLitterScore = 0
        for litter in self.teleStackLitter:
            self.teleLitterScore += float(int(litter)*6)
        self.teleLitterScore += float(self.teleLitterToLandfill)
        coopScore = float(sum(self.teleStepStackTotes))*float(5)
            
        self.teleScore = (self.teleToteScore + self.teleContainerScore + self.teleLitterScore + coopScore)

        self.scoredInAuto = True if self.autoScore > 0 else False
        self.scoredInTele = True if self.teleScore > 0 else False
        self.hasFoul      = True if self.postFouls > 0 else False

        self.offensiveScore = (self.autoScore + self.teleScore)
        self.foulScore = (6*self.postFouls)

        self.totalScore = (self.offensiveScore - self.foulScore)
