"""
By: Renato Lulic
Instagram: renato_lulic
Date: September 14, 2022
For instructions or information, please refer to https://github.com/Reno-Codes/ENS-Domain-Name-Checker/blob/main/README.md
"""

import os
import random
import time
# TODO from alive_progress import alive_bar
from termcolor import colored
from datetime import datetime, timedelta
from python_graphql_client import GraphqlClient
os.system('color')

print(colored("""
$$$$$$$$\ $$\   $$\  $$$$$$\  $$$$$$$\  $$\   $$\  $$$$$$\  
$$  _____|$$$\  $$ |$$  __$$\ $$  __$$\ $$$\  $$ |$$  __$$\ 
$$ |      $$$$\ $$ |$$ /  \__|$$ |  $$ |$$$$\ $$ |$$ /  \__|
$$$$$\    $$ $$\$$ |\$$$$$$\  $$ |  $$ |$$ $$\$$ |$$ |      
$$  __|   $$ \$$$$ | \____$$\ $$ |  $$ |$$ \$$$$ |$$ |      
$$ |      $$ |\$$$ |$$\   $$ |$$ |  $$ |$$ |\$$$ |$$ |  $$\ 
$$$$$$$$\ $$ | \$$ |\$$$$$$  |$$$$$$$  |$$ | \$$ |\$$$$$$  |
\________|\__|  \__| \______/ \_______/ \__|  \__| \______/
""", "yellow"))
print(colored("ENS Domain Name Checker by Reno-Codes", "green"))
print("Github: ", colored("https://github.com/Reno-Codes/ENS-Expiration-Date-Checker", "cyan"),"\n")


# Read readme.md
# Get API KEY on -> https://thegraph.com/studio/apikeys/

# Include 90 days of grace period into date (True/False)
gracePeriod = True

# TODO: Progress bar at line 102

def compute(tasks):
    for i in range(tasks):
        ... # process items as usual.
        yield  # insert this :)

ensOptions = int(input("[1] - Check one by one\n[2] - Check ENS domains from .txt file\n[3] - Generate random ENS domains and check them\n\n[1, 2, 3] - Your answer: "))
def main():
    if ensOptions == 1:
        # Read API Key
        API_KEY = read_Api()

        while True:
            domain = input("Check ENS domain: ")

            if is_domain_registered(domain, API_KEY):
                try:
                    _, extension = domain.lower().split(".")

                    if extension == "eth":
                        # Get labelhash
                            get_labelhash(domain, API_KEY)

                    else:
                        print(colored("ENS Domain must end with '.eth'", "red"))

                except ValueError:
                    print(colored("ENS Domain must contain 1 dot (example.eth)", "red"))


    elif ensOptions == 2:
        # Read API Key
        API_KEY = read_Api()

        fileCounter = 1
        txtFileList = []
        path="./"  
        dirList=os.listdir(path)
        for filename in dirList:
            try:
                _, ext = filename.split(".")
                if ext == "txt":
                    print(f"[{fileCounter}] -> {filename}")
                    txtFileList.append(filename)
                    fileCounter += 1

            except ValueError:
                pass
        
        
        domainFile = int(input("\nFrom which .txt file to check ENS domains?\n- Your answer: "))

        sortedDomains = []

        # Read from domains.txt file
        try:
            with open(f"{txtFileList[domainFile - 1]}") as file:
                for line in file:
                        # Appending from file(list) to the list "sortedDomains"
                        sortedDomains.append(line.rstrip())

                if len(sortedDomains) < 1:
                        print(colored("domains.txt file is empty!", "red"))
                        print(colored("Add some ENS domains to domains.txt file and try again!", "yellow"))
                    
            # # TODO progress bar
            # with alive_bar(100) as bar:
            #     for i in compute(len(sortedDomains)):
            #         bar()

            # Loop over sortedDomains and sort them
            for ens in sorted(sortedDomains):
                domain = ens
                if is_domain_registered(domain, API_KEY):
                    try:
                        _, extension = domain.lower().split(".")

                        if extension == "eth":
                    # Get labelhash
                            get_labelhash(domain, API_KEY)

                        else:
                            print(colored("ENS Domain must end with '.eth'", "red"))

                    except ValueError:
                        print(colored("ENS Domain must contain 1 dot (example.eth)", "red"))
                        
        except FileExistsError:
            print(colored("Error! - domains.txt file does not exist!"))

    
    elif ensOptions == 3:
        # Read API Key
        API_KEY = read_Api()

        # Get digits
        try:
            get_digits = int(input("\nHow many digits?: "))
            if get_digits < 3:
                print(colored("Error! Must be a number greater than 2\n", "red"))
                get_digits = int(input("\nHow many digits?: "))
        except:
            print(colored("Error! Must be a number greater than 2!", "red"))
            print("exiting...")
            time.sleep(4)
            exit()
        
        # Get quantity
        try:
            get_quantity = int(input(f"How many {get_digits}-digit ENS domains to generate?: "))
        except:
            print(colored("Error! Must be a number!", "red"))
            print("exiting...")
            time.sleep(4)
            exit()

        generate_Random_Ens(get_digits, get_quantity)
        randomSorted = []

        # Read from domains.txt file
        try:
            with open(f"random-domains.txt") as file:
                for line in file:
                        # Appending from file(list) to the list "randomSorted"
                        randomSorted.append(line.rstrip())

                if len(randomSorted) < 1:
                        print(colored("random-domains.txt file is empty!", "red"))
                        print(colored("Try generating again...", "yellow"))
                        print("exiting...")
                        time.sleep(4)
                        exit()
                    
            # # TODO progress bar
            # with alive_bar(100) as bar:
            #     for i in compute(len(randomSorted)):
            #         bar()

            # Loop over randomSorted and sort them
            for ranDomain in sorted(randomSorted):
                domain = ranDomain
                if is_domain_registered(domain, API_KEY):
                    try:
                        _, extension = domain.lower().split(".")

                        if extension == "eth":
                    # Get labelhash
                            get_labelhash(domain, API_KEY)

                        else:
                            print(colored("ENS Domain must end with '.eth'", "red"))

                    except ValueError:
                        print(colored("ENS Domain must contain 1 dot (example.eth)", "red"))
                        
        except FileExistsError:
            print(colored("Error! - domains.txt file does not exist!"))


# Read API Key
def read_Api():

    try:
        with open("config.ini", "r") as configFile:
            formatAPI = configFile.readline()
            temp, API_KEY = formatAPI.replace(" ", "").split("=")
            if is_api_valid(API_KEY):
                return API_KEY
            else:
                print(colored(f"Your API Key is not valid.\nPlease enter valid API Key!", "red", attrs=["bold"]))
                print(colored("You can get API KEY on -> https://thegraph.com/studio/apikeys/\n", "yellow", attrs=["bold"]))
                # Ask user to input API Key
                add_Api()
            

    except:
        return add_Api()

# Ask user to input API Key
def add_Api():

    API_KEY = input("- Enter your API Key: ")

    with open("config.ini", "w") as configFile:
        configFile.write(f"[API_KEY] = {API_KEY}")
        if is_api_valid(API_KEY):
                return API_KEY
        else:
            print(colored(f"Your API Key is not valid.\nPlease enter valid API Key!", "red", attrs=["bold"]))
            print(colored("You can get API KEY on -> https://thegraph.com/studio/apikeys/\n", "yellow", attrs=["bold"]))
            # Ask user to input API Key
            add_Api()


# Get labelhash
def get_labelhash(d, api):

    client = GraphqlClient(
        endpoint=f"https://gateway.thegraph.com/api/{api}/subgraphs/id/EjtE3sBkYYAwr45BASiFp8cSZEvd1VHTzzYFvJwQUuJx")

    queryEnsDomain = {"ensDomain": f"{d.lower()}"}

    query = """
    query ensQuery($ensDomain: String) 
    {
         domains(where:{name:$ensDomain})
        {
            name
            labelhash
        }
    }
    """
    data = client.execute(query=query, variables=queryEnsDomain)
    labelhash = data["data"]["domains"][0]["labelhash"]
    get_expirationDate(client, labelhash, data)
    
    
# Get Expiration Date from ENS Domain labelhash
def get_expirationDate(client, labelhash, data):

    queryEnsLabelhash = {"labelhash": "{}".format(labelhash)}

    query2 = """
    query idQuery($labelhash: String)
    {
        registrations(first: 1, where:{id:$labelhash}) 
        {
            id
            registrationDate
            expiryDate
        }
    }
    """

    data2 = client.execute(query=query2, variables=queryEnsLabelhash)

    # Print ENS Domain
    print(colored("- [ENS Domain]:", "green"), colored(f"[ {data['data']['domains'][0]['name']} ]", "cyan", attrs=["underline"]))

    # Print Registration Date
    print(colored("- [Registration Date]:", "green"), datetime.fromtimestamp(int(data2["data"]["registrations"][0]["registrationDate"])), 
    "(", datetime.fromtimestamp(int(data2["data"]["registrations"][0]["registrationDate"])).strftime("%b %d, %Y at %H:%M"), ")")

    # Print Expiration Date
    print(colored("- [Expiration Date]:", "yellow"), datetime.fromtimestamp(int(data2["data"]["registrations"][0]["expiryDate"])),
    "(", colored(datetime.fromtimestamp(int(data2["data"]["registrations"][0]["expiryDate"])).strftime("%b %d, %Y at %H:%M"), "yellow", attrs=["bold"]), ")")

    # Print Grace Period Calculation
    if gracePeriod:
        grace = datetime.fromtimestamp(int(data2["data"]["registrations"][0]["expiryDate"]))
        modified_date = grace + timedelta(days=90)
        formattedGraceDate = modified_date.strftime("%b %d, %Y at %H:%M")
        print(colored("- [Grace Period Expiration]:", "red"), modified_date, "(", colored(formattedGraceDate, "red", attrs=["bold"]), ")\n")

# Check if API Key is valid
def is_api_valid(api):

    client = GraphqlClient(
        endpoint=f"https://gateway.thegraph.com/api/{api}/subgraphs/id/EjtE3sBkYYAwr45BASiFp8cSZEvd1VHTzzYFvJwQUuJx")

    queryEnsDomain = {"ensDomain": "100.eth"}

    query = """
    query ensQuery($ensDomain: String) 
    {
         domains(where:{name:$ensDomain})
        {
            name
            labelhash
        }
    }
    """
    data = client.execute(query=query, variables=queryEnsDomain)
    try: # API Key Check
       if data["errors"]["message"].lower() == "invalid api key":
                return False
    except:
        try:
            if data["data"]["domains"][0]["labelhash"]:
                print(colored("Success! API Key is valid!\n", "green"))
                return True
        except:
            # API Key valid, but domain free (can't read labelhash)
            return False


# Check if domain is already registered
def is_domain_registered(d, api):
    client = GraphqlClient(
        endpoint=f"https://gateway.thegraph.com/api/{api}/subgraphs/id/EjtE3sBkYYAwr45BASiFp8cSZEvd1VHTzzYFvJwQUuJx")

    queryEnsDomain = {"ensDomain": f"{d.lower()}"}

    query = """
    query ensQuery($ensDomain: String) 
    {
         domains(where:{name:$ensDomain})
        {
            name
            labelhash
        }
    }
    """
    data = client.execute(query=query, variables=queryEnsDomain)
    # Check if domain is already registered
    try:
        if data["data"]["domains"][0]["labelhash"]:
            return True

    except:
        print(colored(f"\n[FREE DOMAIN] - {d.lower()} is available to register!", "green"))
        print(f"Register it here ->" , colored(f"[ https://app.ens.domains/name/{d.lower()}/register ]", "cyan"))
        with open("free_domains.txt", "a") as freeFile:
            freeFile.write(f"{d.lower()}\n")
        print(colored("Added to free_domains.txt file!\n", "yellow"))
        return False


# Generate random ENS domain
def generate_Random_Ens(dig, qty):
    chrs = 'abcdefghijklmnopqrstuvwxyz'

    characters = dig

    quantity = qty

    words = []
    for w in range(0, quantity - 1):
        result = ''.join(random.choice(chrs) for _ in range(characters))
        words.append(result + ".eth")


    test_list = list(set(words))
    
    with open("random-domains.txt", "a") as randomWordFile:
        for word in test_list:
            randomWordFile.write(f"{word}\n")

    print(colored("\nFinished.", "green"))
    print(colored("Saved to random-domains.txt!", "green"))


if __name__ == "__main__":
    main()
