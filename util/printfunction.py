
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