import random
from django.contrib.auth.models import User
from adventure.models import Player, Room
from django.db import models

Room.objects.all().delete()
title_adj = ["Dank","Dark","Creepy","Shrouded","Old","Uneven","Disheveled","Bloodstained","Unkempt","Cluttered","Gloomy","Lightless","Obscured","Pitch-Black"]
title_noun = ["Corridor", "Corridor", "Corridor", "Hall","Stairway","Attic", "Bathroom", "Boudoir", "Conservatory", "Hallway", "Hallway", "Hallway", "Library", "Parlor", "Nursery", "Den", "Study", "Foyer", "Vestibule", "Basement"]
description_start = ["You approach a(n)","You step into a(n)", "You warily wander towards a(n)", "You enter a(n)", "You find a(n)", "You find your way into a(n)"]
description_end = ["There isn't much to see here.", "It's dark, and damp.", "You hear something shriek as you step forward, you'd better keep moving.", "It's very dark in here.", "You begin to feel anxious, you must keep searching.", "This might be the right way.", "Who knows what lies ahead?", "Keep going."]
class World:
  def __init__(self):
    self.grid = None
    self.width = 0
    self.height = 0
  def generate_rooms(self, size_x, size_y, num_rooms):
    self.grid = [None] * size_y
    self.width = size_x
    self.height = size_y
    for i in range( len(self.grid) ):
      self.grid[i] = [None] * size_x
    x = (size_x//2) 
    y = (size_y//2)
    start_x = x
    start_y = y
    room_count = 0
    direction = [-1, 1]
    vertical_or_horizontal = ['x', 'y']
    firstroom = Room(room_count, "Dark Atrium", "You begin your journey in a wide open atrium, covered in the shadow of night. Choose your path carefully going forward.", x, y)
    self.grid[y][x] = firstroom
    room_count += 1
    firstroom.save()
    previous_room = firstroom
    while room_count < num_rooms:
      hit_a_wall = False
      one_or_negative_one = random.choice(direction)
      x_or_y = random.choice(vertical_or_horizontal)
      current_title_noun = random.choice(title_noun)
      current_title_adj = random.choice(title_adj)
      current_title = f"{current_title_adj} {current_title_noun}"
      current_description = f"{random.choice(description_start)} {current_title_noun}. {random.choice(description_end)}"
      if x_or_y == 'x':
        if one_or_negative_one == 1:
          if x < (size_x - 1):
            room_direction = "e"
            x += 1
          else:
            hit_a_wall = True
        else: 
          if x > 0:
            room_direction = "w"
            x -= 1
          else:
            hit_a_wall = True
      elif x_or_y == 'y':
        if one_or_negative_one == 1:
          if y < (size_y - 1):
            room_direction = "n"
            y += 1
          else:
            hit_a_wall = True
        else:
          if y > 0:
            room_direction = "s"
            y -= 1
          else:
            hit_a_wall = True
      if hit_a_wall == False and self.grid[y][x] is not None:
        if previous_room is not None:
          previous_room.connect_rooms(self.grid[y][x], room_direction)
        previous_room = self.grid[y][x]
      elif hit_a_wall == False and self.grid[y][x] is None:
        room = Room(title=current_title, description=current_description, x=x, y=y)
        room.save()
        self.grid[y][x] = room
        if previous_room is not None:
          previous_room.connect_rooms(room, room_direction)
        previous_room = room
        room_count += 1
      else:
        pass
    players = Player.objects.all()
    for p in players:
      p.currentRoom=firstroom.id
      p.save()

world=World()
num_rooms = 150
width = 15
height = 15
world.generate_rooms(width, height, num_rooms)

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
