import time

from src.platform_checker import PlatformChecker
from src.utils.request_status_checker import raise_if_failed

if PlatformChecker.is_device():
    from machine import ADC
    from urequests import post
else:
    from platform_mocks.machine import ADC
    from requests import post

from src.wifi.wifi_client import WiFiClient
from src.components.status_led import StatusLed

ADC_RANGE = 1024.0
MAX_MEASUREMENT_VOLTAGE = 19.01  # If Vin = ~20 V -> Vadc = 3.3 V(Adjusted for measuring around 12V is 19.01)
MEASUREMENT_OFFSER_ERROR = 1
REMOTE_API_URI = 'http://192.168.0.109:8432'


def _send_measure(voltage: float) -> None:
    response = post(f'{REMOTE_API_URI}/measures', json={
        'voltage': voltage
    })
    # If it failed raise an exception
    raise_if_failed(response)


def _take_measure(status_led: StatusLed, adc: ADC) -> None:
    status_led.set_status(True)
    try:
        read = adc.read()
        adjusted_read = abs(read - MEASUREMENT_OFFSER_ERROR)
        voltage = (adjusted_read / ADC_RANGE) * MAX_MEASUREMENT_VOLTAGE
        print(f'Read: {read} | Measured voltage: {voltage}V')
        _send_measure(voltage)
    except Exception as e:
        print(e)
    status_led.set_status(False)


def _orchestrate(wifi_client: WiFiClient, status_led: StatusLed, adc: ADC) -> None:
    if not wifi_client.has_any_network_configured():
        return

    # Try connect to WiFi
    while not wifi_client.is_connected():
        wifi_client.connect()
        time.sleep(1)

    _take_measure(status_led, adc)


def main() -> None:
    wifi_client = WiFiClient()
    status_led = StatusLed(False)
    adc = ADC(0)

    while True:
        _orchestrate(wifi_client, status_led, adc)
        time.sleep(5)
