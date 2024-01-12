
// A single transmission of adverisement data on BLE
typedef struct _HolbeaconFakeAdvertisementEvent {
    uint64_t time;
    uint8_t *advertisement_data;
    uint8_t *advertisement_length;
} HolbeaconFakeAdvertisementEvent;

#define HOLBEACON_REGISTERS_LENGTH 0x33

typedef struct _HolbeaconFake {

    // FIXME: i2c transport

    // internal state
    uint64_t last_run_time;
    // the register map data
    uint8_t configration_registers[HOLBEACON_REGISTERS_LENGTH];

    // statistics
    // TODO: split this out
    uint64_t advertisement_counter;
    uint64_t advertisement_last_time;

} HolbeaconFake; 

HolbeaconError
holbeacon_fake_init(HolbeaconFake *self) 
{
    self->last_run_time = 0;

    self->advertisement_counter = 0;
    self->advertisement_last_time = 0;

    return HolbeaconOK;
}

void
holbeacon_fake_emit_transmit(HolbeaconFake *self, uint64_t time)
{
    // FIXME: call callback with HolbeaconFakeAdvertisementEvent
    self->advertisement_counter += 1;
    self->advertisement_last_time = time;
}

HolbeaconError
holbeacon_fake_run(HolbeaconFake *self, uint64_t time)
{
    if (time < self->last_run_time) {
        return HolbeaconErrorUnknown;
    }
    uint64_t time_since_last = time - self->last_run_time;

    // FIXME: split into periods. Send N times per period
    holbeacon_fake_emit_transmit(self, time);

    self->last_run_time = time;

    return HolbeaconOK;
}

