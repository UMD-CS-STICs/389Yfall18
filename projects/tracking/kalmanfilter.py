import numpy as np

DT = 1. / 30

# STEP 1: Setting Up Matrices
# Just as we did in the codelab, we need to set up our matrices to perform updates later.
# Peek in the __init__ method below to see what our state vector is, and then fill out A,
# or our state update function. Keep in mind that these matrixes will depend on DT, the amount
# of time between kalman filter updates

A = np.array([[]])

# Next, we need to fill out B, or the control signal update. In our case, you can assume
# that our control signal will be a 2x1 matrix with acceleration in the x and y directions.
# Given our state vectors (if you forget what this looks like, check the __init__ method),
# what would this matrix look like? (Hint: How does acceleration affect velocity and position?
# These kinematics equations may be useful: v' = v + a*dt and p' = p + 0.5 * a * dt^2)

B = np.array([[]])

# Now, let's fill out C. This matrix needs to convert an arbitrary state vector into the
# expected measurement. In this case, we want to sense position in x and y as a 2x1 vector.
# Given our state vectors, wohat would this look like?

C = np.array([])

# We will give you R and I. Don't worry about these. Q will be passed into
# the measurement update.

R = np.array([
    [2, 0, 0, 0],
    [0, 2, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

I = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])


class KalmanFilter(object):
    '''Your implementation of a Histogram Filter'''

    def __init__(self):
        # Since we are trying to avoid multuple pedestrians, we will track multiple states and
        # covariances using hashes. Each pedestrian will have a unique id (this solves the
        # correspondence - not corresponDANCE - problem for you). The state vector per pedestrian
        # looks like the following:
        # [[pos_x],
        #  [pos_y],
        #  [vel_x],
        #  [vel_y]]
        # So, each state is a 4x1 vector, and each covariance matrix is 4x4. Remember, our car is
        # moving to the right with a certain (positive velocity), and the pos_x, pos_y, etc. in the
        # state is relative to that car. This would mean that a pedestrian who could run as fast as
        # the car alongside it would have a velocity (x) of 0.
        self.covariances = {}
        self.states = {}

    # Step 2: Prediction Update
    def prediction(self, control_signal):
        # In the preduction update, the only additional value we need to compute is the control signal
        # of the pedestrians. Above, we have given you information on how the car's velocity changes.
        # From this, you need to compute the acceleration of the pedestrian relative to the car.
        # control_signal is a 2x1 vector in the form:
        # [[x_accel],
        #  [y_accel]]

        # Now, we must iterate across all of our current pedestrians and update their states/covariances!
        # Resave the states and covariances using the pedestrian_id as the key.
        for p_id in self.states:
            # TODO: Update states and covariances! Hint: np.dot(mat1, mat2) will multiple two matrices, and
            # np.transpose(m) will give you the transpose of the matrix.
            pass

    # STEP 3: Measurement Update
    def measurement(self, measurements, Q):
        # measurements is a hash where the keys are pedestrians' ids and the values are observed an array
        # that looks like [pos_x, pos_y]. Q is the covariance matrix representing the uncertainty of the sensor.
        #
        # Keep in mind that pedestrians will be visible for a little, and then go off the screen. This means
        # that we will save the state of pedestrian #13, for example, for some time, and then simply stop
        # sensing her. When this happens, you should remove her state and covariance matrix from the hash.
        # You know this happens because your measurements hash will not contain a key of 13 even though your
        # current states and covariances hashes do. There are multiple ways of handling this - it is up to you!
        #
        # When you are iterating through your measurements hash, there are two cases:
        # 1) This ID is already present in the states and covariances hashes
        #       This means that you have already been tracking this person! In this case, just perform the updates
        #       as we did in the codelab. Remember that in measurements, the values are matrixes of size 2x1, and
        #       contain values [[pos_x], [pos_y]].
        # 2) The ID is not already present in your states and covariances matrix
        #        This means that this is the first time we are observing this pedestrian. When this happens, we need
        #        to create an initial state and covariance. Please set your initial state vectors to use the measurement
        #        as the pos_x, and pos_y. Use 0 for both the vel_x and vel_y. Set your initial covariance matrix to:
        #        [[x, 0,   0, 0],
        #         [0, y,   0, 0],
        #         [0, 0, 1e5, 0],
        #         [0, 0,    , 1e5]]
        #        where x is the the variance of the measurement in the x direction and y is the variance of
        #        the measurement in the y direction. Both of these values are in the Q matrix.
        new_states = {}
        new_covariances = {}
        for id_pedestrian in measurements:
            measurement = measurements[id_pedestrian]

        self.states = new_states
        self.covariances = new_covariances
