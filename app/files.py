from app import app
from datetime import date
import os
import datetime
import sys
import comtypes.client


def time():
    new_date = date.today()
    new_time = datetime.datetime.now()
    current_date = new_time.strftime("%Y/%m/%d %H-%M-%S")
    return current_date


def folder_checker(args):
    # new_path='D:\React\himalayafrontend\public\%s'%args
    # os.chdir('D:\React\himalayafrontend\public')
    new_path = f'./{args}'

    if not os.path.exists(new_path):
        os.mkdir(args)
        return({'path': new_path, 'status': True})

    else:
        return({'path': new_path, 'status': False})


def file_extension(args):
    new_file = None
    if "." in args:
        new_split = args.rsplit(".", 2)
        new_file = new_split[1].upper()
    else:
        return False

    if new_file in app.config['ALLOWED_IMAGE_EXTENSION']:
        return True
    else:
        return False


def File_checker(args, kwargs):
    new_path = '%s/%s' % (args, kwargs)
    print(new_path)
    # os.chdir(args)
    if not os.path.exists(new_path):
        return True
    else:
        return False


def init_powerpoint():
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    return powerpoint


def ppt_to_pdf(powerpoint, inputFileName, outputFileName, formatType=32):
    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName + ".pdf"
    deck = powerpoint.Presentations.Open(inputFileName)
    deck.SaveAs(outputFileName, formatType)  # formatType = 32 for ppt to pdf
    deck.Close()


def convert_files_in_folder(powerpoint, folder):
    files = os.listdir(folder)
    pptfiles = [f for f in files if f.endswith((".ppt", ".pptx"))]
    for pptfile in pptfiles:
        fullpath = os.path.join(folder, pptfile)
        ppt_to_pdf(powerpoint, fullpath, fullpath)


def ppt_to_pdf():
    powerpoint = init_powerpoint()
    cwd = os.getcwd()
    convert_files_in_folder(powerpoint, cwd)
    powerpoint.Quit()
