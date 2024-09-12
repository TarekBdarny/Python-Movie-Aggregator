import argparse
import os
parser = argparse.ArgumentParser(
                    prog='decrypt a file',
                    description= 'This tool decrypt a file'
                    )
                    
parser.add_argument('-f' ,
'--filename' ,
help='Enter the file name to decrypt',
required=True
)
parser.add_argument('-t' ,
'--type' ,
help='What you want to decrypt image/file [i= image] [f=file]',
required=True
)

args = parser.parse_args()

if not os.path.exists(args.filename):
    print('File not found!')
    exit()
if args.filename[0:4] != 'enc_':
    print("This file cannot be decrypted")
    print("File must start with 'enc_'")
    exit()

ceasar_dec = lambda chunk ,key=3 : chr(ord(chunk) - key % 26)
ceasar_dec_bytes = lambda chunk ,key=3 : bytes([(ord(chunk) - key)%256])

if args.type in ['f', 'F']:
    f = open(args.filename , 'r+')
    file_data = f.read()
    decrypted_data = ""
    for ch in file_data:
        decrypted_char = ceasar_dec(ch)
        if ch == '\n':
            decrypted_char = '\n'
        elif ch == ' ':
            decrypted_char = ' '
        decrypted_data += decrypted_char
    f = open(args.filename.replace("enc_" , "") , 'w+')
    f.write(decrypted_data)
else:
    f = open(args.filename , 'rb+')
    chunk = f.read(1) 
    file_arr = bytearray()

    while chunk:
        file_arr += bytes([(ord(chunk) -3)%256])
        chunk = f.read(1)

    f = open(args.filename.replace("enc_" , "") , 'wb+')
    f.write(file_arr)

os.remove(args.filename)
print("File successfully decrypted!")