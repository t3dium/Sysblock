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
    sample = ("""
# Host addresses
127.0.0.1  localhost
127.0.1.1  computer
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters

    """)
    with open(host_path, 'w') as undo:
        undo.write(sample)
        print("finished, you may now close this program")


def custom_redirect_repeat():
    print("Enter", Fore.CYAN, "Y", Fore.WHITE, "if you would like to redirect more than domain, else",
          Fore.RED, "N", Fore.WHITE, "to run once")
    global run_once_or_multiple4
    run_once_or_multiple4 = input("--> ")
    run_once_or_multiple4 = run_once_or_multiple4.lower()
    custom_redirects()


def custom_redirects():
    global domain, redirect, custom_redirect
    domain = input("Enter the domain you want to be redirected")
    redirect = input("What domain would you like to redirect it to:")
    custom_redirect = (redirect+" "+domain)
    apply_custom_redirects()


def apply_custom_redirects():
    with open(host_path, 'a') as host2:
        host2.write(custom_redirect)
        host2.write("\n")
        host2.close()
        print(Fore.LIGHTGREEN_EX, "Added the following redirect  :",
              domain, " --> ", redirect)
        print(Fore.WHITE)
    ##repeating##
    if run_once_or_multiple4 == ("y"):
        print("repeating..")
        custom_redirects()
    else:
        quit()

# def whitelist_apply():
#     print("Enter the domain you want to whitelist", Fore.RED, "Note that domains do not include https:// nor bits after the slash", Fore.CYAN, "for e.g google.com")
#     excludedWord = input("--->  ")
#
#     try:
#         with open(host_path, 'r') as fr:
#             lines = fr.readlines()
#
#             with open(host_path, 'w') as fw:
#                 for line in lines:
#                     # strip() is used to remove '\n'
#                     # present at the end of each line
#                     if line.strip('\n') != '8-August':
#                         fw.write(line)
#         print("Finished")
#     except:
#         print("Error")
#     ##
#     if run_once_or_multiple == ("Y"):
#         print("repeating..")
#         whitelist_apply()
#     else:
#         quit()
#
#
# def whitelist():
#     #if the user wants to whitelist multiple domains, this definition will loop
#     print("Enter", Fore.CYAN, "Y", Fore.WHITE, "if you would like to whitelist more than domain, else", Fore.RED, "N", Fore.WHITE, "to run once")
#     global run_once_or_multiple
#     run_once_or_multiple = input("--> ")
#     whitelist_apply()


def blacklist_apply():
    print(Fore.CYAN, " Enter the domain you want blacklisted.", Fore.RED,
          "Do not include https, or bits after the slash.", Fore.CYAN, "An example looks like this: google.com")
    url_to_blacklist = input("--->  ")
    thing = ((url_to_blacklist) + (" 0.0.0.0") + '\n')
    with open(host_path, 'a') as host_file:
        host_file.write(thing)
    if run_once_or_multiple2 == ("y"):
        print("repeating..")
        blacklist_apply()
    else:
        quit()


def blacklisting():
    print("Enter", Fore.CYAN, "Y", Fore.WHITE, "if you would like to blacklist more than domain, else",
          Fore.RED, "N", Fore.WHITE, "to run once")
    global run_once_or_multiple2
    run_once_or_multiple2 = input("--> ")
    run_once_or_multiple2 = run_once_or_multiple2.lower()
    blacklist_apply()


def cleanup():
    #removing unecessary comments from hosts
    with open(host_path, "r") as file:
        for line in file:
            if line.startswith('#'):
                continue
            line = line.strip()


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

    sleep(5)
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
    table.add_column("Blocklist", justify="left", style="magenta")
    table.add_column("Info", justify="left", style="green")

    table.add_row("1", "Apply Adblock",
                  "Will be prompted to choose blocklists afterwards")
    table.add_row(" ", " ", " ")
    table.add_row("2", "Whitelisting", "Coming Soon...")
    table.add_row("3", "Blacklisting", "Block Specific Domains")
    table.add_row(" ", " ", " ")
    table.add_row("4", "UNDO ALL CHANGES",
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
        blacklisting()

    elif choice == ("4"):
        custom_redirect_repeat()

    elif choice == ("5"):
        print(Fore.RED)
        continue1 = input(
            "Are you sure? Enter Y to undo any changes and remove all filters.")
        print(Fore.WHITE)
        if continue1.upper() == ("Y"):
            print("un-doing...")
            undo()

    else:
        print(Fore.RED, "Please select an option, Returning to Menu")
        sleep(0.4)
        menu()


menu()
