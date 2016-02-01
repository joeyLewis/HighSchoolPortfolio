#------------------------------------------------------------------------------
# cranking module
#   -- contains the functions and classes for controlling the ranking window
#------------------------------------------------------------------------------
from Tkinter import *

from model.calculate import *

#------------------------------------------------------------------------------
# get_none function
#   -- passes through so that a None list can delete all of its contents
#------------------------------------------------------------------------------
def get_none(sort=None,rev=None):
    pass

#------------------------------------------------------------------------------
# RankingController Class
#   -- used to get and set data for Ranking objects and their Listings
#------------------------------------------------------------------------------
class RankingController():

    # use these to index values to display, use the system: ("key",term)
    # where key corredsponds to a value in self.rankingTypes and term is
    # the function to call when that option is selected
    rankingTypes = ["None",
                    "Offensive Score",
                    "Total Score",
                    "Auto Score",
                    "Auto Stack Score","Auto Container Score","Auto Robot Score",
                    "Tele Score",
                    "Tele Tote Score","Tele Container Score","Tele Litter Score",
                    "Foul Score"]

    rankingIndex = [("None",get_none),
                    ("Offensive Score",get_off_rank),
                    ("Total Score",get_tot_rank),
                    ("Auto Score",get_auto_rank),
                    ("Auto Stack Score",get_auto_stack_rank),
                    ("Auto Container Score",get_auto_container_rank),
                    ("Auto Robot Score",get_auto_robot_rank),
                    ("Tele Score",get_tele_rank),
                    ("Tele Tote Score",get_tele_tote_rank),
                    ("Tele Container Score",get_tele_container_rank),
                    ("Tele Litter Score",get_tele_litter_rank),                     
                    ("Foul Score",get_foul_rank)]

    sortOptions = [("Maximum","max"),("Average","avg"),("Minimum","min")]

    def __init__(self):
        self.sort = StringVar()
        self.sort.set("avg")
        self.rev = BooleanVar()
        self.rev.set(1)
        self.data = None

    def load_rankings(self,kind="None"):
        for value, func in self.rankingIndex:
            if value==kind:
                self.data = func(sort=self.sort.get(),rev=self.rev.get())
                break
