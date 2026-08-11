import contextlib
import http.server
import threading
import unittest
import urllib.request

from scripts.pilot10_package_contract import ROOT
from scripts.validate_pilot10_prototype import PROTOTYPE, validate


class Pilot10PrototypeTests(unittest.TestCase):
    def test_static_contract_passes(self):
        self.assertEqual([], validate())

    def test_repository_root_http_route_serves_interface_and_release(self):
        handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(
            *args, directory=ROOT, **kwargs
        )
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"
            with contextlib.closing(urllib.request.urlopen(f"{base}/prototype/first-ten/")) as response:
                html = response.read().decode("utf-8")
            with contextlib.closing(urllib.request.urlopen(f"{base}/data/reviewed/a1-first-10-lessons-pilot-v1.json")) as response:
                release = response.read().decode("utf-8")
            with contextlib.closing(urllib.request.urlopen(f"{base}/prototype/first-ten/observer.html")) as response:
                observer = response.read().decode("utf-8")
        finally:
            server.shutdown()
            thread.join(timeout=2)
            server.server_close()
        self.assertIn("أول 10 دروس", html)
        self.assertIn('"lesson_id": "U2-L01"', release)
        self.assertIn("observer-app.js", observer)

    def test_no_script_exceeds_two_hundred_lines(self):
        for path in (PROTOTYPE / "scripts").glob("*.js"):
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 200)

    def test_ordinary_route_is_a_simple_student_journey(self):
        index = (PROTOTYPE / "index.html").read_text(encoding="utf-8")
        lesson = (PROTOTYPE / "scripts/lesson-view.js").read_text(encoding="utf-8")
        activity = (PROTOTYPE / "scripts/activity-view.js").read_text(encoding="utf-8")
        catalog = (PROTOTYPE / "scripts/catalog-view.js").read_text(encoding="utf-8")
        self.assertNotIn('href="observer.html"', index)
        for phrase in ("Video Placeholder", "data-video-done", "data-mastery-done", "data-save-feedback"):
            self.assertIn(phrase, lesson)
        self.assertIn("data-check-activity", activity)
        self.assertIn("data-copy-feedback", catalog)

    def test_optional_video_drop_folder_is_documented(self):
        media_readme = PROTOTYPE / "media/README.md"
        self.assertTrue(media_readme.is_file())
        self.assertIn("U1-L01.mp4", media_readme.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
