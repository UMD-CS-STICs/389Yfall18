import numpy as np
import cv2


def extract_lanes(img):
    ''' This method extracts the lane pixels from the image.
    The result should be a binary image where white pixels corresponds to lane pixels.'''
    # TODO: your code here
    # This color conversion is just here as an example
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def fit_lanes(img):
    ''' This method takes as input the result of extract_lanes and produces two
    polynomial models'''
    # TODO: your polynomial model code here
    # These are just here as an example
    poly_left = [1.28526510e-05, -1.56755218e-02,  6.06658643e+00, -4.32990741e+02]
    poly_right = [-1.16718928e-02,  7.93217666e+00, -7.12537601e+02]
    return poly_left, poly_right


def draw_lanes(poly1, poly2, y, img):
    '''
    Draws two lane lines on the road defined by polynomials 1 and 2.
    The polynomials should be passed as an array. For example if the left
    lane was described by the polynomial 1 + 2x + 3x^2 you would pass
    the array [1, 2, 3]. Y is the domain the polynomials are defined over
    and img is the image that the lanes will by drawn on.
    '''
    poly1 = np.poly1d(poly1)
    poly2 = np.poly1d(poly2)
    lanes = np.zeros(img.shape)

    x = poly1(y)
    mask = np.bitwise_and(x >= 0, x < img.shape[1]-1)
    y_safe = (y[mask] + 0.5).astype(int)
    x_safe = (x[mask] + 0.5).astype(int)
    lanes[y_safe,x_safe] = 255
    points = np.vstack((x_safe[::20], y_safe[::20]))
    last = np.array([x_safe[-1], y_safe[-1]]).reshape(2, 1)
    lane_points = np.hstack((points, last))

    x = poly2(y)
    mask = np.bitwise_and(x >= 0, x < img.shape[1]-1)
    y_safe = (y[mask] + 0.5).astype(int)
    x_safe = (x[mask] + 0.5).astype(int)
    lanes[y_safe,x_safe] = 255
    points = np.vstack((x_safe[::20], y_safe[::20]))
    points = np.fliplr(points)
    last = np.array([x_safe[-1], y_safe[-1]]).reshape(2, 1)
    lane_points = np.hstack((lane_points, last, points))

    lane_points = lane_points.T

    lanes = cv2.dilate(lanes, np.ones((5,5), np.uint8), iterations=1)
    points = np.argwhere(lanes == 255)
    img[points[:,0],points[:,1]] = (0, 0, 255)

    overlay = np.copy(img)

    cv2.fillConvexPoly(overlay, np.int32(lane_points), (0, 255, 0))
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, img, 1-alpha, 0, img)
    return img


def video_loop():
    cap = cv2.VideoCapture('car.mp4')

    while(cap.isOpened()):
        # get the next frame from the video
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # apply your pipeline to get the lane pixels
        lane_pixels = extract_lanes(frame)

        # fit your model to the lane pixels
        model1, model2 = fit_lanes(lane_pixels)

        # draw your model on the original frame
        y = np.arange(frame.shape[0]/2, frame.shape[0])
        result = draw_lanes(model1, model2, y, np.copy(frame))

        # put all three images in a grid
        output = np.zeros((480*2, 640*2, 3), dtype='uint8')
        output[:480,:640] = frame
        output[:480,640:, 0] = lane_pixels
        output[:480,640:, 1] = lane_pixels
        output[:480,640:, 2] = lane_pixels
        output[480:,:640] = result

        # draw the car's position to the screen
        car_position = 0
        cv2.putText(output, "Car Position: {}".format(car_position), (640, 480), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_4)

        cv2.imshow('frame', output)
        if cv2.waitKey(28) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_loop()
