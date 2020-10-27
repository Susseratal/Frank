import json
import os.path
import os
import datetime
import time
import sys
import getpass
import asyncio

from werkzeug.security import generate_password_hash, check_password_hash

from calculator import calculator
from notes import Notebook

notebook = Notebook()


async def reminder(delay, what):
    await asyncio.sleep(int(delay))
    print(str(what))


async def main():
    def delay_print(s):
        for c in s:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.025)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def read_password():
        return getpass.getpass("Password: ", stream=None)

    def save_config():
        settings["notes"] = notebook.notes
        json.dump(settings, open(configfilename, "w"))

    def show_help():
        print(" ")
        delay_print("To make a simple calculation, type 'calculate'")
        print(" ")
        time.sleep(0.3)
        delay_print("To make a note, type 'make note'")
        print(" ")
        time.sleep(0.3)
        delay_print("To make a timed reminder, type 'reminder'")
        print(" ")
        time.sleep(0.3)
        delay_print("To check your notes, type 'show notes'")
        print(" ")
        time.sleep(0.3)
        delay_print("To delete a note, type 'delete notes'")
        print(" ")
        time.sleep(0.3)
        delay_print("To check your profile, type 'show data'")
        print(" ")
        time.sleep(0.3)
        delay_print("To check the date and time, type 'show time'")
        print(" ")
        time.sleep(0.3)
        delay_print("To quit, type 'quit'")
        print(" ")
        time.sleep(0.3)
        delay_print("To see this message again, type 'help'")
        print(" ")
        time.sleep(0.3)
        delay_print("To delete your data, type 'delete data'")

    def read_multiline_input():
        rtn = []
        while True:
            line = input()
            if line.strip() == "":
                break
            rtn.append(line)
        return rtn

    baseconfigfilename = os.path.join(os.path.dirname(sys.argv[0]), "savedata_")

    delay_print("powering up.... ")
    time.sleep(0.05)
    enter = input("Are you a new or returning user? ")
    enter = enter.lower()

    if enter == "returning":
        while True:
            chooseuser = input("Please enter a username(case sensitive): ")
            configfilename = (baseconfigfilename + chooseuser)
            if os.path.isfile(configfilename):
                settings = json.load(open(configfilename))
                username = settings["username"]
                password = settings["password"]
                notebook.notes = settings["notes"]
                while not (check_password_hash(password, read_password())):
                    print("incorrect")
                break
            elif chooseuser == "cancel":
                delay_print("As you wish")
                sys.exit()
            else:
                delay_print("You don't seem to be in our databases")
                sys.exit()

    elif enter == "new":
        settings = {}
        username = input("Please choose a username: ")
        settings["username"] = username
        password = getpass.getpass(prompt="Password: ", stream=None)
        settings["password"] = generate_password_hash(password)
        configfilename = (baseconfigfilename + username)
        save_config()
        print("To see the help message, type 'Show help' ")

    loop = asyncio.get_event_loop()
    while True:
        delay_print("What do you want to do: ")
        command = await loop.run_in_executor(None, sys.stdin.readline)
        command = command.rstrip().lower()
        if command == "calculate":
            calculator()

        elif command == "make note":
            delay_print("What would you like me to remember " + username + "? ")
            note = read_multiline_input()
            notebook.addnote(note)
            save_config()

        elif command == "show data":
            delay_print("Your name: " + username + " ")
            print(" ")
            time.sleep(0.3)
            delay_print("Your notes are: ")
            for note in notebook.notes:
                print(note)
            print(" ")
            time.sleep(0.3)
            delay_print("The time is: ")
            print(datetime.datetime.now().strftime("%c"))
            print(" ")

        elif command == "make reminder":
            mem = str(input("What would you like me to remember: "))
            wait = int(input("How long would you like me to wait: "))
            asyncio.create_task(reminder(wait, mem))

        elif command == "show notes":
            print(" ")
            delay_print("Your notes:")
            for note in notebook.notes:
                for line in note:
                    print(line)
                print(" ")

        elif command == "delete note":
            notenumber = 1
            for note in notebook.notes:
                delay_print(str(notenumber) + ". " + note[0])
                notenumber = notenumber + 1
            delete = int(input("Which number note do you want to delete? ")) - 1
            del notebook.notes[delete]
            save_config()

        elif command == "show time":
            delay_print("The time is: ")
            delay_print(datetime.datetime.now().strftime("%c"))

        elif command == "delete data":
            delay_print("are you sure? (y or n)")
            check = input("")
            check = check.lower()
            if check == "y":
                while not (check_password_hash(password, read_password())):
                    print("incorrect")
                delay_print("Deleting user: " + username + "...")
                time.sleep(0.3)
                os.remove("savedata_" + username)
                sys.exit()
            else:
                delay_print("Understood")

        elif command == "quit":
            delay_print("Powering down...")
            sys.exit()

        else:
            delay_print("Sorry, " + username + ", I didn't understand that.")


asyncio.run(main())
