import os
import random
from colorama import init, Fore, Style
import RPi.GPIO as GPIO
import time

init(autoreset=True)


def generate_pin():
    return [random.randint(0, 9) for _ in range(5)]


def check_pin(user_pin, correct_pin):
    result = []
    result_final = []
    correct_count = 0
    wrong_spot_count = 0
    for i in range(5):
        if user_pin[i] == correct_pin[i]:
            if user_pin[i] == correct_pin[0]:
                correct_count += 1
            if user_pin[i] == correct_pin[1]:
                correct_count += 1
            if user_pin[i] == correct_pin[2]:
                correct_count += 1
            if user_pin[i] == correct_pin[3]:
                correct_count += 1
            if user_pin[i] == correct_pin[4]:
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
            if user_pin[i] == correct_pin[4]:
                wrong_spot_count += 1
            if wrong_spot_count >= 2:
                result.append(Fore.YELLOW + "Wrong Spot." + "(" + str(wrong_spot_count) + ") ")
                result_final.append(Fore.YELLOW + "Wrong Spot.")
                wrong_spot_count = 0
            else:
                result.append(Fore.YELLOW + "Wrong Spot.")
                result_final.append(Fore.YELLOW + "Wrong Spot.")
                wrong_spot_count = 0



        else:
            result.append(Fore.RED + "Incorrect!")
            result_final.append(Fore.RED + "Incorrect!")

    return result, result_final


max_attempts = 5


def main():

    SOLENOID_PIN = 17
    DOOR_SENSOR_PIN = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOLENOID_PIN, GPIO.OUT)
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.output(SOLENOID_PIN, GPIO.LOW)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        correct_pin = generate_pin()
        print(Fore.GREEN + "===========================")
        print(Fore.GREEN + "Welcome to the Box PIN Game!")
        print(Fore.GREEN + "===========================")
        print("You have {} attempts.".format(max_attempts))
        print(Style.RESET_ALL)
        attempt = 1
        win_or_lose = False
        quit_game = False
        while attempt != 6:
            if GPIO.input(DOOR_SENSOR_PIN) == GPIO.HIGH:
                time.sleep(7)
                if GPIO.input(DOOR_SENSOR_PIN) == GPIO.HIGH:
                    print("Door is not closed")
                continue
            print("\n" + Fore.CYAN + "Attempt #{}".format(attempt))
            user_input = input("Enter a 5-digit PIN: ")
            if user_input == "quit":
                GPIO.cleanup()
                quit_game = True
                break

            if len(user_input) != 5 or not user_input.isdigit():
                print(Fore.RED + "Invalid input! Please enter a 5-digit PIN.")
                continue

            attempt += 1
            user_pin = [int(digit) for digit in user_input]

            result = check_pin(user_pin, correct_pin)[0]
            result_final = check_pin(user_pin, correct_pin)[1]

            print("Result: ", " ".join(result))

            if result_final == [Fore.GREEN + "Correct!"] * 5:
                print()
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.GREEN + "===========================================")
                print()
                print(Fore.GREEN + "Congratulations! You entered the correct PIN.")
                print()
                print(Fore.GREEN + "===========================================")
                GPIO.output(SOLENOID_PIN, GPIO.HIGH)
                time.sleep(0.3)
                door_open = False
                while door_open == False:
                    if GPIO.input(DOOR_SENSOR_PIN) != GPIO.HIGH:
                        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
                        continue

                    if GPIO.input(DOOR_SENSOR_PIN) == GPIO.HIGH:
                        door_open = True
                        GPIO.output(SOLENOID_PIN, GPIO.LOW)
                win_or_lose = True

                print()
                print()

                break

            if attempt < max_attempts:
                print(Fore.YELLOW + "Try again.")
        if quit_game == True:
            break

        if win_or_lose == False:
            print()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.RED + "Sorry, you've used all your attempts. The correct PIN was:", correct_pin)
            print()
            print()


if __name__ == "__main__":
    main()