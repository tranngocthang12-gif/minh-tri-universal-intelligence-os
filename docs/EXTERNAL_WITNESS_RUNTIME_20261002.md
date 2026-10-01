# EXTERNAL WITNESS RUNTIME — 2026-10-02

**Status:** REWRITE-DETECTION IMPLEMENTED / REMOTE PUBLICATION AUTHORITY DESIGNATED / FIRST OWNER-BRAIN WITNESS NOT YET OBSERVED

## Threat
A local attacker with write access can replace both `events.jsonl` and `state.json` with a different internally valid history. A local hash chain alone cannot prove that the new history is the same history previously observed.

## Control
Preserve a ledger checkpoint outside the local brain writer's authority:

```text
LOCAL BRAIN (read-only transport)
  -> event_count + head
  -> anchor
  -> external witness receipt
  -> CLOUD WRITE AUTHORITY
```

For the current ChatGPT Project architecture, the intended first publication authority is the connected cloud GitHub connector, **provided its credential is not exposed to the Owner-PC brain host or local writer**. The local host remains read-only and receives no GitHub mutation credential.

The repository module `minhtri.witness` validates:
- witness schema/project identity;
- receipt digest;
- embedded anchor integrity;
- remote authority/locator metadata;
- exact historical local ledger prefix against the externally preserved checkpoint.

## Whole-history rewrite proof
`tests/test_external_witness_rewrite.py` creates an original ledger and external receipt, then replaces both the original event log and snapshot with a different, internally valid ledger. Local `Ledger.verify()` succeeds on the rewritten ledger, while `verify_local_history_against_witness()` fails with `LOCAL_HISTORY_DIVERGES_FROM_EXTERNAL_WITNESS`.

This demonstrates the missing property: **an internally valid full rewrite is detectable once an earlier checkpoint is preserved outside the local writer's authority.**

## Publication boundary
The external publisher must:
1. obtain `event_count` and `head` through the authenticated read-only brain transport;
2. create the anchor/receipt;
3. write it through a cloud authority unavailable to the local brain process;
4. read it back before reporting publication success;
5. preserve its remote revision/locator in the handoff.

The local brain host must never receive the cloud write credential.

## Current activation truth
Repository CI can prove the algorithm and process boundary. It cannot prove the first real Owner-PC ledger anchor because this ChatGPT session has no route to the Owner's local `brain/` yet.

Therefore do not set `external_anchor_publication=true` until:
- Owner-PC local host is observed running;
- a cloud publisher reads the actual local head through that host;
- a real external receipt is written and read back;
- the same actual local ledger verifies against that receipt.

No chat statement alone upgrades this status.
