# Author: Rouvr (https://github.com/Rouvr/)
# This file is free to use or modify.
# This script is used to teleport offline players in Minecraft by editing their player data files.
# Edit functionality under PlayerTeleporter.edit_playerdata() 
# nbtlib required

"""
This script is used to teleport offline players in Minecraft by editing their player data files.
Classes:
    PTParser: Parses command-line arguments for player data processing.
    PlayerTeleporter: Handles the teleportation of players by editing their player data files.
PTParser:
    Methods:
        parse_input(argv): Parses command-line arguments and returns them as a dictionary.
        _parse_double(value): Helper function to parse doubles, including converting integers to doubles.
        _parse_dimension(value): Helper function to parse the dimension argument.
PlayerTeleporter:
    Attributes:
        usage (str): Usage string for the script.
        data_dir (str): Directory containing player data files.
        coordinates (tuple): Tuple containing the coordinates (x, y, z), dimension, pitch, and yaw.
        whitelist (str): Path to the whitelist file.
        blacklist (str): Path to the blacklist file.
        player_regex (Pattern): Regular expression pattern to match player data files.
    Methods:
        __init__(args): Initializes the PlayerTeleporter with the provided arguments.
        validate_input(): Validates the input arguments.
        edit_playerdata(): Edits the player data files to teleport players.
        teleport_player(player_data): Teleports a player to the specified coordinates and dimension.
"""

import typing
import os
import nbtlib
from nbtlib.tag import Double, Int, Float, List
import re
import sys
import argparse


class PlayerTeleporter():
    usage = "file data_dir x y z dimension [pitch] [yaw] [--whitelist=whitelist_file] [--blacklist=blacklist_file]"

    def __init__(self, args: typing.Dict):
        self.data_dir = args.get('data_dir', None)
        self.coordinates = (args.get('x', 0.0), args.get('y', 0.0), args.get('z', 0.0), args.get('dimension', 0), args.get('pitch', 0.0), args.get('yaw', 0.0))
        self.whitelist = args.get('whitelist', None)
        self.blacklist = args.get('blacklist', None) 
        self.player_regex = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.dat$")
        self.validate_input()


    def validate_input(self):
        if not self.data_dir:  
            print(f"Usage: {PlayerTeleporter.usage}")
            raise ValueError("data_dir is required")

        #check if data_dir is a directory
        if not os.path.isdir(self.data_dir):
            print(f"Enter a valid directory : {self.data_dir} is not a valid directory")
            raise ValueError("data_dir is not a directory")
        
        #check if whitelist and blacklist are valid files
        if self.whitelist and not os.path.isfile(self.whitelist):
            print(f"Enter a valid whitelist file : {self.whitelist} is not a valid file")
            raise ValueError("whitelist is not a valid file")
        
        if self.blacklist and not os.path.isfile(self.blacklist):
            print(f"Enter a valid blacklist file : {self.blacklist} is not a valid file")
            raise ValueError("blacklist is not a valid file")
        

    def edit_playerdata(self):
        records_count = 0
        for player_file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, player_file)

            #Only open files with player data
            if not self.player_regex.fullmatch(player_file):
                continue

            #Load data
            try:
                player_data = nbtlib.load(file_path)
            except Exception as e:
                print(f"Error loading player data for {player_file} : {e}")
                continue

            #Automatically exclude blacklisted players if provided blacklist
            #Use whitelist only if one is provided
            if self.blacklist and player_file in self.blacklist:
                continue   

            if self.whitelist and not player_file in self.whitelist:
                continue
            
            self.teleport_player(player_data)

            #---------------------------------------------------------------------------------------------
            #For custom actions add functions here ie. heal player
            #self.heal_player(player_data)
            #---------------------------------------------------------------------------------------------

            try:
                player_data.save(file_path)
                records_count += 1
            except Exception as e:
                print(f"Error saving player data for {player_file} : {e}")

        print(f"Edited {records_count} players")

    def teleport_player(self, player_data):        
        # Ensure the position and rotation lists are properly formatted NBT lists
        player_data['Pos'] = List[Double]([Double(self.coordinates[0]), Double(self.coordinates[1]), Double(self.coordinates[2])])
        player_data['Dimension'] = Int(self.coordinates[3])
        player_data['Rotation'] = List[Float]([Float(self.coordinates[4]), Float(self.coordinates[5])])
        #print(f"Teleported player to {self.coordinates[:3]} in dimension {self.coordinates[3]} with rotation {self.coordinates[4:]}")

class PTParser():
    #This class was done with the help of ChatGPT, parsing arguments for player data processing

    #alternative to passing dimension by its ID
    dimension_dict = {"overworld": 0, "nether": 1, "end": 2}
    
    def parse_input(self, argv):
        # Create an argument parser
        parser = argparse.ArgumentParser(description="Parse command-line arguments for player data processing.")
        
        # Required arguments
        parser.add_argument('data_dir', type=str, help="Directory containing player data files")
        parser.add_argument('x', type=self._parse_double, help="X coordinate (must be a double or int)")
        parser.add_argument('y', type=self._parse_double, help="Y coordinate (must be a double or int)")
        parser.add_argument('z', type=self._parse_double, help="Z coordinate (must be a double or int)")
        parser.add_argument('dimension', type=self._parse_dimension, help="Dimension (integer in [0,1,2] or string in ['overworld', 'end', 'nether'])")
        
        # Optional arguments
        parser.add_argument('pitch', nargs='?', type=self._parse_double, help="Player pitch (optional, must be a double or int)")
        parser.add_argument('yaw', nargs='?', type=self._parse_double, help="Player yaw (optional, must be a double or int)")
        parser.add_argument('--whitelist', type=str, help="Path to the whitelist file (optional)")
        parser.add_argument('--blacklist', type=str, help="Path to the blacklist file (optional)")

        try:
            # Parse the arguments
            args = parser.parse_args(argv)

            return {
                'data_dir': args.data_dir,
                'x': args.x,
                'y': args.y,
                'z': args.z,
                'dimension': args.dimension if args.dimension else 0,
                'pitch': args.pitch if args.pitch else 0.0,
                'yaw': args.yaw if args.yaw else 0.0,
                'whitelist': args.whitelist,
                'blacklist': args.blacklist
            }

        except argparse.ArgumentTypeError as e:
            print(f"Argument error: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def _parse_double(self, value):
        try:
            return float(value)  
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid double value: {value}")

    def _parse_dimension(self, value):
        try:
            # Check if it's an integer dimension (0 = overworld, 1 = nether, 2 = end)
            dim_int = int(value)
            if dim_int in [0, 1, 2]:
                return dim_int
            else:
                raise argparse.ArgumentTypeError(f"Invalid dimension integer: {value}")
        except ValueError:
            # Otherwise, check if it's a valid dimension string
            if value.lower() in ["overworld", "nether", "end"]:
                return self.dimension_dict[value.lower()]
            else:
                raise argparse.ArgumentTypeError(f"Invalid dimension string: {value}")



if __name__ == "__main__":
    # Parse the command-line arguments
    args = PTParser().parse_input(sys.argv[1:])
    if not args:
        print(f"Usage: {PlayerTeleporter.usage}")
        sys.exit(1)

    # Initialize the PlayerTeleporter with the parsed arguments
    pt = PlayerTeleporter(args)
    # Edit the player data files to teleport players
    pt.edit_playerdata()

