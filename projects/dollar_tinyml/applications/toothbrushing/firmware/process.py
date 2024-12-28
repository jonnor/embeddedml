
import array

class GravitySplitter():

    def __init__(self, samplerate, lowpass_cutoff=0.5):

        rc = 1.0/(2*3.14*lowpass_cutoff)
        dt = 1.0/samplerate
        self.lowpass_alpha = rc / (rc + dt)

        self.gravity = None
        self.motion = array.array('f', [0, 0, 0])

    def process(self, xyz):
        assert len(xyz) == 3, xyz

        if self.gravity is None:
            # jump straigth to it, to avoid slow ramp-in
            self.gravity = array.array('f', xyz)
        
        a = self.lowpass_alpha
        for i in range(len(xyz)):
            self.gravity[i] = (a * self.gravity[i]) + ((1.0 - a) * xyz[i])
            self.motion[i] = xyz[i] - self.gravity[i]


