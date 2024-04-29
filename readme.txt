Files that need to be on the PC:
server.py
transmitter.py
receiver.py

Files that need to be on the Pi:
main.py
control.py
image.py

Make sure I2C port is activated in raspi-config

Setting up the virtual environment:
sudo apt install picamera2
python -m venv tank-venv --system-site-packages
source tank-venv/bin/activate
pip3 install picamera2
pip3 install adafruit-circuitpython-servokit
pip3 install adafruit-circuitpython-motorkit


Run the command "sudo pigpiod" when you start the Pi

Run server.py on the PC to start the server, then run main.py on the pi to run the client. 