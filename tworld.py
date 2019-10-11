#!/usr/bin/env python3

import os
import sys
import json
import uuid
import shlex
import random
import readline
import traceback

DEBUG = True

def debug(*messages):
    if DEBUG:
        print(*messages)

def load_settings(filepath):
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        print("Could not load setting file '%s'!" % filepath, file=sys.stderr)
        sys.exit(1)
    
    with open(filepath) as settings_file:
        json_text = settings_file.read()
        settings = json.loads(json_text)

    return settings

def main():
    import pprint
    
    # Load the settings file
    settings = load_settings("Rooms.txt")
    pprint.pprint(settings)

    session = tui_session()
    session.get_username()
    session.start_game(settings)

    print(session.game.settings.get("welcome", ""))

    while session.game.is_active:
        cmd = session.get_command()
        cmd.run(session)

class user:
    def __init__(self, name=""):
        if not name:
            self.name = "Player%i" % random.randrange(1000, 9999)
        else:
            self.name = name

class tui_session:
    def __init__(self):
        self.user = user()
        self.game = None

    def get_input(self, prompt):
        return input(prompt)

    def print(self, text):
        print(text)
    
    def get_username(self):
        self.user.name = self.get_input("What is your name? ")

    def parse_line(self, line):
        debug("parsing '%s'" % line)
        line_parts = shlex.split(line)
        command = line_parts[0]
        args = line_parts[1:]
        user_input = {"command": command, "args": args}
        debug(user_input)
        return {"command": command, "args": args}
    
    def get_command(self, prompt="> "):
        line = self.get_input(prompt)
        line_parts = self.parse_line(line)
        cmd = command(line_parts["command"], line_parts["args"])
        return cmd

    def start_game(self, config):
        self.game = game(config)
        self.game.add_player
        self.game.is_active = True

class game:
    def __init__(self, config):
        self.is_active = False
        # Set game settings
        self.settings = config["settings"]
        del config["settings"]
        # Create game map
        self.game_map = game_map(config)
        if "spawn_char" in self.settings:
            self.game_map._spawn_char = self.settings["spawn_char"]

    def add_player(player, coordinates=None):
        # If coordinates are given, use those
        if coordinates:
            pass
        # add player to map>characters
        pass
    
    class InvalidPlayerLocation(Exception): pass

class game_map:
    _spawn_char = "_"
    
    def __init__(self, config):
        self.tiles = config.get("map", [])
        self.entities = {
            "items": config.get("items", []),
            "paths": config.get("paths", []),
            "puzzles": config.get("puzzles", []),
            "monsters": config.get("monsters", []),
            "structures": config.get("structures", [])
        }
        self.characters = dict() # {Character1: {viewed: [(x1, y1), (x2, y2), ...], location: (x, y)}, Character2: ...}

    @property
    def spawn_points(self):
        coordinates = list()
        # Find all spawn_point_char's
        for y in len(self.tiles):
            for x in len(self.tiles):
                if self.tiles[y][x] == _spawn_char:
                    coordinates.append((x, y))
        return coordinates

    def get_entity_at_coordinates(coordinates):
        if self.is_valid_location(coordinates):
            pass
    
    def get_entity(entity_id):
        entities = self.get_entities()
        if entity_id not in entities:
            raise InvalidEntity("Invalid entity id '%i'" % entity_id)
        return entities[entity_id]
    
    def get_entities(self):
        entities = dict()
        for key in self.entities:
            for entity in self.entities[key]:
                if "id" in entity:
                   entities["id"] = entity
        return entities
    
    def edit_tile(self, x, y, entity_id):
        if entity_id not in self.get_entities():
            raise InvalidEntity("Invalid entity id '%i'" % entity_id)
        try:
            self.tiles[y][x] = entity_id
        except IndexError:
            raise InvalidCoordinates("Invalid coordinates: (%i, %i)" % (x, y))

    def player_can_move_to(self, coordinates):
        pass
    
    def move_character(self, character, x, y):
        pass

    def is_valid_location(self, coordinates):
        if len(coordinates) != 2:
            return False
        try:
            self.tiles[coordinates[1], coordinates[0]]
        except IndexError:
            return False
        return True

    class InvalidCoordinates(Exception): pass
    class InvalidEntity(Exception): pass

class entity:
    def __init__(self, name, description, visible=True):
        self.uid = uuid.uuid4()
        self.name = name
        self.description = description

class character(entity):
    def __init__(self, name, description="", visible=True, health=100, attack=20, session=None):
        entity.__init__(self, name, description, visible)
        self.name = name
        self.session = session
        self.description = description
        self.health = health
        self.attack = attack

class item(entity):
    def __init__(self, name, description="", visible=True):
        entity.__init__(self, name, description, visible)

class structure(entity):
    pass

class command:
    def __init__(self, name, args=[]):
        self.name = name
        self.args = args
        self.func = commands.find_command(name)
    
    def run(self, session):
        self.func(session, *self.args)
    
    @property
    def help(self):
        return self._func.__doc__

class commands:
    def find_command(name):
        if hasattr(commands, "do_" + name):
            return getattr(commands, "do_" + name)
        raise commands.InvalidCommand("Invalid command: %s" % name)
    
    def do_help(session, *args):
        """Get helpful information about the game or a specific command."""
        if len(args) > 0:
            cmd_name = args[0]
            try:
                cmd = commands.find_command(cmd_name)
            except commands.InvalidCommand:
                return "No such command '%s'" % cmd_name
            return cmd.__doc__
        return "This is the help command"
    
    def do_up(session, *args):
        """Move up in the map grid."""
        pass
    
    def do_left(session, *args):
        """Move left in the map grid."""
        pass
    
    def do_right(session, *args):
        """Move right in the map grid."""
        pass
    
    def do_down(session, *args):
        """Move down in the map grid."""
        pass

    def do_map(session, *args):
        """View the discovered portions of the map."""
        pass
    
    class InvalidCommand(Exception): pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting...")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)