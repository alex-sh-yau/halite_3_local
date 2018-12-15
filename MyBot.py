#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction
from hlt.positionals import Position

from hlt.game_map import MapCell

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """


while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    ship_status = {}
    
#    starting_point = game_map.normalize(me.shipyard.position)
    
    for ship in me.get_ships():
    
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))
        
        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"
            
        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(move))
                continue
        elif ship.halite_amount >= constants.MAX_HALITE / 4:
            ship_status[ship.id] = "returning"
        
        
        
        ##############---Move---#################
        
        ### Note for clearing blockages:
        ### if ship.position.directional_offset(direction) is occupied, move in an orthogonal direction
        
        
        
#        if game.turn_number > 375:
#            command_queue.append(
#                ship.move(
#                    random.choice(
#                        [game_map.get_unsafe_moves(ship.position, me.shipyard.position)])))

#                ship.move(
#                    game_map.naive_navigate(ship, me.shipyard.position)))
        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            if ship.halite_amount > 600:
                command_queue.append(
                    ship.move(
                        game_map.naive_navigate(ship, me.shipyard.position)))
            #In the line under: #ship.position != me.shipyard.position and 
            elif ship.halite_amount <= 600:
                pos = ship.position
                maximum = 0
                for i in range(pos.x - 5, pos.x + 5):
                    for j in range (pos.y - 5, pos.y + 5):
                        if game_map[Position(i,j)].halite_amount > maximum:
                            maximum = game_map[Position(i,j)].halite_amount
                            max_pos = Position(i,j)
                command_queue.append(
                    ship.move(
                        game_map.naive_navigate(ship, max_pos)))      
#            else:
#                command_queue.append(
#                    ship.move(
#                        random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
############### How to mark unsafe?????
#            MapCell.mark_unsafe(game_map[ship.position])
#            naive_navigate is doing this
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 300 and me.halite_amount >= 1500 and len(me._ships) * 500 < me.halite_amount and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)


