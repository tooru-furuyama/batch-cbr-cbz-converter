#!/usr/bin/env python3
import sys
import os
import argparse
import json
import subprocess
import pprint
import glob

class Pack:

    def __init__(self):
        self.__verbose = True
        self.__multi_threads = 1
        self.__command = 'rar.exe'
        self.__param = 'a'
        self.__list_folder = []
        self.__in_filetype = 'jpg'
        self.__out_filetype = ''
        self.__out_fileextension = 'cbr'
        self.__profile_json = 'config.json'
        return


    def set_input_filetype(self, filetype):
        self.__in_filetype = filetype
        return


    def set_output_filetype(self, filetype):
        self.__out_filetype = filetype
        return


    def config_load(self):
        profile_path = os.path.split(__file__)[0] + os.sep + self.__profile_json
        self.__verbose_print__(profile_path)

        try:
            config_file = open(profile_path, 'r')
            config_data = json.load(config_file)
            self.__verbose_print__(config_data)

            self.__verbose = config_data['exec_options']['verbose_option']

            if len(self.__in_filetype) == 0:
                self.__in_filetype = config_data['compression_options']['input_filetype']
            if len(self.__out_filetype) == 0:
                self.__out_filetype = config_data['compression_options']['output_filetype']

            self.__out_fileextension = config_data['compression_options']['output_fileextension']
            self.__verbose_print__('Output file type and file extension: ' + self.__out_filetype + ', ' + self.__out_fileextension)

            self.__multi_threads = config_data['exec_options']['max_process']

            if self.__out_filetype == 'rar':
                self.__command = config_data['exec_options']['rar_path']
                self.__param = config_data['compression_options']['rar_option']
                if self.__multi_threads > 1:
                    self.__param = ' '.join([self.__param, '-mt' + str(self.__multi_threads)])

            elif self.__out_filetype == 'zip':
                self.__command = config_data['exec_options']['7zip_path']
                self.__param = config_data['compression_options']['7zip_option']
                if self.__multi_threads > 1:
                    self.__param = ' '.join([self.__param, '-mmt' + str(self.__multi_threads)])

            self.__verbose_print__('Command location:   ' + self.__command)
            self.__verbose_print__('Command parameters: ' + self.__param)

        except:
            print('Error: Configuration file load error')
            sys.exit()
        
        return


    def __list_directories__(self, path):
        self.__list_folder = glob.glob(glob.escape(path) + os.sep + '**' + os.sep, recursive = True)
        self.__verbose_print__(self.__list_folder)
        return


    def exec(self):
        self.__list_directories__(os.getcwd())

        shell_command = []
        for folder_path in self.__list_folder:
            folder_name = os.path.basename(os.path.dirname(folder_path))
            target_file = '*.' + self.__in_filetype
            if len(glob.glob(os.path.join(glob.escape(folder_path), target_file))) > 0:
                current_path = os.getcwd()
                os.chdir(folder_path)
                shell_command = ' '.join([self.__command, self.__param, '"' + current_path + os.sep + folder_name + '.' + self.__out_fileextension + '"', '"' + target_file + '"'])
                self.__verbose_print__(shell_command)
                self.__exec__(shell_command)
                os.chdir(current_path)

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


    def __verbose_pprint__(self, dbg_data):
        if self.__verbose:
            print('VERBOSE: ', end='')
            print(type(dbg_data))
            pprint.pprint(dbg_data)
        return


def main():
    parser = argparse.ArgumentParser(description='Re-pack files into RAR with Recovery')
    parser.add_argument('-i', '--input_filetype', type=str, default='', help='Specify input file type. jpg, png or etc.')
    parser.add_argument('-o', '--output_filetype', type=str, default='', help='Specify output file extension. rar or cbr.')
    args = parser.parse_args()

    pack = Pack()
    if len(args.input_filetype) > 0:
        pack.set_input_filetype(args.input_filetype)
    if len(args.output_filetype) > 0:
        pack.set_output_filetype(args.output_filetype)
    pack.config_load()

    pack.exec()
    return

if __name__ == '__main__':
    main()
