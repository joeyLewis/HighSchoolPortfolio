#------------------------------------------------------------------------------
# stack module
#   -- makes sense of each of the different types of stacks
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Stack Class
#   -- each one of these stores information for one stack
#   -- there may be more than one of these per team per match
#------------------------------------------------------------------------------
class Stack(object):
    """Data object for storing information about stacks."""

    def __init__(self, data):
        # all stack data
        index = 0
        self.x = data[index]
        index += 1
        self.y = data[index]
        index += 1

        i = 0
        self.totes = []
        while (i < 6):
            self.totes.append(data[index])
            index += 1
            i += 1

        self.container = data[index]
        index += 1
        self.containerHeight = data[index]
        index += 1
        self.litter = data[index]
        index += 1
        self.knockedOver = data[index]

        self.highestTote = 0
        i = len(self.totes)
        while(i > 0):
            if(self.totes[i-1]):
                self.highestTote = i
                break
            i -= 1

        self.totalTotes = 0
        i = 0
        while(i < len(self.totes)):
            self.totalTotes += 1 if self.totes[i] else 0
            i += 1

#------------------------------------------------------------------------------
# StepStack Class
#   -- each one of these stores information for one stack made on the step
#   -- there may be more than one of these per team per match
#------------------------------------------------------------------------------
class StepStack(object):

    def __init__(self, data):
        # all step stack data
        index = 0
        self.x = float(data[index])
        index += 1
        self.y = float(data[index])
        index += 1

        i = 0
        self.totes = []
        while (i < 6):
            self.totes.append(bool(int(data[index])))
            index += 1
            i += 1

        self.knockedOver = bool(data[index])

        self.highestTote = 0
        i = len(self.totes)
        while(i > 0):
            if(self.totes[i-1]):
                self.highestTote = i
                break
            i -= 1

        self.totalTotes = 0
        i = 0
        while(i < len(self.totes)):
            self.totalTotes += 1 if self.totes[i] else 0
            i += 1
            
