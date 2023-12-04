
import os.path

import structlog
import serial

log = structlog.get_logger()

def parse():
    import argparse
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--out', metavar='FILE', type=str, default='',
                        help='Where to put output')

    parser.add_argument('--port', metavar='FILE', type=str, default='/dev/ttyACM0',
                        help='Serial port to read from')
    parser.add_argument('--baudrate', metavar='NUMBER', type=int, default=115200,
                        help='Baudrate of serial')
    parser.add_argument('--timeout', type=float, default=0.1,
                        help='Max time between reads')

    args = parser.parse_args()

    return args


def main():
    args = parse()

    baud = args.baudrate
    timeout = args.timeout
    out = args.out
    port = args.port

    with serial.Serial(port, baud, timeout=timeout) as ser:
        assert not os.path.exists(out), out

        with open(out, 'wb+') as outfile:

            log.info('files-opened', serial=port, output=out)

            while True:
                line = ser.readline()
                #log.info('line', line=line)
                if line:
                    outfile.write(line)

if __name__ == '__main__':
    main()

