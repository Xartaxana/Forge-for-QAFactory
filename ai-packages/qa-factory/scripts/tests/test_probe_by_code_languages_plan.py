"""probe_by_code.py: the live probe of a test in ANY language - the PLAN half (B-373 part c, D-0028; split from
test_probe_by_code_languages.py, TD-11c N9).

The seed table of pairs at their positions, the lexer and the body, the candidates and the heads, the guards of the plan, the
report-id tail and the run shape (R6), and the verdict table (R8): every check here runs on bytes in this process, no probe
is launched. The stand-in runner, the language table and the fixtures live in probe_by_code_languages_common.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import copy  # noqa: E402
import re  # noqa: E402
from harness import check, check_eq, check_in, finish  # noqa: E402
import assertion_detectors as AD  # noqa: E402
import probe_by_code as PBC  # noqa: E402
from probe_by_code_languages_common import (WRAP, plan, refusal_of)  # noqa: E402


# (language, pair id, statement, the statement after the inversion)
SEED_PLANS = [
    ("csharp", "X1", "Assert.Equal(4, x);", "Assert.NotEqual(4, x);"),
    ("csharp", "X2", "Assert.NotEqual(4, x);", "Assert.Equal(4, x);"),
    ("csharp", "X3", "Assert.True(x > 0);", "Assert.False(x > 0);"),
    ("csharp", "X4", "Assert.False(x);", "Assert.True(x);"),
    ("csharp", "X5", "Assert.Null(x);", "Assert.NotNull(x);"),
    ("csharp", "X6", "Assert.NotNull(x);", "Assert.Null(x);"),
    ("csharp", "X7", "Assert.Empty(xs);", "Assert.NotEmpty(xs);"),
    ("csharp", "X8", "Assert.NotEmpty(xs);", "Assert.Empty(xs);"),
    ("csharp", "X9", 'Assert.Contains("a", xs);', 'Assert.DoesNotContain("a", xs);'),
    ("csharp", "X10", 'Assert.DoesNotContain("a", xs);', 'Assert.Contains("a", xs);'),
    ("csharp", "X1", "Assert.Equal<int>(4, x);", "Assert.NotEqual<int>(4, x);"),
    ("csharp", "N1", "Assert.That(x, Is.EqualTo(3));", "Assert.That(x, Is.Not.EqualTo(3));"),
    ("csharp", "N2", "Assert.That(x, Is.Not.EqualTo(3));", "Assert.That(x, Is.EqualTo(3));"),
    ("csharp", "N1", 'Assert.That(Foo(1, "a,b"), Is.EqualTo(3));', 'Assert.That(Foo(1, "a,b"), Is.Not.EqualTo(3));'),
    ("csharp", "N3", "ClassicAssert.AreEqual(3, x);", "ClassicAssert.AreNotEqual(3, x);"),
    ("csharp", "N4", "Assert.AreNotEqual(3, x);", "Assert.AreEqual(3, x);"),
    ("java", "J1", "assertEquals(4, x);", "assertNotEquals(4, x);"),
    ("java", "J1", "Assertions.assertEquals(4, x);", "Assertions.assertNotEquals(4, x);"),
    ("java", "J2", "assertNotEquals(4, x);", "assertEquals(4, x);"),
    ("java", "J3", "assertTrue(x > 0);", "assertFalse(x > 0);"),
    ("java", "J4", "Assert.assertFalse(x);", "Assert.assertTrue(x);"),
    ("java", "J5", "assertNull(x);", "assertNotNull(x);"),
    ("java", "J6", "assertNotNull(x);", "assertNull(x);"),
    ("java", "A1", "assertThat(x).isEqualTo(3);", "assertThat(x).isNotEqualTo(3);"),
    ("java", "A1", 'assertThat(x).as("sum").isEqualTo(3);', 'assertThat(x).as("sum").isNotEqualTo(3);'),
    ("java", "A1", 'assertThat(f(a, (b))).describedAs("s(%s)", y).isEqualTo(3);',
     'assertThat(f(a, (b))).describedAs("s(%s)", y).isNotEqualTo(3);'),
    ("java", "A2", "assertThat(x).isNotEqualTo(3);", "assertThat(x).isEqualTo(3);"),
    ("java", "A3", "assertThat(b).isTrue();", "assertThat(b).isFalse();"),
    ("java", "A4", "assertThat(b).isFalse();", "assertThat(b).isTrue();"),
    ("java", "A5", "assertThat(o).isNull();", "assertThat(o).isNotNull();"),
    ("java", "A6", "assertThat(o).isNotNull();", "assertThat(o).isNull();"),
    ("java", "A7", 'assertThat(xs).contains("a");', 'assertThat(xs).doesNotContain("a");'),
    ("java", "A8", 'assertThat(xs).doesNotContain("a");', 'assertThat(xs).contains("a");'),
    ("typescript", "T1", "expect(x).not.toBe(3);", "expect(x).toBe(3);"),
    ("typescript", "T1", "await expect(p).resolves.not.toBe(3);", "await expect(p).resolves.toBe(3);"),
    ("typescript", "T2", "expect(x).toBe(3);", "expect(x).not.toBe(3);"),
    ("typescript", "T2", "expect.soft(x).toBe(3);", "expect.soft(x).not.toBe(3);"),
    ("typescript", "T2", "await expect(p).rejects.toThrow('x');", "await expect(p).rejects.not.toThrow('x');"),
    ("typescript", "T2", "expect(x).toBe(3)", "expect(x).not.toBe(3)"),
]


def seed_table_plans() -> None:
    """Every pair of the seed table is applied at its position, on its own shape, and only there."""
    covered = set()
    for lang, pair_id, stmt, after in SEED_PLANS:
        source = WRAP[lang][0].replace("{stmt}", stmt)
        mutated, detail, _ctx = plan(lang, source)
        label = f"{lang} {pair_id}: {stmt}"
        # the statement starts at the HEAD: a leading `await` is outside it (and untouched)
        check_eq(f"{label}: the inverted statement", detail["statement_after"], after.replace("await ", "", 1) if stmt.startswith("await ") else after)
        check_eq(f"{label}: the pair of the table (by its id)", detail["pair_id"], pair_id)
        check_eq(f"{label}: only that statement changed", mutated.decode("utf-8").replace(after, stmt, 1), source)
        check_eq(f"{label}: the same number of lines", mutated.count(b"\n"), source.count("\n"))
        check_eq(f"{label}: style, language and the invert mutation", (detail["style"], detail["language"], detail["mutation"]),
                 ("detector", lang, "invert"))
        check_in(f"{label}: the marker carries the instance, the statement and the fires_as", "probe-IID invert: " + stmt.replace("await ", "", 1)[:20],
                 detail["marker"])
        check_in(f"{label}: ...and `fires as /`", " fires as /", detail["marker"])
        check_eq(f"{label}: the fires_as of the record is the pair's own",
                 detail["fires_as"], next(p["fires_as"] for _l, e in AD.assertion_detectors().items() for f in e["assertions"]
                                          for p in (f["invert"] or []) if p.get("id") == pair_id))
        covered.add(pair_id)
    every = {p["id"] for e in AD.assertion_detectors().values() for f in e["assertions"] for p in (f["invert"] or [])}
    check_eq("every pair of the table has a plan above", sorted(every - covered), [])


def lexer_and_body() -> None:
    cs_body = "        {\n            %s\n            Assert.Equal(4, x);\n        }\n"

    def cs(first: str, name: str = "Adds") -> str:
        return ("namespace A\n{\n    public class T\n    {\n        // Assert.Null(a);\n        /* Assert.Null(b);\n           \" */\n"
                f"        public void {name}()\n" + cs_body % first + "    }\n}\n")

    # E8: an assertion in a comment or a string is never the first assertion
    for label, first in (("a line comment", "// Assert.Null(a);"), ("a block comment", "/* Assert.Null(a); */"),
                         ("a string", 'var s = "Assert.Null(a);";'), ("a verbatim string with a doubled quote",
                                                                      'var s = @"x ""Assert.Null(a);"" y";'),
                         ("a raw string", 'var s = """Assert.Null(a); " quotes """;'), ("a char literal", "var c = '{';")):
        _m, detail, _c = plan("csharp", cs(first), node="t/T.cs::T.Adds")
        check_eq(f"E8 ({label}): the first assertion is the real one", detail["statement_after"], "Assert.NotEqual(4, x);")
    # an apostrophe in a comment does not open a char literal; a brace in a string is not a brace
    _m, detail, _c = plan("csharp", cs("// it's here\n            var b = \"}{\";"), node="t/T.cs::T.Adds")
    check_eq("an apostrophe in a comment and braces in a string do not move the body", detail["statement_after"],
             "Assert.NotEqual(4, x);")
    # a declaration inside a comment or a string is not a candidate
    text = cs("var a = 1;").replace("// Assert.Null(a);", "// public void Adds() {")
    check_eq("E3: a declaration in a comment is not a candidate", plan("csharp", text, node="t/T.cs::T.Adds")[1]["candidates"],
             [8])
    # a file the lexer cannot read to its end, or whose brackets do not balance, is refused
    text = cs("var a = 1;") + '\n/* never closed'
    check_in("an unterminated block comment is refused", "inside a block comment", refusal_of(lambda: plan("csharp", text, node="t/T.cs::T.Adds")))
    text = cs("var a = 1;") + '\nvar s = "never closed;'
    check_in("an unterminated string is refused", "inside a string literal", refusal_of(lambda: plan("csharp", text, node="t/T.cs::T.Adds")))
    text = cs("var a = 1;").replace("        }\n    }\n}\n", "        }\n    }\n")
    check_in("unbalanced brackets are refused, naming the line", "do not balance at line",
             refusal_of(lambda: plan("csharp", text, node="t/T.cs::T.Adds")))
    # TypeScript (F1b): a regex literal is lexed as one - its quote opens no string
    ts = "describe('c', () => {\n  test('adds', () => {\n    const r = /\"/;\n    expect(x).toBe(3);\n  });\n});\n"
    check_eq("TS: a regex literal holding a quote is a literal (the lexer reads it, no refusal)",
             plan("typescript", ts)[1]["statement_after"], "expect(x).not.toBe(3);")
    ts ="describe('c', () => {\n  test('adds', () => {\n    const s = `a ${b} }`;\n    expect(x).toBe(3);\n  });\n});\n"
    check_eq("TS: a template literal with a brace in it is one string", plan("typescript", ts)[1]["statement_after"],
             "expect(x).not.toBe(3);")

    # F1 (i): a quote the lexer takes for an opener that is none (a regex literal `/can't/`) pairs up with the NEXT
    # quote, and everything between is misread: a head can then sit "in code" that is really a string. A `'` or `"`
    # string cannot cross a line break (`multiline: false`), which is how that misreading shows
    # (the regex literal itself is lexed as one since F1b; an apostrophe in text the lexer does not know - JSX text -
    # still opens a "string", and that string crosses the line)
    ts_trap = ("describe('c', () => {\n  test('adds', () => {\n    const t = <b>don't</b>;\n"
               "    const label = 'expect(a).toBe(1)'; // don't\n    expect(sum(1, 2)).toBe(3);\n  });\n});\n")
    message = refusal_of(lambda: plan("typescript", ts_trap))
    check_in("F1 (i): an apostrophe in JSX text (a string the lexer cannot know) is refused", "single-line string that crosses a line break", message)
    check_in("F1 (i): naming the line the string opens at", "opens at line 3", message)
    check_in("F1 (i): and that nothing was changed", "Nothing was changed", message)
    # F1b: the critic's input on ONE line. The regex literal `/can't/` is a literal, so the apostrophe opens no
    # string, `'expect(a).toBe(1)'` stays a string, and no head is ever planned INSIDE it
    def body(*lines):
        return "describe('c', () => {\n  test('adds', () => {\n" + "".join(f"    {line}\n" for line in lines) + "  });\n});\n"

    trap = "const r = /can't/; const label = 'expect(a).toBe(1)'; // don't"
    message = refusal_of(lambda: plan("typescript", body(trap)))
    check_in("F1b (i): the string holds the only `expect`: no head at all, a refusal - never a write inside the string",
             "no recognised assertion", message)
    source = body(trap, "expect(x).toBe(2);")
    mutated, detail, _c = plan("typescript", source)
    check_eq("F1b (ii): a real head after the one-line trap is found and planned", detail["statement_after"], "expect(x).not.toBe(2);")
    check_eq("F1b (ii): the string literal is byte-identical in the plan, only the real statement changed",
             (mutated.decode().count("'expect(a).toBe(1)'"), mutated.decode().replace("expect(x).not.toBe(2);", "expect(x).toBe(2);")),
             (1, source))
    division = "const h = a / b; const s = 'expect(a).toBe(1)'; expect(h).toBe(2);"
    mutated, detail, _c = plan("typescript", body(division))
    check_eq("F1b (iii): a division stays a division: the plan targets `expect(h).toBe(2)`, never the string",
             detail["statement_before"], "expect(h).toBe(2);")
    check_eq("F1b (iii): ...and the string is intact", "'expect(a).toBe(1)'" in mutated.decode(), True)
    check_eq("F1b (iv): `x = y /g/ 2` is division after an identifier, then a division again: code",
             plan("typescript", body("const x = y /g/ 2; const s = 'expect(a).toBe(1)'; expect(x).toBe(2);"))[1]["statement_before"],
             "expect(x).toBe(2);")
    check_eq("F1b (iv): a division after `)` and after `]` too",
             plan("typescript", body("const k = (a) / 2 + b[0] / 3; const s = 'expect(a).toBe(1)'; expect(k).toBe(2);"))[1]["statement_before"],
             "expect(k).toBe(2);")
    check_eq("F1b (v): a class holding a slash does not close the literal (`/[/]'/`)",
             plan("typescript", body("const r = /[/]'/; const s = 'expect(a).toBe(1)'; expect(r).toBe(2);"))[1]["statement_before"],
             "expect(r).toBe(2);")
    check_eq("F1b (v): an escaped slash does not close it either (`/a\\/'b/`)",
             plan("typescript", body("const r = /a\\/'b/; const s = 'expect(a).toBe(1)'; expect(r).toBe(2);"))[1]["statement_before"],
             "expect(r).toBe(2);")
    check_eq("F1b: after the word `return` a `/` opens a literal",
             plan("typescript", body("const f = () => { return /it's/.test(s); }; const s = 'expect(a).toBe(1)'; expect(f).toBe(2);"))[1]
             ["statement_before"], "expect(f).toBe(2);")
    message = refusal_of(lambda: plan("typescript", body("const r = /abc", "expect(x).toBe(2);")))
    check_in("F1b (vi): an unterminated regex literal is refused, naming its line", "regex literal that opens at line 3 and does not "
             "close on its line", message)
    check_in("F1b (vi): and that nothing was changed", "Nothing was changed", message)
    check_eq("F1b: the regex rule is TS's: a `/` in a C# file is a division (no regex_literal key)",
             plan("csharp", WRAP["csharp"][0].replace("{stmt}", "var h = a / b; var q = (a) /c/ d; Assert.Equal(4, h);"))[1][
                 "statement_before"], "Assert.Equal(4, h);")
    cs_trap = ("namespace A\n{\n  class T\n  {\n    public void Adds()\n    {\n      var s = \"opens here;\n"
               "      and closes there\";\n      Assert.Equal(4, x);\n    }\n  }\n}\n")
    check_in("F1 (i): a C# string that crosses a line break is refused too", "single-line string that crosses a line break",
             refusal_of(lambda: plan("csharp", cs_trap, node="t/T.cs::T.Adds")))
    java_trap = "class C {\n  @Test void adds() {\n    char c = '\n';\n    assertEquals(4, x);\n  }\n}\n"
    check_in("F1 (i): a Java char literal that crosses a line break is refused too", "single-line string that crosses a line break",
             refusal_of(lambda: plan("java", java_trap, node="t/C.java::C.adds")))
    ok_strings = ("describe('c', () => {\n  test('adds', () => {\n    const a = 'one \\\n two';\n    const t = `x\n y ${a}`;\n"
                  "    expect(sum(1, 2)).toBe(3);\n  });\n});\n")
    check_eq("F1 (i) control: a backslash-newline continuation and a template literal MAY cross lines",
             plan("typescript", ok_strings)[1]["statement_after"], "expect(sum(1, 2)).not.toBe(3);")
    check_eq("F1 (i) control: a C# verbatim string may cross lines",
             plan("csharp", WRAP["csharp"][0].replace("{stmt}", 'var s = @"a\nb"; Assert.Equal(4, x);'))[1]["statement_after"],
             "Assert.NotEqual(4, x);")
    # F1 (ii): a conditional-compilation directive: every branch lexes as code, one is compiled
    cs_if = ("namespace A\n{\n  class T\n  {\n    public void Adds()\n    {\n#if NET6\n      Assert.Equal(4, x);\n#else\n"
             "      Assert.Equal(5, x);\n#endif\n    }\n  }\n}\n")
    for at in (None, 8, 10):
        message = refusal_of(lambda: plan("csharp", cs_if, node="t/T.cs::T.Adds", at=at))
        check_in(f"F1 (ii): #if/#else/#endif is refused, naming the directive and its line (--at {at})",
                 "conditional-compilation directive `#if NET6` at line 7", message)
    check_in("F1 (ii): the door is the data row / the product probe, not --at", "red_sandbox.py --probe", message)
    check_in("F1 (ii): and it is not a verdict on the test", "not a verdict on the test", message)
    check_in("F1 (ii): a directive OUTSIDE the test is refused too (the whole method may be inactive)", "`#if DEBUG` at line 1",
             refusal_of(lambda: plan("csharp", "#if DEBUG\n" + WRAP["csharp"][0].replace("{stmt}", "Assert.Equal(4, x);") + "#endif\n")))
    region = WRAP["csharp"][0].replace("{stmt}", "#region r\n            Assert.Equal(4, x);\n            #endregion // #if Y")
    check_eq("F1 (ii) control: `#region` and a `#if` inside a comment are no directive",
             plan("csharp", region)[1]["statement_after"], "Assert.NotEqual(4, x);")
    # E4: the body is the block that opens right after the parameter list - never the first `{`
    java = "class C {\n    @Test(expected = {X.class})\n    void adds(int[] a, Map<String, int[]> m) throws Exception, Other {\n        assertEquals(4, x);\n    }\n}\n"
    check_eq("method style: the body opens after the balanced parameter list and a `throws` list",
             plan("java", java, node="t/C.java::C.adds")[1]["statement_after"], "assertNotEquals(4, x);")
    for label, text in (("a C# `=>` expression body", "class T {\n  public void Adds() => Assert.Equal(1, 1);\n}\n"),
                        ("an interface declaration", "interface T {\n  void Adds();\n}\n")):
        lang, node = ("csharp", "t/T.cs::T.Adds") if "C#" in label else ("java", "t/T.java::T.Adds")
        message = refusal_of(lambda: plan(lang, text, node=node))
        check_in(f"E4 ({label}): refused, naming the shape", "no block opens where the body", message)
        check_in(f"E4 ({label}): and that nothing was mutated", "never mutated", message)
    # call style: the first body_open at depth 1; the Playwright destructuring brace is not the body (the first `{`)
    pw = "test('adds', async ({ page }) => {\n  await expect(page).toHaveTitle('x');\n});\n"
    _m, detail, _c = plan("typescript", pw)
    check_eq("E4 (call style): `({ page }) => {` - the body is the block after `=>`, not the first `{`",
             (detail["statement_after"], detail["line"]), ("expect(page).not.toHaveTitle('x');", 2))
    tag = "test('adds', { tag: '@smoke' }, async ({ page }) => {\n  await expect(page).toHaveTitle('x');\n});\n"
    check_eq("E4 (call style): an options object with a tag does not move the body",
             plan("typescript", tag)[1]["statement_after"], "expect(page).not.toHaveTitle('x');")
    fn = "test('adds', async function () {\n  expect(x).toBe(3);\n});\n"
    check_eq("E4 (call style): a `function` callback is a body too", plan("typescript", fn)[1]["line"], 2)
    for label, text in (("a concise arrow", "test('adds', () => expect(x).toBe(3));\n"),
                        ("a nested arrow at depth 2", "test('adds', wrap(() => {\n  expect(x).toBe(3);\n}));\n"),
                        ("no callback", "test('adds');\n")):
        message = refusal_of(lambda: plan("typescript", text))
        check_in(f"E4 ({label}): refused, naming the shape", "no block opens where the body", message)
    # `test.each` / a template title with a substitution are not a literal title
    # EP1-36 (named to the critic): the pin was a refusal for EVERY `${` title. It now holds for an entry WITHOUT `title_template`
    # (the old behaviour, kept); the typescript entry has one, so its templated title is a pattern and `template` is set.
    real = AD.assertion_detectors

    def without_template():
        doc = copy.deepcopy(real())
        doc["typescript"].pop("title_template", None)
        return doc
    AD.assertion_detectors = without_template
    try:
        check_in("a title with a `${` substitution is refused by an entry that has no `title_template`", "template substitution",
                 refusal_of(lambda: PBC.parse_node("t/x.test.ts::adds ${n}")))
    finally:
        AD.assertion_detectors = real
    check_eq("EP1-36: the typescript entry reads the title as a pattern", PBC.parse_node("t/x.test.ts::adds ${n}").get("template"), True)


def candidates_and_heads() -> None:
    def many(n: int) -> str:
        body = "".join(f"    public class C{i}\n    {{\n        public void Adds()\n        {{\n            Assert.Equal({i}, x);\n        }}\n    }}\n"
                       for i in range(n))
        return "namespace A\n{\n" + body + "}\n"

    node = "t/T.cs::Adds"
    message = refusal_of(lambda: plan("csharp", many(1) + "", node=node)) or "ok"
    check_eq("one declaration: no refusal", message, "ok")
    for count in (2, 5, 6, 9):
        message = refusal_of(lambda: plan("csharp", many(count), node=node))
        listed = len(re.findall(r"line \d+", message))
        check_in(f"E3 ({count} declarations): refused, with the door --at <line>", "--at <line>", message)
        check_eq(f"E3 ({count} declarations): at most 5 candidate lines are listed", listed, min(count, 5))
        check_eq(f"E3 ({count} declarations): 'and N more' only beyond 5",
                 re.search(r"and (\d+) more", message).group(1) if "more" in message else "", "" if count <= 5 else str(count - 5))
        check_in(f"E3 ({count} declarations): nothing was changed", "Nothing was changed", message)
    _m, detail, _c = plan("csharp", many(3), node=node, at=14)
    check_eq("--at picks the candidate whose body holds the line (and the head that starts there)",
             (detail["statement_after"], detail["at"], detail["candidates"]), ("Assert.NotEqual(1, x);", 14, [5, 12, 19]))
    check_eq("...the first body", plan("csharp", many(3), node=node, at=7)[1]["statement_after"], "Assert.NotEqual(0, x);")
    check_in("--at in no body is refused", "lies in 0 of the 3 bodies", refusal_of(lambda: plan("csharp", many(3), node=node, at=1)))
    check_in("--at on a line that starts no assertion is refused", "no recognised assertion starts on line 13",
             refusal_of(lambda: plan("csharp", many(3), node=node, at=13)))
    check_in("no declaration: refused, saying which pattern and where the row is", "no declaration of 'Nope'",
             refusal_of(lambda: plan("csharp", many(2), node="t/T.cs::Nope")))
    # E6: no recognised assertion
    body = "class T {\n  void Adds() {\n    var a = 1;\n    Helpers.Expect(a);\n  }\n}\n"
    message = refusal_of(lambda: plan("csharp", body, node="t/T.cs::T.Adds"))
    check_in("E6: no assertion in the body: refused, naming --oracle", "--oracle", message)
    check_in("E6: ... and the data door (add a head)", "references/detectors.json assertion_probes.csharp", message)
    # E7: the first assertion is a form with invert null: refused, never a later one
    text = "class T {\n  void Adds() {\n    Assert.Throws<E>(() => Foo());\n    Assert.Equal(4, x);\n  }\n}\n"
    message = refusal_of(lambda: plan("csharp", text, node="t/T.cs::T.Adds"))
    check_in("E7: the first assertion has no inversion: refused, naming it", "`Assert.Throws` at line 3", message)
    check_in("E7: ... and that it never skips to a later one", "never skips to a later assertion", message)
    _m, detail, _c = plan("csharp", text, node="t/T.cs::T.Adds", at=4)
    check_eq("E7 door: --at names the later assertion", detail["statement_after"], "Assert.NotEqual(4, x);")
    # E7: a recognised form with no pair at its position: refused (Hamcrest assertThat(x, is(y)), a chain)
    text = "class C {\n  @Test void adds() {\n    assertThat(x, is(3));\n    assertEquals(1, 1);\n  }\n}\n"
    message = refusal_of(lambda: plan("java", text, node="t/C.java::C.adds"))
    check_in("E7: Hamcrest assertThat(x, is(y)): no pair matches at its position - refused", "no inversion pair", message)
    text = "class C {\n  @Test void adds() {\n    assertThat(x).extracting(\"a\").isEqualTo(3);\n  }\n}\n"
    check_in("E7 (`find` is matched AT the position, never searched over the statement): a later `.isEqualTo` is not inverted",
             "no inversion pair", refusal_of(lambda: plan("java", text, node="t/C.java::C.adds")))
    text = "describe('c', () => {\n  it('adds', () => {\n    expect(x).toEqual(3);\n    expect(y).not.toBe(2);\n  });\n});\n"
    check_eq("E7: Chai-free TS `.toEqual` is a plain pair", plan("typescript", text, node="t/x.test.ts::adds")[1]["statement_after"],
             "expect(x).not.toEqual(3);")
    text = "describe('c', () => {\n  it('adds', () => {\n    expect(x).to.equal(3);\n  });\n});\n"
    check_in("E7: Chai `.to.equal` matches no pair: refused", "no inversion pair",
             refusal_of(lambda: plan("typescript", text, node="t/x.test.ts::adds")))
    # a multi-line chain: `find`'s `\\s*` would eat the line break - refused with the pair named (a known data gap)
    text = "class C {\n  @Test void adds() {\n    assertThat(x)\n        .isEqualTo(3);\n  }\n}\n"
    message = refusal_of(lambda: plan("java", text, node="t/C.java::C.adds"))
    check_in("a chain split over lines: refused because the pair would move a line", "would change the line breaks", message)
    check_in("...naming the pair", "pair A1", message)
    # the statement extents: `;` outside any bracket; a TS newline that no continuation covers
    text = "class T {\n  void Adds() {\n    Assert.Equal(4,\n        Foo(1, 2));\n    Assert.True(y);\n  }\n}\n"
    _m, detail, _c = plan("csharp", text, node="t/T.cs::T.Adds")
    check_eq("a statement over two lines: extent and the line count kept", (detail["line"], detail["end_line"]), (3, 4))
    ts = "describe('c', () => {\n  it('adds', () => {\n    expect(a)\n      .toBe(3)\n    expect(b).toBe(4)\n  });\n});\n"
    _m, detail, _c = plan("typescript", ts)
    check_eq("TS: a chain continued on the next line is ONE statement; the newline after it ends it",
             (detail["line"], detail["end_line"], detail["statement_after"]), (3, 4, "expect(a).not\n      .toBe(3)"))
    ts = "describe('c', () => {\n  it('adds', () => {\n    expect(a).toBe(3) // note\n    expect(b).toBe(4)\n  });\n});\n"
    check_eq("TS: a trailing comment is not part of the statement", plan("typescript", ts)[1]["statement_after"],
             "expect(a).not.toBe(3)")
    ts = "describe('c', () => {\n  it('adds', () => {\n    expect(a).toBe(3)\n  });\n});\n"
    check_eq("TS: the last statement of the block, with no `;`", plan("typescript", ts)[1]["statement_after"],
             "expect(a).not.toBe(3)")
    check_in("C#: a statement the block closes over is refused (`;` demanded)", "is not ended by `;`",
             refusal_of(lambda: plan("csharp", "class T {\n  void Adds() {\n    Assert.Equal(4, x)\n  }\n}\n", node="t/T.cs::T.Adds")))


def plan_guards() -> None:
    doc = AD.assertion_detectors()
    # A2: a fires_as that matches the mutated statement itself is refused (the run's own text could fire it)
    entry = copy.deepcopy(doc["typescript"])
    entry["assertions"][0]["invert"][1]["fires_as"] = "^expect"
    text = WRAP["typescript"][0].replace("{stmt}", "expect(x).toBe(3);")
    message = refusal_of(lambda: plan("typescript", text, entry=entry))
    check_in("A2: refused when fires_as matches statement_after", "would also match the mutated statement's own text", message)
    check_in("A2: naming the pair", "pair T2", message)
    check_eq("A2 control: the shipped pair is fine on the same text", plan("typescript", text)[1]["pair_id"], "T2")
    # A2, the real-world shape: a subject named `received`
    text = WRAP["typescript"][0].replace("{stmt}", "expect(received).toBe(3);")
    check_in("A2: a subject literally named `received` makes T2's text match the mutated statement: refused",
             "would also match the mutated statement's own text", refusal_of(lambda: plan("typescript", text)))
    text = WRAP["typescript"][0].replace("{stmt}", "expect(page).toHaveTitle('x');")
    check_eq("A2 control: `expect(page)` is not `expect(received)`: planned", plan("typescript", text)[1]["pair_id"], "T2")
    # R5: `find` is applied with `re.match` at exactly the form's position - even a `find` the data wrote WITHOUT
    # the `^` the seed rows carry is never searched for over the rest of the statement
    entry = copy.deepcopy(doc["csharp"])
    form = next(f for f in entry["assertions"] if f["matcher_at"] == "second_arg")
    form["invert"][0]["find"] = "Is\\.(?!Not\\b)"
    nested = WRAP["csharp"][0].replace("{stmt}", "Assert.That(x, Foo(Is.EqualTo(1)));")
    check_in("R5: a `find` with no `^` is matched at the position, not found later in the statement",
             "no inversion pair", refusal_of(lambda: plan("csharp", nested, entry=entry)))
    plain = WRAP["csharp"][0].replace("{stmt}", "Assert.That(x, Is.EqualTo(1));")
    check_eq("R5 control: the same `find` at the second argument itself is applied",
             plan("csharp", plain, entry=entry)[1]["statement_after"], "Assert.That(x, Is.Not.EqualTo(1));")
    # E9: the newline count / the breaks / the brackets
    entry = copy.deepcopy(doc["csharp"])
    entry["assertions"][0]["invert"][0]["replace"] = "Assert.NotEqual(\n"
    text = WRAP["csharp"][0].replace("{stmt}", "Assert.Equal(4, x);")
    check_in("E9: a replacement that adds a line break is refused", "would change the line breaks",
             refusal_of(lambda: plan("csharp", text, entry=entry)))
    entry = copy.deepcopy(doc["csharp"])
    entry["assertions"][0]["invert"][0]["replace"] = "Assert.NotEqual(("
    check_in("E9: a replacement that unbalances the brackets is refused", "bracket balance",
             refusal_of(lambda: plan("csharp", text, entry=entry)))
    entry = copy.deepcopy(doc["csharp"])
    entry["assertions"][0]["invert"][0]["replace"] = "Assert.NotEqual /* "
    check_in("E9: a replacement that opens a comment (lexical state) is refused", "bracket balance or the lexical state",
             refusal_of(lambda: plan("csharp", text, entry=entry)))
    # E21: BOM and CRLF kept; a non-UTF-8 file refused
    source = WRAP["csharp"][0].replace("{stmt}", "Assert.Equal(4, x);")
    crlf = source.replace("\n", "\r\n").encode("utf-8")
    mutated, detail, _c = plan("csharp", crlf)
    check_eq("E21: CRLF line ends are kept byte for byte", mutated, crlf.replace(b"Assert.Equal", b"Assert.NotEqual", 1))
    check_eq("E21: and the line numbers read `\\r\\n` as one break", detail["line"], 10)
    bom = b"\xef\xbb\xbf" + crlf
    mutated, detail, _c = plan("csharp", bom)
    check_eq("E21: a BOM is kept", mutated, bom.replace(b"Assert.Equal", b"Assert.NotEqual", 1))
    check_eq("E21: and does not move a line", detail["line"], 10)
    lone = source.replace("\n", "\r").encode("utf-8")
    check_eq("E21: a lone CR is a line break too", plan("csharp", lone)[1]["line"], 10)
    check_in("E21: a file that is not UTF-8 is refused", "is not UTF-8",
             refusal_of(lambda: plan("csharp", b"class T {\n  void Adds() {\n    Assert.Equal(1, \xff);\n  }\n}\n", node="t/T.cs::T.Adds")))
    check_in("E21: a non-UTF-8 file is named, nothing was changed", "Nothing was changed",
             refusal_of(lambda: plan("csharp", b"\xff\xfe", node="t/T.cs::T.Adds")))


def tail_and_names() -> None:
    cs = AD.assertion_detectors()["csharp"]
    java = AD.assertion_detectors()["java"]
    ts = AD.assertion_detectors()["typescript"]
    ok = PBC._tail_matches
    check("R6(c): the id ends with the tail, after a dot", ok("Acme.Tests.CalcTests.Adds", "CalcTests.Adds", cs))
    check("R6(c): the id IS the tail", ok("CalcTests.Adds", "CalcTests.Adds", cs))
    check("R6(c): a method name alone", ok("Acme.CalcTests.Adds", "Adds", cs))
    check("R6(c): a trailing (...) of the id is stripped", ok("Acme.CalcTests.Adds(a: 1, b: (2))", "CalcTests.Adds", cs))
    check("R6(c): `::` of a JUnit id is the tail's join", ok("com.acme.CalcTest::adds()", "CalcTest.adds", java))
    check("R6(c): a TS id `a b::a b` ends with the title after a space", ok("calc adds::calc adds", "adds", ts))
    check("R6(c): a Vitest row name with ` > ` separators", ok("Calc > adds", "Calc adds", ts))
    check("R6(c): whitespace is folded on both sides", ok("calc   adds", "calc adds", ts))
    check("R6(c) the boundary is a character of `.  /:`: `/` counts", ok("src/sum.test.ts/adds", "adds", ts))
    check("R6(c) the boundary: `:` counts", ok("file.cs:Adds", "Adds", cs))
    check("R6(c): a different method does not match", not ok("Acme.CalcTests.AddsMore", "Adds", cs))
    check("R6(c): a longer method name ending in the tail does not match (no boundary)", not ok("Acme.CalcTests.MyAdds", "Adds", cs))
    check("R6(c): the class decides when it is given", not ok("Acme.OtherTests.Adds", "CalcTests.Adds", cs))
    check("R6(c): an empty id matches nothing", not ok("", "Adds", cs))
    check("R6(c): a title that really ends in `)` is still found (both spellings are tried)", ok("calc returns f()", "returns f()", ts))
    # F2: for a call-style entry the join and the boundary are both a space, so the id of `calc does not adds` also
    # "ends with" `adds`; another test of the file whose LONGER title the id ends with is refused
    two = ("describe('calc', () => {\n  test('adds', () => {\n    expect(a).toBe(1);\n  });\n"
           "  test('does not adds', () => {\n    expect(a).toBe(1);\n  });\n  it('more things', () => {\n    expect(a).toBe(1);\n  });\n});\n")
    longer = PBC._longer_title
    check("F2 (the premise): the plain tail check passes for the OTHER test's id", ok("calc does not adds::calc does not adds", "adds", ts))
    check_eq("F2: the report id of the longer-titled test is caught, with the title and its line",
             longer(two, ts, "adds", "calc does not adds::calc does not adds"), ("does not adds", 5))
    check_eq("F2 control: the id of the test itself is not", longer(two, ts, "adds", "calc adds::calc adds"), ("", 0))
    check_eq("F2 control: another title that does not end with the tail is not", longer(two, ts, "adds", "calc more things::calc more things"), ("", 0))
    check_eq("F2 control: a file with one title has no other", longer(two.split("  test('does not adds'")[0] + "});\n", ts, "adds",
                                                                      "calc does not adds::x"), ("", 0))
    check_eq("F2: the longer title is found by its own tail too (`does not adds` is not refused for itself)",
             longer(two, ts, "does not adds", "calc does not adds::calc does not adds"), ("", 0))
    check_eq("F2: a comment or a string holding a declaration is no other test",
             longer(two.replace("  test('does not adds', () => {\n    expect(a).toBe(1);\n  });\n",
                                "  // test('does not adds', () => {\n  //   expect(a).toBe(1);\n  // });\n"),
                    ts, "adds", "calc does not adds::x"), ("", 0))
    # parse_node: the tail, the name and the segments
    spec = PBC.parse_node("tests\\CalcTests.cs::Acme.Tests.CalcTests.Adds")
    check_eq("parse: backslashes are slashes, the name is the last segment", (spec["file"], spec["function"], spec["language"]),
             ("tests/CalcTests.cs", "Adds", "csharp"))
    check_eq("parse: the tail is the segments joined by tail_join", spec["tail"], "Acme.Tests.CalcTests.Adds")
    spec = PBC.parse_node("t/Outer.cs::Outer+Inner.Adds(a: 1)")
    check_eq("parse: `+` separates nested classes; a trailing (...) of the name is stripped", (spec["function"], spec["tail"]),
             ("Adds", "Outer.Inner.Adds"))
    spec = PBC.parse_node("t/CalcTest.java::CalcTest#adds")
    check_eq("parse: `#` separates a Java class from its method", (spec["function"], spec["chain"]), ("adds", ["CalcTest"]))
    spec = PBC.parse_node("t/x.test.ts::adds two  numbers")
    check_eq("parse: a TS title keeps its words (folded), no separator splits it", (spec["function"], spec["tail"]),
             ("adds two numbers", "adds two numbers"))
    check_in("parse: a method name that is not an identifier is refused", "not an identifier",
             refusal_of(lambda: PBC.parse_node("t/T.cs::T.Adds Two")))
    check_in("parse: nothing after `::` is refused", "nothing follows", refusal_of(lambda: PBC.parse_node("t/T.cs::::")))
    check_eq("parse: a Python node carries its language, entry and tail since N3b (reader stays `ast`)",
             (lambda s: (s["language"], s["reader"], s["tail"], bool(s["entry"]["forms"])))(PBC.parse_node("tests/test_calc.py::TestX::test_y[p]")),
             ("python", "ast", "TestX::test_y", True))
    check_eq("parse: .PY (upper case) is not Python's path and has no entry",
             "no assertion probe" in refusal_of(lambda: PBC.parse_node("tests/test_calc.PY::test_y")), True)
    check_eq("E10 (the interim rule): a file under roots.test and no protected path",
             PBC._in_test_root({"profiles": [{"roots": {"test": "tests"}}], "app_root": ".", "protected_app_paths": ["src"]},
                               "tests/Helpers.cs"), True)
    for label, cfg, rel in (("outside every test root", {"profiles": [{"roots": {"test": "tests"}}]}, "src/Calc.cs"),
                            ("under a protected path", {"profiles": [{"roots": {"test": "tests"}}], "protected_app_paths": ["tests/app"]},
                             "tests/app/Calc.cs"),
                            ("under a protected path given relative to app_root",
                             {"profiles": [{"roots": {"test": "backend/tests"}}], "app_root": "backend", "protected_app_paths": ["tests/app"]},
                             "backend/tests/app/x.cs"),
                            ("with no test root at all", {"profiles": []}, "tests/x.cs"),
                            ("when everything is protected", {"profiles": [{"roots": {"test": "tests"}}], "protected_app_paths": ["."]},
                             "tests/x.cs"),
                            ("only a prefix of a root's name", {"profiles": [{"roots": {"test": "tests"}}]}, "tests2/x.cs")):
        check_eq(f"E10: {label} is not an oracle place", PBC._in_test_root(cfg, rel), False)


def verdict_table() -> None:
    entry = AD.assertion_detectors()["csharp"]
    detail = {"line": 11, "end_line": 12, "language": "csharp", "candidates": [8], "at": None, "pair": 0, "pair_id": "X1",
              "fires_as": "^Assert\\.NotEqual\\(\\) Failure"}
    msg = "Assert.NotEqual() Failure: Values are equal\nExpected: Not 4"

    def row(status, message=msg, text="", kind="failure"):
        # a skipped row holds no failure or error problem (a row that does is `failed`, never read as not executed, t-2045 E-P)
        problems = [] if status in ("passed", "not_run", "skipped") else [{"kind": kind, "message": message, "text": text}]
        return {"test_id": "x", "status": status, "problems": problems}

    def site(line=11, kind="assertion", **extra):
        return dict({"location": f"tests/CalcTests.cs:{line}", "failure_kind": kind, "frame": "  at X"}, **extra)

    unread = {"site_unread": "trx/csharp", "reason": "no frame matched"}
    dotnet, wrapper = ["dotnet", "test", "--filter", "x"], ["bash", "run.sh"]

    def judge(r, s, d=None, *, among=False, argv=dotnet, e=entry):
        return PBC.judge_probe_row(r, s, e, d or detail, among=among, argv=argv)

    cells = [
        ("passed + --at among 2+ candidates", judge(row("passed"), {}, dict(detail, candidates=[8, 20], at=15), among=True), "incomplete"),
        ("passed + compiled + a wrapper launcher (F9)", judge(row("passed"), {}, argv=wrapper), "incomplete"),
        ("passed + compiled + no launcher at all", judge(row("passed"), {}, argv=[]), "incomplete"),
        ("passed + compiled + launcher builds by default", judge(row("passed"), {}), "no_failure"),
        ("passed + .exe launcher is the same launcher", judge(row("passed"), {}, argv=["C:\\Program Files\\dotnet\\dotnet.exe", "test"]), "no_failure"),
        ("error", judge(row("error", kind="error"), {}), "incomplete"),
        ("failed + site unread", judge(row("failed"), unread), "incomplete"),
        ("failed + no location and no marker", judge(row("failed"), {}), "incomplete"),
        # N3b: only the marker proves; the place and the library's wording (`fires_as`) are facts, never a verdict
        ("failed in the statement + the marker in its text", judge(row("failed", msg, "qa-probe-t1"), site(), dict(detail, message_marker="qa-probe-t1", fires_as=None)), "intended_failure"),
        ("failed on the statement's last line + the marker", judge(row("failed", msg, "qa-probe-t1"), site(12), dict(detail, message_marker="qa-probe-t1", fires_as=None)), "intended_failure"),
        ("failed in the statement + fires_as does not match", judge(row("failed", "Assert.NotEqual() has failed"), site()), "incomplete"),
        ("failed one line above the statement", judge(row("failed"), site(10)), "incomplete"),
        ("failed one line below the statement", judge(row("failed"), site(13)), "incomplete"),
        ("failed in another project file (exception)", judge(row("failed"), site(11, "exception")), "incomplete"),
        ("failed in the statement + fires_as matches, no marker", judge(row("failed"), site()), "incomplete"),
        ("skipped", judge(row("skipped"), {}), "not_executed"),
        ("not_run", judge(row("not_run"), {}), "not_executed"),
    ]
    for label, got, verdict in cells:
        check_eq(f"R8: {label} -> {verdict}", got["verdict"], verdict)
    check("R8: every non-verdict says what it could not read (a note)",
          all(got["note"] for _l, got, v in cells if v in ("incomplete", "not_executed")))
    check("R8: an intended_failure carries no note and no mismatch",
          cells[8][1]["note"] == "" and cells[8][1]["mismatches"] == [])
    check_in("F9: the wrapper note names the launcher and the builders", "bash run.sh", cells[1][1]["note"])
    check_in("F9: the no_failure note names the launcher that builds by default", "builds by default (`dotnet test`)",
             judge(row("passed"), {})["note"])
    check_in("E5: the --at note says a pass does not tell which body ran", "does not say which body ran", cells[0][1]["note"])
    # t-1968 N2 (spec "Required behaviour" item 1) replaced the old note: the pair travels in `judgment_facts.fires_as_pair` (pinned in test_probe_marker_judgment.py)
    check_in("E15: the drift note says the factory cannot read the text and the code critic judges it", "the code critic judges it",
             cells[10][1]["note"])
    check_eq("E15: ...and the cause is judgment", cells[10][1].get("cause"), "judgment")
    check_eq("R8 N3b: a failure at another place is judgment, never wrong_location, whatever the wording says",
             [(cells[i][1]["verdict"], cells[i][1].get("cause"), cells[i][1]["actual_location"]) for i in (11, 12, 13, 14)],
             [("incomplete", "judgment", None)] * 4)
    check_eq("R8: observed keeps the message head, the frame and the site",
             (cells[8][1]["observed"]["message_head"], cells[8][1]["observed"]["frame"], cells[8][1]["observed"]["location"]),
             ("Assert.NotEqual() Failure: Values are equal", "  at X", "tests/CalcTests.cs:11"))
    # TS: not compiled - a pass is a no_failure through any launcher, with the residual risk said in `observed`
    ts = AD.assertion_detectors()["typescript"]
    tdetail = dict(detail, language="typescript")
    got = PBC.judge_probe_row(row("passed"), {}, ts, tdetail, among=False, argv=["bash", "run.sh"])
    check_eq("E14: TypeScript is not compiled: a pass through any launcher is a no_failure", got["verdict"], "no_failure")
    check_in("E14: ... with the residual risk said in `observed`", "compiled output", got["observed"].get("residual", ""))
    # the message and the text: message first; the text above the first frame when the message is empty or misses
    ts_detail = dict(tdetail, fires_as=AD.assertion_detectors()["typescript"]["assertions"][0]["invert"][1]["fires_as"])
    jest_text = ("Error: expect(received).not.toBe(expected) // Object.is equality\n\nExpected: not 3\nReceived: 3\n"
                 "      at Object.<anonymous> (/clone/src/sum.test.ts:11:20)")
    for label, message, text, expected in (("empty message, matching text", "", jest_text, True),
                                           ("a message that does not match, a text that does", "src/sum.test.ts:11:20 adds", jest_text, True),
                                           ("a matching message, no text", "expect(received).not.toBe(expected)", "", True),
                                           ("neither matches", "boom", "Error: boom\n      at x (/a.ts:1:1)", False),
                                           ("a code frame echoing the statement is not the start of the text",
                                            "", "boom\n  > 11 |   expect(received).not.toBe(3);\n      at Object.<anonymous> (/clone/src/sum.test.ts:11:20)", False)):
        got = PBC.judge_probe_row(row("failed", message, text), site(), ts, dict(ts_detail, language="typescript"), among=False, argv=[])
        check_eq(f"R8 (L8) N3b: {label}: the wording alone proves nothing", got["verdict"] == "intended_failure", False)
        check_eq(f"R8 (L8): {label}: `fires_on` still reads it (the `missed` note's fact)",
                 PBC.fires_on(row("failed", message, text), ts, ts_detail["fires_as"]), expected)
    check_eq("the text above the first frame: stops at a frame or a skipped line",
             PBC.text_head("a\nb\n      at x (/p/a.ts:1:2)\nc", ts), "a\nb")
    check_eq("the launcher words: basenames, .exe/.cmd/.bat stripped, joined by spaces",
             PBC.launcher_words(["C:\\x\\mvn.cmd", "/usr/bin/dotnet", "'npx.exe'"]), "mvn dotnet npx")
    check_eq("builds_by_default is matched at a token boundary", (PBC.builds_by_default(["dotnet", "test"], entry),
                                                                   PBC.builds_by_default(["dotnetx", "test"], entry),
                                                                   PBC.builds_by_default(["dotnet"], entry)), ("dotnet test", "", ""))
    check_eq("...and a prefix of several words", PBC.builds_by_default(["dotnet", "test", "--no-restore"], entry), "dotnet test")
    check_eq("...java's launchers", [PBC.builds_by_default([l, "test"], AD.assertion_detectors()["java"]) for l in ("mvn", "mvnw.cmd", "gradle", "gradlew")],
             ["mvn", "mvnw", "gradle", "gradlew"])


def main() -> None:
    seed_table_plans()
    lexer_and_body()
    candidates_and_heads()
    plan_guards()
    tail_and_names()
    verdict_table()
    finish("test_probe_by_code_languages_plan")


if __name__ == "__main__":
    main()
