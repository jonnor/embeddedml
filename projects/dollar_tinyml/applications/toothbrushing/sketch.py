
def median(values):
    L = len(values)
    if L == 0:
        raise ValueError('Input empty')
    if L == 1:
        return values[0]

    ordered = sorted(values)
    is_odd = (L % 2) == 1
    if is_odd:
        out = ordered[L//2]
    else:
        l = ordered[(L//2)-1]
        h = ordered[(L//2)-0]
        out = (l+h)/2

    #print('median', out, values)
    return out 

def buffer_push_end(values : list, new, length):
    assert len(values) <= length
    # NOTE: mutates values
    if len(values) == length:
        values = values[1:]
    values.append(new)
    assert len(values) <= length
    return values


class StateMachine:

    SLEEP = 'sleep'
    IDLE = 'idle'
    BRUSHING = 'brushing'
    DONE = 'done'
    FAILED = 'failed'

    def __init__(self,
            time=0.0,
            prediction_filter_length=5,
        ):

        # config
        self.brushing_target_time = 120.0
        self.done_wait_time = 1.0
        self.idle_time_max = 5.0
        self.brushing_threshold = 0.6
        self.not_brushing_threshold = 0.4
        self.motion_threshold = 0.3
        self.prediction_filter_length = prediction_filter_length

        # state
        self.state = self.SLEEP
        self.state_enter_time = time
        self.last_time = time
        self.motion_history = [0.0] * self.prediction_filter_length
        self.brushing_history = [0.0] * self.prediction_filter_length
        self.brushing_time = 0.0 # how long active

        self._state_functions = {
            self.SLEEP: self.sleep_next,
            self.IDLE: self.idle_next,
            self.BRUSHING: self.brushing_next,
            self.DONE: self.done_next,
            self.FAILED: self.failed_next,
        }

    def _get_predictions(self):
        # return filtered predictions
        m = median(self.motion_history)
        b = median(self.brushing_history)
        return m, b

    def _update_predictions(self, motion, brushing):
        # update filter states
        l = self.prediction_filter_length
        self.motion_history = buffer_push_end(self.motion_history, motion, l)
        self.brushing_history = buffer_push_end(self.brushing_history, brushing, l)
        # return filter outputs
        return self._get_predictions()

    def next(self, time, motion, brushing):
        # Handle logic common to all states,
        # and then delegate to current state
        motion, brushing = self._update_predictions(motion, brushing)
        kwargs = dict(time=time, motion=motion, brushing=brushing)
        func = self._state_functions[self.state]
        next_state = func(**kwargs)
        if not next_state is None:
            print('transition', self.state, next_state)
            self.state = next_state
            self.state_enter_time = time
        self.last_time = time

    # State functions
    def sleep_next(self, motion, **kwargs):
        # reset accumulated time
        self.brushing_time = 0.0

        print('sleep-next', motion)

        if motion > self.motion_threshold:
            return self.IDLE

    def idle_next(self, time, brushing, **kwargs):
        is_brushing = brushing > self.brushing_threshold
        since_enter = time - self.state_enter_time

        print('idle-next', is_brushing, since_enter)

        if is_brushing:
            return self.BRUSHING

        if since_enter > self.idle_time_max:
            return self.FAILED

    def brushing_next(self, time, brushing, **kwargs):
        is_idle = brushing < self.not_brushing_threshold

        if is_idle:
            return self.IDLE
        else:
            # still brushing
            since_last = time - self.last_time
            self.brushing_time += since_last
            if self.brushing_time > self.brushing_target_time:
                return self.DONE

    def done_next(self, time, **kwargs):
        since_enter = time - self.state_enter_time
        if since_enter >= self.done_wait_time:
            return self.SLEEP

    def failed_next(self, time, **kwargs):
        since_enter = time - self.state_enter_time
        if since_enter >= self.fail_wait_time:
            return self.SLEEP


class Effects():

    def __init__(self):

        pass

    # DONE.
        # green LED.
        # buzzer happy tones
    # FAIL
        # buzzer sad tones
        # red LED
    # IDLE. 
        # no sound
        # no LED
    # BRUSHING. 
        # arpeggiated notes. Ascending on progress. Or even a little song ??

    # SLEEP. reduce wakeup time?

def run_scenario(sm, trace, default_dt = 0.1):

    capture_outputs = ['state', 'brushing_time']

    time = 0.0
    for row in trace:
        # inputs
        dt = row.get('dt', default_dt)
        time += dt
        mp = row['mp']
        if mp is None:
            mp = 0.5 # TODO: randomize

        # run
        inputs = dict(time=time, motion=mp, brushing=row['bp'])
        sm.next(**inputs)

        outputs = { o: getattr(sm, o) for o in capture_outputs }
        yield row, inputs, outputs

def check_expectations(row, outputs):

    # check expectations
    expect_state = row.pop('s')
    state = outputs['state']
    assert state == expect_state, (state, expect_state)

    expect_brushing_time = row.pop('bt', None)
    brushing_time = round(outputs['brushing_time'], 3)
    if expect_brushing_time is not None:
        e = round(expect_brushing_time, 3)
        assert brushing_time == e, (brushing_time, e)


def test_states_basic_happy():
    # check that we can reach the DONE/success state

    # make effect of median filter present but short
    sm = StateMachine(prediction_filter_length=3)
    sm.brushing_target_time = 2.0 # make it quick to hit target
    sm.done_wait_time = 1.0

    assert sm.state == sm.SLEEP

    LOW = 0.1
    HIGH = 0.8
    X = None # dont-care

    # expected outputs (s: sm.state), and inputs (everything else)
    trace = [
        dict(mp=LOW, bp=LOW, s=sm.SLEEP),
        dict(mp=LOW, bp=LOW, s=sm.SLEEP),
        # medial filter should reject short states
        dict(mp=HIGH, bp=LOW, s=sm.SLEEP),
        dict(mp=LOW, bp=LOW, s=sm.SLEEP),
        # longer case should transition
        #dict(mp=HIGH, bp=LOW, s=sm.SLEEP),
        dict(mp=HIGH, bp=LOW, s=sm.IDLE),
        # if not brushing, should stay idle
        dict(mp=X, bp=LOW, s=sm.IDLE),
        dict(mp=X, bp=LOW, s=sm.IDLE),
        dict(mp=X, bp=LOW, s=sm.IDLE),
        # if starting brushing, should count the time spent
        dict(mp=X, bp=HIGH, s=sm.IDLE),
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, bt=0.0),
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, bt=0.1),
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, bt=0.2),
        # if not brushing, should go to idle
        dict(mp=X, bp=LOW, s=sm.BRUSHING, bt=0.3),
        dict(mp=X, bp=LOW, s=sm.IDLE, bt=0.3),
        dict(mp=X, bp=LOW, s=sm.IDLE, bt=0.3),
        # if starting brushing again, should continue counting
        dict(mp=X, bp=HIGH, s=sm.IDLE),
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, bt=0.3),
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, bt=0.4),
        # if brushing for long enough, will eventually get done
        dict(mp=X, bp=HIGH, s=sm.BRUSHING, dt=1.0, bt=1.4),
        dict(mp=X, bp=HIGH, s=sm.DONE, dt=1.0, bt=2.4),
        # done will automatically transition to sleep
        dict(mp=X, bp=HIGH, s=sm.DONE, dt=0.5),
        dict(mp=X, bp=HIGH, s=sm.SLEEP, dt=0.6),
    ]

    gen = run_scenario(sm, trace)
    for row, inputs, outputs in gen:
        print('next-ran', inputs, outputs, row)
        check_expectations(row, outputs)

def test_states_basic_sad():
    # check that we can reach FAIL state

    # make effect of median filter present but short
    sm = StateMachine(prediction_filter_length=3)
    sm.brushing_target_time = 2.0 # make it quick to hit target
    sm.done_wait_time = 1.0

    assert sm.state == sm.SLEEP

    LOW = 0.1
    HIGH = 0.8
    X = None # dont-care

    # expected outputs (s: sm.state), and inputs (everything else)
    trace = [
    ]

    gen = run_scenario(sm, trace)
    for row, inputs, outputs in gen:
        print('next-ran', inputs, outputs)
        check_expectations(row, outputs)


def main():
    test_states_basic_happy()
    test_states_basic_sad()

if __name__ == '__main__':
    main()
