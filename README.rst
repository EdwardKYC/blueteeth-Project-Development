.. zephyr:code-sample:: ble_peripheral_nus
   :name: Peripheral NUS
   :relevant-api: bluetooth

   Implement a simple echo server using the Nordic UART Service (NUS).

Overview
********

This sample demonstrates the usage of the NUS service (Nordic UART Service) as a serial
endpoint to exchange data. In this case, the sample assumes the data is UTF-8 encoded,
but it may be binary data. Once the user connects to the device and subscribes to the TX
characteristic, it will start receiving periodic notifications with "Hello World!\n".

Requirements
************

* BlueZ running on the host, or
* A board with Bluetooth LE support

Building and Running
********************

This sample can be found under :zephyr_file:`samples/bluetooth/peripheral_nus` in the
Zephyr tree.

See :ref:`bluetooth samples section <bluetooth-samples>` for details.

* nRF52840 BLE RGB LED Controller and Battery Monitor

This project implements a Bluetooth Low Energy (BLE) peripheral application on the **nRF52840** platform using **Zephyr RTOS**.  
The firmware supports remote control of RGB LEDs via BLE commands and periodically reports battery voltage information through the **Nordic UART Service (NUS)**.

---

** Features

- Bluetooth LE advertising and connection via NUS (Nordic UART Service)
- Remote RGB LED color control using plain-text BLE commands
- Periodic battery voltage monitoring via SAADC
- BLE message transmission containing battery percentage data
- Automatic restart of advertising after disconnection

---

** Hardware Configuration

The following GPIOs and peripherals are used in this application:

| Pin      | Function        | Description                              |
|----------|-----------------|------------------------------------------|
| P0.13    | LED Red         | Output, active high                      |
| P0.14    | LED Green       | Output, active high                      |
| P0.15    | LED Blue        | Output, active high                      |
| P0.02    | ADC Input (AIN0)| Reads voltage from battery divider input |

> ⚠ Ensure that the battery voltage is scaled appropriately through a resistor divider to stay within the SAADC input range.

---

** BLE Communication

*** LED Control Commands

This firmware listens for text-based commands sent over the NUS service. To control the LED color, send:

