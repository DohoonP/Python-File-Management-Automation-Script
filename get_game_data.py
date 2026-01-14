#  Assumptions:

#  - data directory contains many files and directories
#  - you are only interested in the games contaiend in this directory
#  - each game is stored in a directory that contains the word "game"
#  - each game directory contains a single .go file that must be compiled before it can be run


#  Project Steps/Requirements:

#  - Find all game directories from /data
#  - Create a new /games directory 
#  - Copy and remove the "game" suffix of all games into the /games directory
#  - Create a .json file with the information about the games
#  - Compile all of the game code 
#  - Run all of the game code-

import os                           
import json
import shutil                       # copy and overwrite operation
from subprocess import PIPE, run    # allowing to run any terminal command (ex compile go code)
import sys                          # access to command line arguments (ex python get_game_data.py /data /new_games)

# what we are looking for in our directory 

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]

# walk thru the source directory to look at all the files and directories and then match any directories that have this game 

def find_all_game_paths(source):
    game_paths = []
    
# 'dirs' gives all the names of directories not the paths to those directories
# for later use

    for root, dirs, files in os.walk(source):           # walk recursively through whatever the source directory is that you pass to this walk command
                                                        # it's going to give you the root directories and the files that are contained in the current level that it's walking through.
                                                        # it'll look in data, but then it would after looking in data, look inside of blank, then look inside of hello world
                                                        # and look inside of rock, paper, scissors game. It will look through all of those directories.
                                                        
        for directory in dirs:                          # we need to look through all of the directories
            if GAME_DIR_PATTERN in directory.lower():   # get the name of my directory and match that against my game dir pattern. / .lower() just in case of capital letters
                path = os.path.join(source, directory)
                game_paths.append(path)                 # adding path to array (or list of paths)
                                                        # append():appends an element to the end of the list
                                
        break                                           # since we only care about the first kind of top level directory, we only really need to run this command one time.

    return game_paths                                   # only checking names of directories


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)


def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break

        break

    if code_file_name is None:
        return

    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command, path)


def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result", result)

    os.chdir(cwd)



def main(source, target):
    cwd = os.getcwd()   #cwd = current working directory   // getcwd() means the directory we ran this python file from
    source_path = os.path.join(cwd, source)         # os.path.join() = to create paths
    target_path = os.path.join(cwd, target)

    game_paths = find_all_game_paths(source_path)   # game_paths -> ['C:\Users\godba\Desktop\python practice\data\hello_world_game' 'C:\Users ... \data\rock_paper_scissors_game' 'C:\Users ... \data\simon_says_game']
    new_game_dirs = get_name_from_paths(game_paths, "_game")
 
    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)



# only want to execute the main script here if I am running this Python file directory directly

# if I'm not directly running this python file, I don't want to be executing the code that's going to run through and do all of our operations.

# this just checks that you ran the file directly and it won't execute anything in here


if __name__ == "__main__":      # ex in terminal, get_game_data.py data new_data
    args = sys.argv             # args = ['get_game_data.py', 'data', 'new_data']
    if len(args) != 3:          # number of arguments
        raise Exception("You must pass a source and target directory - only.")

    source, target = args[1:]   # source = source directory  /   target = new directory
                                # to strip off the name of the Python file, which we don't want, 
                                # and just get the two arguments here and then store them in separate variables. 
                                
    main(source, target)
