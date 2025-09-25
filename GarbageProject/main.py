import Controller
import cv2
import time
from collections import deque


def main():
    c = Controller.Controller()
    target_hz = 40
    time_per_loop = 1 / target_hz

    frame_times = deque(maxlen=30)
    avg_hz = target_hz

    while True:
        start_time = time.time()

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        if key == ord("g"):
            c.toggle_grayscale()
        if key == ord(" "):
            cv2.waitKey()
        if key == ord("u"):
            c.toggle_ui()
        if key == ord("l"):
            c.toggle_ui_labels()
        if key == ord("c"):
            c.toggle_ui_colors()


        image = c.get_image()
        marked_image = c.mark_image(image, avg_hz)
        c.display_image(marked_image)


        # sleep if faster than target_hz
        time_passed = time.time() - start_time
        if time_passed < time_per_loop:
            time.sleep(time_per_loop - time_passed)

        # calculate actual fps for displaying
        time_passed = time.time() - start_time
        frame_times.append(time_passed)
        avg_hz = round( 1 / (sum(frame_times) / len(frame_times)) , 1)





if __name__ == '__main__':
    main()