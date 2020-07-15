import json
import os.path
import os
import datetime
import time
import sys
import getpass
from calculator import calculator
from notes import Notebook
notebook = Notebook()

def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.035)
    sys.stdout.write("\n")
    sys.stdout.flush()
def read_password():
    return getpass.getpass("Password: ", stream=None)
def save_config():
    settings["notes"]=notebook.notes
    json.dump(settings, open(configfilename, "w"))
def show_help ():
    print (" ")
    delay_print ("To make a simple calculation, type 'calculate'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To make a note, type 'make note'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To make a timed reminder, type 'reminder'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To check your notes, type 'show notes'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To delete a note, type 'delete notes'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To check your profile, type 'show data'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To check the date and time, type 'show time'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To quit, type 'quit'")
    print (" ")
    time.sleep (0.3)
    delay_print ("To see this message again, type 'help'")
    print (" ")
    time.sleep(0.3)
    delay_print ("To delete your data, type 'delete data'")

baseconfigfilename = os.path.join(os.path.dirname(sys.argv[0]), "savedata_")

delay_print("powering up.... ")
time.sleep(0.05)
enter = input ("Are you a new or returning user? ")
enter=enter.lower()

if enter == "returning":
    while True:
        chooseuser = input ("Please enter a username(case sensitive): ")
        configfilename = (baseconfigfilename + chooseuser)
        if os.path.isfile(configfilename):
            settings=json.load(open(configfilename))
            username=settings["username"]
            password=settings["password"]
            notebook.notes=settings["notes"]
            while read_password() != password:
                print ("incorrect")
            break
        elif chooseuser == "cancel":
            delay_print ("As you wish")
            sys.exit()
        else:
            delay_print ("You don't seem to be in our databases")
            sys.exit()

elif enter =="new":
    settings={}
    username = input ("Please choose a username: ")
    settings["username"]=username
    password = getpass.getpass(prompt="Password: ", stream=None)
    settings["password"]=password
    configfilename = (baseconfigfilename + username)
    save_config()
    show_help()
    
while True:
    command = input ("What do you want to do? ")
    command = command.lower()
    if command == "calculate":
        calculator()
    elif command == "make note":
        note = input("What would you like me to remember " + username + "? ")
        notebook.addnote(note)
        save_config()
    elif command == "show data":
        delay_print ("Your name: " + username + " ")
        print (" ")
        time.sleep (0.3)
        delay_print ("Your notes are: ")
        for note in notebook.notes:
            print (note)
        print (" ")
        time.sleep (0.3)
        delay_print ("The time is: ")
        print (datetime.datetime.now().strftime("%c"))
        print (" ")
    elif command == "make reminder":
        delay_print ("I haven't yet written this section as it will require a full rework of the command line system. ")
        time.sleep(0.3)
        delay_print ("Sorry for the inconvenience, Iain")
        time.sleep(0.3)
        #reminder = input("What would you like to be reminded of? ")
        #wait = int(input("How long do you want to wait before being reminded? "))
        #time.sleep (wait)
        #print (reminder)
        #in order to get this function working, I'm going to have to restructure the command line interface. 
    
    elif command == "show notes":
        print (" ")
        delay_print ("Your notes:")
        for note in notebook.notes:
            delay_print (note)
        print (" ")
    elif command == "delete note":
        notenumber = 1
        for note in notebook.notes:
            delay_print (str(notenumber) + ". " + note)
            notenumber = notenumber +1
        delete = int(input("Which number note do you want to delete? "))-1
        del notebook.notes[delete]

        save_config()

    elif command == "quit":
        delay_print ("Goodbye " + username + ", I hope to see you again soon.")
        time.sleep(1)
        sys.exit()
    elif command == "show time":
        delay_print ("The time is: ")
        delay_print (datetime.datetime.now().strftime("%c"))
    elif command == "delete data":
        delay_print ("are you sure? (y or n)")
        check = input ("")
        check = check.lower()
        if check == ("y"):
            while read_password() != password:
                print ("incorrect")
            delay_print ("Deleting user: " + username + "...")
            time.sleep(0.3)
            os.remove ("savedata_" + username)
            sys.exit()
        else:
            delay_print("Understood")
    else:
        delay_print ("Sorry, " + username + ", I didn't understand that.")
