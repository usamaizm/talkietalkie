# TalkieTalkie

**Talk. Share. Respond.**

TalkieTalkie is an early-stage communication-app concept centered on making it quick and easy to talk with people and share things with them.

The original idea includes:
- starting a conversation with minimal friction;
- sending a file to someone as quickly as possible;
- reacting to messages with a thumbs-up or thumbs-down;
- stacking or grouping messages and shared items into a useful conversation flow.

These are concept goals, not claims about implemented features.

## Product principles

1. **Fast communication:** make the common action—sending a message—quick and obvious.
2. **Simple sharing:** reduce the steps needed to send a file or other item.
3. **Lightweight feedback:** support clear positive and negative reactions.
4. **Readable conversations:** explore message stacking and grouping without hiding context.
5. **Privacy and user control:** make sharing destinations and visibility explicit.

## Status

**Concept stage.** The repository currently contains the initial product description. No production app, backend, messaging protocol, or file-transfer service is claimed to exist.

## Initial protocol prototype

A transport-neutral JSON message-envelope prototype is available in the `talkietalkie/` Python package. It models text messages, file metadata, replies, grouping, and thumbs-up/thumbs-down reactions. It does not implement a network service, encryption, accounts, durable storage, or file transfer. See [Message Envelope Draft 0.1](PROTOCOL.md), the [JSON Schema](schema/message-0.1.schema.json), and the [example messages](examples/); run `make test`.

## Product questions to resolve

- Which platforms should be supported first?
- Is the first release one-to-one messaging, group messaging, or both?
- How should identity, contacts, and invitations work?
- What file types and size limits should sharing support?
- What does “stacking” mean in the interaction design?
- What privacy, encryption, retention, and abuse-reporting requirements apply?

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## Contributing

Contributions should preserve the product's simplicity and document user-facing behavior, privacy implications, and platform requirements.

## License

No license is asserted here until the repository's existing licensing decision is reviewed and documented.


## Ecosystem integration

This project is part of a set of independent, interoperable open projects. See the [ecosystem integration contract](https://github.com/usamaizm/AIDB/blob/main/docs/ECOSYSTEM_INTEGRATION.md) for its role, interoperability boundaries, and integration principles.


## Contributor attribution

Human and AI contributors must follow the [contributor identity and attribution protocol](CONTRIBUTOR_PROTOCOL.md). Keep the authenticated GitHub account separate from a contributor's self-declared identity; never guess who performed earlier work.
