import random
import time
import api_caller
import document_generator
import printer
import util


__author__ = 'Ziga Vucko'


PRINT_DELAY = 5 * 60  # 5 minutes
RESTART_DELAY = 20 * 60  # 20 minutes


def increment_serial_no(serial_no):
    serial_no += 1
    file = open('serial_number.txt', 'w')
    file.write(str(serial_no))
    file.close()
    return serial_no


def main():
    file = open('keywords.txt', 'r')
    keywords = file.read().splitlines()
    file.close()

    file = open('serial_number.txt', 'r')
    serial_no = int(file.read())
    file.close()

    # update the cache
    print(util.timestamp() + ' Updating the cache')
    for keyword in keywords:
        api_caller.run(keyword)

    # generate and print documents continuously every 5 minutes on different printers
    printer_no = 0
    while True:
        if 10 < util.current_time().hour < 18:
            random.shuffle(keywords)
            document_generator.run(keywords[:3], serial_no)
            printer_no = printer.run(printer_no)
            serial_no = increment_serial_no(serial_no)

            # delay generation and printing of a new document
            time.sleep(PRINT_DELAY)
        else:
            print(util.timestamp() + ' Out of working hours (10-18)')

            # delay the potential restart of the process every 20 minutes
            time.sleep(RESTART_DELAY)


if __name__ == '__main__':
    main()
