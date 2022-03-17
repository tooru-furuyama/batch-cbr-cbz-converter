#!/usr/bin/env python3
import os
import argparse
import json
from pathlib import Path
import subprocess
import multiprocessing

class UnPack:

    def __init__(self):
        self.__verbose = True
        self.__max_proccess = 1
        self.__command = 'unrar.exe'
        self.__param = 'x'
        self.__in_filetype = ''
        self.__profile_json = 'config.json'
        return


    def set_input_filetype(self, filetype):
        self.__in_filetype = filetype
        return


    def config_load(self):
        profile_path = os.path.split(__file__)[0] + os.sep + self.__profile_json
        self.__verbose_print__(profile_path)

        try:
            config_file = open(profile_path, 'r')
            config_data = json.load(config_file)
            self.__verbose_print__(config_data)

            self.__verbose = config_data['exec_options']['verbose_option']
            self.__max_proccess = config_data['exec_options']['max_process']
            if len(self.__in_filetype) == 0:
                self.__in_filetype = config_data['decompression_options']['input_filetype']
            
            if self.__in_filetype == 'rar' or self.__in_filetype == 'cbr':
                self.__command = config_data['exec_options']['unrar_path']
                self.__param = config_data['decompression_options']['unrar_option']
            elif self.__in_filetype == 'zip' or self.__in_filetype == 'cbz':
                self.__command = config_data['exec_options']['7zip_path']
                self.__param = config_data['decompression_options']['7zip_option']

            self.__verbose_print__('Command location:   ' + self.__command)
            self.__verbose_print__('Command parameters: ' + self.__param)

        except:
            print('Error')
        
        return


    def exec(self):
        target_file = '*.' + self.__in_filetype
        filelist = Path(os.getcwd()).glob(target_file)
        self.__verbose_print__(filelist)

        if self.__max_proccess > multiprocessing.cpu_count():
            mp = multiprocessing.cpu_count()
        else:
            mp = self.__max_proccess

        self.__verbose_print__('Number of processes: ' + str(mp))

        shell_command = []
        for file in filelist:
            in_filename = '\"' + file.name + '\"'
            shell_command.append(' '.join([self.__command, self.__param, in_filename]))

        self.__verbose_print__(shell_command)

        with multiprocessing.Pool(processes=mp) as worker:
            try:
                worker.map(self.__exec__, shell_command)

            except multiprocessing.TimeoutError:
                print('Error: Multiprocessing error')

        return


    def __exec__(self, shell_command):
        success = True
        try:
            subprocess.run(shell_command, shell=True)
        except:
            success=False

        return success


    def __verbose_print__(self, dbg_data):
        if self.__verbose:
            print('VERBOSE: ', end='')
            print(dbg_data)
        return


def main():
    parser = argparse.ArgumentParser(description='Re-pack files into RAR with Recovery')
    parser.add_argument('-i', '--input_filetype', type=str, default='', help='Specify input file type. rar, zip or etc.')
    args = parser.parse_args()

    unpack = UnPack()
    if len(args.input_filetype) > 0:
        unpack.set_input_filetype(args.input_filetype)
    unpack.config_load()

    unpack.exec()
    return

if __name__ == '__main__':
    main()
