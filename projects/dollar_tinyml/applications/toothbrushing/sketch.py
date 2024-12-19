
def median(values):
    L = len(values)
    if L == 0:
        raise ValueError('Input empty')
    if L == 1:
        return values[0]

    ordered = sorted(values)
    is_odd = L % 2
    if is_odd:
        return ordered[L//2]
    else:
        l = ordered[L//2]
        h = ordered[(L//2)+1]
        return (l+h)/2

class StateMachine:

    SLEEP = 'SLEEP'
    IDLE = 'idle'
    BRUSHING = 'brushing'
    DONE = 'done'

    def __init__(self,
            time=0.0,
        ):

        # state
        self.state = self.SLEEP
        self.state_enter_time = time
        self.last_time = time

        # config
        self.brushing_target_time = 120.0
        self.done_wait_time = 1.0
        self.brushing_threshold = 0.6
        self.not_brushing_threshold = 0.4
        self.motion_threshold = 0.3
        self.prediction_filter_length = 5

        self._state_functions = {
            self.SLEEP: sleep_next,
            self.IDLE: idle_next,
            self.BRUSHING: brushing_next,
            self.DONE: done_next,
        }
        self._reset()

    def _reset(self):
        self.prediction_histories = {
            'motion': [],
            'brushing': [],
        }
        self.brushing_time = 0.0 # how long active

    def _update_predictions(self, predictions):
        # FIXME: fix this logic
        # roll data out if full
        # push latest data in
        self.prediction_history
        history = self.prediction_histories[input]
        m = median(history)

        return m

    def next(self, time, predictions):
        # Handle logic common to all states,
        # and then delegate to current state
        predictions = self._update_predictions(predictions)
        func = self._state_function[self.state]
        next_state = func(time, predictions)
        if next is not None:
            self.state = next_state
            self.state_enter_time
        self.last_time = time
        return

    # State functions
    def sleep_next(self, time, predictions):
        self.reset()
        prediction = predictions[1]
        if prediction > self.motion_threshold:
            return self.IDLE

    def idle_next(self, time, predictions):
        prediction = predictions[0]
        is_brushing = prediction > self.brushing_threshold
        if is_brushing:
            return self.BRUSHING

    def brushing_next(self, time, predictions):
        prediction = predictions[0]
        is_idle = prediction < self.not_brushing_threshold

        if is_idle:
            return self.IDLE

        since_last = time - self.last_time
        self.brushing_time += since_last
        if self.brushing_time > self.brushing_time_target:
            return self.DONE

    def done_next(self, time, predictions):
        since_enter = time - self.state_enter_time
        if since_last >= self.done_wait_time:
            return self.SLEEP

    def failed_next(self, time, predictions):
        since_last = time - self.state_enter_time
        if since_last >= self.fail_wait_time:
            return self.SLEEP


class Effects():

    def __init__(self):

        pass

    # DONE. green LED. buzzer happy sound?
    # SLEEP. reduce wakeup time
    # IDLE. yellow LED??
    # BRUSHING. Nothing??

def test_states_basics():

    sm = StateMachine()
    sm.prediction_filter_length = 3
    assert sm.state == sm.SLEEP

    MOTION_LOW = 0.1
    MOTION_HIGH = 0.8
    BRUSHING_LOW = 0.3
    BRUSHING_HIGH = 0.8

    # expected outputs (s: sm.state), and inputs (everything else)
    trace = [
        dict(mp=MOTION_LOW, bp=BRUSHING_LOW, s=sm.SLEEP),
        # medial filter should reject short states
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.SLEEP),
        dict(mp=MOTION_LOW, bp=BRUSHING_LOW, s=sm.SLEEP),
        # longer case should transition
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.SLEEP),
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.IDLE),
        # if not brushing, should stay idle
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.IDLE),
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.IDLE),
        dict(mp=MOTION_HIGH, bp=BRUSHING_LOW, s=sm.IDLE),

        # if starting brushing, should could the time spent
        dict(mp=MOTION_HIGH, bp=BRUSHING_HIGH, s=sm.IDLE),
        dict(mp=MOTION_HIGH, bp=BRUSHING_HIGH, s=sm.BRUSHING),
        dict(mp=MOTION_HIGH, bp=BRUSHING_HIGH, s=sm.BRUSHING, bt=0.2),
        dict(mp=MOTION_HIGH, bp=BRUSHING_HIGH, s=sm.BRUSHING, bt=0.3),
    ]

    default_dt = 0.1
    time = sm.time
    for row in trace:
        expect_state = row.pop('s')
        expect_brushing_time = row.pop('bt', None)

        dt = row.get('dt', default_dt)
        time += dt
        predictions = (row['mp'], row['bp'])
        sm.next(time, predictions)

        assert sm.state == expect_state, (sm.state, expect_state)

        if expect_brushing_time is not None:
            assert sm.brushing_time == expect_brushing_time, (sm.brushing_time, expect_brushing_time)

def main():

    test_states_basics()

if __name__ == '__main__':
    main()
