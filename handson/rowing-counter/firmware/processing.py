
import math
import array

# No enum module in MicroPython at the moment :(
class State():
    WAIT_POS = 0
    POS_PEAK = 1
    WAIT_NEG = 2
    NEG_PEAK = 3
    CANCEL = 4
    ACCEPT = 5

# XXX: must match order of State class
state_names = [
    'wait-pos',
    'pos-peak',
    'wait-neg',
    'neg-peak',
    'cancel',
    'accept',
]

class LowpassFilter:
    def __init__(self, cutoff_freq, sample_rate):
        # Calculate smoothing factor (alpha)
        rc = 1.0 / (2 * math.pi * cutoff_freq)
        dt = 1.0 / sample_rate
        self.alpha = dt / (rc + dt)
        self.output = None
    
    def filter(self, input_value):
        if self.output is None:
            self.output = input_value
        else:
            self.output = self.alpha * input_value + (1 - self.alpha) * self.output
        return self.output

class DataProcessor():

    def __init__(self,
        samplerate,
        lowpass_cutoff=10.0,
        initial=State.WAIT_POS,
        pos_level=0.2,
        neg_level=-0.2,
        pos_time_min=0.1,
        neg_time_min=0.1,
        state_time_max=2.0,
        ):

        self.state = initial
        self.time_in_state = 0
        self.lowpass = LowpassFilter(lowpass_cutoff, samplerate)

        self.samplerate = samplerate
        self.pos_level = pos_level
        self.neg_level = neg_level

        # convert from seconds to number of samples
        self.pos_time_min = int(pos_time_min * samplerate)
        self.neg_time_min = int(neg_time_min * samplerate)
        self.time_max = int(state_time_max * samplerate)

        self.accepts = 0
        self.cancels = 0
    
    def process(self, values, filtered, states):
        """
        Analyze the accelerometers sensor data,
        to determine what is happening
        """

        assert len(values) == len(states), (len(values), len(states))
        assert len(values) == len(filtered), (len(values), len(filtered))

        for index, raw in enumerate(values):
            # TODO: add in a low-pass filter        

            value = self.lowpass.filter(raw)
            # FIXME: 

            # state-machine
            # default to keeping previous state
            new_state = self.state

            if self.state == State.CANCEL:
                # after cancel, immediately go back to start
                new_state = State.WAIT_POS
            elif self.state == State.ACCEPT:
                new_state = State.WAIT_POS

            elif self.state == State.WAIT_POS:
                if value >= self.pos_level:
                    new_state = State.POS_PEAK

            elif self.state == State.POS_PEAK:
                if value < self.pos_level:
                    if self.time_in_state > self.pos_time_min:
                        new_state = State.WAIT_NEG
                    else:
                        new_state = State.CANCEL
                else:
                    if self.time_in_state >= self.time_max:
                        new_state = State.CANCEL

            elif self.state == State.WAIT_NEG:
                if value < self.neg_level:
                    new_state = State.NEG_PEAK
                else:
                    if self.time_in_state >= self.time_max:
                        new_state = State.CANCEL

            elif self.state == State.NEG_PEAK:
                if value >= self.neg_level:
                    if self.time_in_state > self.neg_time_min:
                        new_state = State.ACCEPT
                    else:
                        new_state = State.CANCEL
                else:
                    if self.time_in_state >= self.time_max:
                        new_state = State.CANCEL

            if new_state != self.state:
                self.time_in_state = 0
            else:
                self.time_in_state += 1

            self.state = new_state
            states[index] = new_state
            filtered[index] = value

            if new_state == State.ACCEPT:
                self.accepts += 1
            if new_state == State.CANCEL:
                self.cancels += 1

