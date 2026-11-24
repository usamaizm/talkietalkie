"""Validation and serialization for the TalkieTalkie draft message envelope.

This module does not implement accounts, encryption, delivery, or file transfer.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Any


_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def _required_text(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _timestamp(value: Any) -> None:
    _required_text("created_at", value)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("created_at must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("created_at must include a timezone")


@dataclass(frozen=True)
class Attachment:
    name: str
    media_type: str
    size_bytes: int
    sha256: str | None = None

    def validate(self) -> None:
        _required_text("attachment.name", self.name)
        if self.name in {".", ".."} or "/" in self.name or "\\" in self.name:
            raise ValueError("attachment.name must be a filename, not a path")
        _required_text("attachment.media_type", self.media_type)
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise ValueError("attachment.size_bytes must be an integer")
        if self.size_bytes < 0:
            raise ValueError("attachment.size_bytes cannot be negative")
        if self.sha256 is not None and not _SHA256.fullmatch(self.sha256):
            raise ValueError("attachment.sha256 must be 64 hexadecimal characters")


@dataclass(frozen=True)
class Message:
    message_id: str
    conversation_id: str
    sender_id: str
    created_at: str
    kind: str
    text: str | None = None
    attachment: Attachment | None = None
    reply_to: str | None = None
    group_id: str | None = None
    version: str = "0.1"

    def validate(self) -> None:
        if self.version != "0.1":
            raise ValueError("unsupported message envelope version")
        for name in ("message_id", "conversation_id", "sender_id"):
            _required_text(name, getattr(self, name))
        _timestamp(self.created_at)
        if self.reply_to is not None:
            _required_text("reply_to", self.reply_to)
        if self.group_id is not None:
            _required_text("group_id", self.group_id)
        if self.kind == "text":
            _required_text("text", self.text)
            if self.attachment is not None:
                raise ValueError("text messages cannot include an attachment")
        elif self.kind == "file":
            if self.text is not None:
                raise ValueError("file messages cannot include text payload")
            if not isinstance(self.attachment, Attachment):
                raise ValueError("file messages require attachment metadata")
            self.attachment.validate()
        else:
            raise ValueError("kind must be 'text' or 'file'")


@dataclass(frozen=True)
class Reaction:
    message_id: str
    sender_id: str
    value: str
    created_at: str
    version: str = "0.1"

    def validate(self) -> None:
        if self.version != "0.1":
            raise ValueError("unsupported reaction version")
        _required_text("message_id", self.message_id)
        _required_text("sender_id", self.sender_id)
        if self.value not in {"thumbs_up", "thumbs_down"}:
            raise ValueError("reaction value must be thumbs_up or thumbs_down")
        _timestamp(self.created_at)


def message_to_dict(message: Message) -> dict[str, Any]:
    message.validate()
    return asdict(message)


def message_from_dict(value: dict[str, Any]) -> Message:
    if not isinstance(value, dict):
        raise ValueError("message must be an object")
    raw_attachment = value.get("attachment")
    attachment = Attachment(**raw_attachment) if isinstance(raw_attachment, dict) else None
    message = Message(
        message_id=value.get("message_id"),
        conversation_id=value.get("conversation_id"),
        sender_id=value.get("sender_id"),
        created_at=value.get("created_at"),
        kind=value.get("kind"),
        text=value.get("text"),
        attachment=attachment,
        reply_to=value.get("reply_to"),
        group_id=value.get("group_id"),
        version=value.get("version", "0.1"),
    )
    message.validate()
    return message
