import cv2

class Ui:

    def __init__(self):
        a=0

    def _add_text(self, image, type):

        text = type #should be enum
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.5
        thickness = 1
        text_color = (255, 255, 255)
        bg_color = (30, 30, 30)
        border_color = (50, 50, 50)
        border_thickness = 3

        (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)

        # in place of actual positions
        x = (image.shape[1] - text_width) // 2
        y = (image.shape[0] + text_height) // 2

        top_left = (x - 3, y - text_height - 3)
        bottom_right = (x + text_width + 3, y + 3)

        cv2.rectangle(image, top_left, bottom_right, border_color, thickness=border_thickness)
        cv2.rectangle(image, top_left, bottom_right, bg_color, thickness=cv2.FILLED)
        cv2.putText(image, text, (x, y), font, scale, text_color, thickness, cv2.LINE_AA)

        return image

    def _add_color(self, image, type):

        # make color change based on type
        bg_color = (0, 0, 255)
        border_color = (0, 0, 100)
        border_thickness = 3
        alpha = 0.3

        # in place of actual positions
        x = (image.shape[1]) // 2
        y = (image.shape[0]) // 2
        height = 300
        width = 300

        top_left = (x - 3 - width//2, y - 3 - height//2)
        bottom_right = (x + 3 + width//2, y + 3 + height//2)

        overlay = image.copy()

        cv2.rectangle(overlay, top_left, bottom_right, border_color, thickness=border_thickness)
        cv2.rectangle(overlay, top_left, bottom_right, bg_color, thickness=cv2.FILLED)

        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)


        return image

    def _add_hz(self, image, hz):
        text = str(hz) +"fps"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.3
        thickness = 1
        text_color = (255, 255, 255)
        bg_color = (30, 30, 30)
        border_color = (50, 50, 50)
        border_thickness = 3

        (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)

        x = (image.shape[1] - text_width - 3)
        y = (text_height + 3)

        top_left = (x - 3, y - text_height - 3)
        bottom_right = (x + text_width + 3, y + 3)

        cv2.rectangle(image, top_left, bottom_right, border_color, thickness=border_thickness)
        cv2.rectangle(image, top_left, bottom_right, bg_color, thickness=cv2.FILLED)
        cv2.putText(image, text, (x, y), font, scale, text_color, thickness, cv2.LINE_AA)

        return image


    def apply_ui_overlay(self, image, TrashPiece, display_labels, display_colors, hz):
        img = image.copy()

        if display_colors:
            img = self._add_color(img, "Garbage")
        if display_labels:
            img = self._add_text(img, "Garbage")

        img = self._add_hz(img, hz)
        return img