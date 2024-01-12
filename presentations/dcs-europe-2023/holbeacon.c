
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
#define HOLBEACON_REG_CHIPID_HIGH 0x31

#define HOLBEACON_REG_PDUDATA 0x10

// Flag definitions
#define HOLBEACON_RFTXSTART_REGISTER 0x1A
#define HOLBEACON_RFTXSTART_BIT 7

#define HOLBEACON_RSTPDUFF_REGISTER 0x11
#define HOLBEACON_RSTPDUFF_BIT 7


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


// Return error if it is set 
#define HOLBEACON_CHECK_ERROR(expr) \
    do { \
        const HolbeaconError _e = (expr); \
        if (_e != HolbeaconOK) { \
            return _e; \
        } \
    } while (0);

// Convenience for reading single byte-sized register
HolbeaconError
holbeacon_read_register(Holbeacon *self, uint8_t addr, uint8_t data[0])
{
    const int ret = holbeacon_i2c_read(self->i2c_user_data, data, 1, addr);
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

// Convenience for modifying a single byte-sized register
HolbeaconError
holbeacon_set_register(Holbeacon *self, uint8_t addr, uint8_t update)
{
    uint8_t read;
    HOLBEACON_CHECK_ERROR(holbeacon_read_register(self, addr, &read));

    uint8_t value = read;
    // FIXME: modify value using mask     

    HOLBEACON_CHECK_ERROR(holbeacon_write_register(self, addr, value));

    return HolbeaconOK;
}

// Convenience for modifying a single byte-sized register
HolbeaconError
holbeacon_clear_register(Holbeacon *self, uint8_t addr, uint8_t update)
{
    uint8_t read;
    HOLBEACON_CHECK_ERROR(holbeacon_read_register(self, addr, &read));

    uint8_t value = read;
    // FIXME: modify value using mask     

    HOLBEACON_CHECK_ERROR(holbeacon_write_register(self, addr, value));

    return HolbeaconOK;
}

HolbeaconError
holbeacon_check_chip_id(Holbeacon *self)
{
    uint8_t high;
    uint8_t low;
    HOLBEACON_CHECK_ERROR(holbeacon_read_register(self, HOLBEACON_REG_CHIPID_HIGH, &high));
    HOLBEACON_CHECK_ERROR(holbeacon_read_register(self, HOLBEACON_REG_CHIPID_LOW, &low));
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

    // Set RSTPDUFF to 1
    const uint8_t RSTPDUFF_MASK = (uint8_t)(1<<HOLBEACON_RSTPDUFF_BIT);
    HOLBEACON_CHECK_ERROR(holbeacon_set_register(self, HOLBEACON_RSTPDUFF_REGISTER, RSTPDUFF_MASK));

    // Wait for RSTPDUFF to become 0
    // FIXME iterate, with spacing and timeout

    // Write all packet data to PDUDATA register
    for (int i=0; i<length; i++) {
        const uint8_t val = data[i];
        HOLBEACON_CHECK_ERROR(holbeacon_write_register(self, HOLBEACON_REG_PDUDATA, val));
    }

    // Set PDULEN to the length
    // FIXME modify lower 6 bits, make sure top bit is preserved

    return HolbeaconOK;
}


HolbeaconError
holbeacon_transmit_enable(Holbeacon *self, bool transmit) 
{

    const uint8_t mask = (uint8_t)1<<HOLBEACON_RFTXSTART_BIT;
    const uint8_t addr = HOLBEACON_RFTXSTART_REGISTER;
    if (transmit) {
        return holbeacon_set_register(self, addr, mask);
    } else {
        return holbeacon_clear_register(self, addr, mask);
    }
    
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


