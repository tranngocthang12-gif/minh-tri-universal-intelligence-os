import base64
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from minhtri.pc_reconnect_sync import build_snapshot, apply_snapshot, SyncBlocked, _git_blob

SHA1="a"*40
SHA2="b"*40
PATHS={
"state/bootstrap.json":{"schema":"minhtri-bootstrap-root/v1","project":"MINH_TRI_UNIVERSAL_INTELLIGENCE_OS","durable_continuity_authority":"GITHUB_PROTECTED_MAIN","current_state":"state/current.yaml","task_registry":"state/tasks.yaml","master_blueprint":"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md","law_precedence":"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md","role_bootstrap":"docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md","recovery_entrypoint":"docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md"},
"state/current.yaml":{"schema":"minhtri-current-state/v1","project":"MINH_TRI_UNIVERSAL_INTELLIGENCE_OS","durable_continuity_authority":"GITHUB_PROTECTED_MAIN","boot_root":"state/bootstrap.json","master_blueprint":"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md","law_precedence":"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md","role_bootstrap":"docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md","task_registry":"state/tasks.yaml","current_architecture":"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md","active_task_id":"ARCH-MASTER-BLUEPRINT-V1"},
"state/tasks.yaml":{"registry_authority":"state/tasks.yaml","tasks":[{"task_id":"ARCH-MASTER-BLUEPRINT-V1","status":"DONE"}]},
"config/pc_reconnect_sync_selection_v1.json":{"schema":"minhtri-pc-sync-selection/v1","authority":"PROTECTED_MAIN_ONLY","selected_main_paths":["docs/learning/A172.md"]},
"docs/vnext/MASTER_BLUEPRINT_V1_20261006.md":"Blueprint",
"docs/vnext/FOUNDATION_LAW_CONSOLIDATED_V1_20261006.md":"Law",
"docs/GITHUB_FIRST_ROLE_BOOTSTRAP_20261002.md":"Boot",
"docs/vnext/continuity/RECOVERY_ENTRYPOINT_V1.md":"Recovery",
"docs/LAW_UNIVERSAL_LEARNING_CONTINUITY_20261004.md":"Learning",
"docs/learning/A172.md":"Accepted"
}

def simulator(items=None,sha=SHA1,protected=True,compare="ahead",tamper=None):
    rows=copy.deepcopy(PATHS if items is None else items)
    def fetch(endpoint):
        if endpoint=="branches/main":
            return {"protected":protected,"commit":{"sha":sha}}
        if endpoint.startswith("compare/"):
            return {"status":compare}
        if not endpoint.startswith("contents/"):
            raise AssertionError(endpoint)
        path=endpoint.split("?",1)[0][len("contents/"):]
        value=rows[path]
        data=(json.dumps(value).encode() if isinstance(value,dict) else value.encode())
        blob=_git_blob(data)
        if tamper==path:
            blob="f"*40
        return {"type":"file","path":path,"size":len(data),"sha":blob,"encoding":"base64","content":base64.b64encode(data).decode()}
    return fetch

class ReconnectTest(unittest.TestCase):
    def root(self,tmp):
        return Path(tmp)/"minhtri-runtime-current"/"pc-reconnect-sync"

    def test_exact_main_snapshot_and_no_learning_proof(self):
        x=build_snapshot(simulator())
        self.assertEqual(x["head"],SHA1)
        self.assertIn("ACTIVE_TASK_NOT_EXECUTABLE_DONE",x["manifest"]["route_warnings"])
        self.assertFalse(x["manifest"]["local_brain_written"])
        self.assertFalse(x["manifest"]["background_learning_enabled"])

    def test_unprotected_main_blocks(self):
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(protected=False))

    def test_blob_tamper_blocks(self):
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(tamper="state/current.yaml"))

    def test_wrong_canonical_authority_blocks(self):
        items=copy.deepcopy(PATHS);items["state/current.yaml"]["durable_continuity_authority"]="LOCAL_PC"
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(items))

    def test_mismatched_route_blocks(self):
        items=copy.deepcopy(PATHS);items["state/current.yaml"]["task_registry"]="state/other.yaml"
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(items))

    def test_unmerged_learning_selection_rejected(self):
        items=copy.deepcopy(PATHS);items["config/pc_reconnect_sync_selection_v1.json"]["selected_main_paths"]=["docs/learning/A173_DRAFT.md"]
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(items))

    def test_path_traversal_rejected(self):
        items=copy.deepcopy(PATHS);items["config/pc_reconnect_sync_selection_v1.json"]["selected_main_paths"]=["docs/learning/../../private.json"]
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(items))

    def test_missing_active_task_rejected(self):
        items=copy.deepcopy(PATHS);items["state/current.yaml"]["active_task_id"]="MISSING"
        with self.assertRaises(SyncBlocked):build_snapshot(simulator(items))

    def test_cache_atomic_pointer_and_idempotence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self.root(tmp);x=build_snapshot(simulator())
            a=apply_snapshot(x,root,simulator())
            self.assertEqual(a["status"],"NONCANONICAL_CACHE_UPDATED")
            b=apply_snapshot(x,root,simulator())
            self.assertEqual(b["status"],"CACHE_ALREADY_CURRENT")
            self.assertEqual(json.loads((root/"current.json").read_text())["head"],SHA1)

    def test_corrupted_old_cache_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self.root(tmp);x=build_snapshot(simulator());apply_snapshot(x,root,simulator())
            (root/"snapshots"/SHA1/"files"/"state"/"current.yaml").write_text("MUTATED")
            with self.assertRaises(SyncBlocked):apply_snapshot(x,root,simulator())

    def test_refuses_rewind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=self.root(tmp)
            apply_snapshot(build_snapshot(simulator()),root,simulator())
            with self.assertRaises(SyncBlocked):
                apply_snapshot(build_snapshot(simulator(sha=SHA2)),root,simulator(sha=SHA2,compare="behind"))
            self.assertEqual(json.loads((root/"current.json").read_text())["head"],SHA1)

    def test_refuses_non_approved_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SyncBlocked):
                apply_snapshot(build_snapshot(simulator()),Path(tmp)/"ledger",simulator())

if __name__=="__main__":
    unittest.main()
