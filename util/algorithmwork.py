# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random
from django.contrib.auth.models import User
from adventure.models import Player, Room
from django.db import models

# Room.objects.all().delete()


# class Room():
#     def __init__(self, id, name, description, x, y):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.n_to = None
#         self.s_to = None
#         self.e_to = None
#         self.w_to = None
#         self.x = x
#         self.y = y
#     def __repr__(self):
#         # if self.e_to is not None:
#         #     return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
#         return f"({self.x}, {self.y})"
#     def connect_rooms(self, connecting_room, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
#         reverse_dir = reverse_dirs[direction]
#         setattr(self, f"{direction}_to", connecting_room)
#         setattr(connecting_room, f"{reverse_dir}_to", self)

#     #unused function
#     def get_room_in_direction(self, direction):
#         '''
#         Connect two rooms in the given n/s/e/w direction
#         '''
#         return getattr(self, f"{direction}_to")
title_adj = ["Dank","Dark","Creepy","Shrouded","Old","Uneven","Disheveled","Bloodstained","Unkempt","Cluttered","Gloomy","Lightless","Obscured","Pitch-Black"]
title_noun = ["Corridor", "Corridor", "Corridor", "Hall","Stairway","Attic", "Bathroom", "Boudoir", "Conservatory", "Hallway", "Hallway", "Hallway", "Library", "Parlor", "Nursery", "Den", "Study", "Foyer", "Vestibule", "Basement"]
description_start = ["You approach a(n)","You step into a(n)", "You warily wander towards a(n)", "You enter a(n)", "You find a(n)", "You go into a(n)"]
description_end = ["There isn't much to see here.", "It's dark, and damp.", "You hear something shriek as you step forward, you'd better keep moving.", "It's very dark in here.", "You begin to feel anxious, you must keep searching.", "This might be the right way.", "Who knows what lies ahead?", "Keep going."]

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        x = (size_x//2) 
        y = (size_y//2)
        room_count = 0

        # Start generating rooms to the east
        direction = [-1, 1]  # -1 = south or west, 1 = north or east
        vertical_or_horizontal = ['x', 'y']

        firstroom = Room(room_count, "Dark Atrium", "You begin your journey in a wide open atrium, covered in the shadow of night. Choose your path carefully going forward.", x, y)
        self.grid[y][x] = firstroom
        room_count += 1

        firstroom.save()

        # While the room count is less than the current number of rooms
        # Navigate randomly (within the set grid boundary) and create rooms/connections accordingly
        previous_room = firstroom
        
        while room_count < num_rooms:
            ## Pick a direction (x or y) for movement
            ## Generate -1 or 1 randomly
            hit_a_wall = False
            one_or_negative_one = random.choice(direction)
            x_or_y = random.choice(vertical_or_horizontal)

            current_title = f"{random.choice(title_adj)} {random.choice(title_noun)}"
            current_description = f"{random.choice(description_start)} {random.choice(description_end)}"
        
            if x_or_y == 'x':    #we are moving east or west

                if one_or_negative_one == 1: #moving east
                    if x < (size_x - 1):
                        room_direction = "e"
                        x += 1
                    else:
                        hit_a_wall = True

                else:    #moving west
                    if x > 0:
                        room_direction = "w"
                        x -= 1
                    else:
                        hit_a_wall = True

            elif x_or_y == 'y':  #we are moving north or south

                if one_or_negative_one == 1: #moving north
                    if y < (size_y - 1):
                        room_direction = "n"
                        y += 1
                    else:
                        hit_a_wall = True

                else: #moving south
                    if y > 0:
                        room_direction = "s"
                        y -= 1
                    else:
                        hit_a_wall = True

            #check to see if there is a room after moving
            if hit_a_wall == False and self.grid[y][x] is not None:
                #connect the room to the previous one
                if previous_room is not None:
                    previous_room.connect_rooms(self.grid[y][x], room_direction)
                previous_room = self.grid[y][x]

            #if there is no room after moving
            elif hit_a_wall == False and self.grid[y][x] is None:
                #create a room
                room = Room(title=current_title, description=current_description, x=x, y=y)
                room.save()

                #save the room in the grid
                self.grid[y][x] = room

                #connect the room to the previous one
                if previous_room is not None:
                    previous_room.connect_rooms(room, room_direction)
                
                #because we created a room, increment room_count and update previous_room
                previous_room = room
                room_count += 1
            else:
                #if we hit this, we hit a wall. So try choosing another direction
                pass

        players = Player.objects.all()
        for p in players:
            p.currentRoom=firstroom.id
            p.save()

 # def print_rooms(self):
    #     '''
    #     Print the rooms in room_grid in ascii characters.
    #     '''

    #     # Add top border
    #     str = "# " * ((3 + self.width * 5) // 2) + "\n"

    #     # The console prints top to bottom but our array is arranged
    #     # bottom to top.
    #     #
    #     # We reverse it so it draws in the right direction.
    #     reverse_grid = list(self.grid) # make a copy of the list
    #     reverse_grid.reverse()
    #     for row in reverse_grid:
    #         # PRINT NORTH CONNECTION ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.n_to is not None:
    #                 str += "  |  "
    #             else:
    #                 str += "     "
    #         str += "#\n"
    #         # PRINT ROOM ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.w_to is not None:
    #                 str += "-"
    #             else:
    #                 str += " "
    #             if room is not None:
    #                 str += f"{room.id}".zfill(3)
    #             else:
    #                 str += "   "
    #             if room is not None and room.e_to is not None:
    #                 str += "-"
    #             else:
    #                 str += " "
    #         str += "#\n"
    #         # PRINT SOUTH CONNECTION ROW
    #         str += "#"
    #         for room in row:
    #             if room is not None and room.s_to is not None:
    #                 str += "  |  "
    #             else:
    #                 str += "     "
    #         str += "#\n"

    #     # Add bottom border
    #     str += "# " * ((3 + self.width * 5) // 2) + "\n"

    #     # Print string
    #     print(str)
   

w=World()
num_rooms = 20
width = 5
height = 5
w.generate_rooms(width, height, num_rooms)


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
