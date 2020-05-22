import sys
from concurrent.futures.process import ProcessPoolExecutor
from multiprocessing import Process
from multiprocessing.pool import Pool

from rainbow_table import RainbowTable

rainbow_table = RainbowTable()
indexes = []

def load_input_arguments():
    for argument in sys.argv:
        if argument.startswith("-help"):
            #print helpa
            break
        if argument.startswith("-n="):
            n = int(argument[3:])
            rainbow_table.set_num_process(n)
        if argument.startswith("-rainbow_file="):
            rainbow_file = argument[14:]
            rainbow_table.load_table(rainbow_file)
        if argument.startswith("-plain_texts_file="):
            plain_texts_file = argument[18:]
            rainbow_table.load_plain_texts(plain_texts_file)
        if argument.startswith("-chains="):
            chains = int(argument[8:])
            rainbow_table.set_chains(chains)
        if argument.startswith("-chain_length="):
            chain_length = int(argument[14:])
            rainbow_table.set_chain_length(chain_length)
        if argument.startswith("-password_length="):
            password_length = int(argument[17:])
            rainbow_table.set_password_length(password_length)
        if argument.startswith("-alphabet_file="):
            alphabet_file = argument[15:]
            rainbow_table.load_alphabet(alphabet_file)
        if argument.startswith("-crack="):
            crack = argument[7:]
            rainbow_table.set_crack(crack)


def divide_indexes_range(vector_size, n):
    global indexes
    indexes = [0] * (n + 1)
    indexes[0] = 0
    rang = int(vector_size / n)
    for i in range(1, n):
        indexes[i] = i * rang
    indexes[n] = vector_size


if __name__ == "__main__":
    load_input_arguments()
    if rainbow_table.check_consistence_data() is False:
        exit(0)
    rainbow_table.print_data()
    if rainbow_table.get_crack() is not None:
        n = rainbow_table.get_num_process()
        divide_indexes_range(100, n)
        print("Tekst jawny do szukanego hasha to: " + rainbow_table.get_crack())
    else:
        size = rainbow_table.get_table_size()
        chains = rainbow_table.get_chains()
        if chains != size:
            rainbow_table.generate_plain_texts()
        else:
            if rainbow_table.is_table_seeded():
                rainbow_table.generate_plain_texts()
        n = rainbow_table.get_num_process()
        results = None
        with ProcessPoolExecutor(max_workers=n) as executor:
            results = executor.map(rainbow_table.create_chain, range(100))
        for result in results:
            rainbow_table.modify_table(result)
        rainbow_table.export_rainbow_table()
        print("Tablica zapisana do pliku wynikowego")

