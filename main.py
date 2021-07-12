import os
import sys
import datetime
import json

with open(sys.argv[1], "r") as f:
    s = f.read()
    data = json.loads(s)
print(data)

start_date = datetime.date.fromisoformat(data['start_date'])
end_date = datetime.date.fromisoformat(data['end_date'])
start_time = datetime.time.fromisoformat(data['start_time'])
end_time = datetime.time.fromisoformat(data['end_time'])
print("starts at", start_date, start_time)
print("ends at", end_date, end_time)

days = end_date - start_date + datetime.timedelta(days=1)
days = days.days
hours = datetime.datetime.combine(datetime.date.min, end_time) - datetime.datetime.combine(datetime.date.min, start_time)
hours = hours.seconds//3600
timeslots_per_day = hours//2
total_timeslots = timeslots_per_day * days
print(days, "days,", hours, "hours per day,", timeslots_per_day, "timeslots per day")

n_participants = len(data["participants"])
n_games = n_participants*(n_participants-1)
n_vars = n_games * total_timeslots
print(n_participants, "participants,", n_games, "games in total")
print(n_vars, "variables")

clauses = []

# cada juego ocurre en al menos un timeslot
game_clauses = [[j for j in range(i, i+total_timeslots)] for i in range(1, n_vars+1, total_timeslots)]
clauses += game_clauses

# cada juego ocurre en un solo timeslot
for clause in game_clauses:
    for i in range(len(clause)):
        for j in range(i+1, len(clause)):
            clauses.append([-clause[i], -clause[j]])

# solo ocurre un juego por timeslot
timeslot_vars = [[i+slot for i in range(1, n_vars, total_timeslots)] for slot in range(total_timeslots)]
for var_list in timeslot_vars:
    for i in range(len(var_list)):
        for j in range(i+1, len(var_list)):
            clauses.append([-var_list[i], -var_list[j]])

def get_var(participant_home, participant_visitor, timeslot):
    assert(participant_home != participant_visitor)
    game = participant_visitor
    if participant_visitor > participant_home :
        game -= 1
    n = 1
    n += participant_home * (n_participants-1) * total_timeslots
    n += game * total_timeslots
    n += timeslot
    return n

def get_vars(participant_home, participant_visitor, day):
    n = get_var(participant_home, participant_visitor, day * timeslots_per_day)
    return [n+i for i in range(timeslots_per_day)]

# un participante puede jugar a lo sumo una vez por día
for day in range(days):
    for player1 in range(n_participants):
        acum = []
        for player2 in range(n_participants):
            if player1 == player2:
                continue
            acum += get_vars(player1, player2, day)
            acum += get_vars(player2, player1, day)
        for i in range(len(acum)):
            for j in range(i+1, len(acum)):
                clauses.append([-acum[i], -acum[j]])

# un participante no puede jugar de "local" en dos días consecutivos
# un participante no puede jugar de "visitante" en dos días consecutivos
for player1 in range(n_participants):
    for day in range(days-1):
        local1 = []
        local2 = []
        visitor1 = []
        visitor2 = []
        for player2 in range(n_participants):
            if player1 == player2:
                continue
            local1 += get_vars(player1, player2, day)
            local2 += get_vars(player1, player2, day+1)
            visitor1 += get_vars(player2, player1, day)
            visitor2 += get_vars(player2, player1, day+1)
        for list1, list2 in [(local1, local2), (visitor1, visitor2)]:
            for v1 in list1:
                for v2 in list2:
                    clauses.append([-v1, -v2])

out = "p cnf {} {}\n".format(n_vars, len(clauses))
out += " 0\n".join([" ".join(map(str, clause)) for clause in clauses])+" 0"

open("sat.txt", "a").close()
with open("sat.txt", "w", encoding="utf-8") as f:
    f.truncate()
    f.write(out)

os.system("glucose/parallel/glucose-syrup_static sat.txt {}".format(sys.argv[2]))