from bleak import BleakClient

class ConnectedDevice:
    def __init__(self, name, mac_address, client=None):
        self.name = name
        self.mac_address = mac_address
        self.client = client 

    def __repr__(self):
        return f"ConnectedDevice(name='{self.name}', mac_address='{self.mac_address}')"

# 建立空的列表來存放裝置
connected_devices = []