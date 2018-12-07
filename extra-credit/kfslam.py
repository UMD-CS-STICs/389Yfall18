import numpy as np


class KFSlam(object):
    '''Your implementation of a Histogram Filter'''

    def __init__(self, robot):
        self.landmark_id_to_index = {}
        self.covariances = np.array([[0, 0], [0, 0]])
        self.states = np.array([[robot.x], [robot.y]])
        self.x_noise = robot.x_noise
        self.y_noise = robot.y_noise

    def A(self):
        return np.identity(self.states.shape[0])

    def B(self):
        n = self.states.shape[0]
        b = np.zeros((n, 2))
        b[0, 0], b[1, 1] = 1, 1
        return b

    def R(self, control_signal):
        n = self.states.shape[0] - 2
        result = np.diag(np.hstack(([self.x_noise,self.y_noise], np.zeros(n))))
        result[0,0] *= abs(control_signal[0,0])
        result[1,1] *= abs(control_signal[1,0])
        return result

    def I(self):
        return self.A()

    # control signal contains your change in odom as a 2x1 vector
    def prediction(self, control_signal):
        self.states = np.dot(self.A(), self.states) + \
            np.dot(self.B(), control_signal)
        self.covariances = self.covariances + self.R(control_signal)

    def measurement(self, measurements, Q):
        for measurement in measurements:
            landmark_id = list(measurement.keys())[0]
            dx, dy = measurement[landmark_id][0], measurement[landmark_id][1]
            if landmark_id not in self.landmark_id_to_index:
                original_dim = self.states.shape[0]
                self.landmark_id_to_index[landmark_id] = original_dim
                addition = np.array(
                    [[self.states[0, 0] + dx], [self.states[1, 0] + dy]])
                self.states = np.concatenate((self.states, addition))
                self.covariances = np.append(
                    self.covariances, np.zeros((2, original_dim)), 0)
                self.covariances = np.append(
                    self.covariances, np.zeros((original_dim + 2, 2)), 1)
                self.covariances[original_dim, original_dim] = 500
                self.covariances[original_dim + 1, original_dim + 1] = 500
                # import pdb;pdb.set_trace()

        for measurement in measurements:
            landmark_id = list(measurement.keys())[0]
            index = self.landmark_id_to_index[landmark_id]
            C = np.zeros((2, self.states.shape[0]))
            C[0, 0], C[1, 1] = -1, -1
            C[0, index], C[1, index + 1] = 1, 1
            K1 = np.dot(self.covariances, np.transpose(C))
            K2 = np.linalg.inv(np.dot(C, np.dot(self.covariances, C.T)) + Q)
            kalman_gain = np.dot(K1, K2)
            k_m = np.array([[measurement[landmark_id][0]], [measurement[
                           landmark_id][1]]]) - np.dot(C, self.states)
            self.states = self.states + np.dot(kalman_gain, k_m)
            self.covariances = np.dot(
                self.I() - np.dot(kalman_gain, C), self.covariances)
