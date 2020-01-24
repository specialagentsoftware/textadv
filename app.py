import cmd
import textwrap
import sys
import os
import time
import random
from pyfiglet import Figlet
import texttable
from clint.textui import puts, colored, indent
import spacy
import textwrap

# Constants
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
NEXTLOCATION = 'nextlocation'
SOLVED_MESSAGE = 'message'


room_solved = {'it': False, 'processing': False, 'admin': False,
               'warehouse': False, 'smoking area': False, 'parkinglot': False, }

columns, rows = os.get_terminal_size(1)
nlp = spacy.load("en_core_web_sm")

troll = {
    'it': {
        DESCRIPTION: "You awaken to find yourself sitting in a dingy lackluster IT cave. There are rats, holes in the ceiling and souless IT Zombies shuffling around.\nThere is a faint smell of rancid feces. You realize immediately that you are smelling the code.\nYou are baffled as to what choices you must have made in your life to make this your end.\nIn the distance you can hear a free range pull request bellow.\n",
        INFO: "Wild packs of clueless administrators are ambling stupidly around trying to find someone to blame for the poor performance of the business.\n",
        PUZZLE: "Frantically, the shell of a former IT director zombie runs up to you. He leans in expectantly.\nYou can see clearly that his backbone is broken.\nYou realize it's not important though,as he never used it.\nYou think you know the only phrase that will satisfy him. What is it?\n",
        SOLVED: "pull request",
        SOLVED_MESSAGE: "Upon hearing the magic words that will set him free, the IT director zombie breaks into maniacle laughter and begins to emit masterbasion sounds.\nHe knows his administrative masters will be soo happy.\nThe IT Director Zombie disentigrates into a puddle of the administrators creampies.\nVery loudly the doors to your IT coffin have swung open and you are staring out into the black abyss\nYou move forward, as anything has to be better than the IT cave.",
        NEXTLOCATION:'processing',
    },
    'processing': {
        DESCRIPTION: "You find yourself standing in the middle of a large wide open area.\nYou can smell urine, wait.. that's meth.\nOk this must be processing.\nYou have heard tales about this place but no living IT employee has ever seen it.\n",
        INFO: "As you round a corner, you hear the growl of a truly fearsome beast.\nYou can hardly believe your luck. You are standing right in front of an OZ.\n",
        PUZZLE: "The OZ steps forward, letting lose a powerful roar\nThe chest beating subsides for a moment.\nThe OZ then asks you a question: 'What is the most evil form of communication?'\n",
        SOLVED: "electronic",
        SOLVED_MESSAGE: "The OZ has heard your answer, and is pleased.He decides not to feast upon your bowels. Lovingly, he tosses you through a wall.\n",
        NEXTLOCATION:'admin',
    },
    'admin': {
        DESCRIPTION: "You awaken sometime later to find all of your clothing gone.\n For some reason you feel like you shit a motorcycle.\nYour ass burns horribly.\nWith a powerful shot of fear, you realize why.\nYou are in admin now.",
        INFO: "A rather large and ungainly throne made of strung out employees sits in the middle of the atrium.\nUpon that throne sits a powerful WARDon.\nHis sexual harrassment powers are world famous.\n",
        PUZZLE: "The WARDon takes a momentary interest in you.\n However, when he determines you dont have a vagina he looks away.\n",
        SOLVED: "vagina",  # Will work after you solve all other puzzles?
        SOLVED_MESSAGE: "You had never until today realized that not having a vagina would come in so handy\nYou notice a small portal at the back of the room.\nYou make your way through it into the unknown.\n",
        NEXTLOCATION:'warehouse',
    },
    'warehouse': {
        DESCRIPTION: "You find yourself in lush woodlands, bursting with wildlife\nand a cacaphony of chirping.",
        INFO: "A rough-looking man sits next to a little cabin.\nHis eyes are glued to bird-watching binoculars.",
        PUZZLE: "The rough-looking man asks,\n'What is the airspeed of an unladen European swallow?'",
        SOLVED: "25",
        SOLVED_MESSAGE: "Upon hearing the magic words that will set him free, the IT director zombie breaks into maniacle laughter and begins to emit masterbasion sounds.\nHe knows his administrative masters will be soo happy\n",
        NEXTLOCATION:'smoking area',
    },
    'smoking area': {
        DESCRIPTION: 'You find yourself encompassed by strong winds and sandy dunes.',
        INFO: 'A terrified looking man is hiding among some cacti.',
        PUZZLE: "The fearful man asks,\n'What can measure time, while eventually, all crumbles to it?'",
        SOLVED: "sand",
        SOLVED_MESSAGE: "Upon hearing the magic words that will set him free, the IT director zombie breaks into maniacle laughter and begins to emit masterbasion sounds.\nHe knows his administrative masters will be soo happy\n",
        NEXTLOCATION:'parkinglot',
    },
    'parkinglot': {
        DESCRIPTION: "You find yourself next to a still, soothing pond.\nAn old man gazes at a table nearby.",
        INFO: "You greet the old man.\nHe beckons you to look at the intricate twelve-sided table.",
        PUZZLE: "Each side of the table has a unique symbol, though all are familar to you.\nWhich symbol do you sit by?",
        SOLVED: "",  # Should be your astrological sign.
        SOLVED_MESSAGE: "Upon hearing the magic words that will set him free, the IT director zombie breaks into maniacle laughter and begins to emit masterbasion sounds.\nHe knows his administrative masters will be soo happy\n",
        NEXTLOCATION:'free',
    },
    'free': {
        DESCRIPTION: "You have done it, you can smell the fresh air. Well, it's Corbin. You are out of the unspeakable hell.",
        INFO: "As you walk away from this nuclear cesspool of a fuck hole, you relax soo much that you shit all over yourself.",
        PUZZLE: "",
        SOLVED: "",  # Should be your astrological sign.
        SOLVED_MESSAGE: "",
        NEXTLOCATION:'',
    }
}


class player:
    def __init__(self):
        self.name = ''
        self.special = ''
        self.role = ''
        self.location = 'it'
        self.won = False
        self.solves = 0
        self.hp = 5
        self.mp = 0


# Player setup
player1 = player()

# Build the title screen


def splashscreen():
    os.system('cls' if os.name == 'nt' else 'clear')
    custom_fig = Figlet(font='standard', width=columns, justify='center')
    print()
    slow_print(
        "  Can you escape the most prolific hell since Hitler's Germany?", 0.05)
    time.sleep(2.0)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored.blue(custom_fig.renderText('Troll')))
    time.sleep(1.0)
    print(colored.yellow(custom_fig.renderText('Presents')))
    time.sleep(1.0)
    title_screen()


def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    custom_fig = Figlet(font='slant', width=columns, justify='center')
    print(colored.red(custom_fig.renderText('Escape Troll !')))
    bodyfig = Figlet(font='term', width=columns, justify='center')
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText(
        '# Welcome to the most challenging game to be invented since troll search #'))
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText(
        ".: Play :."))
    print(bodyfig.renderText(
        ".: Help :."))
    print(bodyfig.renderText(
        ".: Quit :."))
    title_screen_options()

# Define options and handle input


def title_screen_options():
    option = getinput()
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("quit"):
        sys.exit()
    elif option.lower() == ("help"):
        help_menu()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Invalid command, please try again.")
        option = getinput()
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("quit"):
            sys.exit()
        elif option.lower() == ("help"):
            help_menu()


# collect data and setup game
def setup_game():
    os.system('cls' if os.name == 'nt' else 'clear')
    bodyfig = Figlet(font='term', width=columns, justify='center')
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText('# Before we begin, there are some things we need to know #'))
    print(bodyfig.renderText('#' * 74))
    print("")
    slow_print("What be yar name, maytee?\n", 0.05)
    name = getinput()
    if(name):
        player1.name = name
        slow_print("Ahoy, "+name+"\n", 0.05)
        slow_print("Ah..sorry for the pirate thing. I am not sure what came over me.\n", 0.05)
        slow_print("I mean, I don't even like pirates. I am terrified by them really.\n", 0.05)
        slow_print("They smell of walnuts.\n",0.05)
        slow_print("It is weird though because, I like walnuts.\n",0.05)
        slow_print("Honestly, I am not sure what it is exactly about pirates I find disagreeable.\n",0.05)
        slow_print("My mom used to bake walnuts, before the accident actually.\nYou know on second thought, I really like the smell of walnuts.\n",0.05)
        slow_print("Wait..where were we, oh yes. I need some more information from you.\n",0.05)
    else:
        slow_print(
            "I am going to need a name, super chief. You are looping until I get one\n", 0.05)
        setup_game()
    slow_print("What is your profession?.\n",0.05)
    profession = getinput()
    player1.role = profession
    if(profession):
        player1.role = profession
        slow_print("So you are an , "+profession+ "?..cool. That will come in handy here at troll.\n", 0.05)
    else:
        slow_print("I am going to need a profession, big shoots. You are looping until I get one\n", 0.05)
        setup_game()
    slow_print("Just as you were thinking that you kind of liked it here, everything starts to get all 'raptory'.\nAll of a sudden, Your arms are far too short and you crave human flesh.\n", 0.05)
    slow_print("You feel as though you are falling...\n",0.05)
    slow_print("falling..\n",0.05)
    slow_print("falling..\n",0.05)
    print(colored.red("*You are waking up."))
    time.sleep(3.00)
    print_location()


def help_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    bodyfig = Figlet(font='term', width=columns, justify='center')
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText('# Help, How To, How Do I #'))
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText("Just give up hope now actually, thats the best hope\n"))
    print(bodyfig.renderText("Seriously, just jump in and hold on, there is no hope\n"))
    print(bodyfig.renderText("Troll just really sucks like that. You will get nothing\n"))
    print(bodyfig.renderText("If you manage to figure out how to play and then win, congrats\n"))
    print(bodyfig.renderText("True to form, there is no documentation, no hints\n"))
    print(bodyfig.renderText("By design when you finally figure it out.. you will be so sick of it.\n"))
    print(bodyfig.renderText("This is the true essence of the troll experience.\n"))
    print("\n")
    print(bodyfig.renderText('#' * 74))
    print(bodyfig.renderText(
        ".: Play :."))
    print(bodyfig.renderText(
        ".: Help :."))
    print(bodyfig.renderText(
        ".: Quit :."))
    title_screen_options()


def parse_input(player_input):
    doc = nlp(player_input)

    for token in doc:
        print(token.text, token.pos_, token.dep_)


def slow_print(message, speed):
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(1.50)

def print_location():
    os.system('cls' if os.name == 'nt' else 'clear')
    statusbar()
    bodyfig = Figlet(font='term', width=columns, justify='center')
    print(bodyfig.renderText('\n' + ('#' * (4 + len(player1.location)))))
    print(bodyfig.renderText('# ' + player1.location.upper() + ' #'))
    print(bodyfig.renderText('#' * (4 + len(player1.location))))
    print('\n')
    slow_print(troll[player1.location][DESCRIPTION],0.05)
    examine(False)

def examine(skip = False):
    #statusbar()
    if room_solved[player1.location] == False:
        if skip != True:
            slow_print(troll[player1.location][INFO],0.05)
            slow_print(troll[player1.location][PUZZLE],0.05)
            if player1.location != 'admin':
                puzzle_answer = getinput()
                checkpuzzle(puzzle_answer)
            else:
                player1.location = troll[player1.location][NEXTLOCATION]
                print_location()
        else:
            puzzle_answer = getinput()
            checkpuzzle(puzzle_answer)
    else:
        print("There is nothing new for you to see here.")

def checkpuzzle(puzzle_answer):
        if puzzle_answer == (troll[player1.location][SOLVED]):
            room_solved[player1.location] = True
            slow_print(troll[player1.location][SOLVED_MESSAGE],0.05)
            print(colored.red("\nYou have solved the puzzle. Onwards!"))
            time.sleep(3.0)
            player1.location = troll[player1.location][NEXTLOCATION]
            print_location()
        elif player1.location == 'admin':
            room_solved[player1.location] = True
            slow_print(troll[player1.location][SOLVED_MESSAGE],0.05)
            print(colored.red("\nYou have solved the puzzle. Onwards!"))
            time.sleep(3.0)
            player1.location = troll[player1.location][NEXTLOCATION]
            print_location()
        else:
            slow_print("Wrong answer! -1 hp, Try again.\n",0.05)
            player1.hp - 1
            examine(True)

def getinput():
    return input(' > ')

def statusbar():
        bodyfig = Figlet(font='term', width=columns, justify='center')
        print(bodyfig.renderText('Player stats: ' + player1.name))
        stats = 'Player: ' + player1.name + ' | Health: ' + str(player1.hp) + ' | Class: ' + player1.role
        print(bodyfig.renderText('%' * (len(stats) + 4)))
        print(bodyfig.renderText('% '+stats+' %'))
        print(bodyfig.renderText('%' * (len(stats) + 4)))

# Begin loop
splashscreen()
