#Autor: Remigiusz Kamiński
import sys
import random
from sympy import isprime
def generate():
    with open('elgamal.txt', 'r') as file:
        p = int(file.readline())
        g = int(file.readline())

    priv = generate_private_key(p)

    with open('private.txt', 'w') as file:
        file.write(str(p) + '\n')
        file.write(str(g) + '\n')
        file.write(str(priv))

    public_key = pow(g, priv, p)

    with open('public.txt', 'w') as file:
        file.write(str(p) + '\n')
        file.write(str(g) + '\n')
        file.write(str(public_key))

def encrypt():
    with open('public.txt', 'r') as file:
        p = int(file.readline())
        g = int(file.readline())
        potega = int(file.readline())

    with open('plain.txt', 'r') as file:
        tekst = file.read()
    
    check(tekst, p)
    
    nowy = generate_private_key(p)

    nowyG = pow(g, nowy, p)

    nowaPot = pow(potega, nowy, p)
    multi = check(tekst, p) * nowaPot
    encryptedMsg = multi % p

    with open('crypto.txt', 'w') as file:
        file.write(str(nowyG) + '\n')
        file.write(str(encryptedMsg))

def decrypt():
    with open('crypto.txt', 'r') as file:
        nowyG = int(file.readline())
        encryptedMsg = int(file.readline())

    with open('private.txt', 'r') as file:
        p = int(file.readline())
        g = int(file.readline())
        priv = int(file.readline())

    czynnik = pow(nowyG, priv, p)
    czynnik_odwrotny = pow(czynnik, -1, p)
    decrypted_msg = (encryptedMsg * czynnik_odwrotny) % p

    decrypted_text = decrypted_msg.to_bytes((decrypted_msg.bit_length() + 7) // 8, 'big').decode()

    with open('decrypted.txt', 'w') as file:
        file.write(str(decrypted_text))

def signature():
    with open('private.txt', 'r') as file:
        p = int(file.readline())
        g = int(file.readline())
        priv = int(file.readline())

    with open('message.txt', 'r') as file:
        tekst = file.read()
    
    check(tekst, p)

    k = generate_private_key(p)

    r = pow(g, k, p)

    modinv = pow(k, -1, p-1)
    x = (check(tekst, p) - priv * r) * modinv % (p-1)

    with open('signature.txt', 'w') as file:
        file.write(str(r) + '\n')
        file.write(str(x))

def verify():
    with open('public.txt', 'r') as file:
        p = int(file.readline())
        g = int(file.readline())
        potega = int(file.readline())

    with open('message.txt', 'r') as file:
        tekst = file.read()

    with open('signature.txt', 'r') as file:
        r = int(file.readline())
        x = int(file.readline())

    gm = pow(g, check(tekst, p), p)
    betar = pow(potega, r, p)
    rx = pow(r, x, p)
    betarx = (betar * rx) % p

    if gm == betarx:
        with open('verified.txt', 'w') as file:
            file.write('Wynik weryfikacji: true')
            print('Wynik weryfikacji: true')
    else:
        with open('verified.txt', 'w') as file:
            file.write('Wynik werfyikacji: false')
            print('Wynik weryfikacji: false')
    

def convert(b):
    return int.from_bytes(b.encode(), 'big')
    

def check(a, p):
    tekst = a
    tekstliczba = convert(tekst)
    m = int(tekstliczba)
    if m > p:
        print("Wiadomość m nie spełnia założenia m<p")
        exit(1)
    return m
   
        

def generate_private_key(p):
    priv = random.randint(1, p-1)
    while not isprime(priv) or not is_coprime(priv, p-1):
        priv = random.randint(1, p-1)
    return priv

def is_coprime(a, b):
    while b != 0:
        a, b = b, a % b
    return a == 1

def main():
    if sys.argv[1] == '-k':
        generate()
    elif sys.argv[1] == '-e':
        encrypt()
    elif sys.argv[1] == '-d':
        decrypt()
    elif sys.argv[1] == '-s':
        signature()
    elif sys.argv[1] == '-v':
        verify()
    else:
        print('Wrong option')
        exit(1)

if __name__ == '__main__':
    main()
