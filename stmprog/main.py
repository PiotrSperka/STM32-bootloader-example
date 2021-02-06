import getopt
import sys
import serial

inputfile = ''
outputfile = ''
serialport = ''
baudrate = 115200


def read(serialport, baudrate, outputfile):
    with serial.Serial(serialport, baudrate) as ser:
        ser.timeout = 10
        ser.write("read\n")
        ser.read(5)  # read echo
        data = ser.read(192 * 1024)  # read firmware backup
        with open(outputfile, "wb") as file:
            file.write(data)


def write(serialport, baudrate, inputfile):
    with open(inputfile, "rb") as file:
        data = file.read()
        with serial.Serial(serialport, baudrate) as ser:
            ser.write("erase\n")
            ser.read(6)
            result = ser.readline()
            if result != "OK":
                print("Erase failed")
                sys.exit(2)

            ser.write("write\n")
            ser.read(6)
            result = ser.readline()
            if result != "OK":
                print("Write init failed")
                sys.exit(2)

            toWrite = len(data)
            written = 0

            while toWrite > 0:
                length = 1024
                if length > toWrite:
                    length = toWrite

                ser.write(str(length) + "\n")
                ser.readline()
                result = ser.readline()
                if result != "OK":
                    print("Write size failed")
                    sys.exit(2)

                ser.write(data[written:(written + length)])
                result = ser.readline()
                if result != "OK":
                    print("Write failed")
                    sys.exit(2)

                written = written + length
                toWrite = toWrite - length
                print("Written:", written, "bytes")

            ser.write("reset\n")
            ser.read(6)
            result = ser.readline()
            if result != "OK":
                print("Reset failed")
                sys.exit(2)


def main(argv):
    global inputfile, outputfile, serialport, baudrate

    try:
        opts, args = getopt.getopt(argv, "hpb:i:o:", ["port=", "baud=", "ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--port"):
            serialport = arg
        elif opt in ("-b", "--baud"):
            baudrate = int(arg)

    print('Input file is', inputfile)
    print('Output file is', outputfile)
    print('Port is', serialport)
    print('Baudrate is', baudrate)

    if len(outputfile) > 0:
        read(serialport, baudrate, outputfile)

    if len(inputfile) > 0:
        write(serialport, baudrate, inputfile)


if __name__ == '__main__':
    main(sys.argv[1:])
