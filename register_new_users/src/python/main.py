import os
from pathlib import Path
import uuid

import cv2


class Register:
    CAMERA_INDEX = 0
    ESCAPE_KEY = 27
    SAVE_KEY = "s"

    def __init__(self):
        # paths
        self.base_dir = Path(__file__).resolve().parent
        self.files_dir = self.base_dir / "files"
        self.output_dir = self.files_dir / "output"

        # capture handler
        self.cap = None

        # subject
        self.name = None

    def run(self):
        self._get_name()
        self._create_capture_handler()
        self._get_frames()

    def _get_name(self):
        self.name = input("What's your name?: ")

        if not self.name:
            raise ValueError("Invalid name")

    @property
    def _file_base_dir(self):
        name = self.name.lower().replace(" ", "_")
        return self.output_dir / name

    def stop(self):
        self._release_capture_handler()

    def _create_capture_handler(self):
        self.cap = cv2.VideoCapture(self.CAMERA_INDEX)

        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

    def _get_frames(self):
        while True:
            # get frame
            ret, frame = self.cap.read()

            if not ret:
                self.stop()
                break

            # show the frame
            cv2.imshow("frame", frame)

            # wait a second for user to press any key
            print("Press ESCAPE to exit")
            pressed_key = self._wait_user_input()

            # exit
            if self._is_escape_key(pressed_key):
                self.stop()
                break

            # save frame
            if self._is_save_key(pressed_key):
                self._save_frame(frame)

    def _release_capture_handler(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def _wait_user_input(self):
        return cv2.waitKey(1) & 0xFF

    def _is_escape_key(self, key):
        return key == self.ESCAPE_KEY

    def _is_save_key(self, key):
        return key == ord(self.SAVE_KEY)

    @property
    def _output_file_path(self):
        return self._file_base_dir / f"{uuid.uuid4().hex}.jpg"

    def _save_frame(self, frame):
        os.makedirs(self._file_base_dir, exist_ok=True)
        path = self._output_file_path
        cv2.imwrite(path.as_posix(), frame)
        print(f"Frame {path} saved")


def main():
    handler = Register()
    handler.run()


if __name__ == "__main__":
    main()
