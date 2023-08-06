import random
import time

#string to binary
def strtobin(msg, msg_len, dec_chk = 'e', key_chk = 'n'):
    if dec_chk == 'd' and key_chk == 'n':
        bin_str = '00' + format(int(msg, 16), 'b')
    else:
        bin_str = ''
        for i in range(msg_len):
                dec_val=ord(msg[i])
                y = bin(dec_val).replace('b', '')
                if len(y)<8:
                    while True:
                        dif=8-len(y)
                        y = y[:1] + '0' + y[1:]
                        if(len(y)==8):
                            break
                    bin_str = bin_str + y
                else:
                    bin_str = bin_str + bin(dec_val).replace('b', '')
    return bin_str

#binary to string
def bintostr(bin_msg, msg_len, chk = 'e'):
    run = True
    ctr1 = 0
    enc_msg = ''
    while run:
        if chk == 'e':
            for i in range(msg_len*2):
                enc_hex = f'{int(bin_msg[(i * 4):((i+1) * 4)], 2):X}'
                enc_msg+=enc_hex
                ctr1+=1
            if(ctr1==msg_len*2):
                run = False
        else:
            for i in range(msg_len):
                enc_char=chr(int(bin_msg[(i * 8):(( i+ 1) * 8)], 2))
                enc_msg+=enc_char
                ctr1+=1
            if(ctr1==msg_len):
                break
    return enc_msg

#generating a random number for the seed in genkey function
def seedgen():
    random.seed(256)
    return random.random()

#generating a key
def genkey(msg_len):
    ranstr = 'bvualesgvnrgsunlrgtunlagligovlarnoagegi'
    key = ''
    rseed = seedgen()
    random.seed(rseed)
    for i in range(0, msg_len):
        x = random.randint(0, 20)
        key = key + ranstr[x]
    return key

#performing xor on the message
def xorop(msg, msg_key, dec_chk = 'e'):
    xored_msg = ''
    bin_msg=strtobin(msg, len(msg_key), dec_chk)
    bin_key=strtobin(msg_key, len(msg_key), dec_chk, 'y')
    for i in range(0, (len(msg_key)*8)):
        if bin_msg[i]==bin_key[i]:
            xored_msg+='0'
        else:
            xored_msg+='1'
    enc_msg = bintostr(xored_msg, len(msg_key), dec_chk)
    return enc_msg


def decrypt(enc_msg, msg_key):
    dec_msg = xorop(enc_msg, msg_key, 'd')
    print("\n\t\tDecrypting...\n")
    time.sleep(2)
    return dec_msg, msg_key


def encrypt(msg, msg_key = 'n'):
    if msg_key == 'n':
        msg_key = genkey(len(msg))
    print("\n\t\tEncrypting...\n")
    time.sleep(2)
    enc_msg = xorop(msg, msg_key)
    if msg_key == 'n':
        print("Your key:", msg_key)
    return enc_msg, msg_key