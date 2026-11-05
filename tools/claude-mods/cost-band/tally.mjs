// Tallies a Claude Code session's tokens and API-list-price dollars from its transcripts.
// Usage: node tally.mjs <sessionId>
// Prints one JSON object. Reads incrementally: byte offsets are kept in a state file in the temp dir.
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

// USD per 1M tokens: input, output, cache read. Cache writes: 1.25x input (5m), 2x input (1h).
// Source: platform.claude.com/docs/en/about-claude/pricing, read 2026-11-02. Longest prefix wins.
// Fast mode (Opus 5.5 $8/$40, Opus 5 and 4.8 $10/$50) is 2x the base price; caching multipliers apply on top.
const PRICES = [
  ['claude-fable-5-1', 10, 50, 0.25],
  ['claude-mythos-5-1', 10, 50, 0.25],
  ['claude-fable-5', 10, 50, 1.0],
  ['claude-mythos-5', 10, 50, 1.0],
  ['claude-opus-5-5', 4, 20, 0.2],
  ['claude-opus-5', 5, 25, 0.5],
  ['claude-opus-4', 5, 25, 0.5], // Opus 4.5 - 4.8
  ['claude-opus-4-1', 15, 75, 1.5],
  ['claude-opus-4-0', 15, 75, 1.5],
  ['claude-opus-4-2', 15, 75, 1.5], // claude-opus-4-20250514 (Opus 4)
  ['claude-sonnet-5-5', 2, 10, 0.1],
  ['claude-sonnet-5', 2, 10, 0.2],
  ['claude-sonnet-4', 3, 15, 0.3],
  ['claude-haiku-5-5', 0.1, 0.5, 0.01], // prompts up to 100K tokens; above: HAIKU_5_5_LONG
  ['claude-haiku-4', 1, 5, 0.1],
  ['claude-3-5-haiku', 0.8, 4, 0.08],
]
// Claude Haiku 5.5 for a prompt (input + cache read + cache write) over 100,000 tokens.
const HAIKU_5_5_LONG = ['claude-haiku-5-5', 0.5, 2.5, 0.05]
const HAIKU_5_5_LIMIT = 100_000

function priceOf(model, prompt = 0) {
  let best = null
  for (const row of PRICES) {
    if (model.startsWith(row[0]) && (best === null || row[0].length > best[0].length)) best = row
  }
  if (best !== null && best[0] === 'claude-haiku-5-5' && prompt > HAIKU_5_5_LIMIT) return HAIKU_5_5_LONG
  return best
}

const CHUNK = 16 * 1024 * 1024

const emptyTotals =() => ({ input: 0, output: 0, cacheRead: 0, cacheWrite: 0, usd: 0, calls: 0 })

function addUsage(t, model, u) {
  const c5 = u.cache_creation?.ephemeral_5m_input_tokens
  const c1 = u.cache_creation?.ephemeral_1h_input_tokens
  const write = u.cache_creation_input_tokens ?? 0
  // Older lines have no TTL split: count the whole write as 5m.
  const w5 = c5 ?? (c1 === undefined ? write : 0)
  const w1 = c1 ?? 0
  const input = u.input_tokens ?? 0
  const output = u.output_tokens ?? 0
  const read = u.cache_read_input_tokens ?? 0
  t.input += input
  t.output += output
  t.cacheRead += read
  t.cacheWrite += w5 + w1
  t.calls += 1
  const p = priceOf(model, input + read + w5 + w1)
  if (p === null) return false
  const k = u.speed === 'fast' ? 2 : 1
  t.usd += (k * (input * p[1] + output * p[2] + read * p[3] + w5 * p[1] * 1.25 + w1 * p[1] * 2)) / 1e6
  return true
}

function findTranscript(sessionId) {
  const root = path.join(os.homedir(), '.claude', 'projects')
  for (const dir of fs.readdirSync(root)) {
    const f = path.join(root, dir, sessionId + '.jsonl')
    if (fs.existsSync(f)) return f
  }
  return null
}

const sessionId = process.argv[2]
if (!sessionId || !/^[\w-]+$/.test(sessionId)) {
  console.log(JSON.stringify({ error: 'no session id' }))
  process.exit(0)
}
const main = findTranscript(sessionId)
if (main === null) {
  console.log(JSON.stringify({ error: 'transcript not found' }))
  process.exit(0)
}

const statePath = path.join(os.tmpdir(), 'cost-band-' + sessionId + '.json')
let state = { files: {} }
try {
  state = JSON.parse(fs.readFileSync(statePath, 'utf8'))
} catch {}

// Reads the new complete lines of one file and folds them into its saved entry.
function scan(file) {
  const st = fs.statSync(file)
  let e = state.files[file]
  if (e === undefined || st.size < e.offset) {
    e = { offset: 0, totals: emptyTotals(), byModel: {}, seen: [], last: null, unknown: [] }
  }
  const seen = new Set(e.seen)
  const fd = fs.openSync(file, 'r')
  // Chunks keep a huge transcript under the engine's string limit; a chunk ends at its last newline.
  while (st.size > e.offset) {
    const buf = Buffer.alloc(Math.min(CHUNK, st.size - e.offset))
    fs.readSync(fd, buf, 0, buf.length, e.offset)
    const end = buf.lastIndexOf(0x0a)
    if (end < 0) {
      // A line longer than a chunk is not a usage line worth reading whole: skip past it.
      if (buf.length < CHUNK) break
      e.offset += buf.length
      continue
    }
    {
      for (const line of buf.subarray(0, end).toString('utf8').split('\n')) {
        if (!line.includes('"usage"')) continue
        let j
        try {
          j = JSON.parse(line)
        } catch {
          continue
        }
        const m = j.message
        if (j.type !== 'assistant' || !m?.usage || !m.model || m.model === '<synthetic>') continue
        // One API response is written as several lines that repeat its usage.
        const id = m.id ?? j.requestId ?? j.uuid
        if (seen.has(id)) continue
        seen.add(id)
        if (!addUsage(e.totals, m.model, m.usage) && !e.unknown.includes(m.model)) e.unknown.push(m.model)
        const bm = (e.byModel[m.model] ??= emptyTotals())
        addUsage(bm, m.model, m.usage)
        e.last = {
          ts: j.timestamp,
          model: m.model,
          ttl1h: (m.usage.cache_creation?.ephemeral_1h_input_tokens ?? 0) > 0 || e.last?.ttl1h === true,
        }
      }
      e.offset += end + 1
    }
  }
  fs.closeSync(fd)
  e.seen = [...seen].slice(-5000)
  state.files[file] = e
  return e
}

const sum = (a, b) => {
  for (const k of Object.keys(a)) a[k] += b[k]
  return a
}

const m = scan(main)
const subDir = path.join(path.dirname(main), sessionId, 'subagents')
const sub = emptyTotals()
let agents = 0
const unknown = new Set(m.unknown)
if (fs.existsSync(subDir)) {
  for (const name of fs.readdirSync(subDir)) {
    if (!name.endsWith('.jsonl')) continue
    const e = scan(path.join(subDir, name))
    if (e.totals.calls > 0) agents += 1
    sum(sub, e.totals)
    for (const u of e.unknown) unknown.add(u)
  }
}

try {
  fs.writeFileSync(statePath, JSON.stringify(state))
} catch {}

const all = sum(sum(emptyTotals(), m.totals), sub)
const fed = all.input + all.cacheRead + all.cacheWrite
console.log(
  JSON.stringify({
    model: m.last?.model ?? null,
    lastTs: m.last?.ts ?? null,
    ttlMs: m.last?.ttl1h ? 3600_000 : 300_000,
    main: m.totals,
    sub,
    agents,
    cacheHit: fed > 0 ? all.cacheRead / fed : null,
    unknownModels: [...unknown],
  }),
)
