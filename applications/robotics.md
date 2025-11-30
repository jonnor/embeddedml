
# Factor graphs

Used both for perception (such as localization) and motion.

Outer part might be non-linear, but
inner part requires linear algebra solver. 
Bucket elimination / QR factorization.
Factor graphs are typically sparse, and this sparsity can be exploited during inference.

Factor graphs are form of graphical models.
Relates to Baysian Nets and Markov Networks. Both can be converted / seen as factor graphs.

MIT Robotics - Frank Dellaert - Factor Graphs for Perception and Action
https://www.youtube.com/watch?v=-yCC7mpgL4w

GTSAM, open-source library that supports factor graphs and more.
https://github.com/borglab/gtsam

One can solve particular factor graphs over time,
either forward or backward, to get Djistra style search.
Or to use linear quadratic regulators LQR over it.


# Actuation

Brushless motors with encoders are.
SimpleFOC makes this quite accessible.
Can wrap


# Perception

Lidar has become quite affordable and compact.
LD06 around 50 USD.
Has serial output, at 5-13 hz, nominally 10 Hz.
Up to 12 meter measuring radius.
1 degree angular resolution.
Around 1 watt. 5V, 180 mA.
Operates at 230400 baud, so max 25 kB/s data rate.
In practice get 10x 360 angular measurements, each 3 bytes.
So around 2 kB/s.

# Open source projects

- Ardupilot / ArduRover etc
- ROS / microROS


# Path planning

Assuming we have a map of the environment already, we can jump straight to path planning, and can do global path planning.

Local planning is often needed for obstacle avoidance.

### RRT* (Rapidly-exploring Random Tree Star)

RTT first proposed in 1998 by LaValle.
RTT* was introduced in 2011 by Karaman and Frazzoli.
Widely used in robotics.

Builds a graph using random nodes.
The star version refines this graph by considering shortest path. 
Can be done anytime, returning first a pretty bad solution, that can later be refined.
Can use bounded memory. By removing either non-promising nodes, or just at random.
Large number of variations proposed in literature.

# Localization

Localization is the problem of finding where the robot is in the environment,
based on what it can observe.
There can be many ambiguities in this, and uncertanty due to.
Need to integrate observations over time.

Particle filters are a key component.
Attempts many different poses, computes likelyhood to keep the best estimates. Hopefully converging on a single location over time.
Extended Kalman filters also used.


