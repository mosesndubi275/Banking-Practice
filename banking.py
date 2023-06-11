# Write your code here
import random
import sqlite3
import uuid

options = '1. Create Account \n''2. Login \n' '0. Exit \n'
second_options = '1. Balance \n' '2. Add Income \n' '3. Do Transfer \n' '4. Close Account \n' '5. Log Out \n' '0. ' \
                 'Exit \n'


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
        choice = 'Add Income'
        return choice
    if number == 3:
        choice = 'Do Transfer'
        return choice
    if number == 4:
        choice = 'Close Account'
        return choice
    if number == 5:
        choice = 'Log Out'
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
    card_number = create_card()
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
        return pin


login_screen = menu()
connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute('Create TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, '
               'balance INTEGER DEFAULT 0)')


# Functions that directly deal with the database


def data_base(id_number, card_number, pin_number, balance):
    cursor.execute("Insert Into card VALUES (?,?,?,?)",
                   (id_number, card_number, pin_number, balance))
    connection.commit()
    res2 = cursor.execute('Select * from card')
    return res2.fetchall()


def get_balance(pin_number):
    res = cursor.execute(f"""SELECT balance 
                            FROM card
                            WHERE pin = {pin_number}""")
    cards = res.fetchall()[0][0]
    return cards


def find_account(card_number, pin_number):
    res = cursor.execute(f"""Select * FROM card WHERE number = {card_number} AND pin = {pin_number}""")
    result = res.fetchall()[0]
    return result


def add_income(card_number, deposit_amount):
    res = cursor.execute(f"""UPDATE card
                            SET balance = {deposit_amount} + balance
                            WHERE number = {card_number}""")
    return


def do_transfer(depositing_card, receiving_card):
    try:
        res = cursor.execute(f"Select * from card where number = {receiving_card}")
        result = res.fetchall()
        return result
    except: raise(ValueError("CARD DOES NOT EXIST"))



def close_account():
    pass


while login_screen != 'Exit':
    if login_screen == 'Create Account':
        customer_card = luhn_algorithm()
        customer_pin = create_pin()
        unique_id = str(uuid.uuid4().int)[:4]
        user_info = data_base(unique_id, customer_card, customer_pin, '0')
        message = (
            f"Your card has been created\n"
            f"Your card number:\n"
            f"{customer_card}\n"
            f"Your card PIN:\n"
            f"{customer_pin}")
        print(message)
    login_screen = menu()
    if login_screen == 'Login':
        login_info = input('Enter your card info: ')
        pin = input('Enter your pin: ')
        if login_info and pin in find_account(login_info, pin):
            print('You have Successfully Logged in! ')
            user_options = logged_in_menu()
            if user_options == 'Balance':
                print(f'Your balance is ${get_balance(str(pin))}')
                user_options = logged_in_menu()
            if user_options == 'Logout':
                print('You have Successfully Logged out! ')
            if user_options == 'Exit':
                print('Bye!')
                break
        else:
            print('Wrong user information')
    if login_screen == 'Exit':
        print('Bye!')
