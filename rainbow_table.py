import string
import random
from passlib.hash import des_crypt


class RainbowTable:
    def __init__(self):
        self.n = 1
        self.chains = 0
        self.chain_length = 200
        self.password_length = 8
        self.table = {}
        self.alphabet = string.ascii_letters + string.digits
        self.crack = None
        self.table_seeded = False
        self.data_seeded = 0

    def set_num_process(self, n):
        self.n = n

    def get_num_process(self):
        return self.n

    def set_chains(self, chains):
        self.chains = chains

    def get_chains(self):
        return self.chains

    def set_chain_length(self, chain_length):
        self.chain_length = chain_length

    def set_password_length(self, password_length):
        self.password_length = password_length

    def get_table_size(self):
        return len(self.table)

    def load_table(self, filename):
        self.table_seeded = True
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            i = 0
            for line in lines:
                data = line.split(":")
                self.table[i] = {
                    data[0]: data[1]
                }
                i = i + 1
        self.data_seeded = i

    def load_plain_texts(self, filename):
        with open(filename, "r") as f:
            data = f.read()
            data_splitted = data.split(";")
            for plaintext in data_splitted:
                size = len(self.table)
                self.table[size] = {
                    plaintext: str(0)
                }

    def load_alphabet(self, filename):
        with open(filename, "r") as f:
            self.alphabet = f.read()

    def set_crack(self, crack):
        self.crack = crack

    def get_crack(self):
        return self.crack

    def is_table_seeded(self):
        return self.table_seeded

    def get_data_seeded(self):
        return self.data_seeded

    def check_consistence_data(self):
        if self.crack is not None:
            if not self.table:
                print("Niepodano tablicy do poszukiwania hasza")
                return False
        else:
            if len(self.table) == 0 and self.chains == 0:
                print("Niepodano liczby łańcuchów ani pliku z tekstami jawnymi")
                return False
            if self.chains == 0 and self.is_table_seeded() and len(self.table) == self.data_seeded:
                print("Niepodano liczby łańcuchów ani pliku z tekstami jawnymi")
                return False

    def print_data(self):
        if self.crack is not None:
            print("Tablica tęczowa załadowana z pliku")
            print("Poszukiwania cracka dla hasha: " + self.crack)
        else:
            if self.table_seeded is True:
                print("Tablica tęczowa załadowana z pliku")
            print("Ilość łańcuchów do wygenerowania: " + str(self.chains))
            print("Teksty jawne utworzone/zapisane")
            print("Długość łańcucha: " + str(self.chain_length))
            print("Długość poszukiwanych haseł: " + str(self.password_length))
            print("Tworzenie tablicy tęczowej na zbiorze znaków: " + self.alphabet)
        print("Liczba pracujących procesów: " + str(self.n))

    def generate_plain_texts(self):
        for x in range(self.chains):
            plaintext = ''.join(random.choice(self.alphabet) for _ in range(self.password_length))
            while plaintext in self.table:
                plaintext = ''.join(random.choice(self.alphabet) for _ in range(self.password_length))
            size = len(self.table)
            self.table[size] = {
                plaintext: str(0)
            }

    def print_table(self):
        for key, value in self.table.items():
            for plaintext, hash in value.items():
                print(str(key) + ":" + str(plaintext) + ":" + str(hash))

    @staticmethod
    def reduce(hash, length):
        return hash[0:length]

    @staticmethod
    def hash(plaintext):
        return des_crypt.hash(plaintext)

    def modify_table(self, value):
        self.table[list(value.keys())[0]] = list(value.values())[0]

    def create_chain(self, table_id):
        rainbow_chain = self.table[table_id]
        rainbow_plaintext = list(rainbow_chain.keys())[0]
        plaintext = rainbow_plaintext
        for chain_element in range(self.chain_length):
            hash = self.hash(plaintext)
            plaintext = self.reduce(hash, len(plaintext))
        result = {
            table_id: {
                rainbow_plaintext: hash
            }
        }
        return result

    def crack_hash(self, hash, table_id):
        i = 0

    def export_rainbow_table(self):
        with open("rainbow_result.txt", "w") as f:
            for key, value in self.table.items():
                for plaintext, hash in value.items():
                    f.write(str(plaintext) + ":" + str(hash) + "\n")
