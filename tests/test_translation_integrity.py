import os
import xml.etree.ElementTree as ET
import unittest

class TestTranslationIntegrity(unittest.TestCase):
    def setUp(self):
        self.repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.tw_path = os.path.join(self.repo_dir, "translations", "deskflow_zh_TW.ts")

    def test_translation_file_exists(self):
        self.assertTrue(os.path.isfile(self.tw_path), f"File {self.tw_path} does not exist")

    def test_xml_structure_and_language(self):
        if not os.path.isfile(self.tw_path):
            self.fail("File does not exist")
        tree = ET.parse(self.tw_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "TS")
        self.assertEqual(root.attrib.get("language"), "zh_TW")

    def test_all_messages_translated(self):
        if not os.path.isfile(self.tw_path):
            self.fail("File does not exist")
        tree = ET.parse(self.tw_path)
        root = tree.getroot()
        
        messages = root.findall(".//message")
        self.assertEqual(len(messages), 314, f"Expected 314 messages, found {len(messages)}")

        unfinished = []
        empty = []
        for context in root.findall("context"):
            c_name = context.find("name").text
            for m in context.findall("message"):
                src = m.find("source").text if m.find("source") is not None else ""
                t = m.find("translation")
                if t is None or t.attrib.get("type") == "unfinished":
                    unfinished.append(f"[{c_name}] {src}")
                else:
                    is_numerus = m.attrib.get("numerus") == "yes"
                    if is_numerus:
                        num = t.find("numerusform")
                        if num is None or not num.text or not num.text.strip():
                            empty.append(f"[{c_name}] {src} (numerus)")
                    else:
                        if not t.text or not t.text.strip():
                            empty.append(f"[{c_name}] {src}")

        self.assertEqual(len(unfinished), 0, f"Found {len(unfinished)} unfinished entries: {unfinished[:5]}")
        self.assertEqual(len(empty), 0, f"Found {len(empty)} empty entries: {empty[:5]}")

    def test_localized_name(self):
        if not os.path.isfile(self.tw_path):
            self.fail("File does not exist")
        tree = ET.parse(self.tw_path)
        root = tree.getroot()
        i18n_ctx = None
        for c in root.findall("context"):
            if c.find("name").text == "i18n":
                i18n_ctx = c
                break
        self.assertIsNotNone(i18n_ctx, "Context 'i18n' not found")
        msg = i18n_ctx.find("message")
        self.assertEqual(msg.find("source").text, "LocalizedName")
        self.assertEqual(msg.find("translation").text, "繁體中文")

    def test_canonical_terms_and_no_machine_artifacts(self):
        if not os.path.isfile(self.tw_path):
            self.fail("File does not exist")
        with open(self.tw_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Machine translation blacklist
        self.assertNotIn("窗戶(&W)", content, "Should not translate Window menu as 窗戶")
        self.assertNotIn("窗户", content)
        self.assertNotIn("<translation>出口</translation>", content, "Should not translate Exit as 出口")
        self.assertNotIn("按下回车键执行命令", content)

        # Canonical vocabulary checks
        self.assertIn("伺服器", content)
        self.assertIn("用戶端", content)
        self.assertIn("螢幕", content)
        self.assertIn("剪貼簿", content)
        self.assertIn("背景服務", content)

if __name__ == "__main__":
    unittest.main()
