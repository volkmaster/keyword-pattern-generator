import sys
import util
import settings


__author__ = 'Ziga Vucko'


def increment_printer_no(printer_no):
    printer_no += 1
    return printer_no % len(settings.PRINTER_NAMES)


def run(printer_no):
    printer_name = settings.PRINTER_NAMES[printer_no]

    print(util.timestamp() + ' Printing document on printer #' + str(printer_no) + ' (' + printer_name + ')')

    # Mac OS X and Linux OS
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        print_unix(printer_name)
    # Windows OS
    elif sys.platform.startswith('win'):
        print_windows(printer_name)

    return increment_printer_no(printer_no)


def print_unix(printer_name):
    import subprocess

    proc = subprocess.Popen("lpr -P " + printer_name + ' ' + settings.DOCUMENT_NAME, stdout=subprocess.PIPE, shell=True)
    (output, err) = proc.communicate()
    status = proc.wait()
    if status is not 0:
        print(err)


def print_windows(printer_name):
    import win32ui
    from PIL import Image, ImageWin

    # Constants for GetDeviceCaps

    # HORZRES / VERTRES = printable area
    HORZRES = 8
    VERTRES = 10

    # PHYSICALWIDTH/HEIGHT = total area
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    # Create a device context from a named printer and assess the printable size of the paper.
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

    # Open the image and work out how much to multiply each pixel by to get it as big as possible on the page without
    # distorting.
    img = Image.open(settings.DOCUMENT_NAME)
    ratios = [1.0 * printable_area[0] / img.size[0], 1.0 * printable_area[1] / img.size[1]]
    scale = min(ratios)

    # Start the print job, and draw the image to the printer device at the scaled size.
    hDC.StartDoc(settings.DOCUMENT_NAME)
    hDC.StartPage()

    dib = ImageWin.Dib(img)
    scaled_width, scaled_height = [int(scale * i) for i in img.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = int((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()
