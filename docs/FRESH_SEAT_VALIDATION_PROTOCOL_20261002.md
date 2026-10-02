# FRESH-SEAT VALIDATION PROTOCOL — 2026-10-02

**Status:** CANDIDATE / FAIL-CLOSED / NOT YET EXECUTED

## Purpose

Prove that a genuinely separate chat seat can recover the live MINH TRI brain through
the canonical read-only connector without relying on copied values from the prior chat.

## Preconditions

- use a separate chat UI;
- do not paste the expected event count, head, focus, or lesson values into the prompt;
- the connector must expose exactly:
  - `brain.verify`
  - `brain.recovery_packet`
- no mutation tool may be exposed.

## Required evidence

The fresh seat must call both read-only tools. A control seat then performs an independent
`brain.verify` close to the same validation window.

Record:
- `separate_chat_ui = true`;
- `prompt_seeded_expected_values = false`;
- exact toolset;
- `mutation_tool_exposed = false`;
- fresh-seat `brain.verify` output;
- fresh-seat `brain.recovery_packet` output;
- control-seat `brain.verify` output.

## PASS rule

`src/minhtri/fresh_seat.py::validate_fresh_seat_evidence` must return `PASS`.

The validator requires:
1. fresh verify = VALID;
2. fresh recovery = VALID;
3. control verify = VALID;
4. event_count and head agree across all three reads;
5. exact two-tool allowlist;
6. no mutation exposure;
7. no seeded expected values;
8. explicit separate-chat UI attestation.

## Non-evidence

The following cannot independently establish PASS:
- prose from a chat saying it recovered state;
- GitHub state copied into the prompt;
- a same-chat reconnect;
- a Python harness without the ChatGPT connector;
- historical screenshots or old head values.

## Promotion

Only after validated evidence is committed may:
- `fresh_chat_seat_validation` become `PASS`;
- `end_to_end_seat_brain_transport` become true;
- Research Adapter gate be reconsidered.

This protocol does not prove tunnel persistence or device-compromise resistance.
