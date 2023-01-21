import cv2

from .utilities import Utilities


class Handler:
    CAMERA_INDEX = 0
    ESCAPE_KEY = 27

    def __init__(self):
        self._utilities = Utilities()
        self._classifier = None
        self._capturer = None

    def run(self):
        # download haarcascade_xml if necessary
        if not self._utilities.exists_haarcascade_xml():
            self._utilities.download_haarcascade_xml()

        self._classifier = self._create_classifier()
        self._capturer = self._create_capturer()

        self._get_frames()

    def _create_classifier(self):
        path = self._utilities.haarcascade_xml_path.as_posix()
        return cv2.CascadeClassifier(path)

    def _create_capturer(self):
        self.cap = cv2.VideoCapture(self.CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

    def _get_frames(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                self._release_capture_handler()
                break

            faces = self._detect_faces(frame)
            self._mark_faces(faces, frame)

            cv2.imshow("frame", frame)

            key_pressed = self._wait_user_input()
            if self._is_escape_key(key_pressed):
                self._release_capture_handler()
                break

    def _release_capture_handler(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def _wait_user_input(self):
        return cv2.waitKey(1) & 0xFF

    def _is_escape_key(self, key):
        return key == self.ESCAPE_KEY

    def _detect_faces(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return self._classifier.detectMultiScale(
            rgb,
            scaleFactor=1.3,
            minNeighbors=5
        )

    def _mark_faces(self, faces, frame):
        color = 0, 255, 255  # in BGR
        stroke = 5

        for x, y, w, h in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                stroke
            )
