from pathlib import Path
import urllib.request


class Utilities:
    def download_haarcascade_xml(self):
        print("Downloading haarcascade_frontalface_default.xml")
        urllib.request.urlretrieve(
            self.haarcascade_xml_url,
            self.haarcascade_xml_path
        )

    def exists_haarcascade_xml(self):
        return self.haarcascade_xml_path.is_file()

    @property
    def temporal_folder(self):
        base_dir = Path(__file__).resolve().parent.parent
        return base_dir / "files" / "temporal"

    @property
    def haarcascade_xml_path(self):
        return self.temporal_folder / "haarcascade_frontalface_default.xml"

    @property
    def haarcascade_xml_url(self):
        base_url = "https://raw.githubusercontent.com/opencv/opencv"
        path = "data/haarcascades/haarcascade_frontalface_default.xml"
        return f"{base_url}/master/{path}"
