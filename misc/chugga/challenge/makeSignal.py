import wave, struct

MORSE_CODE_CHARS= {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
}

# https://dccwiki.com/Digital_Packet
class Packet():
    # I know, bits shouldn't be lists of ints
    # it doesn't really matter and I don't want to use a library to work with individual bits
    _preamble = [1] * 14
    _address = [0] * 8
    _data = [0] * 8
    _error = [0] * 8
    time = 0
    
    def __init__(self):
        pass

    def __init__(self, address: list[int]):
        self.setAddress(address)

    def __init__(self, address: list[int], data: list[int]):
        self.setAddress(address)
        self.setData(data)
    
    def __init__(self, address: list[int], data: list[int], time):
        self.setAddress(address)
        self.setData(data)
        self.setTime(time)

    # doesn't support extended addresses
    def setAddress(self, address: list[int]):
        assert(len(address) == 8)
        # avoid extended addresses
        assert(address[0] != 1 and address[1] != 1 or address[2:] == [1,1,1,1,1,1])

        self._address = address
    
    def setData(self, data: list[int]):
        assert(len(data) == 8)
        self._data = data

    def setTime(self, time: int):
        assert(time >= 0)
        self.time = time

    def _generateError(self):
        self._error = [b ^ self._data[i] for i, b in enumerate(self._address)]

    def getPacket(self):
        self._generateError()
        return self._preamble + [0] + self._address + [0] + self._data + [0] + self._error + [1]

    def __repr__(self):
        return f"{self.getPacket()}, T: {self.time}"

# 116 usec
def write1(file):
    file.write("1,0\n" * 1)
    file.write("0,1\n" * 1)
    return 2

# 234 usec
def write0(file):
    file.write("1,0\n" * 2)
    file.write("0,1\n" * 2)
    return 4

# each increment is 58 usec
def writeStretched0(file, tIncrement: int):
    assert(tIncrement <= 206 and tIncrement >= 4)
    file.write("1,0\n" * 2)
    file.write("0,1\n" * (tIncrement - 2))
    return tIncrement

# csv built with time resolution of 1 data point / 58 usec
def buildCSV(packets: list[Packet]):
    packetTime = int(500000 / 58)
    time = 0
    with open("output.csv", "w") as file:
        file.write("A,B\n")
        for i, packet in enumerate(packets):
            print(f"Building packet {i}")
            while time < packet.time * packetTime - 4:
                # print(packet.time * packetTime - time)
                if packet.time * packetTime - time >= 206:
                    time += writeStretched0(file, 206)
                else:
                    time += writeStretched0(file, (packet.time * packetTime - time) % 206)
            for char in packet.getPacket():
                if char == 1:
                    time += write1(file)
                elif char == 0:
                    time += write0(file)
                else:
                    raise ValueError(f"Something other than binary in a packet detected: {char}")
            
def main():
    message = "W0H00TRA1NSAR3AWE5SOME6531209867"
    morseCode = ""
    for char in message:
        morseCode += "".join([c + ' ' for c in MORSE_CODE_CHARS[char]]) + '     '
    print(morseCode)
    
    transmission = ''
    for signal in morseCode:
        match signal:
            case '.':
                transmission += '1'
            case '-':
                transmission += '11'
            case ' ':
                transmission += '0'

    print(transmission)
    lightAddress = [0,0,0,1,0,0,1,0]
    packets: list[Packet] = []
    
    packets.append(Packet(lightAddress, [0,0,0,0,0,0,0,int(transmission[0])], 0))
    for i in range(1, len(transmission)):
        if transmission[i] == transmission[i-1]: continue
        packets.append(Packet(lightAddress, [0,0,0,0,0,0,0,int(transmission[i])], i))

    for packet in packets:
        print(packet)

    buildCSV(packets)
    
if __name__ == '__main__':
    main()
