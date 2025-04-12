#config.py
from bleak import BleakClient

class ConnectedDevice:
    def __init__(self, name, address, client=None):
        self.name = name
        self.address = address
        self.client = client 

    def __repr__(self):
        return f"ConnectedDevice(name='{self.name}', address='{self.address}')"

# 建立空的列表來存放裝置
connected_devices = []