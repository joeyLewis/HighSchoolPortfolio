#------------------------------------------------------------------------------
# calculate module
#   -- functions for handling data input, output, and caclulations
#------------------------------------------------------------------------------
import math
from statlib import stats

from team import *
from entry import *
from match import *

#------------------------------------------------------------------------------
# calculate_data function
#   -- handles data and stores it to the teams
#------------------------------------------------------------------------------
def calculate_data():
    
    for entry in Entry.entries:
        entry.primary_sort()

    # get basic team data from the entries
    for entry in Entry.entries:
        done = False
        for team in Team.team_list:
            if team.number == entry.team:
                assign_basic_team_values(team, entry)

                done = True
        if done == False:
            newTeam = Team(entry.team)
            print "Added Team #: " + str(entry.team)

            assign_basic_team_values(newTeam,entry)

    # get primary offensive information about the team
    for team in Team.team_list:
        team.get_primary_details()
    
    # get basic match data from the entries
    for entry in Entry.entries:
        done = False
        for match in Match.matches:
            if match.number == entry.match:
                assign_basic_match_values(match, entry)

                done = True
        if done==False:
            newMatch = Match(entry.match)
            print "Added Match #: " + str(entry.match)
            assign_basic_match_values(newMatch, entry)

    # get defensive and assistive scores for each entry
    for entry in Entry.entries:
        if entry.defensive or entry.assistive:
            for match in Match.matches:
                if match.number == entry.match:
                    if entry.allianceColor == 0:
                        oppOff = match.offScore1
                        allOff = match.offScore0
                        allDef = match.def0
                    elif entry.allianceColor == 1:
                        oppOff = match.offScore0
                        allOff = match.offScore1
                        allDef = match.def1
        else:
            oppOff = 0
            allOff = 0
            allDef = 0

        entry.secondary_sort(oppOff,allOff,allDef)

        # get total score for the entry
        entry.tertiary_sort()

    # get team defensive and assistive scores
    for entry in Entry.entries:
        for team in Team.team_list:
            if team.number == entry.team:
                team.Scores.dScores.append(entry.defensiveScore)
                team.Scores.aScores.append(entry.assistiveScore)
    for team in Team.team_list:
        team.get_secondary_details()

    # get match defensive and assitive scores
    for entry in Entry.entries:
        for match in Match.matches:
            if match.number == entry.match:
                if entry.allianceColor == 0:
                    match.defScore0 += entry.defensiveScore
                    match.astScore0 += entry.assistiveScore
                elif entry.allianceColor == 1:
                    match.defScore1 += entry.defensiveScore
                    match.astScore1 += entry.assistiveScore
    # get match total scores
    for match in Match.matches:
        match.get_total()

    # weight = (s[m]/(s[w]-s[1]))
    for entry in Entry.entries:
        for match in Match.matches:
            if match.number == entry.match:
                entry.wScore = abs(entry.totalScore/(match.total0 - match.total1)) if match.total0 != match.total1 else entry.totalScore
                entry.woScore = abs(entry.offensiveScore/(match.offScore0 - match.offScore1)) if match.offScore0 != match.offScore1 else entry.offensiveScore
                entry.wdScore = abs(entry.defensiveScore/(match.defScore0 - match.defScore1)) if match.defScore0 != match.defScore1 else entry.defensiveScore
                entry.waScore = abs(entry.assistiveScore/(match.astScore0 - match.defScore1)) if match.astScore0 != match.astScore1 else entry.assistiveScore
                    
    # get team average, weighted, total, and max/min scores
    for team in Team.team_list:
        for entry in Entry.entries:
            if entry.team == team.number:
                team.Scores.wScores.append(entry.wScore)
                team.Scores.woScores.append(entry.woScore)
                team.Scores.wdScores.append(entry.wdScore)
                team.Scores.waScores.append(entry.waScore)
                team.Scores.tScores.append(entry.totalScore)

        team.get_tertiary_details()
        team.get_final_details()
        
#------------------------------------------------------------------------------
# calculate_pit_data function
#   - handles pit data and stores it to the teams
#------------------------------------------------------------------------------
def calculate_pit_data():
    for entry in PitEntry.entries:
        done = False
        for team in Team.team_list:
            if team.number == entry.team:
                assign_pit_entry_values(team, entry)
                done = True
        if done == False:
            newTeam = Team(entry.team)
            print "Added Team #: " + str(entry.team)
            assign_pit_entry_values(Team.team_list[len(Team.team_list)-1],entry)
        
#------------------------------------------------------------------------------
# assign_basic_team_values function
#   -- assigns some basic values from an entry to a team
#   -- still needs error handling
#------------------------------------------------------------------------------
def assign_basic_team_values(team, entry):
    team.Info.matches.append(entry.match)
    team.Info.numOff += int(entry.offensive)
    team.Info.numDef += int(entry.defensive)
    team.Info.numAst += int(entry.assistive)

    team.Info.autoHadAuto += int(entry.autoHadAuto)
    team.Info.autoMobilityBonus += int(entry.autoMobilityBonus)
    team.Info.autoGoalieZone += int(entry.autoGoalieZone)
    team.Info.autoHighScored.append(float(entry.autoHighScored))
    team.Info.autoLowScored.append(float(entry.autoLowScored))
    team.Info.autoHotScored.append(float(entry.autoHotScored))
    team.Info.autoScoredAuto += int(entry.scoredInAuto)

    team.Info.teleHadTele += int(entry.teleHadTele)
    team.Info.teleHighScored.append(float(entry.teleHighScored))
    team.Info.teleScoredHigh += 1 if entry.teleHighScored>=1 else 0
    team.Info.teleLowScored.append(float(entry.teleLowScored))
    team.Info.teleTrussScored.append(float(entry.teleTrussScored))
    team.Info.teleScoredTruss += 1 if entry.teleTrussScored>=1 else 0
    team.Info.teleCatchScored.append(float(entry.teleCatchScored))
    team.Info.teleCaught += 1 if entry.teleCatchScored>=1 else 0
    team.Info.teleAssistScored.append(float(entry.teleAssistScored))
    team.Info.teleScoredTele += int(entry.scoredInTele)
    times = []
    for time in entry.teleIntakeTimes: 
        times.append(time)
    avgTime = sum(times)/len(times) if len(times)>=1 else 0
    team.Info.teleIntakeTimes.append(avgTime)
    for hotSpot in entry.teleHotSpots:
        team.Info.teleHotSpots.append(hotSpot)

    team.Info.postRegFouls.append(entry.postRegFouls)
    team.Info.postTechFouls.append(entry.postTechFouls)
    team.Info.postHadRegFoul += int(entry.hasRegFoul)
    team.Info.postHadTechFoul += int(entry.hasTechFoul)
    team.Info.postDisabled += int(entry.postDisabled)
    team.Info.postNoShow += int(entry.postNoShow)
    team.Info.postHadYellow += int(entry.postYellowCard)
    team.Info.postHadRed += int(entry.postRedCard)
    team.Info.postAggressive += int(entry.postAggressive)

    team.Scores.oScores.append(entry.offensiveScore)
    team.Scores.autoScores.append(entry.autoScore)
    team.Scores.teleScores.append(entry.teleScore)
    team.Scores.foulScores.append(entry.foulScore)
    
#------------------------------------------------------------------------------
# assign_basic_match_values function
#   -- assigns some basic values from the entry to a match
#   -- still needs error handling
#------------------------------------------------------------------------------
def assign_basic_match_values(match, entry):
    match.teams.append(entry.team)
    if entry.allianceColor == 0:
        match.all0.append(entry.team)
        match.offScore0 += entry.offensiveScore
        match.off0 += int(entry.offensive)
        match.def0 += int(entry.defensive)
        match.ast0 += int(entry.assistive)
                    
    elif entry.allianceColor == 1:
        match.all1.append(entry.team)
        match.offScore1 += entry.offensiveScore
        match.off1 += int(entry.offensive)
        match.def1 += int(entry.defensive)
        match.ast1 += int(entry.assistive)

#------------------------------------------------------------------------------
# assign_pit_entry_values function
#   -- takes PitEntry values and puts them into a team
#   -- still needs error handling
#------------------------------------------------------------------------------
def assign_pit_entry_values(team, entry):
    
    team.PitInfo.robLength = entry.robLength
    team.PitInfo.robWidth = entry.robWidth
    team.PitInfo.robHeight = entry.robHeight
    team.PitInfo.robWieght = entry.robWieght
    team.PitInfo.clearance = entry.clearance
    team.PitInfo.wheelSpace = entry.wheelSpace
    team.PitInfo.driveSystem = entry.driveSystem
    team.PitInfo.shiftGear = entry.shiftGear
    team.PitInfo.centerMass = entry.centerMass
    team.PitInfo.driver1 = entry.driver1
    team.PitInfo.exp1 = entry.exp1 + " Competitions"
    team.PitInfo.driver2 = entry.driver2
    team.PitInfo.exp2 = entry.exp2 + " Competitions"
    team.PitInfo.driver3 = entry.driver3
    team.PitInfo.exp3 = entry.exp3 + " Competitions"

#------------------------------------------------------------------------------
# get_rank functions
#   -- calculates rankings for avg, min, and max scores for each team
#------------------------------------------------------------------------------
def get_off_rank(sort="avg",rev=True):

    TeamRankings.off_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numOff > 0:
                TeamRankings.off_rank.append([team.Scores.avgOffScore,team.number])
        elif sort == "max":
            if team.Info.numOff > 0:
                TeamRankings.off_rank.append([team.Scores.maxOffScore,team.number])
        elif sort == "min":
            if team.Info.numOff > 0:
                TeamRankings.off_rank.append([team.Scores.minOffScore,team.number])

    TeamRankings.off_rank.sort(reverse=rev)

    return TeamRankings.off_rank

def get_def_rank(sort="avg",rev=True):

    TeamRankings.def_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numDef > 0:
                TeamRankings.def_rank.append([team.Scores.avgDefScore,team.number])
        elif sort == "max":
            if team.Info.numDef > 0:
                TeamRankings.def_rank.append([team.Scores.maxDefScore,team.number])
        elif sort == "min":
            if team.Info.numDef > 0:
                TeamRankings.def_rank.append([team.Scores.minDefScore,team.number])

    TeamRankings.def_rank.sort(reverse=rev)

    return TeamRankings.def_rank

def get_ast_rank(sort="avg",rev=True):

    TeamRankings.ast_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numAst > 0:
                TeamRankings.ast_rank.append([team.Scores.avgAstScore,team.number])
        elif sort == "max":
            if team.Info.numAst > 0:
                TeamRankings.ast_rank.append([team.Scores.maxAstScore,team.number])
        elif sort == "min":
            if team.Info.numAst > 0:
                TeamRankings.ast_rank.append([team.Scores.minAstScore,team.number])

    TeamRankings.ast_rank.sort(reverse=rev)

    return TeamRankings.ast_rank

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

def get_tele_rank(sort="avg",rev=True):

    TeamRankings.tele_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.teleHadTele > 0:
                TeamRankings.tele_rank.append([team.Scores.avgTeleScore,team.number])
        elif sort == "max":
            if team.Info.teleHadTele > 0:
                TeamRankings.tele_rank.append([team.Scores.maxTeleScore,team.number])
        elif sort == "min":
            if team.Info.teleHadTele > 0:
                TeamRankings.tele_rank.append([team.Scores.minTeleScore,team.number])

    TeamRankings.tele_rank.sort(reverse=rev)

    return TeamRankings.tele_rank

def get_foul_rank(sort="avg",rev=False): # foul rank default from least points to most

    TeamRankings.foul_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.postHadRegFoul or team.Info.postHadTechFoul:
                TeamRankings.foul_rank.append([team.Scores.avgFoulScore,team.number])
        elif sort == "max":
            if team.Info.postHadRegFoul or team.Info.postHadTechFoul:
                TeamRankings.foul_rank.append([team.Scores.maxFoulScore,team.number])
        elif sort == "min":
            if team.Info.postHadRegFoul or team.Info.postHadTechFoul:
                TeamRankings.foul_rank.append([team.Scores.minFoulScore,team.number])

    TeamRankings.foul_rank.sort(reverse=rev)

    return TeamRankings.foul_rank

def get_w_rank(sort="avg",rev=True):

    TeamRankings.w_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
                TeamRankings.w_rank.append([team.Scores.avgWScore,team.number])
        elif sort == "max":
                TeamRankings.w_rank.append([team.Scores.maxWScore,team.number])
        elif sort == "min":
                TeamRankings.w_rank.append([team.Scores.minWScore,team.number])

    TeamRankings.w_rank.sort(reverse=rev)

    return TeamRankings.w_rank

def get_wo_rank(sort="avg",rev=True):

    TeamRankings.wo_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numOff > 0:
                TeamRankings.wo_rank.append([team.Scores.avgWOScore,team.number])
        elif sort == "max":
            if team.Info.numOff > 0:
                TeamRankings.wo_rank.append([team.Scores.maxWOScore,team.number])
        elif sort == "min":
            if team.Info.numOff > 0:
                TeamRankings.wo_rank.append([team.Scores.minWOScore,team.number])

    TeamRankings.wo_rank.sort(reverse=rev)

    return TeamRankings.wo_rank

def get_wd_rank(sort="avg",rev=True):

    TeamRankings.wd_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numDef > 0:
                TeamRankings.wd_rank.append([team.Scores.avgWDScore,team.number])
        elif sort == "max":
            if team.Info.numDef > 0:
                TeamRankings.wd_rank.append([team.Scores.maxWDScore,team.number])
        elif sort == "min":
            if team.Info.numDef > 0:
                TeamRankings.wd_rank.append([team.Scores.minWDScore,team.number])

    TeamRankings.wd_rank.sort(reverse=rev)

    return TeamRankings.wd_rank

def get_wa_rank(sort="avg",rev=True):

    TeamRankings.wa_rank = []
    
    for team in Team.team_list:
        if sort == "avg":
            if team.Info.numAst > 0:
                TeamRankings.wa_rank.append([team.Scores.avgWAScore,team.number])
        elif sort == "max":
            if team.Info.numAst > 0:
                TeamRankings.wa_rank.append([team.Scores.maxWAScore,team.number])
        elif sort == "min":
            if team.Info.numAst > 0:
                TeamRankings.wa_rank.append([team.Scores.minWAScore,team.number])

    TeamRankings.wa_rank.sort(reverse=rev)

    return TeamRankings.wa_rank

#------------------------------------------------------------------------------
# predict functions
#   -- calculates predicted alliance scores predicts match outcomes
#------------------------------------------------------------------------------
def predict_scores(team1=None,team2=None,team3=None):
    pOff1 = float(team1.pOff.rstrip("%"))/100
    pOff2 = float(team2.pOff.rstrip("%"))/100
    pOff3 = float(team3.pOff.rstrip("%"))/100
    pDef1 = float(team1.pDef.rstrip("%"))/100
    pDef2 = float(team2.pDef.rstrip("%"))/100
    pDef3 = float(team3.pDef.rstrip("%"))/100
    pAst1 = float(team1.pAst.rstrip("%"))/100
    pAst2 = float(team2.pAst.rstrip("%"))/100
    pAst3 = float(team3.pAst.rstrip("%"))/100
    try:
        offScore = ((team1.avgOff*pOff1)+(team2.avgOff*pOff2)+(team3.avgOff*pOff3))
        defScore = ((team1.avgDef*pDef1)+(team2.avgDef*pDef2)+(team3.avgDef*pDef3))
        astScore = ((team1.avgAst*pAst1)+(team2.avgAst*pAst2)+(team3.avgAst*pAst3))
    except:
        offScore = 0
        defScore = 0
        astScore = 0

    expectedScores = [offScore, defScore, astScore]

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
