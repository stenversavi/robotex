import random
from colorama import init, Fore, Style

init(autoreset=True)


def generate_pin():
    return [random.randint(0, 9) for _ in range(4)]


def check_pin(user_pin, correct_pin):
    result = []
    result_final = []
    #Correcti ja wrong spoti korral checki kas seda on veel, lisa counti ja lisa stringi
    correct_count = 0
    wrong_spot_count = 0
    for i in range(4):
        if user_pin[i] == correct_pin[i]:
            if user_pin[i] == correct_pin[0]:
                correct_count += 1
            if user_pin[i] == correct_pin[1]:
                correct_count += 1
            if user_pin[i] == correct_pin[2]:
                correct_count += 1
            if user_pin[i] == correct_pin[3]:
                correct_count += 1
            if correct_count >= 2:
                result.append(Fore.GREEN + "Correct!" + "(" + str(correct_count) + ") ")
                result_final.append(Fore.GREEN + "Correct!")
                correct_count = 0
            else:
                result.append(Fore.GREEN + "Correct!")
                result_final.append(Fore.GREEN + "Correct!")
                correct_count = 0
        elif user_pin[i] in correct_pin and user_pin[i] != correct_pin[i]:
            if user_pin[i] == correct_pin[0]:
                wrong_spot_count += 1
            if user_pin[i] == correct_pin[1]:
                wrong_spot_count += 1
            if user_pin[i] == correct_pin[2]:
                wrong_spot_count += 1
            if user_pin[i] == correct_pin[3]:
                wrong_spot_count += 1
            if correct_count >= 2:
                result.append(Fore.YELLOW + "Wrong Spot." + "(" + str(wrong_spot_count) + ") ")
                result_final.append(Fore.YELLOW + "Wrong Spot.")
                wrong_spot_count = 0
            else:
                result.append(Fore.YELLOW + "Wrong Spot.")
                result_final.append(Fore.YELLOW + "Wrong Spot.")
                correct_count = 0    
                
                
        else:
            result.append(Fore.RED + "Incorrect!")
            result_final.append(Fore.RED + "Incorrect!")

    return result, result_final




max_attempts = 5


def main():
    while True:
        correct_pin = generate_pin()
        #correct_pin = [3,3,0,0]
        print(Fore.GREEN + "===========================")
        print(Fore.GREEN + "Welcome to the Box PIN Game!")
        print(Fore.GREEN + "===========================")
        print("You have {} attempts.".format(max_attempts))
        print(Style.RESET_ALL)
        attempt=1
        win_or_lose = False
        while attempt != 6:
            print("\n" + Fore.CYAN + "Attempt #{}".format(attempt))
            user_input = input("Enter a 4-digit PIN: ")

            if len(user_input) != 4 or not user_input.isdigit():
                print(Fore.RED + "Invalid input! Please enter a 4-digit PIN.")
                continue
            attempt += 1
            user_pin = [int(digit) for digit in user_input]

            result = check_pin(user_pin, correct_pin)[0]
            result_final = check_pin(user_pin, correct_pin)[1]
            
            print("Result: ", " ".join(result))

            if result_final == [Fore.GREEN + "Correct!"] * 4:
                print()
                print(Fore.GREEN + "Congratulations! You entered the correct PIN.")
                win_or_lose = True
                print()
                print()
                break

            if attempt < max_attempts:
                print(Fore.YELLOW + "Try again.")

        if win_or_lose==False:
            print()
            print(Fore.RED + "Sorry, you've used all your attempts. The correct PIN was:", correct_pin)
            print()
            print()



if __name__ == "__main__":
    main()