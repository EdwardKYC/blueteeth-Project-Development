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

.. zephyr:code-sample:: ble_rgb_led_battery_monitor
   :name: BLE RGB LED & Battery Monitor
   :relevant-api: bluetooth, gpio, adc

   Control RGB LEDs and monitor battery percentage over BLE using Nordic UART Service (NUS) on nRF52840.

Overview
********

This sample demonstrates how to create a BLE peripheral using the Nordic UART Service (NUS)
to support two-way communication with a BLE central. The application allows users to:

* Remotely control RGB LED colors via BLE commands.
* Periodically read and send battery voltage data (converted to percentage).
* Maintain BLE advertising and handle reconnect logic automatically.

LEDs are controlled via GPIO, and battery voltage is read using the SAADC. The data is reported
in a custom string format via BLE using the NUS service.

Requirements
************

* Nordic nRF52840-based development board (e.g., Dongle, DK)
* GPIO-connected RGB LEDs (active high)
* Battery voltage connected to SAADC input (AIN0) with voltage divider (e.g., 1:6)
* A BLE central such as Nordic nRF Connect app or a BlueZ-based host

User Commands
*************

To change LED colors, the BLE central should send a UTF-8 encoded string in the following format:

.. code-block:: console

   change color: <color>

Supported color values:

* red
* green
* blue
* yellow
* cyan
* magenta
* white
* off

Example:

.. code-block:: console

   change color: magenta

Battery Monitoring
******************

Every 10 seconds, the device reads the analog battery voltage, scales it, converts to percentage,
and sends the result via BLE as a UTF-8 string:

.. code-block:: console

   <battery_percentage>, -1, 1, nrf03

Example:

.. code-block:: console

   83, -1, 1, nrf03

The percentage is derived from voltage levels between 3.0V (0%) and 4.2V (100%).

Building and Running
********************

This sample is located in your project directory.

Use the following command to build for the nRF52840 Dongle:

.. code-block:: console

   west build -b nrf52840dongle_nrf52840
   west flash

Make sure you have a valid `prj.conf` with the following essential configurations:

.. code-block:: ini

   CONFIG_BT=y
   CONFIG_BT_PERIPHERAL=y
   CONFIG_BT_DEVICE_NAME="nrf03"
   CONFIG_BT_NUS=y
   CONFIG_ADC=y
   CONFIG_BT_MAX_CONN=1

Testing
*******

1. Flash the firmware onto the nRF52840 device.
2. Open **nRF Connect** mobile app or similar BLE central software.
3. Scan and connect to the device named `nrf03`.
4. Use the UART/NUS console to send commands like `change color: green`.
5. Observe RGB LED color change and periodic battery status messages every 10 seconds.

References
**********

* :ref:`bluetooth samples section <bluetooth-samples>`
* :ref:`adc_interface`
* :ref:`gpio_interface`
* :ref:`nus_service`
