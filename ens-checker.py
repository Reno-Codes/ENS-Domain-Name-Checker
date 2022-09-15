"""
By: Renato Lulic
Instagram: renato_lulic
Date: September 14, 2022
For instructions or information, please refer to https://github.com/Reno-Codes/ENS-Expiration-Date-Checker/blob/main/README.md
"""

import os
from termcolor import colored
from datetime import datetime, timedelta
from python_graphql_client import GraphqlClient
os.system('color')

print(colored("""
$$$$$$$$\ $$\   $$\  $$$$$$\  $$$$$$$$\ $$$$$$$\   $$$$$$\  
$$  _____|$$$\  $$ |$$  __$$\ $$  _____|$$  __$$\ $$  __$$\ 
$$ |      $$$$\ $$ |$$ /  \__|$$ |      $$ |  $$ |$$ /  \__|
$$$$$\    $$ $$\$$ |\$$$$$$\  $$$$$\    $$ |  $$ |$$ |      
$$  __|   $$ \$$$$ | \____$$\ $$  __|   $$ |  $$ |$$ |      
$$ |      $$ |\$$$ |$$\   $$ |$$ |      $$ |  $$ |$$ |  $$\ 
$$$$$$$$\ $$ | \$$ |\$$$$$$  |$$$$$$$$\ $$$$$$$  |\$$$$$$  |
\________|\__|  \__| \______/ \________|\_______/  \______/
""", "yellow"))
print(colored("ENS Expiration Date Checker by Reno-Codes", "green"))
print("Github: ", colored("https://github.com/Reno-Codes/ENS-Expiration-Date-Checker", "cyan"),"\n")


# Read readme.md
# Get API KEY on -> https://thegraph.com/studio/apikeys/

# Include 90 days of grace period into date (True/False)
gracePeriod = True


def main():
    
    while True:
        # Read API Key
        API_KEY = read_Api()
        domain = input("Check ENS domain: ")

        try:
            name, extension = domain.lower().split(".")

            if extension == "eth":
                # Check if API Key is valid
                if is_api_valid(domain.lower(), API_KEY):
                    # Get labelhash
                    get_labelhash(domain, API_KEY)

                else:
                    print(colored(f"Your API Key is not valid.\nPlease enter valid API Key!", "red", attrs=["bold"]))
                    print(colored("You can get API KEY on -> https://thegraph.com/studio/apikeys/\n", "yellow", attrs=["bold"]))
                    # Ask user to input API Key
                    add_Api()

            else:
                print(colored("ENS Domain must end with '.eth'", "red"))

        except ValueError:
            print(colored("ENS Domain must contain 1 dot (example.eth)", "red"))


# Read API Key
def read_Api():

    try:
        with open("config.txt", "r") as configFile:
            formatAPI = configFile.readline()
            temp, API_KEY = formatAPI.replace(" ", "").split("=")
            return API_KEY

    except:
        return add_Api()

# Ask user to input API Key
def add_Api():

    API_KEY = input("Enter your API Key: ")

    with open("config.txt", "w") as configFile:
        configFile.write(f"[API_KEY] = {API_KEY}")
        return API_KEY


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
    try:
        data = client.execute(query=query, variables=queryEnsDomain)
        labelhash = data["data"]["domains"][0]["labelhash"]
        get_expirationDate(client, labelhash, data)

    except IndexError:
        print(colored(f"{d.lower()} is not registered.", "green"))
    
    


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
    print(colored("- [ENS Domain]:", "green"), f"{data['data']['domains'][0]['name']}")

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


def is_api_valid(d, api):

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
    try:
        data = client.execute(query=query, variables=queryEnsDomain)
        labelhash = data["data"]["domains"][0]["labelhash"]
        return True
        
    except:
        pass


if __name__ == "__main__":
    main()
