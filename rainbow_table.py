import string
import random
from passlib.hash import des_crypt


class RainbowTable:
    def __init__(self):
        self.n = 2
        self.chains = 200
        self.chain_length = 200
        self.password_length = 8
        self.table = {}
        self.alphabet = string.ascii_letters + string.digits
        self.crack = None
        self.table_file = None
        self.plaintext_file = None

    def set_num_process(self, n):
        self.n = n

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
        self.table_file = filename
        return 0

    def load_plaintexts(self, filename):
        self.plaintext_file = filename
        with open(filename) as f:
            data = f.read()
            data_splitted = data.split(";")
            for plaintext in data_splitted:
                self.table[plaintext] = 0
        self.chains = len(self.table)

    def load_alphabet(self, filename):
        with open(filename) as f:
            self.alphabet = f.read()

    def set_crack(self, crack):
        self.crack = crack

    def check_consistence_data(self):
        if self.crack is not None:
            if not self.table:
                print("Niepodano tablicy do poszukiwania hasza")
                return False

    def print_data(self):
        if self.crack is not None:
            print("Tablica tęczowa załadowana")
            print("Poszukiwania cracka dla hasha: " + self.crack)
        else:
            if self.table_file is not None:
                print("Tablica tęczowa załadowana")
            print("Teksty jawne utworzone/zapisane")
            print("Ilość łańcuchów: " + str(self.chains))
            print("Długość łańcucha: " + str(self.chain_length))
            print("Długość poszukiwanych haseł: " + str(self.password_length))
            print("Tworzenie tablicy tęczowej na zbiorze znaków: " + self.alphabet)
        print("Liczba pracujących procesów: " + str(self.n))

    def generate_plaintexts(self):
        for x in range(self.chains):
            plaintext = ''.join(random.choice(self.alphabet) for _ in range(self.password_length))
            while plaintext in self.table:
                plaintext = ''.join(random.choice(self.alphabet) for _ in range(self.password_length))
            self.table[plaintext] = 0

    def print_table(self):
        for key, value in self.table.items():
            print(key + ": " + str(value))

    def crack_hash(self, hash):
        return 0

    @staticmethod
    def hash(plaintext):
        return des_crypt.hash(plaintext)

