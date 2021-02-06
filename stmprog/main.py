import getopt
import sys
import serial

inputfile = ''
outputfile = ''
serialport = ''
baudrate = 115200


def read(serialport, baudrate, outputfile):
    with serial.Serial(serialport, baudrate) as ser:
        ser.timeout = 20
        ser.write(str.encode("read\n"))
        with open(outputfile, "wb") as file:
            for x in range(192):
                data = ser.read(1024)
                print("Progress:", "{:.2f}".format(100*x/192), "%")
                file.write(data)


def write(serialport, baudrate, inputfile):
    with open(inputfile, "rb") as file:
        data = file.read()
        with serial.Serial(serialport, baudrate) as ser:
            ser.write(str.encode("erase\n"))
            result = ser.readline()
            if result != str.encode("OK\r\n"):
                print("Erase failed")
                sys.exit(2)

            ser.write(str.encode("write\n"))
            result = ser.readline()
            if result != str.encode("OK\r\n"):
                print("Write init failed")
                sys.exit(2)

            toWrite = len(data)
            written = 0

            while toWrite > 0:
                length = 1024
                if length > toWrite:
                    length = toWrite

                ser.write(str.encode(str(length) + "\n"))
                result = ser.readline()
                if result != str.encode("OK\r\n"):
                    print("Write size failed")
                    sys.exit(2)

                ser.write(data[written:(written + length)])
                result = ser.readline()
                if result != str.encode("OK\r\n"):
                    print("Write failed")
                    sys.exit(2)

                written = written + length
                toWrite = toWrite - length
                print("Written:", written, "bytes")

            ser.write(str.encode("0\n"))
            result = ser.readline()
            if result != str.encode("OK\r\n"):
                print("Write size failed")
                sys.exit(2)

            ser.write(str.encode("reset\n"))
            result = ser.readline()
            if result != str.encode("OK\r\n"):
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
