#Remigiusz KAmiński
def hash_to_binary_and_count_diff(hash1, hash2):
    binary1 = bin(int(hash1, 16))[2:].zfill(len(hash1)*4)
    binary2 = bin(int(hash2, 16))[2:].zfill(len(hash2)*4)
    diff_bits = sum(bit1 != bit2 for bit1, bit2 in zip(binary1, binary2))
    percent_diff = (diff_bits / (len(binary1) * 1.0)) * 100
    return diff_bits, percent_diff

def main():
    hashArr = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'b2']
    file = open("hash.txt", "r")
    writer = open("diff.txt", "w")
    file = file.read().splitlines()
    for i in range(0, len(file), 2):
        hash1 = file[i].strip().replace(" ", "").rstrip("-")
        hash2 = file[i+1].strip().replace(" ", "").rstrip("-")
        diff_bits, percent_diff = hash_to_binary_and_count_diff(hash1, hash2)
        writer.write("Typ hasha: " + hashArr[i//2] + "\n")
        writer.write("Hash 1: " + hash1 + "\n")
        writer.write("Hash 2: " + hash2 + "\n")
        writer.write("Liczba różnych bitów: " + str(diff_bits) + " z " + str(len(hash1)*4) + "\n")
        writer.write("Różnica procentowa: " + str(percent_diff) + "%\n")
        writer.write("\n")



if __name__ == '__main__':
    main()