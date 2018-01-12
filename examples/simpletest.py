# Simple example to send a message and then wait indefinitely for messages
# to be received.  This uses the default RadioHead compatible GFSK_Rb250_Fd250
# modulation and packet format for the radio.
# Author: Tony DiCola
import time

import board
import busio
import digitalio

import adafruit_rfm69


# Define radio parameters.
RADIO_FREQ_MHZ   = 915.0  # Frequency of the radio in Mhz. Must match your
                          # module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip.
CS    = digitalio.DigitalInOut(board.D5)
RESET = digitalio.DigitalInOut(board.D6)
G0    = digitalio.DigitalInOut(board.D9)

# Initialize SPI bus.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, G0, RADIO_FREQ_MHZ)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = '\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

# Print out some chip state:
print('Temperature: {0}C'.format(rfm69.temperature))
print('Frequency: {0}mhz'.format(rfm69.frequency_mhz))
print('Bit rate: {0}kbit/s'.format(rfm69.bitrate/1000))
print('Frequency deviation: {0}hz'.format(rfm69.frequency_deviation))

# Send a packet.
rfm69.send('Hello world!\r\n')
print('Sent hello world message!')

# Wait to receive packets.
print('Waiting for packets...')
while True:
    packet = rfm69.receive()
    # Optionally change the receive timeout from its default of 0.5 seconds:
    #packet = rfm69.receive(timeout_s=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is None:
        print('Received nothing! Listening again...')
    else:
        # Received a packet!
        print('Received: {0}'.format(packet))