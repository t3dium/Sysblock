#!/usr/bin/python -ex
from colorama import init
from colorama import Fore
from datetime import *
from time import *
import subprocess
import requests
import os
import sys
import syslog

#Check for root
if not os.geteuid() == 0:
    sys.exit("\nYou must have root privilages to run sysblock, re-run the command: sudo python3 sysblock, make sure you use sudo.\n")

#some variables
# - Ignore this, its used for testing the program
host_path = r'/etc/hosts'
# host_path = r"C:\Windows\System32\drivers\etc\hosts"


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
#     f = open(host_path, 'r')
#     lines = f.readlines()
#     f.close()
#
#     newLines = []
#     for line in lines:
#         newLines.append(' '.join([word for word in line.split() if word != excludedWord]))
#
#     f = open(host_path, 'w')
#     for line in lines:
#         f.write("{}\n".format(line))
#     f.close()

    ###
    # if run_once_or_multiple == ("Y"):
    #     print("repeating..")
    #     whitelist_apply()
    # else:
    #     quit()


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


def apply_blocklist():
    print(" Applying...")

    def lines(t):
        lines = open(t).read().splitlines()
        return(lines)

    #PROCESSING THE USER SELECTED BLOCKLIST
    row = lines(blocklist)
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


#DOWNLOADING THE USER SELECTED blocklist
def downloading():
    global url

    def download_blocklist():
        myfile = requests.get(url)
        open((blocklist), 'wb').write(myfile.content)
        print(" Downloaded")
        apply_blocklist()

    global blocklist
    if blocklist_choice.lower() == ("full"):
        blocklist = ("oisd_full.txt")
        url = 'https://dbl.oisd.nl/'
        download_blocklist()

    elif blocklist_choice.lower() == ("lightweight"):
        print(Fore.WHITE, "Downloading Lightweight blocklist...")
        blocklist = ("oisd_basic.txt")
        url = 'https://dbl.oisd.nl/basic/'
        download_blocklist()

    elif blocklist_choice.lower() == ("custom"):
        print("Please enter a blocklist url,", Fore.RED, "note that this must be a DOMAIN/Hosts blocklist.",
              Fore.LIGHTMAGENTA_EX, "You can find some at filterlists.com")
        url = input("--->   ")
        blocklist = ("custom_blocklist.txt")
        download_blocklist()

    else:
        print(Fore.RED, "Incorrect option, returning to menu")
        sleep(0.4)
        menu()


def menu():
    print(Fore.YELLOW, """
         █████╗ ██████╗ ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
        ██╔══██╗██╔══██╗██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
        ███████║██║  ██║██████╔╝██║     ██║   ██║██║     █████╔╝
        ██╔══██║██║  ██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗
        ██║  ██║██████╔╝██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗
        ╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝""", Fore.GREEN, """
        Sysblock, an ad/tracker/malware/crypto blocker

        ---------------------------------
        What would you like to do?
        ---------------------------------
        ████████████████████████████████████████████████████████████
        -------------------------------------------------------------
        1) Apply Adblock
        -------------------------------------------------------------
        ████████████████████████████████████████████████████████████
        -------------------------------------------------------------
        2) Whitelisting - Coming Soon
        3) Blacklisting
        4) Custom Redirects
        -------------------------------------------------------------
        █████████████████████████████████████████████████████████████
        -------------------------------------------------------------
        5) UNDO ANY CHANGES
        -------------------------------------------------------------
        █████████████████████████████████████████████████████████████
        -------------------------------------------------------------

        """)
    choice = input("  Choose an option, 1 is the default.")
    if choice == ("1"):

        #LETTING THE USER CHOOSE A blocklist
        print(Fore.LIGHTMAGENTA_EX)
        global blocklist_choice
        blocklist_choice = input(
            " Please choose a blocklist: Full, or Lightweight (for lower end devices)")
        downloading()

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
