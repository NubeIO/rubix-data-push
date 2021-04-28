import os

url = 'https://github.com/NubeIO/lora-raw/releases/download/v1.5.2/rubix-lora-1.5.2-0801be89.armv7.zip'
cmd = f"wget -c --read-timeout=5 --tries=0 {url}"
os.system(cmd)

folder = "/home/pi/rubix-lora-1.5.2-0801be89.armv7.zip"
# dir = "/home/aidan/code/py-nube/rubix-data-push"
from zipfile import ZipFile


def unpack_zip(zipfile='', path_from_local=''):
    filepath = path_from_local + zipfile
    extract_path = filepath.strip('.zip') + '/'
    parent_archive = ZipFile(filepath)
    parent_archive.extractall(extract_path)
    namelist = parent_archive.namelist()
    parent_archive.close()
    for name in namelist:
        try:
            if name[-4:] == '.zip':
                unpack_zip(zipfile=name, path_from_local=extract_path)
        except:
            print('failed on', name)
            pass
    return extract_path


unpack_zip(folder)
