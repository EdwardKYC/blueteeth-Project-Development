#include <zephyr/kernel.h>
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>
#include <zephyr/sys/printk.h>
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/services/nus.h>
#include <zephyr/drivers/gpio.h>
#include <hal/nrf_gpio.h>
#include <zephyr/drivers/adc.h>

#define DEVICE_NAME "nrf03"
#define DEVICE_NAME_LEN (sizeof(DEVICE_NAME) - 1)

#define LED_RED 13
#define LED_GREEN 14
#define LED_BLUE 15
#define LED_WHITE 16

#define ADC_RESOLUTION  10
#define ADC_GAIN        ADC_GAIN_1
#define ADC_REFERENCE ADC_REF_VDD_1_4
#define ADC_CHANNEL     0  // SAADC 通道 0

static const struct device *adc_dev = DEVICE_DT_GET_ANY(nordic_nrf_saadc);
static struct bt_conn *current_conn = NULL;
static int16_t sample_buffer;

static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA_BYTES(BT_DATA_UUID128_ALL, BT_UUID_NUS_SRV_VAL),
    BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};

static uint8_t led_state = 0;

void set_led_color(uint8_t rgb_code) {
    nrf_gpio_pin_write(LED_RED,   (rgb_code & 0b001));
    nrf_gpio_pin_write(LED_GREEN, (rgb_code & 0b010));
    nrf_gpio_pin_write(LED_BLUE,  (rgb_code & 0b100));
}

// **讀取 ADC 並轉換為 mV**
int read_adc_voltage(void)
{
    struct adc_channel_cfg channel_cfg = {
        .gain = ADC_GAIN,
        .reference = ADC_REFERENCE,
        .acquisition_time = ADC_ACQ_TIME_DEFAULT,
        .channel_id = ADC_CHANNEL,
        .input_positive = SAADC_CH_PSELP_PSELP_AnalogInput0,
    };

    struct adc_sequence sequence = {
        .channels = BIT(ADC_CHANNEL),
        .buffer = &sample_buffer,
        .buffer_size = sizeof(sample_buffer),
        .resolution = ADC_RESOLUTION,
    };

    if (!device_is_ready(adc_dev)) {
        printk("ADC device not found!\n");
        return -1;
    }

    int err = adc_channel_setup(adc_dev, &channel_cfg);
    if (err) {
        printk("ADC channel setup failed: %d\n", err);
        return -1;
    }

    err = adc_read(adc_dev, &sequence);
    if (err) {
        printk("Failed to read ADC: %d\n", err);
        return -1;
    }

    int32_t voltage_mv = sample_buffer;
    adc_raw_to_millivolts(adc_ref_internal(adc_dev), ADC_GAIN, ADC_RESOLUTION, &voltage_mv);

    printk("ADC Voltage: %d mV\n", voltage_mv);
    return voltage_mv;
}

#define V_BATTERY_MAX 100  // 4.2V (mV)
#define V_BATTERY_MIN 0  // 3.0V (mV

int read_battery_percentage(void)
{
    int voltage_mv = read_adc_voltage() * 6;
    return read_adc_voltage;  // 讀取電壓並返回
    /*
    if (voltage_mv < 0) {
        return -1;  // 讀取失敗
    }
    printk("Battery voltage: %d mV\n", voltage_mv);
    // 限制範圍 (避免超過 100% 或小於 0%)
    if (voltage_mv > V_BATTERY_MAX) {
        return 100;
    }
    if (voltage_mv < V_BATTERY_MIN) {
        return 0;
    }

    // 計算剩餘電量 (%)
    int battery_percentage = (voltage_mv - V_BATTERY_MIN) * 100 / (V_BATTERY_MAX - V_BATTERY_MIN);
    return battery_percentage;
    */
}


void send_message(const char *message) {
    if (current_conn) {
        int err = bt_nus_send(NULL, message, strlen(message));
        if (err) {
            printk("Failed to send data: %d\n", err);
        } else {
            printk("Sent data: %s\n", message);
        }
    } else {
        printk("No active connection, unable to send data\n");
    }
}

static void received(struct bt_conn *conn, const void *data, uint16_t len, void *ctx)
{
    char message[CONFIG_BT_L2CAP_TX_MTU + 1] = "";

    ARG_UNUSED(conn);
    ARG_UNUSED(ctx);

    memcpy(message, data, MIN(sizeof(message) - 1, len));
    message[len] = '\0';
    printk("Received data: %s\n", message);

    if (strncmp(message, "change color:", 13) == 0) {
        char *color = message + 13;

        // 去除前後空白
        while (*color == ' ') color++;  // 前面空白
        for (int i = strlen(color) - 1; i >= 0 && color[i] == '\n'; i--) {
            color[i] = '\0';  // 移除尾端換行
        }

        uint8_t rgb_code = 0;

        if (strcmp(color, "off") == 0) rgb_code = 0b000;
        else if (strcmp(color, "red") == 0) rgb_code = 0b001;
        else if (strcmp(color, "green") == 0) rgb_code = 0b010;
        else if (strcmp(color, "yellow") == 0) rgb_code = 0b011;
        else if (strcmp(color, "blue") == 0) rgb_code = 0b100;
        else if (strcmp(color, "magenta") == 0) rgb_code = 0b101;   // 紅+藍
        else if (strcmp(color, "cyan") == 0) rgb_code = 0b110;      // 綠+藍
        else if (strcmp(color, "white") == 0) rgb_code = 0b111;
        else {
            printk("Unknown color: %s\n", color);
            return;
        }

        led_state = rgb_code;
        set_led_color(rgb_code);
        printk("LED color changed to %s (RGB code %d)\n", color, rgb_code);
    }
}

static void notif_enabled(bool enabled, void *ctx)
{
    ARG_UNUSED(ctx);
    printk("NUS Notification %s\n", enabled ? "Enabled" : "Disabled");
}

struct bt_nus_cb nus_listener = {
    .notif_enabled = notif_enabled,
    .received = received,
};

static void connected(struct bt_conn *conn, uint8_t err)
{
    if (err) {
        printk("Connection failed (err %u)\n", err);
        return;
    }
    current_conn = conn;
    printk("Connection established. Handle: %u\n", bt_conn_index(conn));
}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
    printk("Disconnected (reason %u)\n", reason);
    if (current_conn == conn) {
        current_conn = NULL;
    }
    int err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), NULL, 0);
    if (err) {
        printk("Failed to restart advertising: %d\n", err);
    } else {
        printk("Advertising restarted\n");
    }
    
}

static struct bt_conn_cb conn_callbacks = {
    .connected = connected,
    .disconnected = disconnected,
};

void main(void)
{
    int err;
    nrf_gpio_cfg_output(LED_RED);
    nrf_gpio_cfg_output(LED_GREEN);
    nrf_gpio_cfg_output(LED_BLUE);
    nrf_gpio_cfg_output(LED_WHITE);
    set_led_color(0);

    err = bt_enable(NULL);
    if (err) {
        printk("Failed to enable Bluetooth: %d\n", err);
        return;
    }

    err = bt_set_name(DEVICE_NAME);
    if (err) {
        printk("Failed to set Bluetooth name: %d\n", err);
        return;
    } else {
        printk("Bluetooth name set to %s\n", DEVICE_NAME);
    }

    printk("Bluetooth enabled. Starting advertising...\n");

    err = bt_nus_cb_register(&nus_listener, NULL);
    if (err) {
        printk("Failed to register NUS callback: %d\n", err);
        return;
    }

    bt_conn_cb_register(&conn_callbacks);
    err = bt_le_adv_start(BT_LE_ADV_CONN, ad, ARRAY_SIZE(ad), NULL, 0);
    if (err) {
        printk("Failed to start advertising: %d\n", err);
        return;
    }

    printk("Advertising started successfully!\n");

    while (1) {
        k_sleep(K_SECONDS(10));
    
        int battery_percent = read_battery_percentage();
        if (battery_percent < 0) {
            continue;
        }
    
        char message[50];
        snprintf(message, sizeof(message), "%d, -1, 1, nrf03", battery_percent);
        send_message(message);
    }
}
