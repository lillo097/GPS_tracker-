import smbus2
import time
import json
from datetime import datetime


# Constants for INA226 registers
INA226_REG_CONFIG = 0x00
INA226_REG_SHUNT_VOLTAGE = 0x01
INA226_REG_BUS_VOLTAGE = 0x02
INA226_REG_POWER = 0x03
INA226_REG_CURRENT = 0x04
INA226_REG_CALIBRATION = 0x05

# I2C address of the INA226 (default is 0x40, but this may vary)
INA226_I2C_ADDRESS = 0x40

# Create an SMBus object for I2C communication
bus = smbus2.SMBus(1)  # 1 indicates /dev/i2c-1

def write_register(register, value):
    """Write a 16-bit value to a specific INA226 register."""
    bus.write_word_data(INA226_I2C_ADDRESS, register, ((value & 0xFF) << 8) | (value >> 8))

def read_register(register):
    """Read a 16-bit value from a specific INA226 register."""
    raw = bus.read_word_data(INA226_I2C_ADDRESS, register)
    return ((raw & 0xFF) << 8) | (raw >> 8)

def initialize_ina226():
    """Initialize the INA226 module with default settings and calibration."""
    # Reset the configuration register to default values
    write_register(INA226_REG_CONFIG, 0x4127)  # Default configuration

    # Calibration value: adjust based on shunt resistor value and expected current range
    # For example, using a 0.1-ohm shunt resistor and a max current of 2A:
    calibration_value = int(0.00512 / (0.1 * 0.001))  # Example calculation
    write_register(INA226_REG_CALIBRATION, calibration_value)

def read_voltage_current():
    """Read bus voltage and current from INA226."""
    bus_voltage_raw = read_register(INA226_REG_BUS_VOLTAGE)
    shunt_voltage_raw = read_register(INA226_REG_SHUNT_VOLTAGE)
    
    # Convert raw values to meaningful units
   # bus_voltage = (bus_voltage_raw * 1.25e-3) + 0.02  # Voltage in volts (1.25 mV per LSB)
    bus_voltage = (bus_voltage_raw * 1.25e-3) + 0.10 #+ 0.230
    shunt_voltage = shunt_voltage_raw * 2.5e-6  # Voltage in volts (2.5 uV per LSB)

    # Current calculation depends on calibration value; for simplicity:
    current = shunt_voltage / 0.1  # Assuming a 0.1-ohm shunt resistor

    return bus_voltage, current

def salva_e_calcola_media(file_json, tensione, corrente):
    try:
        with open(file_json, 'r') as f:
            dati = json.load(f)
    except FileNotFoundError:
        dati = []

    # Aggiungi i nuovi dati
    nuovo_dato = {
        "tensione": tensione,
        "corrente": corrente,
        "data_ora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    dati.append(nuovo_dato)

    # Salva i dati aggiornati nel file JSON
    with open(file_json, 'w') as f:
        json.dump(dati, f, indent=4)

    # Calcola la media progressiva
    #somma_tensioni = sum(d["tensione"] for d in dati)
    #somma_correnti = sum(d["corrente"] for d in dati)
    #totale = len(dati)

    #media = {
        #"media_tensione": somma_tensioni / totale,
        #"media_corrente": somma_correnti / totale
    #}

    return 

def run_multimeter():
    try:
        initialize_ina226()
       # while True:
        bus_voltage, current = read_voltage_current()
  #          print(f"Bus Voltage: {bus_voltage:.3f} V")
 #           print(f"Current: {current:.3f} A")
#            print("--------------------------")
#        media = salva_e_calcola_media('multimeter_data.json', bus_voltage, current)

       # print(media)

    except KeyboardInterrupt:
        print("Exiting...")
#    finally:
#        bus.close()

    return bus_voltage, current 


#run_multimeter()

