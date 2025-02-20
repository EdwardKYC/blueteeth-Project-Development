import tkinter as tk

connected_devices = {}

class Device:
    def __init__(self, name, mac):
        """
        初始化 Device 類
        :param name: 藍牙裝置名稱
        :param mac: 藍牙裝置 MAC 地址
        """
        self.name = name
        self.mac = mac

    def __str__(self):
        """
        定義裝置的字符串表示
        """
        return f"Device(Name: {self.name}, MAC: {self.mac})"

