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

    def get_max_chain_length(self):
        max_length = 0
        for key, value in self.table.items():
            length = int(list(value.values())[1])
            if length > max_length:
                max_length = length
        return max_length

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
                length = data[1].split("-")
                print(data[1])
                print(length)
                self.table[i] = {
                    data[0]: length[0].strip(),
                    "length": length[1].strip()
                }
                i = i + 1
        self.data_seeded = i

    def load_plain_texts(self, filename):
        with open(filename, "r") as f:
            data = f.read()
            data = data.replace("\n", "")
            data_splitted = data.split(";")
            for plaintext in data_splitted:
                if len(plaintext) == 0:
                    continue
                size = len(self.table)
                self.table[size] = {
                    plaintext: str(0),
                    "length": str(0)
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
                print("Nie podano liczby łańcuchów ani pliku z tekstami jawnymi")
                return False
            if self.chains == 0 and self.is_table_seeded() and len(self.table) == self.data_seeded:
                print("Nie podano liczby łańcuchów ani pliku z tekstami jawnymi")
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
            while self.check_plaintext_exist(plaintext) is False:
                plaintext = ''.join(random.choice(self.alphabet) for _ in range(self.password_length))
            size = len(self.table)
            self.table[size] = {
                plaintext: str(0),
                "chain-length": str(0)
            }

    @staticmethod
    def reduce(hash, length):
        return hash[2:2 + length]

    @staticmethod
    def hash(plaintext):
        return des_crypt.hash(plaintext, salt="AB")

    def check_plaintext_exist(self, plaintext):
        for x in range(len(self.table)):
            chain = self.table[x]
            plain = list(chain.keys())[0]
            if chain == plain:
                return False
        return True

    def modify_table(self, value):
        self.table[list(value.keys())[0]] = list(value.values())[0]

    def get_plaintext(self, table_id):
        return list(self.table[table_id].keys())[0]

    def create_chain(self, table_id):
        rainbow_chain = self.table[table_id]
        rainbow_plaintext = list(rainbow_chain.keys())[0]
        plaintext = rainbow_plaintext
        for chain_element in range(self.chain_length):
            hash = self.hash(plaintext)
            plaintext = self.reduce(hash, len(plaintext))
        result = {
            table_id: {
                rainbow_plaintext: hash,
                "length": self.chain_length
            }
        }
        return result

    def crack_hash_chain(self, hash, table_id):
        rainbow_chain = self.table[table_id]
        rainbow_hash = list(rainbow_chain.values())[0]
        if hash == rainbow_hash:
            return table_id
        return None

    def crack_hash(self, table_id, hash):
        chain = self.table[table_id]
        plain = list(chain.keys())[0]
        temp_hash = self.hash(plain)
        while True:
            if temp_hash == hash:
                self.set_crack(plain)
                break
            plain = self.reduce(temp_hash, len(plain))
            temp_hash = self.hash(plain)

    def export_rainbow_table(self):
        with open("rainbow_result.txt", "w") as f:
            for key, value in self.table.items():
                plaintext = list(value.keys())[0]
                hash = list(value.values())[0]
                length = list(value.values())[1]
                f.write(str(plaintext) + ":" + str(hash) + " - " + str(length) + "\n")
