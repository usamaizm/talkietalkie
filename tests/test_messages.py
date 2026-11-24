import unittest

from talkietalkie import Attachment, Message, Reaction, message_from_dict, message_to_dict


STAMP = "2026-11-24T12:00:00Z"


class MessageEnvelopeTests(unittest.TestCase):
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

    def test_reaction_values_are_limited(self):
        Reaction("m", "u", "thumbs_up", STAMP).validate()
        with self.assertRaises(ValueError):
            Reaction("m", "u", "heart", STAMP).validate()


if __name__ == "__main__":
    unittest.main()
