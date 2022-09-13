"""
By: Renato Lulic
Instagram: renato_lulic
Date: September 14, 2022
For instructions or information, please refer to https://github.com/Reno-Codes/ENS-Expiration-Date-Checker/blob/main/README.md
"""

from datetime import datetime
from python_graphql_client import GraphqlClient

# Read readme.md
# Get API KEY on -> https://thegraph.com/studio/apikeys/
API_KEY = "Your-API-Key"
domain = "100.eth"


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

    # Print ENS Domain, Registration Date and Expiration Date
    print(f"- [ENS Domain]: {data['data']['domains'][0]['name']}")
    print(
        "- [Registration Date]:",
        datetime.fromtimestamp(
            int(data2["data"]["registrations"][0]["registrationDate"])
        ),
    )
    print(
        "- [Expiration Date]:",
        datetime.fromtimestamp(int(data2["data"]["registrations"][0]["expiryDate"])),
    )


if __name__ == "__main__":
    main()
