import os
os.system('color')
from termcolor import colored

# From which number it should start generating?
start_Number = 10000

# Up to which number it should generate?
end_Number = 10500


# Do not change anything below
if start_Number < 100:
    print(colored("\nENS domain must contain at least 3 digits!\nLowest number is 100 (100.eth)", "red"))
else:
    for i in range(start_Number, end_Number + 1):
        with open("domains.txt", "a") as file:
            file.write(str(start_Number) + ".eth\n")
            start_Number += 1
    print(colored("\nFinished.", "green"))
    print(colored("Saved to number-domains.txt!", "green"))