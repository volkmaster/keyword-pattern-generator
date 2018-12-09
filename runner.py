import random
import time
from api import api_caller
import document_generator
import printer
import util
import settings


__author__ = 'Ziga Vucko'


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

    print(util.timestamp() + ' Updating the cache')
    for keyword in keywords:
        api_caller.run(keyword)

    if settings.PRINT_MODE:
        # continuously print generated documents based on 3 random keywords
        printer_no = 0
        while True:
            random.shuffle(keywords)
            document_generator.run(keywords[:3], serial_no)
            printer_no = printer.run(printer_no)
            serial_no = increment_serial_no(serial_no)
            time.sleep(settings.PRINT_DELAY)
    else:
        # generate a single document based on 3 random keywords
        document_generator.run(keywords[:3], serial_no, include_data=True)
        increment_serial_no(serial_no)


if __name__ == '__main__':
    main()
