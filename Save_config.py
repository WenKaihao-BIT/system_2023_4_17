#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/20 21:34
# @Author  : wenkaihao
# @File    : Save_config.py
# @Description : 这个函数是用来balabalabala自己写


class Config:
    def __init__(self):
        self.Serial_Port_Config = None
        self.Serial_Port_Config_Path = 'config/Serial_Port_Configuration.txt'
        self.SetUpConfig()

    def SetUpConfig(self):
        self.Serial_Port_Config = self.ReadConfig(self.Serial_Port_Config_Path)
        print(self.Serial_Port_Config)

    def ReadConfig(self, file_path):
        with open(file_path, 'r') as file:
            # 读取文件内容
            file_content = file.read().splitlines()
            # 初始化一个空字典
            result_dict = {}
            # 遍历列表元素，分割并构建字典
            for item in file_content:
                key, value = item.split('@')
                result_dict[key] = value
            # print(result_dict)  # 输出文件内容
            # print(type(result_dict))
            return result_dict

    def WriteConfig(self, file_path, ConfigName):
        # 初始化一个空字符串
        result_str = ""
        # 遍历字典，构建字符串
        for key, value in ConfigName.items():
            result_str += f"{key}@{value}\n"

        with open(file_path, 'w') as file:
            file.write(result_str)


if __name__ == '__main__':
    c = Config()
    c.Serial_Port_Config['Camera'] = '3'
    print(c.Serial_Port_Config)
    c.WriteConfig(c.Serial_Port_Config_Path, c.Serial_Port_Config)
