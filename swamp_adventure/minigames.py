################################################################################
#                                                                              #
#  minigames.py                                                                #
#                                                                              #
#  This module contains all of the minigame executables that take place on     #
#  the action spaces of the gameboard. Each minigame is a function that        #
#  forces the user to solve some sort of puzzle via the command line. Some     #
#  executables also constitute special conditions, such as the acquisiton of   #
#  the cheese or the game exit condition.                                      #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Revised: 04/14/2025                                                         #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import textwrap
from enum import Enum

from block_print import print_ascii_art

################################################################################
#  CONSTANTS                                                                   #
################################################################################

"""
ReturnCode Enum

The different values returned from the minigames to be handled by the game loop.
"""
class ReturnCode(Enum):
    SUCCESS       = 0
    DEATH         = -1
    BACK          = 1
    SHREK_WHISTLE = 2
    CHEESE        = 3
    SPELL         = 4

################################################################################
#  FUNCTIONS                                                                   #
################################################################################

"""
pub()

Pub minigame — correct choice is to go in and drink the drink.
"""
def pub():
    print(textwrap.dedent("""\
                          Ahead of you, there is a rundown pub. You can either
                          [1] go in, or [2] attempt to go around. Which will
                          you pick?\n"""))
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice != "1" and choice != "2":
            print("That wan't an option stupid. Try again.\n")
        else:
            break
    if choice == "1":
        print("\n")
        print(textwrap.dedent("""\
        You enter the pub. Inside, there is an ancient creepy looking
        bartender and three men. The first man grabs you by the shoulder
        and says 'a stranger! Come stranger, have a sip of my drink... I
        insist.' The second man says 'No! Don't drink that, it's
        poisonous!' The third man third man says 'The second man tells
        the truth!' The first man then says 'The third man is lying!'
        The bartender looks at you and says 'I've always heard you can
        trust two out of every three men. Which two? I've no clue
        myself.' You now have a choice to make — do you drink or not?\n"""))
        while True:
            response = input("Choose: [1] Drink, [2] Refuse to drink, [3] Run away, [4] Fight the bartender: ")
            if response != "1" and response != "2" and response != "3" and response != "4":
                print("That wan't an option stupid. Try again.")
            else:
                break
        if response == "1":
            print("\n")
            print(textwrap.dedent("""\
            You take a sip of the drink. It tastes like swamp water, but
            you feel no ill-affects. The first man looks at you approvingly and
            says 'A brave mouse like you deserves a reward. Take this whistle...
            it may come in handy.' You now have a strange whistle, which you 
            pocket and continue on your way.\n"""))
            return ReturnCode.SHREK_WHISTLE
        elif response == "2":
            print(textwrap.dedent("""\
            You refuse to drink, and the first man looks at you angrily.
            He says 'You think you're too good for my drink? I'll show you!' He
            then lunges at you, but you dodge out of the way and attempt to run
            away. You slip on a poorly placed banana peel and fall to the
            ground, hitting your head hard on the floor. You die.\n"""))
            return ReturnCode.DEATH
        elif response == "3":
            print("You say 'let me think about it for a minute!' and slip back "
            "out the door.\n")
            return ReturnCode.BACK
        elif response == "4":
            print(textwrap.dedent("""\
            For no reason at all, you rush at the bartender and bite him
            hard on the leg for no reason. He screams in pain and falls to the
            ground. You begin to rush up to his neck to bit him again, when
            you realize this was a terrible idea. The last thing you see is
            the boot of the first man coming down on you head.\n"""))
            return ReturnCode.DEATH
    else:
        print(textwrap.dedent("""\
        You attempt to go around the pub, but you are greeted there by 
        Puss in Boots, who already has his sword drawn. He says 'You think you
        can just walk around me? I don't think so!' He then lunges at you with
        his sword. You have no weapon to defend yourself, but you do have a few
        options. You can either [1] try to dodge his attack, [2] try to
        distract him with your charm, or [3] try to fight him off with your
        bare hands. Which will you choose?\n"""))
        while True:
            response = input("Enter 1, 2, or 3: ").strip()
            if response != "1" and response != "2" and response != "3":
                print("That wan't an option stupid. Try again.\n")
            else:
                break
        if response == "1":
            print(textwrap.dedent("""\
            You attempt to dodge his attack, but you trip over your own
            feet and fall to the ground. Puss in Boots then lunges at you and
            stabs you with his sword. You die.\n"""))
            return ReturnCode.DEATH
        elif response == "2":
            print(textwrap.dedent("""\
            You attempt to charm him with your good looks, but quickly
            realize that you neither have good looks, nor any charm. Puss in
            Boots laughs at you, and out of sheer pity, decides to spare your
            life—he lets you through to continue your adventure.\n"""))
            return ReturnCode.SUCCESS
        else:
            print(textwrap.dedent("""\
            You attempt to fight him off with your bare hands, but he is too
            quick for you. He lunges at you with his sword, and you die.\n"""))
            return ReturnCode.DEATH
    return ReturnCode.SUCCESS

def lily_pads():
    print(textwrap.dedent("""\
          You come across a large pool of disgusting swamp water, with a number
          of lily pads floating on the top. You can either [1] try to cross the
          lily pads, or [2] go back. Which will you choose?\n"""))
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice != "1" and choice != "2":
            print("That wan't an option stupid. Try again.\n")
        else:
            break
    if choice != "1":
        return ReturnCode.BACK
    else:
        print(textwrap.dedent("""\
        You approach the water. You see a lily pads arranged in roughly a 3x3
        pattern. You must choose the left (L), right (R), or middle (M) pad in
        each of the three rows. If you fall in, you will have to swim through
        the disgusting water and try again.\n"""))
        count = 1
        while True:
            if count > 3:
                break
            row = input(f"In row {count}, choose L, M, or R: ").strip().upper()
            if row != "L" and row != "M" and row != "R":
                print("That wan't an option stupid. Try again.\n")
                continue
            else:
                count += 1
            if row != "L":
                print(textwrap.dedent("""\
                      The lily pad gives way under you and you fall straight
                      into the disgusting swamp water. Some of it goes in your
                      mouth, and you gag. You swim to the edge and pull
                      yourself out to try again.\n"""))
                count = 1
            else:
                print(textwrap.dedent("""\
                      The lily pad shakes underneath you but does not give way.\n"""))
        print(textwrap.dedent("""\
        You successfully cross the lily pads and make it to the other side.
        You are now free to continue your journey.\n"""))
        return ReturnCode.SUCCESS
         
def troll():
    print(textwrap.dedent("""\
          You come across a troll who blocks your path. He says 'You must answer
          my riddle if you want to pass by! You can ewither [1] try to answer the
          riddle, or [2], run away. Which will you choose?\n"""))
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice != "1" and choice != "2":
            print("That wan't an option stupid. Try again.\n")
        else:
            break
    if choice != "1":
        return ReturnCode.BACK
    else:
        print(textwrap.dedent("""\
        The troll says, 'In the land where fairy tales twise and bend,
        I guard the path you seek to end. I'm feared by knights both bold and
        rash, yet softened once by ogre's splash. My breath brings fire, my
        wings bring flight, but once I wept on a lonely night. My love's unlocked,
        my chains are gone, now tell me, fool, who do I wait on?'\n"""))
        choice = input("Enter your answer: ").strip()
        while choice.lower() != 'donkey':
            print("Wrong, you fool! Try again. \n")
            choice = input("Enter your answer: ").strip()
        print(textwrap.dedent("""\
        The troll looks at you and says 'You are correct! You may pass.'
        He then steps aside and lets you through. You are now free to continue
        your journey.\n"""))
        return ReturnCode.SUCCESS

def cheese_nearby():
    print(textwrap.dedent("""\
          You smell something delicious in the air.... It smells quite nearby... But where?"""))

def cheese():
    for _ in range(10):
        print_ascii_art("cheese")
    print(textwrap.dedent("""\
          OH MY GOD IT'S THE CHEESE! You have found the cheese! THANK GOD
          YOU NOW HAVE YOUR CHEESE. YIPPEEEEEEEEE\n"""))
    print("Now just time to find your way out of this cursed swamp...\n")
    return ReturnCode.CHEESE

def base_three():
    print(textwrap.dedent("""\
          You come across a strange door with a keypad. There is a sign that
          reads '202 + 021'. Too easy! You add the numbers up to get 223, but 
          then you look at the keypad and see only the numbers 0, 1, and 2.
          more confusing still, a small note reads, 'There ARE no numbers 
          greater than 222!' What could this mean?...\n"""))
    print(textwrap.dedent("""\
          You may either [1] solve the lock puzzle or [2], go back. Which will
          you choose?\n"""))
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice != "1" and choice != "2":
            print("That wan't an option stupid. Try again.\n")
        else:
            break
    if choice != "1":
        return ReturnCode.BACK
    else:
        while True:
            answer = input("Enter your answer: ").strip()
            try:
                answer = int(answer)
                if answer == 0:
                    break
                else:
                    print("The lock flashes red and nothing happens. Try again.\n")
            except ValueError:
                print("Your answer must be a number, dummy. Try again\n")
                continue
        print(textwrap.dedent("""\
        The door opens and you are free to continue your journey.\n"""))
        return ReturnCode.SUCCESS
    
def deadend():
    print(textwrap.dedent("""\
          You come across a dead end. You can either [1] try to go back, or
          [2] try to break through the wall. Which will you choose?\n"""))
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice != "1" and choice != "2":
            print("That wan't an option stupid. Try again.\n")
        else:
            break
    if choice == "1":
        return ReturnCode.BACK
    else:
        print(textwrap.dedent("""\
        You attempt to break through the wall, but it is too strong. You
        fall to the ground and hit your head on a rock. You die.\n"""))
        return ReturnCode.DEATH

def wizard():
    print(textwrap.dedent("""\
          You come across a wizard who is blocking your path. He casts a spell
          on you which returns you to the depths of the swamp.\n"""))
    return ReturnCode.SPELL

def shrek_encounter(has_whistle):
    print(textwrap.dedent("""\
          YOU HAVE ENCOUNTERED SHREK IN THE SWAMP. HE IS ENRAGED TO SEE YOU
          HERE."""))
    print_ascii_art("shrek")
    if has_whistle:
        print(textwrap.dedent("""\
          He says 'You have entered my swamp! You must pay the price for
          trespassing!' He then pulls out a sword and lunges at you. You can
          either [1] fight him, [2] try to run away, or [3] blow the whistle the
          man at the pub gave you. Which will you choose?\n"""))
        while True:
            choice = input("Enter 1, 2, or 3: ").strip()
            if choice != "1" and choice != "2" and choice != "3":
                print("That wan't an option stupid. Try again.\n")
            else:
                break
    else:
        print(textwrap.dedent("""\
          He says 'You have entered my swamp! You must pay the price for
          trespassing!' He then pulls out a sword and lunges at you. You can
          either [1] fight him, or [2] try to run away. Which will you choose?\n"""))
        while True:
            choice = input("Enter 1 or 2: ").strip()
            if choice != "1" and choice != "2":
                print("That wan't an option stupid. Try again.\n")
            else:
                break
    if choice == "1":
        print(textwrap.dedent("""\
        Why would you try to fight Shrek. You are a mouse. You have to have
        known that wouldn't work out well. You're dead.\n"""))
        return ReturnCode.DEATH
    elif choice == "2":
        print(textwrap.dedent("""\
            You run away as fast as you can, all the way back to the heart of
            the swamp where you started.\n"""))
        return ReturnCode.SPELL
    else:
        print(textwrap.dedent("""\
        You blow the whistle and Shrek stops in his tracks. He looks at you
        and says 'You have a whistle? I love whistles! You can pass, but
        don't let me catch you here again!'\n"""))
        return ReturnCode.SUCCESS
    