from io import BytesIO

from PIL import Image

import App


class DummyUpload:
    def __init__(self, payload: bytes, mime_type: str = "image/png"):
        self._payload = payload
        self.type = mime_type

    def getvalue(self):
        return self._payload


def make_png_bytes() -> bytes:
    img = Image.new("RGB", (8, 8), color="blue")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def test_input_image_setup_valid_image(monkeypatch):
    upload = DummyUpload(make_png_bytes())
    parts = App.input_image_setup(upload)
    assert isinstance(parts, list)
    assert parts[0]["mime_type"] == "image/png"
    assert isinstance(parts[0]["data"], bytes)


def test_input_image_setup_invalid_image(monkeypatch):
    called = {"value": False}

    def fake_error(message):
        called["value"] = "not a valid image" in message

    monkeypatch.setattr(App.st, "error", fake_error)
    upload = DummyUpload(b"not-an-image", "image/png")
    assert App.input_image_setup(upload) is None
    assert called["value"] is True


def test_input_image_setup_missing_file():
    try:
        App.input_image_setup(None)
        raised = False
    except FileNotFoundError:
        raised = True
    assert raised is True
