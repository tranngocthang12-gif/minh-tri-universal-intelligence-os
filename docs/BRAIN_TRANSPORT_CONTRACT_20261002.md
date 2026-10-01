# READ-ONLY BRAIN TRANSPORT CONTRACT — 2026-10-02

**Status:** CONTRACT ONLY / NOT CONNECTED / NOT END-TO-END VERIFIED

## Goal
Expose the merged BrainReader recovery packet to a replaceable AI seat without granting ledger mutation authority.

## Boundary
The local transport uses one fixed brain directory configured outside remote requests. A caller cannot select filesystem paths.

Allowed methods:
- brain.verify
- brain.recovery_packet
- optional compatibility reads: get_head, get_current_focus, search_lessons

Forbidden:
- Ledger.apply, repair_snapshot, init
- arbitrary filesystem access
- shell execution
- Owner secret/config reads
- publication or other external mutation

## Request and response
recovery_packet accepts only optional query text and bounded integer limit. It returns status, event_count, ledger head, current focus, and lesson matches from one verified read. Ledger verification failure is an error, never empty success.

## Security requirements
1. local/private binding by default;
2. caller authentication at transport boundary;
3. read-only filesystem permission where practical;
4. fixed brain path configured locally;
5. no Owner mutation secret in the transport;
6. strict method allowlist;
7. request/response size limits;
8. audit metadata without secrets/full chat;
9. protocol versioning;
10. fail closed on verification failure.

Transport technology is replaceable; MCP-compatible service is one candidate, not project law.

## End-to-end acceptance
A genuinely fresh seat with no prior transcript must connect through the transport, recover the exact verified head/focus, receive no mutation capability, fail on tampering, fail path redirection, and leave a reproducible handoff.

Until a real local/private transport is installed and this acceptance test passes, end_to_end_seat_brain_transport remains false.

Independent external anchor publication remains separately blocked on an independent write authority. That blocker does not justify mutation rights in this transport.
