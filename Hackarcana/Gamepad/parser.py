import json

f = json.load(open("./files/input.json"))
packets = []
flag = ""

for i in f:
    '''
    In wireshark we see HID data that corresponds with this key in the json file
    Replace removes the :
    b''.fromhex gives hexadecimal values
    '''
    data = b''.fromhex(i["_source"]["layers"]["usbhid.data"].replace(":", ""))
    data = data[1:]

    packets.append(data)
# We have a lot of repetition, this remembers the last move and ignores the next if it's the same
previous = packets[0][8]
keyboard = ("ABCDEFGHIJ"
            "KLMNOPQRST"
            "UVWXYZabcd"
            "efghijklmn"
            "opqrstuvwx"
            "yz.,-=:;{}")
x, y = 0, 0
for p in packets:

    '''
        Offsets
        /* 7.0*/ Direction DPad : 4;
        /* 7.4*/ uint8_t ButtonSquare : 1;
        /* 7.5*/ uint8_t ButtonCross : 1;
        /* 7.6*/ uint8_t ButtonCircle : 1;
        /* 7.7*/ uint8_t ButtonTriangle : 1;
        '''
    b = p[7]

    if b != previous:
        dpad = b & 0b00001111
        btn_sq = (b >> 4) & 1
        btn_cr = (b >> 5) & 1
        btn_cc = (b >> 6) & 1
        btn_tr = (b >> 7) & 1
        previous = b

        #print(dpad, btn_cr, btn_cc)

        '''
            North = 0,
            East = 2
            South = 4
            West = 6
            None = 8
        '''
        if dpad == 0:
            #print("up")
            y = y - 1
        elif dpad == 2:
            #print("right")
            x = x+ 1
        elif dpad == 4:
            #print("down")
            y = y + 1
        elif dpad == 6:
            #print("left")
            x = x - 1
        elif dpad == 8:
            #print("rest")
            pass

        if btn_cc == 1:
            flag += keyboard[x+y*10]

print(flag)