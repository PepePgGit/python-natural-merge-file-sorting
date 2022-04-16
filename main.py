import os
from shutil import copyfile
from random import randrange

from Buffer import Buffer
from Sign import Sign
from Record import RECORD_SIZE
from Chart import Chart


def file_input(file):
    for x in range(10):
        byte = file.read(1)
        while byte != "":
            nowy = Sign(byte)
            nowy.count_ones()
            print(byte)

def kb_input():
    my_input = input('write input: ')
    file_in = open("files/input.txt", "wb")

    for i in range(len(my_input)):
        file_in.write(bytes(my_input[i], 'ascii'))

def rand_input():
    file_in = open("files/input.txt", "wb")
    amount = int(input('amount of records: '))
    for _ in range(amount):
        for i in range(RECORD_SIZE):
            file_in.write(bytes(chr(randrange(32, 126)), 'ascii'))
    file_in.close()
    return amount

def choose_input() -> int:
    print('Wybierz opcje inputu: ')
    print('1. Klawiatura ')
    print('2. Plik')
    print('3. Losowe')
    try:
        mode = int(input('1-3:'))
        return mode
    except ValueError:
        print("Not a number")

if __name__ == '__main__':
    mode = choose_input()
    if mode == 1:
        kb_input()
    if mode == 3:
        records_amount = rand_input()
    #if mode == 2:
        #nic?
        #file_input(file)

    not_sorted = True
    liczba_faz = 0
    while not_sorted:
        # faza in
        file_in = open("files/input.txt", "rb")
        file_b = open("files/B.txt", "wb")
        file_c = open("files/C.txt", "wb")
        A = Buffer(file_in, file_b, file_c, None, 'A')
        B = Buffer(file_in, file_b, file_c, None, 'B')
        C = Buffer(file_in, file_b, file_c, None, 'C')

        A.write_page()
        last_record_val = 0
        while True:
            record = A.read_record()
            if not record:
                break
            new_value = record.get_value()
            if new_value < last_record_val:
                A.switch_direction()
            last_record_val = new_value
            if A.get_direction() == 'B':
                B.write_record(record)
            if A.get_direction() == 'C':
                C.write_record(record)
        B.save_page()  # resztki z B i C do outputu
        C.save_page()

        file_b.close()
        file_c.close()
        file_in.close()


        # faza out
        #file_in = open("out.txt", "wb")
        file_in = open("files/input.txt", "wb")
        file_b = open("files/B.txt", "rb")
        file_c = open("files/C.txt", "rb")
        file_value = open("files/value.txt", "w+")
        B_out = Buffer(file_in, file_b, file_c, None, 'B_out')
        C_out = Buffer(file_in, file_b, file_c, None, 'C_out')
        D = Buffer(file_in, file_b, file_c, file_value, 'D')

        C_out.write_page()
        if C_out.get_size() == 0:
            not_sorted = False  # posortowane
            copyfile('files/B.txt', 'files/input.txt')
        else:
            B_out.write_page()
        last_record_val_B = 0
        last_record_val_C = 0
        while not_sorted:
            if B_out.get_size() != 0 and C_out.get_size() != 0:  # specyficzny i normalny
                if B_out.get_top_value() < last_record_val_B:  # specyficzny
                    while C_out.get_top_value() >= last_record_val_C:
                        record = C_out.read_record()
                        D.write_record(record)
                        last_record_val_C = record.get_value()
                        if C_out.get_size() == 0:
                            break
                    last_record_val_B = 0
                    last_record_val_C = 0
                elif C_out.get_top_value() < last_record_val_C:  # specyficzny
                    while B_out.get_top_value() >= last_record_val_B:
                        record = B_out.read_record()
                        D.write_record(record)
                        last_record_val_B = record.get_value()
                        if B_out.get_size() == 0:
                            break
                    last_record_val_B = 0
                    last_record_val_C = 0
                elif B_out.get_top_value() < C_out.get_top_value():  # normalny
                    record = B_out.read_record()
                    D.write_record(record)
                    last_record_val_B = record.get_value()
                elif B_out.get_top_value() >= C_out.get_top_value():  # normalny
                    record = C_out.read_record()
                    D.write_record(record)
                    last_record_val_C = record.get_value()
            elif B_out.get_size() == 0:
                record = C_out.read_record()
                if not record:
                    break
                D.write_record(record)
            elif C_out.get_size() == 0:
                record = B_out.read_record()
                if not record:
                    break
                D.write_record(record)
        D.save_page()
        liczba_faz += 1

        file_value.close()
        file_b.close()
        file_c.close()
        file_in.close()
        #copyfile('out.txt', 'input.txt')

    # row = [D.read_counter, records_amount]
    # Chart.write_disc_csv(row)
    Chart.disc_sum_chart()

    # row = [liczba_faz, records_amount]
    # Chart.write_phase_csv(row)
    # Chart.phase_chart()

