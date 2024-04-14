#!/usr/bin/env python3
#usage: g <search>
# or just 'g' to enter interactive mode
# use 'help' while in interactive mode to edit settings
import subprocess
import sys
import re
import json
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
command=""

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
                # print(hostname)
                #if the current line matches on the query, add it to the results list
                #if the query has slashes '/' in it, treat them like a wildcard. So '/' = wildcard. Use Regex

                
                
                if re.match(regex_pattern, hostname, re.IGNORECASE):
                    results.append([hostname, ip])

    return results
#define a 2d array of search results
#[hostname, ip]

def print_nicely(results):
    hostnames = [pair for pair in results]
    formatted_hostnames = [f"{i+1}) {hostname[0]}  \t({hostname[1]})" for i, hostname in enumerate(hostnames)]

    #print the options to terminal
    #paginate the output if the results are above max_results
    # if len(hostnames) <= max_results:
    #     #dont paginate, just print them all
    #     for formatted_hostname in formatted_hostnames:
    #         print(formatted_hostname)
        
    # else:
    current_page = 0
    total_pages = -(-len(formatted_hostnames) // max_results)
    while True:
        print('\n'.join(formatted_hostnames[current_page * max_results: (current_page + 1) * max_results]))
        print(f"Page {current_page + 1}/{total_pages}")
        user_input = input("Press 'q' to quit, 'n' for next page: ")
        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 'n':
            current_page = (current_page + 1) % total_pages
        elif user_input.lower().startswith("g "):
            global command 
            command = user_input
            break
        #if input is a number, choose from the search results and spawn ssh
        elif re.match("(\d){1,2}", user_input): #regex
            #spawn ssh session now of that selection
            choice = int(user_input)
            if 0 <= choice <= len(results):
                ip = results[choice-1][1]
                sshcommand = "ssh"
                #add optional command options to ssh if wanted
                if ssh_pre_options != "":
                    sshcommand = ssh_pre_options + " " + sshcommand
                if ssh_post_options != "":
                    sshcommand = sshcommand + " " + ssh_post_options
                sshcommand += " " + ip

                subprocess.run(sshcommand, shell=True)
            
        else:
            print("Invalid input. Please press 'q' to quit or 'n' for next page.")        
    return

def interactive_mode():
    last=""
    results=[]
    global command
    # print(sys.argv)
    #if this script was called without args, display last results.
    #otherwise start search with arg provided
    if len(sys.argv) == 1:
        # Display last results
        #TODO
        # command="last"
        pass
    else:
        command = sys.argv[1]
    
    while True:
        if command == 'help':
            # Edit settings here
            pass

        elif command.lower().startswith("g "):
            last = ""
            command = command.split("g ")[1]
            results = get_search_results(command)
        
        #if input is q, exit program
        elif command == 'q':
            exit()
        
        

        elif command == "last": #regex
            #print last results
            print("Printing last search")
            pass

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
        #optional: cap the amount of results to a certain number
        if command.startswith("g "):
            command = input("Enter command: ")
        print_nicely(results)
        
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
