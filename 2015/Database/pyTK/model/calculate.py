#------------------------------------------------------------------------------
# calculate module
#   -- functions for handling data input, output, and caclulations
#------------------------------------------------------------------------------
import math
from statlib import stats

from team import *
from entry import *

#------------------------------------------------------------------------------
# calculate_data function
#   -- handles data and stores it to the teams
#------------------------------------------------------------------------------
def calculate_data():
    
    for entry in Entry.entries:
        entry.sort()

    # get basic team data from the entries
    for entry in Entry.entries:
        done = False
        for team in Team.team_list:
            if team.number == entry.team:
                assign_team_values(team, entry)

                done = True
        if done == False:
            newTeam = Team(entry.team)
            print "Added Team #: " + str(entry.team)

            assign_team_values(newTeam,entry)

    # get the rest of the information about each team
    for team in Team.team_list:
        team.get_details()

#------------------------------------------------------------------------------
# assign_basic_team_values function
#   -- assigns some basic values from an entry to a team
#   -- still needs error handling
#------------------------------------------------------------------------------
def assign_team_values(team, entry):
    team.Info.matches.append(entry.match)
    team.Info.noShow += int(entry.noShow)

    team.Info.autoHadAuto += int(entry.autoHadAuto)
    team.Info.autoTotesToZone.append(float(entry.autoTotesToZone))
    team.Info.autoContainersToZone.append(float(entry.autoContainersToZone))
    team.Info.autoContainersFromStep.append(float(entry.autoContainersFromStep))
    team.Info.autoTotesFromStep.append(float(entry.autoTotesFromStep))
    team.Info.autoStackTotalTotes.append(float(entry.autoStackTotalTotes))
    team.Info.autoEndInZone += int(entry.autoEndInZone)
    team.Info.autoOther += int(entry.autoOther)

    team.Info.teleStackTotes.append(float(entry.avgTeleStackTotes))
    team.Info.teleStepStackTotes.append(float(entry.avgTeleStepStackTotes))
    team.Info.teleStackHeights.append(float(entry.avgTeleStackHeights))
    team.Info.teleStepStackHeights.append(float(entry.avgTeleStepStackHeights))
    team.Info.teleStackContainers.append(float(entry.avgTeleStackContainers))
    team.Info.teleStackContainerHeights.append(float(entry.avgTeleStackContainerHeights))
    team.Info.teleStackLitter.append(float(entry.avgTeleStackLitter))
    team.Info.teleStackKnockedOver.append(float(entry.avgTeleStackKnockedOver))
    team.Info.teleStepStackKnockedOver.append(float(entry.avgTeleStackKnockedOver))
    team.Info.teleStacksScored.append(float(entry.teleStacksScored))
    team.Info.teleStepStacksScored.append(float(entry.teleStepStacksScored))

    team.Info.teleTotesFromChute.append(float(entry.teleTotesFromChute))
    team.Info.teleLitterFromChute.append(float(entry.teleLitterFromChute))
    team.Info.teleTotesFromLandfill.append(float(entry.teleTotesFromLandfill))
    team.Info.teleLitterToLandfill.append(float(entry.teleLitterToLandfill))

    team.Info.postFouls.append(float(entry.postFouls))
    team.Info.postRedCard += int(entry.postRedCard)
    team.Info.postYellowCard += int(entry.postYellowCard)
    team.Info.postDisabled += int(entry.postDisabled)

    team.Info.scoredInTele += int(entry.scoredInTele)
    team.Info.scoredInAuto += int(entry.scoredInAuto)
    team.Info.hasFoul += int(entry.hasFoul)

    team.Scores.oScores.append(entry.offensiveScore)
    team.Scores.autoScores.append(entry.autoScore)
    team.Scores.autoStackScores.append(entry.autoStackScore)
    team.Scores.autoContainerScores.append(entry.autoContainerScore)
    team.Scores.autoRobotScores.append(entry.autoRobotScore)
    team.Scores.teleScores.append(entry.teleScore)
    team.Scores.teleToteScores.append(entry.teleToteScore)
    team.Scores.teleContainerScores.append(entry.teleContainerScore)
    team.Scores.teleLitterScores.append(entry.teleLitterScore)
    team.Scores.foulScores.append(entry.foulScore)
    team.Scores.tScores.append(entry.totalScore)

#------------------------------------------------------------------------------
# get_rank functions
#   -- calculates rankings for avg, min, and max scores for each team
#------------------------------------------------------------------------------
def get_off_rank(sort="avg",rev=True):

    TeamRankings.off_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.off_rank.append([team.Scores.avgOffScore,team.number])
        elif sort == "max":
            TeamRankings.off_rank.append([team.Scores.maxOffScore,team.number])
        elif sort == "min":
            TeamRankings.off_rank.append([team.Scores.minOffScore,team.number])

    TeamRankings.off_rank.sort(reverse=rev)

    return TeamRankings.off_rank

def get_auto_rank(sort="avg",rev=True):

    TeamRankings.auto_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_rank.append([team.Scores.avgAutoScore,team.number])
        elif sort == "max":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_rank.append([team.Scores.maxAutoScore,team.number])
        elif sort == "min":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_rank.append([team.Scores.minAutoScore,team.number])

    TeamRankings.auto_rank.sort(reverse=rev)

    return TeamRankings.auto_rank

def get_auto_stack_rank(sort="avg",rev=True):

    TeamRankings.auto_stack_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_stack_rank.append([team.Scores.avgAutoStackScore,team.number])
        elif sort == "max":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_stack_rank.append([team.Scores.maxAutoStackScore,team.number])
        elif sort == "min":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_stack_rank.append([team.Scores.minAutoStackScore,team.number])

    TeamRankings.auto_stack_rank.sort(reverse=rev)

    return TeamRankings.auto_stack_rank

def get_auto_container_rank(sort="avg",rev=True):

    TeamRankings.auto_container_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_container_rank.append([team.Scores.avgAutoContainerScore,team.number])
        elif sort == "max":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_container_rank.append([team.Scores.maxAutoContainerScore,team.number])
        elif sort == "min":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_container_rank.append([team.Scores.minAutoContainerScore,team.number])

    TeamRankings.auto_container_rank.sort(reverse=rev)

    return TeamRankings.auto_container_rank

def get_auto_robot_rank(sort="avg",rev=True):

    TeamRankings.auto_robot_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_robot_rank.append([team.Scores.avgAutoRobotScore,team.number])
        elif sort == "max":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_robot_rank.append([team.Scores.maxAutoRobotScore,team.number])
        elif sort == "min":
            if team.Info.autoHadAuto > 0:
                TeamRankings.auto_robot_rank.append([team.Scores.minAutoRobotScore,team.number])

    TeamRankings.auto_robot_rank.sort(reverse=rev)

    return TeamRankings.auto_robot_rank

def get_tele_rank(sort="avg",rev=True):

    TeamRankings.tele_rank = []

    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.tele_rank.append([team.Scores.avgTeleScore,team.number])
        elif sort == "max":
            TeamRankings.tele_rank.append([team.Scores.maxTeleScore,team.number])
        elif sort == "min":
            TeamRankings.tele_rank.append([team.Scores.minTeleScore,team.number])

    TeamRankings.tele_rank.sort(reverse=rev)

    return TeamRankings.tele_rank

def get_tele_tote_rank(sort="avg",rev=True):

    TeamRankings.tele_tote_rank = []

    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.tele_tote_rank.append([team.Scores.avgTeleToteScore,team.number])
        elif sort == "max":
            TeamRankings.tele_tote_rank.append([team.Scores.maxTeleToteScore,team.number])
        elif sort == "min":
            TeamRankings.tele_tote_rank.append([team.Scores.minTeleToteScore,team.number])

    TeamRankings.tele_tote_rank.sort(reverse=rev)

    return TeamRankings.tele_tote_rank

def get_tele_container_rank(sort="avg",rev=True):

    TeamRankings.tele_container_rank = []

    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.tele_container_rank.append([team.Scores.avgTeleContainerScore,team.number])
        elif sort == "max":
            TeamRankings.tele_container_rank.append([team.Scores.maxTeleContainerScore,team.number])
        elif sort == "min":
            TeamRankings.tele_container_rank.append([team.Scores.minTeleContainerScore,team.number])

    TeamRankings.tele_container_rank.sort(reverse=rev)

    return TeamRankings.tele_container_rank

def get_tele_litter_rank(sort="avg",rev=True):

    TeamRankings.tele_litter_rank = []

    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.tele_litter_rank.append([team.Scores.avgTeleLitterScore,team.number])
        elif sort == "max":
            TeamRankings.tele_litter_rank.append([team.Scores.maxTeleLitterScore,team.number])
        elif sort == "min":
            TeamRankings.tele_litter_rank.append([team.Scores.minTeleLitterScore,team.number])

    TeamRankings.tele_litter_rank.sort(reverse=rev)

    return TeamRankings.tele_litter_rank

def get_foul_rank(sort="avg",rev=False): # foul rank default from least points to most

    TeamRankings.foul_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.hasFoul:
                TeamRankings.foul_rank.append([team.Scores.avgFoulScore,team.number])
        elif sort == "max":
            if team.Info.hasFoul:
                TeamRankings.foul_rank.append([team.Scores.maxFoulScore,team.number])
        elif sort == "min":
            if team.Info.hasFoul:
                TeamRankings.foul_rank.append([team.Scores.minFoulScore,team.number])

    TeamRankings.foul_rank.sort(reverse=rev)

    return TeamRankings.foul_rank

def get_tot_rank(sort="avg",rev=True):

    TeamRankings.tot_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            TeamRankings.tot_rank.append([team.Scores.avgTotalScore,team.number])
        elif sort == "max":
            TeamRankings.tot_rank.append([team.Scores.maxTotalScore,team.number])
        elif sort == "min":
            TeamRankings.tot_rank.append([team.Scores.minTotalScore,team.number])

    TeamRankings.tot_rank.sort(reverse=rev)

    return TeamRankings.tot_rank

#------------------------------------------------------------------------------
# predict functions
#   -- calculates predicted alliance scores predicts match outcomes
#------------------------------------------------------------------------------
def predict_scores(team1=None,team2=None,team3=None):
    try:
        # make each team a confidence internal over proportion means and use
        # that confidence interval to calculate a total range of scores (from lowest
        # theoretical to highest theoretical, then take the center of that
        # total range and place it as the expected offensive score
        offScore = (team1.avgOff+team2.avgOff+team3.avgOff)
    except:
        offScore = 0

    expectedScores = [offScore]

    return expectedScores

def predict_outcome(teams=[]):

    team1 = teams[0]
    team2 = teams[1]
    team3 = teams[2]
    team4 = teams[3]
    team5 = teams[4]
    team6 = teams[5]

    # standard deviations
    Sigmas = [[],[],[],[],[],[]]

    for score in team1.Scores.tScores:
        Sigmas[0].append(((score-team1.avgTotal)**2)/len(team1.Scores.tScores))
    for score in team2.Scores.tScores:
        Sigmas[1].append(((score-team2.avgTotal)**2)/len(team2.Scores.tScores))
    for score in team3.Scores.tScores:
        Sigmas[2].append(((score-team3.avgTotal)**2)/len(team3.Scores.tScores))
    for score in team4.Scores.tScores:
        Sigmas[3].append(((score-team4.avgTotal)**2)/len(team4.Scores.tScores))
    for score in team5.Scores.tScores:
        Sigmas[4].append(((score-team5.avgTotal)**2)/len(team5.Scores.tScores))
    for score in team6.Scores.tScores:
        Sigmas[5].append(((score-team6.avgTotal)**2)/len(team6.Scores.tScores))

    r1 = math.sqrt(sum(Sigmas[0]))
    r2 = math.sqrt(sum(Sigmas[1]))
    r3 = math.sqrt(sum(Sigmas[2]))
    b1 = math.sqrt(sum(Sigmas[3]))
    b2 = math.sqrt(sum(Sigmas[4]))
    b3 = math.sqrt(sum(Sigmas[5]))
    
    mur = (float(1)/3)*(team1.avgTotal+team2.avgTotal+team3.avgTotal)
    mub = (float(1)/3)*(team4.avgTotal+team5.avgTotal+team6.avgTotal)
    
    rst = math.sqrt((float(1)/float(9))*(r1**2+r2**2+r3**2))
    bst = math.sqrt((float(1)/float(9))*(b1**2+b2**2+b3**2))
    
    if mur > mub:
        zval = (mur-mub)/math.sqrt((rst**2)+(bst**2)) if math.sqrt((rst**2)+(bst**2)) > 0 else 0
        perr = stats.lzprob(zval)
        perr = round(perr,4)
        return "Red Alliance: " + str(100*perr)
    
    else:
        zval = (mub-mur)/math.sqrt((rst**2)+(bst**2)) if math.sqrt((rst**2)+(bst**2)) > 0 else 0
        perr = stats.lzprob(zval)
        perr = round(perr, 4)
        return "Blue Alliance: " + str(100*perr)
