import sys


def cezar():
    with open('plain.txt', 'r') as file:
        jawny = file.read()
    with open('key.txt', 'r') as file:
        klucz = int(file.read().split(" ")[0])
        print(klucz)
        if klucz < 0 and klucz > 25:
            print('Wrong key')
            return
    with open('crypto.txt', 'w') as file:
        for i in jawny:
            if i.isalpha():
                if i.isupper():
                    file.write(chr((ord(i) + klucz - 65) % 26 + 65))
                else:
                    file.write(chr((ord(i) + klucz - 97) % 26 + 97))
            else:
                file.write(i)
        
def odszyfrujcezar():
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('key.txt', 'r') as file:
        klucz = int(file.read().split(" ")[0])
        if klucz < 0 and klucz > 25:
            print('Wrong key')
            return
    with open('decrypt.txt', 'w') as file:
        for i in krypto:
            if i.isalpha():
                if i.isupper():
                    file.write(chr((ord(i) - klucz - 65) % 26 + 65))
                else:
                    file.write(chr((ord(i) - klucz - 97) % 26 + 97))
            else:
                file.write(i)

def znajdzkluczcezar():
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('plain.txt', 'r') as file:
        jawny = file.read()
    with open('key-found.txt', 'w') as file:
        for klucz in range(26):
            with open('decrypt.txt', 'w') as file2:
                for i in krypto:
                    if i.isalpha():
                        if i.isupper():
                            file2.write(chr((ord(i) - klucz - 65) % 26 + 65))
                        else:
                            file2.write(chr((ord(i) - klucz - 97) % 26 + 97))
                    else:
                        file2.write(i)
            with open('decrypt.txt', 'r') as file3:
                odszyfrowany = file3.read()
                if odszyfrowany == jawny:
                    file.write(str(klucz))
                    print("klucz to: ", klucz)
                    return
    print("Nie znaleziono klucza")


def kryptogramcezar():
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('decrypt.txt', 'w') as file:
        for i in range(26):
            for j in krypto:
                if j.isalpha():
                    if j.isupper():
                        file.write(chr((ord(j) - i - 65) % 26 + 65))
                    else:
                        file.write(chr((ord(j) - i - 97) % 26 + 97))
                else:
                    file.write(j)
            file.write('\n')


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def afiniczny():
    with open('plain.txt', 'r') as file:
        jawny = file.read()
    with open('key.txt', 'r') as file:
        klucz = file.read().split(" ")
        klucz1 = int(klucz[0])
        klucz2 = int(klucz[1])
        print(klucz1, klucz2)
        if klucz1 < 0 and klucz1 > 25 or klucz2 < 0 or gcd(klucz1, 26) != 1:
            print('Wrong key')
            return
    with open('crypto.txt', 'w') as file:
        for i in jawny:
            if i.isalpha():
                if i.isupper():
                    file.write(chr(((ord(i) - 65) * klucz1 + klucz2) % 26 + 65))
                else:
                    file.write(chr(((ord(i) - 97) * klucz1 + klucz2) % 26 + 97))
            else:
                file.write(i)

def odwrotnosc_modulo(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def odszyfrujafiniczny():
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('key.txt', 'r') as file:
        klucz = file.read().split(" ")
        klucz1 = int(klucz[0])
        klucz2 = int(klucz[1])
        if klucz1 < 0 and klucz1 > 25 or klucz2 < 0 or gcd(klucz1, 26) != 1:
            print('Wrong key')
            return
        klucz1_odwrocony = odwrotnosc_modulo(klucz1, 26)
        if klucz1_odwrocony is None:
            print('Wrong key')
            return
    with open('decrypt.txt', 'w') as file:
        for i in krypto:
            if i.isalpha():
                if i.isupper():
                    file.write(chr(((ord(i) - 65 - klucz2) * klucz1_odwrocony) % 26 + 65))
                else:
                    file.write(chr(((ord(i) - 97 - klucz2) * klucz1_odwrocony) % 26 + 97))
            else:
                file.write(i)

def znajdzkluczafiniczny():
    with open('plain.txt', 'r') as file:
        jawny = file.read()
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('decrypt.txt', 'r') as file:
        odszyfrowany = file.read()
    with open('key-found.txt', 'w') as file:
        for i in range(26):
            for j in range(26):
                if gcd(i, 26) == 1:
                    with open('decrypt.txt', 'w') as file2:
                        for k in krypto:
                            if k.isalpha():
                                if k.isupper():
                                    file2.write(chr(((ord(k) - 65 - j) * odwrotnosc_modulo(i, 26)) % 26 + 65))
                                else:
                                    file2.write(chr(((ord(k) - 97 - j) * odwrotnosc_modulo(i, 26)) % 26 + 97))
                            else:
                                file2.write(k)
                    with open('decrypt.txt', 'r') as file3:
                        odszyfrowany = file3.read()
                        if odszyfrowany == jawny:
                            file.write(str(i) + " " + str(j))
                            print("klucz to: ", i, j)
                            return
    print("Nie znaleziono klucza")
                    
def kryptogramafiniczny():
    with open('crypto.txt', 'r') as file:
        krypto = file.read()
    with open('decrypt.txt', 'w') as file:
        for i in range(26):
            for j in range(26):
                if gcd(i, 26) == 1:
                    klucz1_odwrocony = odwrotnosc_modulo(i, 26)
                    for k in krypto:
                        if k.isalpha():
                            if k.isupper():
                                file.write(chr(((ord(k) - 65 - j) * klucz1_odwrocony) % 26 + 65))
                            else:
                                file.write(chr(((ord(k) - 97 - j) * klucz1_odwrocony) % 26 + 97))
                        else:
                            file.write(k)
                    file.write("\n")

                
                    

def main():
    if sys.argv[1] == '-c' and sys.argv[2] == '-e':
        cezar()
    elif sys.argv[1] == '-c' and sys.argv[2] == '-d':
        odszyfrujcezar()
    elif sys.argv[1] == '-c' and sys.argv[2] =='-j':
        znajdzkluczcezar()
    elif sys.argv[1] == '-c' and sys.argv[2] == '-k':
        kryptogramcezar()
    elif sys.argv[1] == '-a' and sys.argv[2] == '-e':
        afiniczny()
    elif sys.argv[1] == '-a' and sys.argv[2] == '-d':
        odszyfrujafiniczny()
    elif sys.argv[1] == '-a' and sys.argv[2] == '-j':
        znajdzkluczafiniczny()
    elif sys.argv[1] == '-a' and sys.argv[2] == '-k':
        kryptogramafiniczny()
    else:
        print("Wrong option")
        return

main()
