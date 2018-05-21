# coding:utf-8
from __future__ import print_function, unicode_literals

import json
import os


class Irs(object):
    __THIS_MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
    __DEFAULT_IRS_PATH = __THIS_MODULE_PATH + '/irs.json'

    def __init__(self, category, maker, model, irs_path=__DEFAULT_IRS_PATH):
        # type(object, str, str, str, str)
        self.__irs_path = irs_path
        self.__irs = self.__load_irs(irs_path)
        self.__category = category
        self.__maker = maker
        self.__model = model
        self.__commands = self.__find_commands()

    @classmethod
    def __load_irs(cls, irs_path):
        # type: (cls, str) -> dict
        try:
            with open(irs_path, 'r') as fp:
                irs = json.load(fp)
            return irs

        except FileNotFoundError:
            print('ERROR:' + ':File exist error')
            print('not found Irs json file')
            raise FileNotFoundError

    def __find_commands(self):
        # type: (self) -> dict
        devices = [device for device in self.__irs['devices'] if device['category'] == self.__category]
        devices = [device for device in devices if device['maker'] == self.__maker]
        device = [device for device in devices if self.__model in device['rc_model']
                  or self.__model in device['device_model']][0]

        return device['commands']

    def get_command(self, request):
        self.__find_commands()
        for command in self.__commands:
            if command['name'] == request:
                return command['data']
        return None

    @property
    def irs(self):
        return self.__irs


def main():
    import sys
    args = sys.argv
    category = args[1]
    maker = args[2]
    model = args[3]
    command = args[4]
    irs = Irs(category, maker, model)
    data = irs.get_command(command)
    print(data)


if __name__ == '__main__':
    main()
