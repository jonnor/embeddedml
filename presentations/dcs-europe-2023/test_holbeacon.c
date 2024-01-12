
#include "holbeacon.c"
#include "holbeacon_fake.c"

#define TEST_ADVERTISEMENT_LENGTH 29
uint8_t TEST_ADVERTISEMENT_DATA[TEST_ADVERTISEMENT_LENGTH] = {0.0}; 



void
test_holbeacon_simple()
{
    Holbeacon _beacon;
    Holbeacon *beacon = &_beacon;

    HolbeaconFake _fake;
    HolbeaconFake *fake = &_fake;

    // FIXME: setup dummy I2C transport

    const HolbeaconError setup_err = holbeacon_setup_default(beacon);

    holbeacon_set_advertisement(beacon, TEST_ADVERTISEMENT_DATA, TEST_ADVERTISEMENT_LENGTH);

    holbeacon_transmit_enable(beacon, true);


    holbeacon_fake_run(fake, 0);

    holbeacon_fake_run(fake, 1000);

    int advertisements = fake->advertisement_counter;
    // FIXME: assert that there are transmission events coming out
}

int
main() {

    test_holbeacon_simple();
}


