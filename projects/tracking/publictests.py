import sys
sys.path.append('./')
from kalmanfilter import *


def test_matrices1():
    test = np.dot(A, B)
    correct = np.array([[0.00166667, 0],
                        [0.,         0.00166667],
                        [0.03333333, 0.],
                        [0.,        0.03333333]])
    np.testing.assert_allclose(test, correct, rtol=1e-5)


def test_matrices2():
    test = np.dot(C, A)
    correct = np.array([[1.,         0.,         0.03333333, 0.],
                        [0.,         1.,         0.,         0.03333333]])
    np.testing.assert_allclose(test, correct, rtol=1e-5)


def test_matrices3():
    test = np.dot(C, B)
    correct = np.array([[0.00055556, 0.],
                        [0.,        0.00055556]])
    np.testing.assert_allclose(test, correct, rtol=1e-5)


def test_prediction():
    kf = KalmanFilter()
    kf.states = {1: np.array([[1.3], [2.1], [3.5], [0.3]]),
                 2: np.array([[2.3], [21.1], [-3.2], [-2.3]]),
                 3: np.array([[4.2], [3.1], [-4.5], [9.2]])}
    kf.covariances = {
        1: np.array([
            [2., 0, 0.32, 0],
            [0, 3., 0.66, 0],
            [0.32, 0.66, 4., 0],
            [0, 0, 0, 5.]]),
        2: np.array([
            [4., 0, 0.32, 5],
            [0, 3., 0.66, 0],
            [0.32, 0.66, 4., 0.5],
            [5, 0, 0.5, 5.]]),
        3: np.array([
            [2., 0, 0.32, 2],
            [0, 4., 0.66, 0],
            [0.32, 0.66, 4., 1],
            [2, 0, 1, 5.]])}
    kf.prediction(np.array([[1.2], [-0.4]]))
    correct_states = {1: np.array([[1.416],
                                   [2.11022222],
                                   [3.46],
                                   [0.31333333]]),
                      2: np.array([[2.19266667],
                                   [21.02355556],
                                   [-3.24],
                                   [-2.28666667]]),
                      3: np.array([[4.04933333],
                                   [3.40688889],
                                   [-4.54],
                                   [9.21333333]])}
    correct_covariances = {1: np.array([[4.02577778,  0.022,  0.45333333,  0.],
                                        [0.022,  5.00555556,  0.66,  0.16666667],
                                        [0.45333333,  0.66,  5.,  0.],
                                        [0.,  0.16666667,  0.,  6.]]),
                           2: np.array([[6.02577778,  0.18922222,  0.45333333,  5.01666667],
                                        [0.18922222,  5.00555556,
                                         0.67666667,  0.16666667],
                                        [0.45333333,
                                         0.67666667,  5.,  0.5],
                                        [5.01666667,  0.16666667,  0.5,  6.]]),
                           3: np.array([[4.02577778,  0.08977778,  0.45333333,  2.03333333],
                                        [0.08977778,  6.00555556,
                                         0.69333333,  0.16666667],
                                        [0.45333333,  0.69333333,  5.,  1.],
                                        [2.03333333,  0.16666667,  1.,  6.]])}
    for i in range(1, 4):
        np.testing.assert_allclose(kf.states[i], correct_states[i], rtol=1e-5)
        np.testing.assert_allclose(
            kf.covariances[i], correct_covariances[i], rtol=1e-5)


def test_measurement():
    kf = KalmanFilter()
    Q = np.array([[50.2, 0.],
                  [0, 50.2]])
    kf.states = {1: np.array([[1.3], [2.1], [3.5], [0.3]]),
                 2: np.array([[2.3], [21.1], [-3.2], [-2.3]]),
                 3: np.array([[4.2], [3.1], [-4.5], [9.2]])}
    kf.covariances = {
        1: np.array([
            [2., 0, 0.32, 0],
            [0, 3., 0.66, 0],
            [0.32, 0.66, 4., 0],
            [0, 0, 0, 5.]]),
        2: np.array([
            [4., 0, 0.32, 5],
            [0, 3., 0.66, 0],
            [0.32, 0.66, 4., 0.5],
            [5, 0, 0.5, 5.]]),
        3: np.array([
            [2., 0, 0.32, 2],
            [0, 4., 0.66, 0],
            [0.32, 0.66, 4., 1],
            [2, 0, 1, 5.]])}

    measurements = {1: np.array([[1], [2]]),
                    2: np.array([[1.4], [15.5]]),
                    4: np.array([[1.4], [15.5]])}
    kf.measurement(measurements, Q)
    correct_states = {1: np.array([[1.28850575],
                                   [2.0943609],
                                   [3.49692032],
                                   [0.3]]),
                      2: np.array([[2.23357934],
                                   [20.78421053],
                                   [-3.27478734],
                                   [-2.38302583]]),
                      4: np.array([[1.4],
                                   [15.5],
                                   [0.],
                                   [0.]])
                      }
    correct_covariances = {
        1: np.array([[1.92337165, 0., 0.30773946, 0.],
                     [0., 2.83082707, 0.62278195, 0.],
                     [0.30773946, 0.62278195, 3.98985034, 0.],
                     [0., 0., 0., 5.]]),
        2: np.array([[3.70479705, 0., 0.29638376, 4.63099631],
                     [0., 2.83082707, 0.62278195, 0.],
                     [0.29638376, 0.62278195, 3.98992273, 0.4704797],
                     [4.63099631, 0., 0.4704797, 4.53874539]]),
        4: np.array([[5.02e+01, 0.00e+00, 0.00e+00, 0.00e+00],
                     [0.00e+00, 5.02e+01, 0.00e+00, 0.00e+00],
                     [0.00e+00, 0.00e+00, 1.00e+05, 0.00e+00],
                     [0.00e+00, 0.00e+00, 0.00e+00, 1.00e+05]])}
    for i in range(1, 5):
        if i == 3:
            if i in kf.states or i in kf.covariances:
                raise KeyError('You did not delete keys.')
        else:
            np.testing.assert_allclose(
                kf.states[i], correct_states[i], rtol=1e-5)
            np.testing.assert_allclose(
                kf.covariances[i], correct_covariances[i], rtol=1e-5)


if __name__ == '__main__':
    test_matrices1()
    test_matrices2()
    test_matrices3()
    test_prediction()
    test_measurement()
    print ('All Tests Pass!')
