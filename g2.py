#!/usr/bin/env python3
#usage: g <search>
# or just 'g' to enter interactive mode
# use 'help' while in interactive mode to edit settings
import subprocess
import sys
import re
import json
import math
import os
#python doesnt interpret '~', bash does that. not python
config_path ="settings.json"


#TODO prompt the user if the file doesnt exist and do whole new settings setup
# Read JSON data from file
with open(os.path.dirname(__file__)+ "/" + config_path, 'r') as file:
    json_data = json.load(file)

# print(json_data)
# Extract values into Python variables
hosts_file_path = os.path.expanduser(json_data["hosts_file_path"])
last_search = json_data["lastsearch"]
wildcard_character = json_data["wildcard_character"]
max_results = json_data["max_results"]
ssh_pre_options = json_data["ssh_pre_options"]
ssh_post_options = json_data["ssh_post_options"]

#needs to be global cause its used everywhere
command=last_search
pagenumber = 0
##
# input "ew/sw"
# With a string query -> read the hosts file and populate results[]
# returns array of [[hostname,ip],[hostname2,ip2],etc]
##
def get_search_results(query):
    results = []
    regex_pattern = ".*" + query.replace(wildcard_character, '.*') + ".*"
    # print(regex_pattern) #testing

    with open(hosts_file_path, 'r') as file:
        for line in file:
            #read current line for hostname and ip
            #if line starts with # (comment) skip to the next
            # print(line.strip())
            line = line.strip()
            if line.startswith('#') or line.startswith('}'):
                pass
            elif line == "":
                pass
            else:
                hostname, ip = line.split()                
                #if current line matches regex, add the fields to results[]
                if re.match(regex_pattern, hostname, re.IGNORECASE):
                    results.append([hostname, ip])
    return results

##
# Interactively spawn ssh session on ip)
##
def execute_ssh(ip):
    sshcommand = "ssh"
    #add optional command options to ssh if wanted
    if ssh_pre_options != "":
        sshcommand = ssh_pre_options + " " + sshcommand
    if ssh_post_options != "":
        sshcommand = sshcommand + " " + ssh_post_options
    sshcommand += " " + ip
    subprocess.run(sshcommand, shell=True)


##
# just print 'max_results' worth of results, with page count too 
# For example if there are 70 search results currently in results[]:
# if page = 0:
#   prints [0-24] of 70 results
# if page = 1:
#   prints [25-50] of 70 results
# and so on...
#
##
def print_nicely(results, page):
    hosts = [pair for pair in results]
    formatted_hostnames = [f"{i+1}) {host[0]}  \t({host[1]})" for i, host in enumerate(hosts)]
    #example output:
    # 1) EWL4SW2160   (127.0.0.1)
    # 2) EWL12SW5300  (127.0.0.1)
    # 3) EWA2SW7700   (127.0.0.1)
    # 4) EWM6SW3540   (127.0.0.1)

    total_pages = -(-len(formatted_hostnames) // max_results)
    print('\n'.join(formatted_hostnames[page * max_results: (page + 1) * max_results]))
    print(f"Page {page + 1}/{total_pages}")
    # user_input = input("Press 'q' to quit, 'n' for next page: ")
    return

def interactive_mode():
    last=""
    results=[]
    pagenumber, max_pages = 0, 0
    global command
    skip_first_go = False
    # print(sys.argv)
    #if this script was called without args, display last results.
    #otherwise start search with arg provided
    if len(sys.argv) == 1:
        command = last_search
        print("Searching last query:")
    else:
        command = sys.argv[1]
    results = get_search_results(command)
    print_nicely(results, pagenumber)
    
    while True:
        command = input("Press 'q' to quit, 'n' for next page: ")#TODO, Make this print fun messages
        max_pages = math.ceil(len(results) / max_results)
        print(max_pages)
        if command.lower() == 'n' or command == "":
            if pagenumber > max_pages:
                pagenumber = 0
            else:
                pagenumber+=1

        elif command.lower().startswith("g "):
            last = ""
            command = command.split("g ")[1]
            results = get_search_results(command)
        
        #if input is q, exit program
        elif command == 'q':
            exit()
        
        else:
            #refine search further
            if last != "":
                results = get_search_results(last + "/" + command)
            else:
                results = get_search_results(command)
        #add the input to last, keeps track of the search
        #if its not the first search ""
        if last != "":
            last = last+"/"+command
        else:
            last = command

        print_nicely(results, pagenumber)


        # # debugging
        # print("Last is: "+last )
        # print("Cmmd is: "+command )
        


#main
if __name__ == "__main__":
    #catch keyboardinterrupt
    try:
        interactive_mode()
    except KeyboardInterrupt:
            print("\nGoodbye")
