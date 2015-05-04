from shutil import rmtree, move
from glob import glob
import os


def create_path_to(file):
    new_file_dir = os.path.dirname(file)
    if new_file_dir != '':
        if not os.path.isdir(new_file_dir):
            os.makedirs(new_file_dir)


def readonly_handler(func, path, execinfo):
    os.chmod(path, 128)
    func(path)


def move_files_to_dir_by_mask(mask, destination, overwrite=False):
    files = glob(mask)

    if not os.path.isdir(destination):
        os.makedirs(destination)

    for file in files:
        new_filename = os.path.join(destination, os.path.basename(file))
        if os.path.isfile(new_filename):
            if overwrite:
                os.remove(new_filename)
            else:
                raise Exception("File already in directory " + new_filename)
        os.rename(file, new_filename)


def remove(mask):
    files_to_delete = glob(mask)
    for file in files_to_delete:
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            rmtree(file, ignore_errors=False, onerror=readonly_handler)


def rename(mask, new_name, overwrite=False):
    file = glob(mask)
    files_count = len(file)
    if files_count < 1:
        raise Exception('No mask file')
    if files_count > 1:
        raise Exception('More than one mask files exists')
    file = file[0]

    if os.path.exists(new_name):
        if overwrite:
            remove(file)
        else:
            raise Exception('Destination file "%s" exists' % new_name)

    create_path_to(new_name)

    if os.path.isdir(file):
        move(file[0], new_name)
    elif os.path.isfile(file):
        os.rename(file, new_name)


def move_files(from_path, to_path):
    files_list = os.listdir(from_path)
    for f in files_list:
        full_from_path = from_path + "/" + f
        move(full_from_path, to_path)


def clear(directory, extensions):
    if not isinstance(extensions, list):
        raise Exception("Extensions should be array")
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_name, file_extension = os.path.splitext(filename)
            if file_extension in extensions:
                try:
                    os.chmod(os.path.join(root, filename), 0x777)
                    os.remove(os.path.join(root, filename))
                except OSError as exc:
                    pass