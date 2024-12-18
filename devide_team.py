from random import sample



def rand_leader(players):
    leaders=sample(players,2)
    teamA_leader=sample(leaders,1)
    teamB_leader=[i for i in leaders if i not in teamA_leader]
    return [teamA_leader,teamB_leader]


def rand_player(players):
    number=int(len(players)/2)
    teamA=sample(players,number)
    teamB =[i for i in players if i not in teamA]
    return [teamA,teamB]