import os
import subprocess
import json
import hashlib
import sys
from getpass import getpass
import nmap
from time import sleep as tsleep, time as ttime
import requests

def clear():
    if os.name == "nt": subprocess.call("cls", shell=True)
    elif os.name == "cmd": subprocess.call("cls", shell=True)
    else: subprocess.call("clear",shell=True)

clear()

nmScan = nmap.PortScanner()

class login_program:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        
    def put_in_file(self):

        with open("log.key", "w+") as file:
            log = {
                "data_1":hashlib.md5(str(self.username).encode()).hexdigest(),    
                "data_2":hashlib.md5(str(self.password).encode()).hexdigest()            
                }
            log_ = json.dumps(log)

            file.write(log_)

    def login_logo(): print("""\033[92m                              
`888                              
 888 .oo.    .oooo.   oooo    ooo 
 888P"Y88b  `P  )88b   `88b..8P'  
 888   888   .oP"888     Y888'    
 888   888  d8(  888   .o8"'88b   
o888o o888o `Y888""8o o88'   888o 
                                 \033[0m\n\033[93mFor Linux/GNU \n""")

    def login_screen(): print("\033[36m\033[01m\033[04mLogin\033[0m\n")




class main_program:
    def main_logo(): print("""
\033[04m\033[01mSelect an Action.\033[0m

╔═══════════╦═════════════════════════════════╦═══════════════╗
║ \033[01mSelection\033[0m ║            \033[01mAction\033[0m               ║   \033[01mCategory\033[0m    ║
╠═══════════╬═════════════════════════════════╬═══════════════╣
║     1     ║ \033[33mPort Scanner\033[0m                    ║   \033[94mNetwork\033[0m     ║
║     2     ║ \033[33mPhisher(Powered by ZPhisher)\033[0m    ║   \033[94mPhishing\033[0m    ║
║     3     ║ \033[33mURL-masker\033[0m                      ║   \033[94mPhishing\033[0m    ║
╚═══════════╩═════════════════════════════════╩═══════════════╝\n""")

    def selection_1():
        ip_inp = input("\nEnter Target IP: \033[36m")

        try:
            print("\033[90mloading...\033[0m\n")
            start_t = ttime()

            rg = requests.get("http://ip-api.com/json/{}".format(str(ip_inp))).json()
            

            nmScan.scan(str(ip_inp), "22-443")
            nmScan.command_line()
            #print(nmScan[str(ip_inp)].all_protocols()[0:])
            str_nm = " ".join(nmScan[str(ip_inp)].all_protocols()[0:])
            

            if nmScan[str(ip_inp)].state() == "up": 
                print("="*34 + "\n")
                success_msg("IP is online")
                success_msg("Country: {}".format(rg["country"]))
                success_msg("City: {}".format(rg["city"]))
                success_msg("Organisation: {}".format(rg["org"]))
                success_msg("Available Protocols: {}".format(str_nm.upper()))
                for host in nmScan.all_hosts():
                    for proto in list(nmScan[host].all_protocols()):
                        lport = nmScan[host][proto].keys()
                        list(lport).sort()
                        for port in lport:
                            print("[\033[92m\033[01m+\033[0m] Port \033[96m%s\033[0m\tState: \033[96m%s\033[0m" % (port, str(nmScan[host][proto][port]["state"]).upper()))
                end_t = ttime()

                result_t = end_t - start_t

                if result_t >= 60: print("\nTime: \033[96m%sm\033[0m" % (round((end_t-start_t)/60, 2)))
                else:  print("\nTime: \033[96m%ss\033[0m" % (round(result_t, 2)))



        except KeyError: error_msg("Host is not accessable")
    

    def selection_2():
        if os.path.exists("./zphisher") == False: 
            print("\nInstalling ZPhisher. Please wait...\n")
            subprocess.run(["git","clone","https://github.com/htr-tech/zphisher.git"], shell=False)
            clear()
            os.chdir("./zphisher")
            subprocess.call("sudo bash zphisher.sh", shell=True)
        else: 
            os.chdir("./zphisher")
            subprocess.call("sudo bash zphisher.sh", shell=True)

    def selection_3():
        URL_inp_1 = str(input("\nURL (http or https): \033[36m"))
        mask_url = str(input("\033[0mMask-Domain: \033[36m"))
        print("\033[90mloading...\033[0m")

        get_url_dat_1 = "https://" + mask_url + "@" + str(subprocess.check_output("curl -s " + "https://is.gd/create.php\?format\=simple\&url\={}".format(URL_inp_1), encoding="UTF-8", shell=True)).replace("https://","")
        
        print()
        success_msg("End-URL: " + str(get_url_dat_1))

    

def error_msg(msg:str): print("[\033[31m\033[01m-\033[0m]\033[91m ERROR:\033[0m \033[31m\033[01m{}\n\033[0m".format(msg))
def success_msg(msg:str): print("[\033[92m\033[01m+\033[0m]\033[32m SUCCESS:\033[0m \033[32m\033[01m{}\n\033[0m".format(msg))




try:
    while True:
        login_program.login_logo()
        login_program.login_screen()

        username__ = str(input("Username: "))
        password__ = str(getpass("Password: "))

        User = login_program(username__, password__)

        try:
            
            with open("log.key", "r", encoding="utf-8") as file_:
                read_file_= json.load(file_)
                __username = read_file_["data_1"]
                __password = read_file_["data_2"]

                if str(hashlib.md5(username__.encode()).hexdigest()) == str(__username) and  str(hashlib.md5(password__.encode()).hexdigest()) == str(__password):
                    success_msg("Login successful")
                    tsleep(1.7)
                    clear()
                    login_program.login_logo()
                    main_program.main_logo()

                    while True:
                        try: 
                            usr_choice_2 = int(input("Select an option (1 - 3): "))
                    
                            if usr_choice_2 == 1: 
                                main_program.selection_1()
                                break;
                            elif usr_choice_2 == 2: 
                                main_program.selection_2()
                                break;
                            elif usr_choice_2 == 3: 
                                main_program.selection_3()
                                break;
                            else: 
                                error_msg("Not a valid input!")
                                tsleep(1.6)
                                clear()
                                login_program.login_logo()
                                main_program.main_logo()

                        except ValueError: error_msg("Invalid input")
                                
                    input("\nPress \033[92m'Enter'\033[0m to go back.")
                    clear()
                    
                else: 
                    error_msg("wrong username/password")
                    tsleep(1.5)
                    clear()

        except IOError: 
            User.put_in_file()
            success_msg("Registration complete")
            tsleep(1.5)
            clear()
        
except KeyboardInterrupt: 
    print("\n\n\033[90mProgram closed.\033[0m\n")
    sys.exit()
