import unittest
import json
from pathlib import Path

from talkietalkie import Attachment, Message, Reaction, message_from_dict, message_to_dict


STAMP = "2026-11-24T12:00:00Z"


class MessageEnvelopeTests(unittest.TestCase):
    def test_published_examples(self):
        examples = Path(__file__).resolve().parents[1] / "examples"
        for name in ("text-message.json", "file-message.json"):
            with self.subTest(example=name):
                value = json.loads((examples / name).read_text(encoding="utf-8"))
                self.assertEqual(message_from_dict(value), message_from_dict(message_to_dict(message_from_dict(value))))
        reaction = json.loads((examples / "reaction.json").read_text(encoding="utf-8"))
        Reaction(**reaction).validate()

    def test_text_message_round_trip(self):
        original = Message(
            message_id="m-1", conversation_id="c-1", sender_id="u-1",
            created_at=STAMP, kind="text", text="Hello",
            reply_to="m-0", group_id="stack-1",
        )
        self.assertEqual(message_from_dict(message_to_dict(original)), original)

    def test_file_message_requires_metadata_not_local_path(self):
        message = Message(
            message_id="m-2", conversation_id="c-1", sender_id="u-1",
            created_at=STAMP, kind="file",
            attachment=Attachment("report.pdf", "application/pdf", 1024, "a" * 64),
        )
        self.assertEqual(message_from_dict(message_to_dict(message)), message)

    def test_rejects_path_traversal_filename(self):
        attachment = Attachment("../secret.txt", "text/plain", 4)
        with self.assertRaises(ValueError):
            attachment.validate()

    def test_rejects_timezone_free_timestamp(self):
        message = Message("m", "c", "u", "2026-11-24T12:00:00", "text", text="hi")
        with self.assertRaises(ValueError):
            message.validate()

    def test_rejects_unknown_message_kind(self):
        message = Message("m", "c", "u", STAMP, "audio")
        with self.assertRaises(ValueError):
            message.validate()

    def test_rejects_unknown_message_fields(self):
        payload = message_to_dict(Message(
            message_id="m", conversation_id="c", sender_id="u",
            created_at=STAMP, kind="text", text="hello",
        ))
        payload["admin"] = True
        with self.assertRaisesRegex(ValueError, "unknown message field"):
            message_from_dict(payload)

    def test_rejects_unknown_attachment_fields(self):
        payload = message_to_dict(Message(
            message_id="m", conversation_id="c", sender_id="u",
            created_at=STAMP, kind="file",
            attachment=Attachment("file.txt", "text/plain", 1),
        ))
        payload["attachment"]["local_path"] = "/etc/passwd"
        with self.assertRaisesRegex(ValueError, "unknown attachment field"):
            message_from_dict(payload)

    def test_rejects_non_object_attachment(self):
        payload = {
            "message_id": "m", "conversation_id": "c", "sender_id": "u",
            "created_at": STAMP, "kind": "file", "attachment": "file.txt",
        }
        with self.assertRaisesRegex(ValueError, "attachment must be an object"):
            message_from_dict(payload)

    def test_rejects_non_string_reaction(self):
        with self.assertRaises(ValueError):
            Reaction("m", "u", [], STAMP).validate()

    def test_reaction_values_are_limited(self):
        Reaction("m", "u", "thumbs_up", STAMP).validate()
        with self.assertRaises(ValueError):
            Reaction("m", "u", "heart", STAMP).validate()


if __name__ == "__main__":
    unittest.main()
