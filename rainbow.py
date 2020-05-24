import sys
from concurrent.futures.process import ProcessPoolExecutor

from rainbow_table import RainbowTable

rainbow_table = RainbowTable()
indexes = []


def load_input_arguments():
    for argument in sys.argv:
        if argument.startswith("-rainbow_file="):
            rainbow_file = argument[14:]
            rainbow_table.load_table(rainbow_file)
    for argument in sys.argv:
        if argument.startswith("-help"):
            print("Jeśli chcesz crackować hasza masz opcję podania następujących parametrów:")
            print("-crack=hasz - hasz do crackowania")
            print("-n=liczba - liczba pracujących procesów")
            print("-rainbow_file=plik - plik z tablicą tęczową")
            print("")
            print("Jeśli chcesz utworzyć tablicę tęczową masz opcję podania następujących argumentów:")
            print("-chains=liczba - ilość łańcuchów w tablicy do wygenerowania")
            print("-plain_texts_file=plik - plik z tekstami jawnymi do tablicy")
            print("-chain_length=liczba - głębokość łańcucha (ilość haszy i redukcji)")
            print("-password_length=liczba - długość generowanych haseł")
            print("-alphabet_file=plik - plik z alfabetem")
            print("-n=liczba - liczba pracujących procesów")
            print("-rainbow_file=plik - plik z tablicą tęczową, nowe łańcuchy będą do niego dopisane")
            print("Argument ilości łańcuchów jest wymagany jeśli nie podano pliku z tekstami jawnymi")
            exit(0)
        elif argument.startswith("-n="):
            n = int(argument[3:])
            rainbow_table.set_num_process(n)
        elif argument.startswith("-plain_texts_file="):
            plain_texts_file = argument[18:]
            rainbow_table.load_plain_texts(plain_texts_file)
        elif argument.startswith("-chains="):
            chains = int(argument[8:])
            rainbow_table.set_chains(chains)
        elif argument.startswith("-chain_length="):
            chain_length = int(argument[14:])
            rainbow_table.set_chain_length(chain_length)
        elif argument.startswith("-password_length="):
            password_length = int(argument[17:])
            rainbow_table.set_password_length(password_length)
        elif argument.startswith("-alphabet_file="):
            alphabet_file = argument[15:]
            rainbow_table.load_alphabet(alphabet_file)
        elif argument.startswith("-crack="):
            crack = argument[7:]
            rainbow_table.set_crack(crack)


if __name__ == "__main__":
    load_input_arguments()
    if rainbow_table.check_consistence_data() is False:
        exit(0)
    rainbow_table.print_data()
    if rainbow_table.get_crack() is not None:
        n = rainbow_table.get_num_process()
        size = rainbow_table.get_table_size()
        started_hash = rainbow_table.get_crack()
        hash = []
        length = []
        for x in range(size):
            hash.append(started_hash)
            length.append(len(rainbow_table.get_plain_text(x)))
        i = 0
        while i < rainbow_table.get_max_chain_length():
            with ProcessPoolExecutor(max_workers=n) as executor:
                results = executor.map(rainbow_table.crack_hash_chain, hash, range(size)) # coś się tu pierdoli
            for result in results:
                if result is not None:
                    rainbow_table.crack_hash(result, started_hash)
                    executor.shutdown()
                    i = size
                    break
            for x in range(size):
                plain = rainbow_table.reduce(hash[x], length[x]) # length na sztywno
                hash[x] = rainbow_table.hash(plain)
            i = i + 1
        if rainbow_table.get_crack() != started_hash:
            print("Tekst jawny do szukanego hasha to: " + str(rainbow_table.get_crack()))
        else:
            print("Nie znaleziono tekstu jawnego dla podanego hasza")
    else:
        size = rainbow_table.get_table_size()
        chains = rainbow_table.get_chains()
        if chains != size:
            rainbow_table.generate_plain_texts()
        else:
            if rainbow_table.is_table_seeded():
                rainbow_table.generate_plain_texts()
        n = rainbow_table.get_num_process()
        seeded = rainbow_table.get_data_seeded()
        rep = rainbow_table.get_table_size() - seeded
        with ProcessPoolExecutor(max_workers=n) as executor:
            results = executor.map(rainbow_table.create_chain, range(seeded, rep + seeded))
        for result in results:
            rainbow_table.modify_table(result)
        rainbow_table.export_rainbow_table()
        print("Tablica zapisana do pliku wynikowego")

