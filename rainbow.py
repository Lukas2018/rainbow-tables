import sys

from rainbow_table import RainbowTable

rainbow_table = RainbowTable()
if __name__ == "__main__":
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
        if argument.startswith("-plaintexts_file="):
            plaintexts_file = argument[17:]
            rainbow_table.load_plaintexts(plaintexts_file)
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
    if rainbow_table.check_consistence_data() is False:
        exit(0)
    rainbow_table.print_data()

