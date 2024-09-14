import os
import morse_talk as mtalk  # pip install morse-talk

# https://dccwiki.com/Digital_Packet
class Packet():
    # I know, bits shouldn't be lists of ints but at this scale it doesn't matter
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
    
    def getAddress(self):
        return self._address
    
    def getData(self):
        return self._data
    
    def _generateError(self):
        self._error = [b ^ self._data[i] for i, b in enumerate(self._address)]

    def getPacket(self):
        self._generateError()
        return self._preamble + [0] + self._address + [0] + self._data + [0] + self._error + [1]

    def __repr__(self):
        return f"{self.getPacket()}, T: {self.time}"

def createCSV(inputFile: str, outputFile: str):
    os.system(f"sigrok-cli -i {inputFile} -o {outputFile} -O csv") # sudo apt install sigrok-cli

def parseCSV(csvFile: str) -> list[int]:
    out = []
    with open(csvFile, 'r') as file:
        for line in file.readlines():
            if line[0] == '1':
                out.append(1)
            elif line[0] == '0':
                out.append(0)
    
    return out

def convertToBits(dccState: list[int]):
    time = len(dccState)
    out = []
    times = []
    while len(dccState) > 0:
        if dccState[-2:] == [1,0] or dccState[-2:] == [0,1]:
            del dccState[-2:]
            time -= 2
            times.append(time)
            out.append(1)

        elif dccState[-2:] == [1,1] or dccState[-2:] == [0,0]:
            
            # delete until there are no more duplicates (handles for long 0s)
            lastVal = dccState[-1]
            while len(dccState) > 0 and dccState[-1] == lastVal:
                dccState.pop()
                time -= 1
            del dccState[-2:]
            time -= 2
            times.append(time)
            out.append(0)
    assert(len(out) == len(times))
    # reverse to put back in the correct order
    return out[::-1], times[::-1]

def buildPackets(bits: list[int], times: list[int]) -> list[Packet]:
    packets = []
    # doesn't support extended addresses as these don't exist in this challenge
    for i, bit in enumerate(bits):
        if bits[i:i+11] == [1] * 10 + [0]:
            # sep1 = bits[i+10]
            address = bits[i+11:i+19]
            # sep2 = bits[i+19]
            data = bits[i+20:i+28]
            # sep3 = bits[i+28]
            # error = bits[i+29:i+37]
            end = bits[i+37]
            assert(end == 1)
            packet = Packet(address, data, times[i])
            # make sure the data in the packets is correct
            assert(packet.getPacket()[-38:] == bits[i:i+38])
            print(packet)
            packets.append(packet)
    return packets

def parseMorseCode(packets: list[Packet]) -> str:
    morseOut = ''
    lastPacket = packets[0]
    # all packets feature a change in state from 1 or 0
    for packet in packets[1:]:
        if packet.getData()[-1] == 0 and lastPacket.getData()[-1] == 1:
            if (packet.time - lastPacket.time < 10000):
                morseOut += '.'
            else:
                morseOut += '-'
        elif packet.getData()[-1] == 1 and lastPacket.getData()[-1] == 0:
            if (packet.time - lastPacket.time > 10000):
                morseOut += ' '
        lastPacket = packet

    return morseOut

def main():
    createCSV('chall.sr', 'out.csv')
    dccState = parseCSV('out.csv')
    bits, times = convertToBits(dccState)
    packets = buildPackets(bits, times)
    
    # all packets are to the same device
    for packet in packets:
        assert(packet.getAddress() == [0,0,0,1,0,0,1,0])
    
    parsedPackets = parseMorseCode(packets)
    print(parsedPackets)
    print(f"CSCTF{{{mtalk.decode(parsedPackets)}}}")

if __name__ == '__main__':
    main()
