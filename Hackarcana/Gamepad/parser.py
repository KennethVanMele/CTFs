import json

input_file = json.load(open("./files/input.json"))
packets = []
keyboard = ("ABCDEFGHIJ"
            "KLMNOPQRST"
            "UVWXYZabcd"
            "efghijklmn"
            "opqrstuvwx"
            "yz.,-=:;{}")
x, y = 0, 0
flag = ""

for i in input_file:
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

for packet in packets:

    '''
        Offsets
        /* 7.0*/ Direction DPad : 4;
        /* 7.4*/ uint8_t ButtonSquare : 1;
        /* 7.5*/ uint8_t ButtonCross : 1;
        /* 7.6*/ uint8_t ButtonCircle : 1;
        /* 7.7*/ uint8_t ButtonTriangle : 1;
        '''
    byte = packet[7]

    if byte != previous:
        dpad = byte & 0b00001111
        btn_square = (byte >> 4) & 1
        btn_cross = (byte >> 5) & 1
        btn_circle = (byte >> 6) & 1
        btn_triangle = (byte >> 7) & 1
        previous = byte

        # print(dpad, btn_cr, btn_cc)

        '''
            North = 0,
            East = 2
            South = 4
            West = 6
            None = 8
        '''

        match dpad:
            case 0:
                y = y - 1
            case 2:
                x = x + 1
            case 4:
                y = y + 1
            case 6:
                x = x - 1
            case 8:
                pass

        assert btn_square == 0
        # assert btn_cross == 0
        assert btn_triangle == 0
        # assert btn_circle == 0

        if btn_circle == 1:
            flag += keyboard[x+y*10]

print(flag)
