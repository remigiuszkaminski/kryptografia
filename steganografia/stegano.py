#Autor: Remigiusz Kamiński
import sys

def hide_message_1(cover_text, message):

    lines = cover_text.splitlines()
    msg = message.strip()

    helper = ''
    for num in msg:
        binary = bin(int(num, 16))[2:].zfill(4)
        helper += binary

    if len(helper) > len(lines):
        sys.exit("Nośnik za krótki")

    if len(helper) != 64:
        sys.exit("Wiadomość nie ma 64 bitów")

    new_cover_lines = []
    for i, bit in enumerate(helper):
        stripped_line = lines[i].rstrip('\n')
        if bit == '1':
            stripped_line += ' \n'
        else:
            stripped_line += '\n'
        new_cover_lines.append(stripped_line)

    new_cover_lines.extend(lines[len(helper):])

    watermark_text = '\n'.join(new_cover_lines)

    with open('watermark.html', 'w') as watermark_file:
        watermark_file.write(watermark_text)
    

def hide_message_2(cover_text, message):
    lines = cover_text.splitlines()
    msg = message.strip()

    helper = ''
    for num in msg:
        binary = bin(int(num, 16))[2:].zfill(4)
        helper += binary

    przerabiarka = "".join(lines).replace("  ", "")
    spc_counter = przerabiarka.count(" ")
    if len(helper) > spc_counter:
        sys.exit("Nośnik za krótki")
    if len(helper) != 64:
        sys.exit("Wiadomość nie ma 64 bitów")
    
    new_cover_lines = ""
    lines = przerabiarka.split(" ")
    for i in range(len(helper)):
        bit = helper[i]
        if bit == "1":
            lines[i] += " "
        new_cover_lines += lines[i] + " "
    new_cover_lines += " ".join(lines[len(helper):])

    with open('watermark.html', 'w') as watermark_file:
        watermark_file.write(new_cover_lines)

def hide_message_3(cover_text, message):
    msg = message.strip()

    lines = cover_text

    helper = ''
    for num in msg:
        binary = bin(int(num, 16))[2:].zfill(4)
        helper += binary
    
    if len(helper) > len(lines):
        sys.exit("Nośnik za krótki")
    if len(helper) != 64:
        sys.exit("Wiadomość nie ma 64 bitów")
    
    replacements = 0
    new_cover_lines = ""
    for i in lines:
        kod = i
        if 'style' in i:
            if replacements < 64 and helper[replacements] == '1':
                kod = i.replace('style', 'styl')
            new_cover_lines += kod
            replacements += 1
        else:
            new_cover_lines += kod

    with open('watermark.html', 'w') as watermark_file:
        watermark_file.write(new_cover_lines)

def hide_message_4(cover_text, message):
    lines = cover_text
    msg = message.strip()

    helper = ''
    for num in msg:
        binary = bin(int(num, 16))[2:].zfill(4)
        helper += binary
    
    przerabiarka = [i.replace("<font></font>", "") for i in lines]
    spc_counter = "".join(przerabiarka).count("<font>")
    if len(helper) > spc_counter:
        sys.exit("Nośnik za krótki")
    if len(helper) != 64:
        sys.exit("Wiadomość nie ma 64 bitów")
    
    new_cover_lines = ""
    replacements = 0
    for i in przerabiarka:
        kod = i
        if '<font>' in i:
            if replacements < 64 and helper[replacements] == '1':
                kod = i.replace('<font>', '<font></font><font>')
            else:
                kod = i.replace('<font>', '</font><font></font>')
            new_cover_lines += kod
            replacements += 1
        else:
            new_cover_lines += kod

    with open('watermark.html', 'w') as watermark_file:
        watermark_file.write(new_cover_lines)


def extract_message_1(watermark_text):
    watermark = watermark_text.splitlines()

    
    helper = ''
    for line in watermark:
        if len(line) > 0:
            if line[-1] == ' ':
                helper += '1'
            else:
                helper += '0'
        if len(helper) == 64:
            break
        
    odszyfrowana = ''
    for i in range(0, len(helper), 4):
        odszyfrowana += hex(int(helper[i:i+4], 2))[2:]

    with open('detect.txt', 'w+') as f:
        f.write(odszyfrowana)
        


def extract_message_2(watermark_text):
    lines = "".join(watermark_text).split(" ")

    helper = ''
    for i in range(len(lines)):
        if lines[i] == '':
            helper += '1'
        else:
            helper += '0'
    helper = helper.replace('01', '1')[:64]
    odszyfrowana = ''
    for i in range(0, len(helper), 4):
        odszyfrowana += hex(int(helper[i:i+4], 2))[2:]

    with open('detect.txt', 'w') as extracted_file:
        extracted_file.write(odszyfrowana)

def extract_message_3(watermark_text):
    watermark = watermark_text.splitlines()

    helper = ''
    for line in watermark:
        if 'style' in line:
            helper += '0'
        elif 'styl' in line:
            helper += '1'
        if len(helper) == 64:
            break

    kodowana = ''
    for i in range(0, len(helper), 4):
        kodowana += hex(int(helper[i:i+4], 2))[2:]
    
    with open('detect.txt', 'w') as extracted_file:
        extracted_file.write(kodowana)

def extract_message_4(watermark_text):
    watermark = watermark_text.splitlines()

    helper = ''
    for line in watermark:
        if '<font></font><font>' in line:
            helper += '1'
        elif '</font><font></font>' in line:
            helper += '0'
        if len(helper) == 64:
            break

    kodowana = ''
    for i in range(0, len(helper), 4):
        kodowana += hex(int(helper[i:i+4], 2))[2:]
    
    with open('detect.txt', 'w') as extracted_file:
        extracted_file.write(kodowana)

def main():
    if len(sys.argv) != 3:
        print("Użycie: program.py [-e | -d]")
        return

    option = sys.argv[1]
    nextoption = sys.argv[2]

    if option == '-e' and nextoption == '-1':
        with open('mess.txt', 'r') as file:
            message = file.read()
        with open('cover.html', 'r') as file:
            cover_text = file.read()

        watermark_text = hide_message_1(cover_text, message)

    elif option == '-e' and nextoption == '-2':
        with open('mess.txt', 'r') as file:
            message = file.read()
        with open('cover.html', 'r') as file:
            cover_text = file.read()

        watermark_text = hide_message_2(cover_text, message)
    
    elif option == '-e' and nextoption == '-4':
        with open('mess.txt', 'r') as file:
            message = file.read()
        with open('cover.html', 'r') as file:
            cover_text = file.readlines()

        watermark_text = hide_message_4(cover_text, message)

    elif option == '-e' and nextoption == '-3':
        with open('mess.txt', 'r') as file:
            message = file.read()
        with open('cover.html', 'r') as file:
            cover_text = file.readlines()

        watermark_text = hide_message_3(cover_text, message)

    elif option == '-d' and nextoption == '-1':
        with open('watermark.html', 'r') as file:
            watermark_text = file.read()

        extract_message_1(watermark_text)

    elif option == '-d' and nextoption == '-2':
        with open('watermark.html', 'r') as file:
            watermark_text = file.read()

        extract_message_2(watermark_text)

    elif option == '-d' and nextoption == '-3':
        with open('watermark.html', 'r') as file:
            watermark_text = file.read()
        
        extract_message_3(watermark_text)

    elif option == '-d' and nextoption == '-4':
        with open('watermark.html', 'r') as file:
            watermark_text = file.read()
        
        extract_message_4(watermark_text)

    else:
        print("Nieprawidłowa opcja.")
if __name__ == "__main__":
    main()