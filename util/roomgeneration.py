# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.
import random

class Room:
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y
    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


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

        room = Room(room_count, "A Generic Title for a Room", "This is a room.", x, y)
        self.grid[y][x] = room
        room_count += 1

        # While the room count is less than the current number of rooms
        # Navigate randomly (within the set grid boundary) and create rooms/connections accordingly
        previous_room = room
        
        while room_count < num_rooms:
            # print("STARTING AT", x, y)
            # print("Room count: ", room_count)
            ## Pick a direction (x or y) for movement
            ## Generate -1 or 1 randomly
            hit_a_wall = False
            one_or_negative_one = random.choice(direction)
            x_or_y = random.choice(vertical_or_horizontal)

        
            if x_or_y == 'x':    #we are moving east or west
                if one_or_negative_one == 1: #moving east
                    if x < (size_x - 1):
                        room_direction = "e"
                        x += 1
                        # print("Moved to: ", x, y)
                    else:
                        # print('ran into a wall')
                        # print("Moved to: ", x, y)
                        hit_a_wall = True

                else:    #moving west
                    if x > 0:
                        room_direction = "w"
                        x -= 1
                        # print("Moved to: ", x, y)
                    else:
                        # print('ran into a wall')
                        # print("Moved to: ", x, y)
                        hit_a_wall = True

            elif x_or_y == 'y':  #we are moving north or south
                if one_or_negative_one == 1: #moving north
                    if y < (size_y - 1):
                        room_direction = "n"
                        y += 1
                        # print("Moved to: ", x, y)
                    else:
                        # print('ran into a wall')
                        # print("Moved to: ", x, y)
                        hit_a_wall = True
                else: #moving south
                    if y > 0:
                        room_direction = "s"
                        y -= 1
                        # print("Moved to: ", x, y)
                    else:
                        # print('ran into a wall')
                        # print("Moved to: ", x, y)
                        hit_a_wall = True

            #check to see if there is a room after moving
            if hit_a_wall == False and self.grid[y][x] is not None:
                # print('There is a room here')
                #connect the room to the previous one
                if previous_room is not None:
                    previous_room.connect_rooms(self.grid[y][x], room_direction)
                previous_room = self.grid[y][x]

            #if there is no room after moving
            elif hit_a_wall == False and self.grid[y][x] is None:
                #create a room
                # print('Creating a new room at, ', x, y)
                room = Room(room_count, "A Generic Title for a Room", "This is a room.", x, y)

                #save the room in the grid
                self.grid[y][x] = room

                #connect the room to the previous one
                if previous_room is not None:
                    previous_room.connect_rooms(room, room_direction)
                
                #because we created a room, increment room_count and update previous_room
                previous_room = room
                room_count += 1
            else:
                # print("Final Else statement")
                # print("Self.grid", self.grid[y][x])
                pass



    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 150
width = 20
height = 20
w.generate_rooms(width, height, num_rooms)
w.print_rooms()


print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
