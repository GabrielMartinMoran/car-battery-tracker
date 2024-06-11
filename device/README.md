[![Python v3.8+](https://img.shields.io/badge/Python-v3.8%2B-blue)](https://www.python.org/downloads)

# Car Battery Tracker

### Setting up the project

Micropython installation reference
document: [ESP8266 Micropython Web](https://micropython.org/download/ESP8266_GENERIC/)

1. Install python or configure a virtual environment in the computer.
2. Install python dependencies specified in `requirements.txt`:

```shell
pip install -r requirements.txt
```

### Running the code in the computer

1. Run the python script `run.py`.

### Running the tests

1. Run the script `run_tests.sh`.

### Flashing the code to the NodeMCU ESP8266 v3

1. Connect the ESP8266 to the computer.
2. Run the script `erase_flash.sh` (avoid if micropython is already installed in the ESP8266).
3. Run the script `flash_micropython.sh`  (avoid if micropython is already installed in the ESP8266).
4. Run the python script `upload_scripts.sh`.
5. Restart the ESP8266.
6. For viewing the ESP8266 logs, the script `serial_connect.sh` can be used.

### ESP8266 Quickref

Here it is a document with the documentation of micropython for using it in the
ESP8266: [ESP8266 Micropython Quickref](https://docs.micropython.org/en/latest/esp8266/quickref.html)

![ESP8266 Pinout](ESP8266.jpg)