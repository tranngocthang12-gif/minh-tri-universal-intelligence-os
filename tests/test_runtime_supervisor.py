import unittest

from minhtri.runtime_supervisor import ProcessSupervisor, SupervisorError


class FakeProcess:
    def __init__(self, returncode):
        self.returncode = returncode

    def wait(self):
        return self.returncode


class SupervisorTests(unittest.TestCase):
    def test_shell_is_never_used(self):
        calls = []

        def popen(argv, **kwargs):
            calls.append((argv, kwargs))
            return FakeProcess(0)

        supervisor = ProcessSupervisor(["tool", "--flag"], popen_factory=popen)
        self.assertEqual(supervisor.run(), 0)
        self.assertEqual(calls[0][0], ["tool", "--flag"])
        self.assertIs(calls[0][1]["shell"], False)

    def test_failed_child_restarts_with_backoff(self):
        codes = iter([7, 8, 0])
        sleeps = []
        events = []

        def popen(argv, **kwargs):
            return FakeProcess(next(codes))

        supervisor = ProcessSupervisor(
            ["tool"],
            min_backoff=1,
            max_backoff=4,
            sleep=sleeps.append,
            popen_factory=popen,
            event_sink=events.append,
        )
        self.assertEqual(supervisor.run(max_restarts=3), 0)
        self.assertEqual(sleeps, [1.0, 2.0])
        self.assertEqual(
            [e["event"] for e in events],
            ["STARTING", "EXITED", "RESTARTING", "STARTING", "EXITED",
             "RESTARTING", "STARTING", "EXITED"],
        )

    def test_restart_limit_fails_closed(self):
        supervisor = ProcessSupervisor(
            ["tool"],
            sleep=lambda _: None,
            popen_factory=lambda *a, **k: FakeProcess(9),
        )
        self.assertEqual(supervisor.run(max_restarts=0), 9)

    def test_invalid_argv_is_rejected(self):
        with self.assertRaises(SupervisorError):
            ProcessSupervisor([])


if __name__ == "__main__":
    unittest.main()
