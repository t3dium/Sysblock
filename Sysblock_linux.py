#!/usr/bin/python -ex
from colorama import init
from colorama import Fore
from datetime import *
import subprocess
import requests
import os
import sys
import syslog
import time
#for tables
from rich.console import Console
from rich.table import Table

#Check for root
if not os.geteuid() == 0:
    sys.exit("\nYou must have root privilages to run sysblock, re-run the command: sudo python3 sysblock, make sure you use sudo.\n")

host_path = r'/etc/hosts'


def undo():
    print("test")
    sample = ("""# Host addresses
127.0.0.1  localhost
127.0.1.1  computer
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters

    """)
    with open(host_path, 'w') as undo:
        undo.write(sample)
        print("finished, you may now close this program")


def custom_redirects():
    domain = input("Enter the domain you want to be redirected")
    redirect = input("What domain would you like to redirect it to:")
    custom_redirect = (redirect+" "+domain)

    with open(host_path, 'a') as host2:
        host2.write(custom_redirect)
        host2.write("\n")
        host2.close()
        print(Fore.LIGHTGREEN_EX, "Added the following redirect  :",
              domain, " --> ", redirect)
        print(Fore.WHITE)
    ##repeating##
    table3 = Table()

    table3.add_column("Keybinding", justify="left",
                      style="magenta", no_wrap=True)
    table3.add_column("Options", justify="left", style="cyan")
    table3.add_row("1", "Whitelist another domain")
    table3.add_row("2", "Return to Menu",)

    console3 = Console()
    console3.print(table3)

    menu_choice3 = input("")
    if menu_choice3 == ("1"):
        custom_redirects()
    else:
        menu()


def whitelist():
    print("Enter the domain you want to whitelist", Fore.RED,
          "Note that domains do not include https:// nor bits after the slash", Fore.CYAN, "for e.g google.com")
    excludedWord = input("--->  ")

    with open(host_path, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if (excludedWord) not in line:
                f.write(line)
        f.truncate()
    ##
    table2 = Table()

    table2.add_column("Keybinding", justify="left",
                      style="magenta", no_wrap=True)
    table2.add_column("Options", justify="left", style="cyan")
    table2.add_row("1", "Whitelist another domain")
    table2.add_row("2", "Return to Menu",)

    console2 = Console()
    console2.print(table2)

    menu_choice2 = input("")
    if menu_choice2 == ("1"):
        whitelist()
    else:
        menu()


def blacklist():
    print(Fore.CYAN, " Enter the domain you want blacklisted.", Fore.RED,
          "Do not include https, or bits after the slash.", Fore.CYAN, "An example looks like this: google.com")
    url_to_blacklist = input("--->  ")
    thing = (("0.0.0.0 ") + (url_to_blacklist) + '\n')
    with open(host_path, 'a') as host_file:
        host_file.write(thing)
    ##
    table1 = Table()
    table1.add_column("Keybinding", justify="left",
                      style="magenta", no_wrap=True)
    table1.add_column("Options", justify="left", style="cyan")
    table1.add_row("1", "Blacklist another domain")
    table1.add_row("2", "Return to Menu",)

    console1 = Console()
    console1.print(table1)

    menu_choice2 = input("")
    if menu_choice2 == ("1"):
        blacklist()
    else:
        menu()


def cleanup():
    #removing unecessary comments from file
    with open(host_path, "r+") as f:
        new_f = f.readlines()
        f.seek(0)
        for line in new_f:
            if ("#") not in line:
                f.write(line)
        f.truncate()


def apply_blocklist():
    print(" Applying...")

    def lines(t):
        lines = open(t).read().splitlines()
        return(lines)

    #PROCESSING THE USER SELECTED BLOCKLIST
    row = lines("blocklist.txt")
    websites = row

    print(Fore.WHITE, "Please wait for a minute or two", Fore.RED,
          "Unfortunately, i haven't found a solution (yet) for having the script detect when the program has finished, so give it a moment before closing.")
    while True:
        with open(host_path, "r+") as f:
            content = f.read()
            for website in websites:
                if website in content:
                    pass
                elif(not website):
                    print("finished")
                else:
                    f.write(website+"\n")
                    #f.write(redirect+"    	"+website+"\n")
    else:
        with open(host_path, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in websites):
                    file.write(line)
            file.truncate()

    time.sleep(5)
    print(Fore.YELLOW, """Sysblock has been applied succesfully,
             try visiting a website usually filled with ads and test if it worked

             !!! IMPORTANT: if you wish to whitelist a site, re-run this script but with option 3""")
    cleanup()


#DOWNLOADING THE USER SELECTED blocklist
def downloading():
    global url

    def download_blocklist():
        myfile = requests.get(url)
        open(("blocklist.txt"), 'ab').write(myfile.content)
        print(" Downloaded blocklists...")
        # apply_blocklist()

    blocklist_choice_final = blocklist_choice.split(',')
    print(blocklist_choice_final)
    if "1" in blocklist_choice_final:
        url = 'https://dbl.oisd.nl/'
        download_blocklist()
    if "2" in blocklist_choice_final:
        url = 'https://dbl.oisd.nl/basic/'
        download_blocklist()
    if "3" in blocklist_choice_final:
        print("Please enter a blocklist url,", Fore.RED, "note that this must be a DOMAIN/Hosts blocklist.",
              Fore.LIGHTMAGENTA_EX, "You can find some at filterlists.com")
        url = input("--->   ")
        download_blocklist()
    if "4" in blocklist_choice_final:
        url = 'https://raw.githubusercontent.com/furkun/ProtectorHosts/main/hosts'
        download_blocklist()
    if "5" in blocklist_choice_final:
        url = 'https://raw.githubusercontent.com/anudeepND/blacklist/master/facebook.txt'
        download_blocklist()
    # if "6" in blocklist_choice_final:
    #
    # if "7" in blocklist_choice_final:


def choose_blocklist():
    #using rich for tables here
    global blocklist_choice
    table = Table(title="Sysblock -  Choose Blocklists")
    table.add_column("Options", justify="left", style="cyan", no_wrap=True)
    table.add_column("Blocklist", justify="left", style="magenta")
    table.add_column("Info", justify="left", style="green")

    table.add_row("1", "Oisd Full", "Main - Recommended")
    table.add_row("2", "Oisd Lightweight", "Main - For low end devices")
    table.add_row("3", "Custom", "Enter the Url")
    table.add_row(" ", " ", " ")
    table.add_row("* 4", "IpGrabber Blocklist", "Extra - Blocks Ip Grabbers")
    table.add_row("* 5", "No Facebook",
                  "Extra - Blocks facebook + trackers completely")
    table.add_row(" ", " ", " ")
    table.add_row("n/a", "More coming soon",
                  "")

    console = Console()
    console.print(table)
    print(Fore.RED, "NOTE: enter your choices in the FOLLOWING FORMAT: 1,2,5 with the COMMAS if theres multiple")
    blocklist_choice = input("")
    downloading()


def menu():
    print(Fore.YELLOW, "")

    table = Table(title="""
 █████╗ ██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
███████║██║  ██║██████╔╝██║     ██║   ██║██║     █████╔╝
██╔══██║██║  ██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗
██║  ██║██████╔╝██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
By t3dium

What would you like to do?""")

    table.add_column("Options", justify="left", style="cyan", no_wrap=True)
    table.add_column("Info", justify="left", style="magenta")
    table.add_column("More Info", justify="left", style="green")

    table.add_row("1", "Apply Adblock",
                  "Will be prompted to choose blocklists afterwards")
    table.add_row(" ", " ", " ")
    table.add_row("2", "Whitelisting", "Coming Soon...")
    table.add_row("3", "Blacklisting", "Block Specific Domains")
    table.add_row("4", "Custom Redirects", "Typically used for lan services")
    table.add_row("5", "Cleanup blocklists",
                  "removes unecessary comment lines")
    table.add_row(" ", " ", " ")
    table.add_row("6", "UNDO ALL CHANGES",
                  "sets hosts back to normal")

    console = Console()
    console.print(table)

    choice = input("  Choose an option, 1 is the default.")
    if choice == ("1"):

        #LETTING THE USER CHOOSE A blocklist
        print(Fore.LIGHTMAGENTA_EX)
        choose_blocklist()

    elif choice == ("2"):
        whitelist()

    elif choice == ("3"):
        blacklist()

    elif choice == ("4"):
        custom_redirects()

    elif choice == ("5"):
        cleanup()

    elif choice == ("6"):
        print(Fore.RED)
        continue1 = input(
            "Are you sure? Enter Y to undo any changes and remove all filters.")
        print(Fore.WHITE)
        if continue1.upper() == ("Y"):
            print("un-doing...")
            undo()

    else:
        print(Fore.RED, "Please select an option, Returning to Menu")
        time.sleep(0.4)
        menu()


menu()
