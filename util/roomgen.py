import random
from django.contrib.auth.models import User
from adventure.models import Player, Room
from django.db import models

Room.objects.all().delete()

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
    room_count = 0
    direction = [-1, 1]
    vertical_or_horizontal = ['x', 'y']
    firstroom = Room(room_count, "Starting Room", "This is the first room in the dungeon.", x, y)
    self.grid[y][x] = firstroom
    room_count += 1
    firstroom.save()
    previous_room = firstroom
    while room_count < num_rooms:
      hit_a_wall = False
      one_or_negative_one = random.choice(direction)
      x_or_y = random.choice(vertical_or_horizontal)
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
        room = Room(title="A Generic Title for a Room", description="This is a room.", x=x, y=y)
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
num_rooms = 20
width = 5
height = 5
world.generate_rooms(width, height, num_rooms)

print(f"\n\nWorld\n  height: {height}\n  width: {width},\n  num_rooms: {num_rooms}\n")
