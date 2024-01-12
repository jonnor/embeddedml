
#include "holbeacon.c"

#define TEST_ADVERTISEMENT_LENGTH 29
uint8_t TEST_ADVERTISEMENT_DATA[TEST_ADVERTISEMENT_LENGTH] = {0.0}; 

void
test_holbeacon_simple()
{
    Holbeacon _beacon;
    Holbeacon *beacon = &_beacon;

    // FIXME: setup dummy I2C transport

    const HolbeaconError setup_err = holbeacon_setup_default(beacon);

    holbeacon_set_advertisement(beacon, TEST_ADVERTISEMENT_DATA, TEST_ADVERTISEMENT_LENGTH);

    holbeacon_transmit(beacon, true);

    // FIXME: assert that there are transmission events coming out
}

int
main() {

    test_holbeacon_simple();
}


