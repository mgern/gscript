# gscript
CLI SSH jumpbox selector. Quickly jump from one jumpbox to ssh hosts at lightning speed!

![Screen-Recording-2024-11-16-2246](https://github.com/user-attachments/assets/a1a9ae6c-4484-4fc1-a601-86b5ba70d089)

Useful if you manage a fleet of network appliances from either your computer or an SSH jump host. 
Pairs well with a well organised hostnaming structure.
No more clicking around in a massive SecureCRT or Mobaxterm tree



# FAQ:
## 0. How to install?
Download g.py, add an alias to it or somehow get it into your PATH
Make a windows hosts style file full of your hostnames and IPs. Point it to that in settings.json

If you want to change anything, just do it, it's Python after all.

## 1. How does it work?
It's a python loop that does Regex and provides the user with a selection of search results, which then just executes SSH in your environment (Windows, linux, anything)

## 2. Can this support intermediate jumphosts between me and the switch/router/server?
Yes you can do this as per normal by editing your ssh_config file if using OpenSSH on Linux

## 3. Can I get Syntax Highlighting by using this tool?
Yes! I pair it with [Chromaterm](https://github.com/hSaria/ChromaTerm) which I've configured in settings.json like so:

![image](https://github.com/user-attachments/assets/bb37e634-183e-429c-baa9-526ec268daf4)

By having 'ct' in ssh_pre_options, it will prepend that to the string before executing 'ssh <hostname'






TODO 
 - ~~refactor code to one while loop~~
 - ~~use the Python shebang or wrapper script so a user can run the file as an executable~~
 - consider the use case for someone using their hosts file legitimately
