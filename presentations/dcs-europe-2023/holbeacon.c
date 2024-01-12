
// 
/*
Holbeacon: Driver for Holtek BLE beacon ICs.

Supports the Holtek BC7161/BC7162 chips,
and modules with these chips such as Holtek BM7161 / BM7162.

Written in portable C99, supporting pluggable I2C transport.

Copyright: Jon Nordby 2024
License: MIT
*/



#include <stdbool.h>
#include <stdint.h>

// Register definitions
#define HOLBEACON_REG_CHIPID_LOW 0x30
#define HOLBEACON_REG_CHIPID_HIGH 0x30

typedef struct _Holbeacon {
    void *i2c_user_data; // pointer to . Is passed to the i2c_read/i2c_write as first argument
} Holbeacon;


typedef enum _HolbeaconError {
    HolbeaconOK = 0,
    HolbeaconErrorUnknown,
    HolbeaconErrorWrongDevice,
    HolbeaconErrorNotImplemented,
    HolbeaconErrorCommunicationFailure,
    HolbeaconErrorSizeMismatch,
    HolbeaconError_Length
} HolbeaconError;



// I2C transport abstraction
int
holbeacon_default_i2c_write(const void *user_data, const uint8_t *buf, uint32_t num_bytes, uint16_t addr)
{
    return HolbeaconErrorNotImplemented;
}

int
holbeacon_default_i2c_read(const void *user_data, uint8_t *buf, uint32_t num_bytes, uint16_t addr)
{
    return HolbeaconErrorNotImplemented;
}


#ifndef holbeacon_i2c_write
#define holbeacon_i2c_write holbeacon_default_i2c_write
#warning "holbeacon_i2c_write not defined"
#endif

#ifndef holbeacon_i2c_read
#define holbeacon_i2c_read holbeacon_default_i2c_read
#warning "holbeacon_i2c_read not defined"
#endif


// Convenience for reading single byte-sized register
HolbeaconError
holbeacon_read_register(Holbeacon *self, uint8_t addr)
{
    uint8_t buffer[1];
    const int ret = holbeacon_i2c_read(self->i2c_user_data, buffer, 1, addr);
    return (ret == 0) ? HolbeaconOK : HolbeaconErrorCommunicationFailure;
}

// Convenience for writing a single byte-sized register
HolbeaconError
holbeacon_write_register(Holbeacon *self, uint8_t addr, uint8_t data)
{
    uint8_t buffer[1];
    buffer[0] = data;
    const int ret = holbeacon_i2c_write(self->i2c_user_data, buffer, 1, addr);    
    return (ret == 0) ? HolbeaconOK : HolbeaconErrorCommunicationFailure;
}

HolbeaconError
holbeacon_check_chip_id(Holbeacon *self)
{
    const uint8_t high = holbeacon_read_register(self, HOLBEACON_REG_CHIPID_HIGH);
    const uint8_t low = holbeacon_read_register(self, HOLBEACON_REG_CHIPID_LOW);
    const bool correct = (high == 0x61) & (low == 0x71);

    if (!correct) {
        return HolbeaconErrorWrongDevice;
    }

    return HolbeaconOK;   
}


HolbeaconError
holbeacon_set_advertisement(Holbeacon *self, const uint8_t *data, uint8_t length)
{
    if (length > 29) {
        return HolbeaconErrorSizeMismatch;
    }

    /* FIXME: implement
    Set RSTPDUFF to 1
    Wait for RSTPDUFF to become 0
    Write all packet data to PDUDATA register
        Header, Address, Payload
    Set PDULEN to the length
    */

    return HolbeaconOK;
}


HolbeaconError
holbeacon_transmit(Holbeacon *self, bool transmit) 
{
    // FIXME: configure RFTXSTART

}


HolbeaconError
holbeacon_configure_transmission(Holbeacon *self)
{

    /* FIXME: implement
    PKT_AUTORS - resends number
    PKT_APRD - resends delay
    PKT_PERIODS - also a time??
    HOP_FNO - channel selection
    RNDDLY_EN - whether to randomize advertizing event period maybe separate out?
    */

    return HolbeaconOK;
}

/* TODO: implement

HolbeaconError
holbeacon_set_power() {
Set power level

    RFTXP_1
    RFTXP_2

}
*/

HolbeaconError
holbeacon_setup_default(Holbeacon *self)
{
    HolbeaconError err = HolbeaconErrorUnknown;
    
    // Check chip ID
    err = holbeacon_check_chip_id(self);
    if (err != HolbeaconOK) {
        return err;
    }

    // Wait for calibration
    // FIXME: implement
    // Cal1

    // Set power management
    // FIXME: implement
    // LSTOS
    

    // Setup transmission timing
    err = holbeacon_configure_transmission(self);
    if (err != HolbeaconOK) {
        return err;
    }    

    return HolbeaconOK;
}


