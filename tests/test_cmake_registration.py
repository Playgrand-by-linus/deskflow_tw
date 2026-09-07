import os
import unittest

class TestCmakeRegistration(unittest.TestCase):
    def setUp(self):
        self.repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cmake_path = os.path.join(self.repo_dir, "translations", "CMakeLists.txt")

    def test_cmake_file_exists(self):
        self.assertTrue(os.path.isfile(self.cmake_path), "translations/CMakeLists.txt does not exist")

    def test_zh_tw_registered_in_trs(self):
        with open(self.cmake_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(
            "${CMAKE_PROJECT_NAME}_zh_TW.ts",
            content,
            "translations/CMakeLists.txt must include ${CMAKE_PROJECT_NAME}_zh_TW.ts in translation list"
        )

if __name__ == "__main__":
    unittest.main()
