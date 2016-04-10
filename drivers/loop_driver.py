from driver import Driver
from ai.cf_ai.cheapest_path_ai import CheapestPathAI
from ai.adversarial_ai import AdversarialAI
from ai.cf_ai.greedy_ai import GreedyAI
from ai.random_ai import RandomAI
from ai.cf_ai.cf_random_ai import CFRandomAI
from ai.cf_ai.cf_base_ai import CFBaseAI
from game import Game
from game.classes import FailureCause,Colors
from human_player.console_player import ConsolePlayer
#import subprocess
import csv


#label = subprocess.check_output(["git", "describe"])
p1_data = list()
p2_data = list()

p1 = CFRandomAI("CFRandom")
p2 = CFBaseAI("CFBase")

players = [p1, p2]
use_gui = False
print_debug = False
exception_on_bad_action=True
pause_between_turns = 0
write_to_csv = True


game_repeat = 2
winning_rounds = 0
for i in range(game_repeat):
    driver = Driver(players,use_gui,print_debug,exception_on_bad_action,pause_between_turns)
    driver.run_game()
    player1_info = driver.game.get_player_info(driver.players[0])
    player2_info = driver.game.get_player_info(driver.players[1])

    p1_data.append([driver.players[0].name,player1_info.get_route_points(),player1_info.get_destination_points(),player1_info.get_destination_deductions(),player1_info.draws,player1_info.connects,player1_info.num_cars])
    p2_data.append([driver.players[1].name,player2_info.get_route_points(),player2_info.get_destination_points(),player2_info.get_destination_deductions(),player2_info.draws,player2_info.connects,player2_info.num_cars])



    if driver.get_winner() == p1.name:
        winning_rounds += 1

winning_rates = winning_rounds/game_repeat
#print "Running game on %s " % label
print "after %d rounds of game"%game_repeat
print "p1 winning rates:",
print "p2 winning rates:", 1 - winning_rates

file_name = p1.name + '_vs_' + p2.name +'.csv'
print file_name

if(write_to_csv):
    with open(file_name, 'w') as csvfile:
        fieldnames = ['AI_1','route_points_1','tickets_points_1','ticket_deductions_1','draws_1','connects_1','cars_left_1','AI_2','route_points_2','tickets_points_2','ticket_deductions_2','draws_2','connects_2','cars_left_2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i,datum in enumerate(p1_data):
            #print p1_data[i]
            #print p2_data[i]
            writer.writerow({'AI_1': p1_data[i][0],'route_points_1' : p1_data[i][1],'tickets_points_1': p1_data[i][2],'ticket_deductions_1': p1_data[i][3],'draws_1': p1_data[i][4],'connects_1': p1_data[i][5],'cars_left_1': p1_data[i][6],'AI_2': p2_data[i][0],'route_points_2': p2_data[i][1],'tickets_points_2': p2_data[i][2],'ticket_deductions_2': p2_data[i][3],'draws_2': p2_data[i][4],'connects_2': p2_data[i][5],'cars_left_2': p2_data[i][6]})
