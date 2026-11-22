"""Unit tests for generate_registry.py. Run from the repo root:

  python3 -m unittest discover -s scripts -v
"""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_registry as gr

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
GENERATOR = SCRIPTS / "generate_registry.py"
REGISTRY = REPO / "registry" / "churches.md"
DATA_FILES = ("churches.json", "tradition.json", "canonical_status.json")


def load_real():
    data = gr.load(REPO, "churches.json")
    traditions = {t["id"]: t for t in gr.load(REPO, "tradition.json")["entries"]}
    statuses = {s["id"]: s for s in gr.load(REPO, "canonical_status.json")["entries"]}
    return data, traditions, statuses


# Each corruption takes (churches, tradition.json) documents and breaks one guard.
def unknown_tradition(churches, _trads):
    churches["entries"][0]["tradition"] = "trad:bogus"

def unknown_status(churches, _trads):
    churches["entries"][0]["canonical_status"] = "cstat:nonexistent"

def duplicate_id(churches, _trads):
    churches["entries"][1]["id"] = churches["entries"][0]["id"]

def entry_count_mismatch(churches, _trads):
    churches["entry_count"] += 1

def tradition_order_drift(churches, trads):
    # A tradition in the data that TRADITION_ORDER does not list: before the
    # fix, every church in it was dropped from the table.
    trads["entries"].append(dict(trads["entries"][0], id="trad:new"))
    churches["entries"][0]["tradition"] = "trad:new"

CORRUPTIONS = {
    "unknown tradition": (unknown_tradition, "trad:bogus"),
    "unknown canonical status": (unknown_status, "cstat:nonexistent"),
    "duplicate id": (duplicate_id, "duplicate ids"),
    "entry_count mismatch": (entry_count_mismatch, "entry_count"),
    "TRADITION_ORDER drift": (tradition_order_drift, "trad:new"),
}


class Validate(unittest.TestCase):
    def setUp(self):
        self.data, self.traditions, self.statuses = load_real()

    def corrupt(self, corruption):
        data = copy.deepcopy(self.data)
        trads_doc = {"entries": copy.deepcopy(list(self.traditions.values()))}
        corruption(data, trads_doc)
        return data, {t["id"]: t for t in trads_doc["entries"]}

    def test_accepts_the_committed_seed(self):
        gr.validate(self.data, self.traditions, self.statuses)  # must not raise

    def test_rejects_each_corruption_naming_the_problem(self):
        for name, (corruption, expected) in CORRUPTIONS.items():
            with self.subTest(guard=name):
                data, traditions = self.corrupt(corruption)
                with self.assertRaises(ValueError) as ctx:
                    gr.validate(data, traditions, self.statuses)
                self.assertIn(expected, str(ctx.exception))

    def test_rejects_tradition_order_naming_an_unknown_tradition(self):
        traditions = dict(self.traditions)
        del traditions["trad:armenian"]
        data = copy.deepcopy(self.data)
        data["entries"] = [e for e in data["entries"] if e["tradition"] != "trad:armenian"]
        data["entry_count"] = len(data["entries"])
        with self.assertRaises(ValueError) as ctx:
            gr.validate(data, traditions, self.statuses)
        self.assertIn("TRADITION_ORDER names traditions not in tradition.json", str(ctx.exception))

    def test_reports_every_problem_at_once(self):
        data, traditions = self.corrupt(lambda c, t: (unknown_tradition(c, t),
                                                      unknown_status(c, t),
                                                      duplicate_id(c, t),
                                                      entry_count_mismatch(c, t)))
        with self.assertRaises(ValueError) as ctx:
            gr.validate(data, traditions, self.statuses)
        message = str(ctx.exception)
        for expected in ("trad:bogus", "cstat:nonexistent", "duplicate ids", "entry_count"):
            self.assertIn(expected, message)


class Render(unittest.TestCase):
    def setUp(self):
        self.data, self.traditions, self.statuses = load_real()

    def test_rendered_row_count_equals_entry_count(self):
        text = gr.render(self.data, self.traditions, self.statuses)
        rows = [line for line in text.splitlines() if line.startswith("| `esi:")]
        self.assertEqual(len(rows), self.data["entry_count"])
        self.assertIn(f"{self.data['entry_count']} canonical draft IDs", text)

    def test_refuses_to_render_a_church_it_cannot_place(self):
        # The guard against the original failure, even if validate() is skipped.
        data = copy.deepcopy(self.data)
        data["entries"][0]["tradition"] = "trad:bogus"
        with self.assertRaises(ValueError) as ctx:
            gr.render(data, self.traditions, self.statuses)
        self.assertIn(data["entries"][0]["id"], str(ctx.exception))


class EndToEnd(unittest.TestCase):
    """Run the real generator, with and without -O, against a copy of the repo.

    The #1 regression was end-to-end: under -O an unresolvable `tradition` gave
    exit 0, "Wrote 24 churches", and a 23-row table. Any reintroduction of
    `assert` as a guard must fail here.
    """

    FLAGS = ([], ["-O"], ["-OO"])

    def make_repo(self, corruption=None):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        (tmp / "data").mkdir()
        (tmp / "registry").mkdir()
        for name in DATA_FILES:
            shutil.copy(REPO / "data" / name, tmp / "data" / name)
        shutil.copy(REGISTRY, tmp / "registry" / "churches.md")
        if corruption:
            churches = json.loads((tmp / "data" / "churches.json").read_text(encoding="utf-8"))
            trads = json.loads((tmp / "data" / "tradition.json").read_text(encoding="utf-8"))
            corruption(churches, trads)
            (tmp / "data" / "churches.json").write_text(json.dumps(churches), encoding="utf-8")
            (tmp / "data" / "tradition.json").write_text(json.dumps(trads), encoding="utf-8")
        return tmp

    def run_generator(self, flags, repo):
        return subprocess.run([sys.executable, *flags, str(GENERATOR), str(repo)],
                              capture_output=True, text=True)

    def test_every_corruption_fails_and_leaves_the_registry_unchanged(self):
        before = REGISTRY.read_bytes()
        for name, (corruption, expected) in CORRUPTIONS.items():
            for flags in self.FLAGS:
                with self.subTest(guard=name, flags=flags or ["(none)"]):
                    repo = self.make_repo(corruption)
                    result = self.run_generator(flags, repo)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn(expected, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual((repo / "registry" / "churches.md").read_bytes(), before)

    def test_valid_input_regenerates_the_registry_byte_identical(self):
        for flags in self.FLAGS:
            with self.subTest(flags=flags or ["(none)"]):
                repo = self.make_repo()
                (repo / "registry" / "churches.md").unlink()
                result = self.run_generator(flags, repo)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((repo / "registry" / "churches.md").read_bytes(),
                                 REGISTRY.read_bytes())


if __name__ == "__main__":
    unittest.main()
