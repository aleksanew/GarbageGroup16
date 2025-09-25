import cv2
import Camera, Ui

class Controller:

    def __init__(self):
        self.cam = Camera.Camera()
        self.ui = Ui.Ui()
        self.grayscale = False
        self.display_labels = True
        self.display_colors = True


    def get_image(self):
        return self.cam.capture_frame(self.grayscale)

    # returns bgr image independent of input image
    def mark_image(self, image, hz):
        img = image.copy()

        # ----------------------------------------------------
        # preprocessing, edge detection and AI functions should
        # be called inside this function
        # ----------------------------------------------------
        if self.grayscale:
            process_grayscale_image = 0
            identify_grayscale_image = 0
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) # convert back to color for markings
        else:
            process_color_image = 0
            identify_color_image = 0

        # ----------------------------------------------------
        # could just pass grayscale variable to process and identify functions
        # if implementation is similar for color and grayscale (uses same function)
        # instead of if-test here
        # ----------------------------------------------------

        TrashPiece = 0 # bounds and type
        return self.ui.apply_ui_overlay(img, TrashPiece, self.display_labels, self.display_colors, hz)


    def display_image(self, image):
        cv2.imshow("Output", image)


    def toggle_ui(self):
        self.display_labels = not self.display_colors
        self.display_colors = not self.display_colors

    def toggle_ui_labels(self):
        self.display_labels = not self.display_labels

    def toggle_ui_colors(self):
        self.display_colors = not self.display_colors

    def set_grayscale(self, grayscale):
        self.grayscale = grayscale

    def toggle_grayscale(self):
        self.grayscale = not self.grayscale
