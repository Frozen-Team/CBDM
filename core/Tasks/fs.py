from shutil import rmtree, move, copytree, copyfile
from glob import glob
import os

from core import sys_config


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
        print('Removing ' + file)
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
        move(file, new_name)
    elif os.path.isfile(file):
        os.rename(file, new_name)


def move_files(from_path, to_path):
    files_list = os.listdir(from_path)
    for f in files_list:
        full_from_path = from_path + "/" + f
        move(full_from_path, to_path)


def clear(directory, extensions=[], except_extensions=[]):
    print('Cleaning up trash')
    log_filename = os.path.join(sys_config.log_folder, 'clear.log')
    create_path_to(log_filename)
    with open(log_filename, "a") as log_file:
        for root, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_name, file_extension = os.path.splitext(filename)
                if bool(extensions):
                    if not isinstance(extensions, list):
                        raise Exception("Extensions should be array")
                        sys.exit(1)
                    if file_extension in extensions:
                        try:
                            if file_extension not in except_extensions:
                                os.chmod(os.path.join(root, filename), 128)
                                log_file.write(str('rm file: ' + filename + '\n'))
                                os.remove(os.path.join(root, filename))
                        except OSError as exc:
                            log_file.write(str('Error rm file: ' + filename + '\n'))
                            pass
                elif bool(except_extensions):
                    if file_extension not in except_extensions:
                        try:
                            os.chmod(os.path.join(root, filename), 128)
                            log_file.write('rm file: ' + filename + '\n')
                            os.remove(os.path.join(root, filename))
                        except OSError as exc:
                            log_file.write(str('Error rm file: ' + filename + '\n'))
                            pass

    remove_empty_folders(directory)


def remove_empty_folders(from_directory):
    print('Removing empty folders from '+from_directory)
    def remove_empty_folders_system(path, log_file):
        if not os.path.isdir(path):
            return

        files = os.listdir(path)
        if len(files):
            for file in files:
                full_path = os.path.join(path, file)
                if os.path.isdir(full_path):
                    remove_empty_folders_system(full_path, log_file)

        files = os.listdir(path)
        if len(files) == 0:
            log_file.write(str("rm empty folder:" + path + '\n'))
            os.rmdir(path)
    log_filename = os.path.join(sys_config.log_folder, 'rm_empty_folders')
    create_path_to(log_filename)
    with open(log_filename, "w+") as log_file:
        remove_empty_folders_system(from_directory, log_file)


def copy(path_to_file_or_dir, destination, overwrite):
    file = path_to_file_or_dir

    if os.path.exists(destination):
        if overwrite:
            remove(destination)
        else:
            raise Exception('Destination file "%s" exists' % destination)

    create_path_to(destination)

    if os.path.isdir(file):
        copytree(file, destination)
    elif os.path.isfile(file):
        copyfile(file, destination)