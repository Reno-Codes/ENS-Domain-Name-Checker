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

# Read readme.md
# Get API KEY on -> https://thegraph.com/studio/apikeys/
API_KEY = "e13b252c43ffc91724a27e33672a7df8"
domain = "100.eth"

# Include 90 days of grace period into date (True/False)
gracePeriod = True


def main():
    get_labelhash()


# Get labelhash
def get_labelhash():
    client = GraphqlClient(
        endpoint=f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/EjtE3sBkYYAwr45BASiFp8cSZEvd1VHTzzYFvJwQUuJx"
    )
    queryEnsDomain = {"ensDomain": f"{domain}"}

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
        print(colored("- [Grace Period Expiration]:", "red"), modified_date, "(", colored(formattedGraceDate, "red", attrs=["bold"]), ")")


if __name__ == "__main__":
    main()
