"""Test redundancy -- which test files add no coverage, a MEASUREMENT (test-diet TD-12).

A measurement, never a gate: it reads, it prints, it exits 0 when it completes. What it is for: the owner (or the
Lead) sees which test files of the package cover no product line that another test file does not also cover, and
how long they take, before deleting tests. LINE COVERAGE ONLY: a file with zero unique lines may still hold the
only assertion on a behaviour -- the list is a set of candidates for a reader, not a verdict.

Usage:
  python tools/test_redundancy.py run --package DIR --out DIR [--jobs 4] [--timeout 900] [--only GLOB | --keep-only] [--force]
  python tools/test_redundancy.py report --data FILE --runs FILE --out DIR

run     starts every `scripts/tests/test_*.py` of the package (DIR = the directory of ai-packages/qa-factory)
        as `sys.executable -B <file>` with cwd = DIR, in a thread pool of --jobs, with COVERAGE_PROCESS_START
        (the rc file written to <out>/coveragerc) and QA_TEST_CONTEXT=<file name> in its environment. The rc
        sets the STATIC coverage context to ${QA_TEST_CONTEXT-}: every line a process (and its grandchildren,
        which inherit the environment) executes is recorded under the name of the test file that started it.
        Children are measured through a .pth file that calls coverage.process_startup(); THIS TOOL DOES NOT
        WRITE IT (the CI job does, as crap-measure does). Writes <out>/runs.json (a list of {file, exit,
        seconds, timed_out}) and the combined <out>/data/.coverage; the per-file logs go to <out>/logs/.
        A file over --timeout seconds is killed with its process tree and recorded timed_out; the run goes on.
        --only filters the file names by fnmatch. --keep-only runs exactly the `keep` rows of the package's
        scripts/tests/test-layers.json, read through the package's selftest.test_layers() (not with --only: exit 2);
        a keep row naming a file absent on disk is skipped and named in one line; no keep rows or no layers file
        is refused with the door "run TD-15.2 first" (exit 1). Files run in name order, as in every mode (the tool
        has no weights, so a keep file is treated like any other file). --out holding old data is refused unless --force, which
        empties <out>/data (and drops the old runs.json) first.
report  reads the combined data (the contexts per line) and runs.json, writes <out>/test-redundancy.json and
        <out>/test-redundancy.md: per test file covered lines, UNIQUE lines (no other context covers them),
        seconds, exit and status (not-measured: zero lines; red: exit != 0 or timed out; else ok). A line with
        an empty context (a process started without QA_TEST_CONTEXT) is counted under "(no context)", shown in
        the totals, and never unique to a file. A red file's lines still count as covered by it, so a line
        shared with a red file is not unique to the other one.

Exit codes: 0 done; 2 refused (nothing matched, coverage missing, old data in --out, missing or empty data).
"""
import argparse
import fnmatch
import json
import os
import pathlib
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

NO_CONTEXT = "(no context)"
NOTE = ("NOTE: line coverage only; a file with zero unique lines may still hold the only assertion on a "
        "behaviour - a candidate for a reader, not a verdict.")
PTH_LINE = "import coverage; coverage.process_startup()"


def refuse(text):
    print(f"test_redundancy: {text}", file=sys.stderr)
    return 2


def coverage_module():
    try:
        import coverage
    except ImportError:
        return None
    return coverage


# ---------------------------------------------------------------- run

def kill_tree(proc):
    """Kill the process and everything it started: taskkill /T on Windows, the process group on POSIX."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, check=False)
    else:
        import signal
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        proc.kill()
    except OSError:
        pass


def run_one(path, package, out, timeout, env_base):
    env = dict(env_base)
    env["QA_TEST_CONTEXT"] = path.name
    env["COVERAGE_PROCESS_START"] = str(out / "coveragerc")
    kwargs = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    t0 = time.monotonic()
    timed_out = False
    with open(out / "logs" / (path.name + ".txt"), "wb") as log:
        proc = subprocess.Popen([sys.executable, "-B", str(path)], cwd=str(package), env=env,
                                stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, **kwargs)
        try:
            rc = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc)
            rc = proc.wait()
    return {"file": path.name, "exit": rc, "seconds": round(time.monotonic() - t0, 2), "timed_out": timed_out}


def write_rc(package, out):
    scripts = (package / "scripts").resolve().as_posix()
    data_file = (out / "data" / ".coverage").resolve().as_posix()
    lines = ["[run]", "parallel = True", f"data_file = {data_file}", f"source = {scripts}",
             "omit = */scripts/tests/*", "context = ${QA_TEST_CONTEXT-}",
             "disable_warnings = no-data-collected, module-not-imported, module-not-measured"]
    rc = out / "coveragerc"
    rc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rc


KEEP_DOOR = "run TD-15.2 first (it writes the keep rows of scripts/tests/test-layers.json)"


def keep_files(package, tests_dir):
    """The `keep` rows as test paths, read through the package's own selftest.test_layers() (AR-13).
    Returns (files, missing names) or raises ValueError carrying the one-sentence refusal."""
    import importlib.util
    scripts = package / "scripts"
    selftest = scripts / "selftest.py"
    if not selftest.is_file():
        raise ValueError(f"{selftest} is missing, so the keep rows cannot be read; expected a package with scripts/selftest.py; {KEEP_DOOR}")
    spec = importlib.util.spec_from_file_location("selftest_of_package", selftest)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(scripts))
    try:
        spec.loader.exec_module(module)
        layers = module.test_layers(tests_dir / "test-layers.json")
    except Exception as exc:  # TestLayersError and import failures: one sentence, the same door
        raise ValueError(f"the keep rows cannot be read through selftest.test_layers() ({type(exc).__name__}: "
                         f"{' '.join(str(exc).split())}); {KEEP_DOOR}") from None
    finally:
        sys.path.remove(str(scripts))
    keep = sorted(layers.get("keep") or {})
    if layers.get("absent") or not keep:
        raise ValueError(f"{tests_dir / 'test-layers.json'} is absent or has no keep rows, nothing to measure; {KEEP_DOOR}")
    present = [tests_dir / name for name in keep if (tests_dir / name).is_file()]
    return present, [name for name in keep if not (tests_dir / name).is_file()]


def cmd_run(args):
    package = pathlib.Path(args.package).resolve()
    tests_dir = package / "scripts" / "tests"
    if args.keep_only and args.only:
        return refuse("--keep-only and --only cannot be given together; expected one of them")
    if args.keep_only:
        try:
            files, missing = keep_files(package, tests_dir)
        except ValueError as exc:
            print(f"test_redundancy: {exc}", file=sys.stderr)
            return 1
        if missing:
            print(f"keep rows naming a file absent on disk, skipped ({len(missing)}): {', '.join(missing)}", flush=True)
        if not files:
            print(f"test_redundancy: every keep row names a file absent on disk, nothing to measure; {KEEP_DOOR}", file=sys.stderr)
            return 1
    else:
        files = sorted(p for p in tests_dir.glob("test_*.py") if not args.only or fnmatch.fnmatch(p.name, args.only))
    if not files:
        return refuse(f"no test file matched in {tests_dir} (--only {args.only!r}); nothing to run")
    out = pathlib.Path(args.out).resolve()
    data_dir = out / "data"
    if (data_dir.is_dir() and any(data_dir.iterdir())) or (out / "runs.json").exists():
        if not args.force:
            return refuse(f"{out} already holds data or runs.json; pass --force to empty {data_dir} and run again")
        shutil.rmtree(data_dir, ignore_errors=True)
        (out / "runs.json").unlink(missing_ok=True)
    cov = coverage_module()
    if cov is None:
        return refuse("the `coverage` module is not importable. Install it (pip install coverage==7.16.2) and create the "
                      "startup file that measures children: python -c \"import sysconfig; "
                      "open(sysconfig.get_paths()['purelib'] + '/zz_coverage_startup.pth', 'w')"
                      f".write('{PTH_LINE}\\n')\"")
    data_dir.mkdir(parents=True, exist_ok=True)
    (out / "logs").mkdir(parents=True, exist_ok=True)
    rc = write_rc(package, out)
    env_base = dict(os.environ)
    lock = threading.Lock()
    done = []

    def work(path):
        rec = run_one(path, package, out, args.timeout, env_base)
        with lock:
            done.append(rec)
            print(f"[{len(done)}/{len(files)}] {rec['file']} exit={rec['exit']} {rec['seconds']}s"
                  f"{' TIMED OUT' if rec['timed_out'] else ''}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        runs = list(pool.map(work, files))
    (out / "runs.json").write_text(json.dumps(runs, indent=1) + "\n", encoding="utf-8")
    red = [r for r in runs if r["exit"] != 0 or r["timed_out"]]
    print(f"ran {len(runs)} test files; red {len(red)}; timed out {sum(r['timed_out'] for r in runs)}", flush=True)
    try:
        measured = cov.Coverage(config_file=str(rc))
        measured.combine(strict=False, keep=False)
        measured.save()
    except Exception as exc:  # NoDataError when nothing was measured; the runs.json is already written
        return refuse(f"coverage combine produced no data ({type(exc).__name__}: {exc}); is the .pth file in place?")
    print(f"combined coverage data: {data_dir / '.coverage'}")
    return 0


# ---------------------------------------------------------------- report

def read_contexts(data_path):
    """{context name: {(product file, line)}} from the combined data. The empty context is NO_CONTEXT."""
    cov = coverage_module()
    if cov is None:
        raise ImportError("the `coverage` module is not importable (pip install coverage==7.16.2)")
    from coverage.sqldata import CoverageData
    data = CoverageData(basename=str(data_path))
    data.read()
    by_ctx = {}
    for fname in data.measured_files():
        short = pathlib.PurePath(fname).as_posix()
        if "/scripts/" in short:
            short = short.rsplit("/scripts/", 1)[1]
        for lineno, ctxs in data.contexts_by_lineno(fname).items():
            for ctx in ctxs:
                by_ctx.setdefault(ctx or NO_CONTEXT, set()).add((short, lineno))
    return by_ctx


def count_statements(data_path):
    """Executable statements of the measured product files (the `product lines total`), or None when no measured
    source file can be read from where the data names it (the report then says unknown, never a number)."""
    cov = coverage_module()
    if cov is None:
        return None
    try:
        measured = cov.Coverage(data_file=str(data_path), config_file=False)
        measured.load()
        names = list(measured.get_data().measured_files())
    except Exception:
        return None
    total, seen = 0, False
    for name in names:
        if not pathlib.Path(name).is_file():
            continue
        try:
            total += len(measured.analysis2(name)[1])
            seen = True
        except Exception:
            continue
    return total if seen else None


def analyse(by_ctx, runs, total_lines=None):
    """The pure core: contexts and run records in, the report dict out."""
    rec = {r["file"]: r for r in runs}
    names = sorted((set(rec) | set(by_ctx)) - {NO_CONTEXT})
    owners = {}
    for ctx, lines in by_ctx.items():
        for line in lines:
            owners.setdefault(line, set()).add(ctx)
    files = []
    for name in names:
        lines = by_ctx.get(name, set())
        r = rec.get(name, {})
        unique = sum(1 for line in lines if owners[line] == {name})
        red = (r.get("exit") not in (0, None)) or bool(r.get("timed_out"))
        status = "not-measured" if not lines else "red" if red else "ok"
        files.append({"file": name, "covered": len(lines), "unique": unique, "seconds": r.get("seconds", 0.0),
                      "exit": r.get("exit"), "timed_out": bool(r.get("timed_out")), "status": status})
    ok = [f for f in files if f["status"] == "ok"]
    # greedy set cover over the ok files
    remaining = {f["file"]: set(by_ctx[f["file"]]) for f in ok}
    secs = {f["file"]: f["seconds"] for f in ok}
    universe = set().union(*remaining.values()) if remaining else set()
    covered, greedy = set(), []
    while remaining:
        best = min(remaining, key=lambda n: (-len(remaining[n] - covered), secs[n], n))
        gain = len(remaining[best] - covered)
        if gain == 0:
            break
        covered |= remaining.pop(best)
        greedy.append({"file": best, "adds": gain, "cumulative_lines": len(covered),
                       "cumulative_share": round(len(covered) / len(universe), 4), "seconds": secs[best]})
    never = sorted(set(secs) - {g["file"] for g in greedy})
    all_lines = set().union(*by_ctx.values()) if by_ctx else set()
    totals = {"test_files": len(files), "ok": len(ok),
              "red": sum(f["status"] == "red" for f in files),
              "not_measured": sum(f["status"] == "not-measured" for f in files),
              "product_lines_covered": len(all_lines),
              "product_lines_total": total_lines,
              "lines_covered_by_ok_files": len(universe),
              "lines_under_no_context": len(by_ctx.get(NO_CONTEXT, ())),
              "ok_files_with_zero_unique": sum(f["unique"] == 0 for f in ok),
              "seconds_of_zero_unique_files": round(sum(f["seconds"] for f in ok if f["unique"] == 0), 2),
              "seconds_all": round(sum(f["seconds"] for f in files), 2),
              "greedy_cover_files": len(greedy)}
    return {"totals": totals, "files": files, "greedy": greedy, "never_needed": never}


def render_md(rep):
    t = rep["totals"]
    out = ["# Test redundancy", "",
           f"- test files: {t['test_files']} (ok {t['ok']}, red {t['red']}, not-measured {t['not_measured']})",
           f"- product lines covered: {t['product_lines_covered']}; by ok files: {t['lines_covered_by_ok_files']}; "
           f"under `{NO_CONTEXT}`: {t['lines_under_no_context']}",
           "- product lines total: " + (str(t["product_lines_total"]) if t.get("product_lines_total") is not None
                                       else "unknown (no measured source file readable where the data names it)"),
           f"- ok files with 0 unique lines: {t['ok_files_with_zero_unique']} "
           f"({t['seconds_of_zero_unique_files']} s of {t['seconds_all']} s in all)",
           f"- greedy cover: {t['greedy_cover_files']} files reach 100% of the lines the ok files cover", "",
           "## A. Deletion candidates: status ok, 0 unique lines, slowest first", "", NOTE, "",
           "| file | covered | seconds |", "|---|---|---|"]
    cand = sorted((f for f in rep["files"] if f["status"] == "ok" and f["unique"] == 0),
                  key=lambda f: (-f["seconds"], f["file"]))
    out += [f"| {f['file']} | {f['covered']} | {f['seconds']} |" for f in cand]
    out += ["", "## B. Greedy set cover over the ok files (share of the lines the ok files cover)", "",
            "| # | file | adds | cumulative lines | cumulative share | seconds |", "|---|---|---|---|---|---|"]
    out += [f"| {i} | {g['file']} | {g['adds']} | {g['cumulative_lines']} | {g['cumulative_share'] * 100:.2f}% | "
            f"{g['seconds']} |" for i, g in enumerate(rep["greedy"], 1)]
    out += ["", f"Ok files the cover never needed ({len(rep['never_needed'])}): " + (", ".join(rep["never_needed"]) or "none"),
            "", "## C. Not measured and red", "", "| file | status | exit | timed out | seconds |", "|---|---|---|---|---|"]
    out += [f"| {f['file']} | {f['status']} | {f['exit']} | {f['timed_out']} | {f['seconds']} |"
            for f in rep["files"] if f["status"] != "ok"]
    return "\n".join(out) + "\n"


def cmd_report(args):
    data_path = pathlib.Path(args.data)
    if not data_path.is_file() or data_path.stat().st_size == 0:
        return refuse(f"the data file {data_path} is missing or empty")
    runs_path = pathlib.Path(args.runs)
    if not runs_path.is_file():
        return refuse(f"the runs file {runs_path} is missing")
    try:
        by_ctx = read_contexts(data_path)
    except ImportError as exc:
        return refuse(str(exc))
    if not by_ctx:
        return refuse(f"the data file {data_path} holds no covered lines")
    rep = analyse(by_ctx, json.loads(runs_path.read_text(encoding="utf-8")), count_statements(data_path))
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "test-redundancy.json").write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    (out / "test-redundancy.md").write_text(render_md(rep), encoding="utf-8")
    t = rep["totals"]
    print("test files {test_files}: ok {ok}, red {red}, not-measured {not_measured}; lines {product_lines_covered}; "
          "ok files with 0 unique lines {ok_files_with_zero_unique} ({seconds_of_zero_unique_files} s); "
          "greedy cover {greedy_cover_files} files; no-context lines {lines_under_no_context}".format(**t))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--package", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--jobs", type=int, default=4)
    r.add_argument("--timeout", type=int, default=900)
    r.add_argument("--only")
    r.add_argument("--keep-only", action="store_true")
    r.add_argument("--force", action="store_true")
    p = sub.add_parser("report")
    p.add_argument("--data", required=True)
    p.add_argument("--runs", required=True)
    p.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    return cmd_run(args) if args.cmd == "run" else cmd_report(args)


if __name__ == "__main__":
    sys.exit(main())
