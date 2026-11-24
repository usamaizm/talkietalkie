# TalkieTalkie Message Envelope Draft 0.1

**Status:** Local data-model prototype only. This is not a network protocol or a security specification.

## Purpose

Define a small transport-neutral message envelope for the initial TalkieTalkie concepts: text messages, file-sharing metadata, replies/grouping, and thumbs-up/thumbs-down reactions. The envelope can be serialized as JSON by the reference Python package. The provisional [JSON Schema](schema/message-0.1.schema.json) and [examples](examples/) define machine-readable draft fixtures.

## Message fields

- version: envelope version, currently 0.1.
- message_id: stable identifier for this message.
- conversation_id: conversation identifier.
- sender_id: application-level sender identifier. This field is not proof of identity.
- created_at: ISO-8601 timestamp with an explicit timezone.
- kind: text or file.
- text: non-empty text payload for text messages.
- attachment: metadata for a file message (filename, media type, byte length, optional SHA-256).
- reply_to: optional message identifier for a reply.
- group_id: optional identifier for a visually stacked/grouped sequence.

File bytes are not embedded in this envelope. The envelope does not prescribe a transfer service, storage location, or download URL.

## Reactions

A reaction is a separate event containing message_id, sender_id, created_at, version, and one of thumbs_up or thumbs_down. A receiver should treat sender identity as an unverified claim until the eventual account/authentication layer verifies it.

## Safety and privacy boundaries

- Never interpret sender_id as authenticated identity.
- Never trust filename, media type, byte length, or digest without validating the received file.
- Do not automatically open or execute shared files.
- A SHA-256 digest can detect accidental or deliberate byte changes only when the expected digest itself is trusted; it does not establish who sent a file.
- The prototype does not encrypt messages, authenticate users, provide access control, transfer files, store messages durably, or prevent replay.
- Do not use this draft for real private conversations or sensitive file sharing.

## Open decisions

Platform, account model, invitation flow, end-to-end encryption, key recovery, delivery guarantees, retention, abuse reporting, file-size limits, malware scanning, offline behavior, and multi-device synchronization remain product and security decisions. They must be resolved before network deployment.
