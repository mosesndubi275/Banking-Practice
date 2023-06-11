import random
import sqlite3
# Create new banking system
"""Objective is to allow a cx to create a new account on our system by issuing them a new card number 
 and pin #. The card has to begin with 400000 followed by 10 digits.
 
 I need a input system for the cx that allows them either create account, login, or exit the script"""

options = '1. Create Account \n''2. Login \n' '0. Exit \n'
second_options = '1. Balance \n' '2. Logout \n' '0. Exit \n'


def menu():
    number = int(input(options))
    if number == 1:
        choice = 'Create Account'
        return choice
    if number == 2:
        choice = 'Login'
        return choice
    if number == 0:
        choice = 'Exit'
        return choice


def logged_in_menu():
    number = int(input(second_options))
    if number == 1:
        choice = 'Balance'
        return choice
    if number == 2:
        choice = 'Logout'
        return choice
    if number == 0:
        choice = 'Exit'
        return choice


def create_card():
    base = 400000
    new_number = random.randint(1000000000, 9999999999)
    card_number = str(base) + str(new_number)
    return int(card_number)


def luhn_algorithm():
    card_number = 4000004978139885
    string_number = [int(i) for i in str(card_number)]
    string_number.pop(-1)
    range_ = range(0, 15)
    for number in range_:
        if number % 2 == 0:
            string_number[number] = (string_number[number] * 2)
    for i, element in enumerate(string_number):
        if element > 9:
            string_number[i] = element - 9
    checksum = [int(i) for i in str(sum(string_number))]

    if checksum[1] != 0:
        final_checksum = abs(checksum[1] - 10)
        final_card_number = [str(i) for i in str(card_number)]
        final_card_number.pop(-1)
        final_card_number.append(str(final_checksum))
        return int("".join(final_card_number))
    else:
        final_checksum = 0
        final_card_number = [str(i) for i in str(card_number)]
        final_card_number.pop(-1)
        final_card_number.append(str(final_checksum))
        return int("".join(final_card_number))


def create_pin():
    pin = random.randint(0000, 9999)
    if len(str(pin)) != 4:
        pin = str(pin) + '0'
        return int(pin)
    else:
        return random.randint(0000, 9999)


login_screen = menu()
user_card_information = {}

while login_screen != 'Exit':
    if login_screen == 'Create Account':
        customer_card = luhn_algorithm()
        customer_pin = create_pin()
        user_card_information[customer_card] = customer_pin
        message = (
            f"Your card has been created\n"
            f"Your card number:\n"
            f"{customer_card}\n"
            f"Your card PIN:\n"
            f"{customer_pin}")
        print(message)
    login_screen = menu()
    if login_screen == 'Login':
        login_info = int(input('Enter your card info: '))
        pin = int(input('Enter your pin: '))
        if login_info in user_card_information and user_card_information[login_info] == pin:
            print('You have Successfully Logged in! ')
            user_options = logged_in_menu()
            if user_options == 'Balance':
                print(0)
                user_options = logged_in_menu()
            if user_options == 'Logout':
                print('You have Successfully Logged out! ')
            if user_options == 'Exit':
                print('Bye!')
                break
        else:
            print('Wrong user information')
    if login_screen == 'Exit':
        user_card_information.clear()
        print('Bye!')
