import os
import argparse
import json
import subprocess
import multiprocessing
import pprint
import glob

class Pack:

    def __init__(self):
        self.__verbose = True
        self.__max_proccess = 1
        self.__command = 'rar.exe'
        self.__param = 'a -ma4 -m5 -rr10'
        self.__list_folder = []
        self.__in_filetype = ''
        self.__out_filetype = ''
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

            if len(self.__in_filetype) == 0:
                self.__in_filetype = config_data['compression_options']['input_filetype']
            if len(self.__out_filetype) == 0:
                self.__out_filetype = config_data['compression_options']['output_filetype']

            self.__verbose = config_data['exec_options']['verbose_option']
            self.__max_proccess = config_data['exec_options']['max_process']
            if self.__out_filetype == 'rar':
                self.__command = config_data['exec_options']['rar_path']
                self.__param = config_data['output_options']['rar_option']

            elif self.__out_filetype == 'zip':
                self.__command = config_data['exec_options']['7zip_path']
                self.__param = config_data['output_options']['7zip_option']

        except:
            print('')
        
        return


    def __list_directories__(self, path):
        self.__list_folder = glob.glob(path + os.sep + '**' + os.sep, recursive = True)
        return


    def exec(self):
        self.__list_directories__(os.getcwd())

        if self.__max_proccess > multiprocessing.cpu_count():
            mp = multiprocessing.cpu_count()
        else:
            mp = self.__max_proccess

        shell_command = []
        for folder_path in self.__list_folder:
            folder_name = os.path.basename(os.path.dirname(folder_path))
            target_file = '*.' + self.__in_filetype
            if len(glob.glob(folder_path + os.sep + target_file)) > 0:
                shell_command.append(' '.join([self.__command, self.__param, '"' + os.getcwd() + os.sep + folder_name + '.' + self.__out_filetype + '"', '"' + folder_path + target_file + '"']))

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
