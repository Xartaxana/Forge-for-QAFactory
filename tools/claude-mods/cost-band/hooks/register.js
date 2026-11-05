// cost-band: a band above the prompt with the model, tokens and API-list-price dollars
// of this session and its subagents, the cache hit rate and the time until the cache goes cold.
// The numbers come from tally.mjs, run with node over the session's transcripts.

const REFRESH_MS = 5000
const TICK_MS = 1000
const NODES = ['node', 'C:/Program Files/nodejs/node.exe']

let data = null
let error = null
let isHidden = false
let isBusy = false
let nodeIndex = 0

const fmtTokens = (n) =>
  n >= 1e9 ? (n / 1e9).toFixed(2) + 'B' : n >= 1e6 ? (n / 1e6).toFixed(1) + 'M' : n >= 1e3 ? Math.round(n / 1e3) + 'K' : String(n)

const fmtUsd = (n) => '$' + (n >= 100 ? n.toFixed(0) : n.toFixed(2))

const tokensOf = (t) => t.input + t.output + t.cacheRead + t.cacheWrite

function coolLine(now) {
  if (data?.lastTs == null) return null
  const left = Date.parse(data.lastTs) + data.ttlMs - now
  const ttl = data.ttlMs >= 3600_000 ? '1ч' : '5м'
  if (left <= 0) return { text: 'кэш (' + ttl + ') остыл', color: 'red' }
  const m = Math.floor(left / 60_000)
  const s = Math.floor((left % 60_000) / 1000)
  return {
    text: 'остынет через ' + m + ':' + String(s).padStart(2, '0') + ' (' + ttl + ')',
    color: left < 120_000 ? 'yellow' : undefined,
  }
}

async function refresh($) {
  if (isBusy) return
  isBusy = true
  try {
    const sid = await $.session.id()
    const root = $.plugin.root
    const script = String(root).replace(/\\/g, '/') + '/tally.mjs'
    let r
    try {
      r = await $.process.run([NODES[nodeIndex], script, String(sid)])
    } catch (err) {
      // The desktop app may start without node on PATH: try the next known location.
      if (nodeIndex < NODES.length - 1) {
        nodeIndex += 1
        r = await $.process.run([NODES[nodeIndex], script, String(sid)])
      } else {
        throw err
      }
    }
    const parsed = JSON.parse(r.stdout.trim().split('\n').pop() || '{}')
    if (parsed.error) {
      error = parsed.error
    } else {
      data = parsed
      error = null
    }
  } catch (err) {
    error = String(err?.message ?? err).slice(0, 200)
  } finally {
    isBusy = false
    $.ui.invalidate('ui.render')
  }
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    data = null
    error = null
    $.clock.every(REFRESH_MS, () => refresh($))
    $.clock.every(TICK_MS, () => {
      if (!isHidden && data !== null) $.ui.invalidate('ui.render')
    })
    void refresh($)
    try {
      await $.command.register({
        name: 'cost-band',
        description: 'Show or hide the cost band above the prompt; "json" prints the raw numbers',
        argumentHint: '[json]',
        immediate: true,
      })
    } catch {}
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    void refresh($)
    return next(e)
  })

  on('command.run', { command: 'cost-band' }, async ($, e) => {
    if (e.args.trim() === 'json') {
      // The first refresh from session.start may still be running: wait for it.
      for (let i = 0; i < 60 && isBusy; i++) await $.clock.sleep(500)
      await refresh($)
      return { text: '```json\n' + JSON.stringify({ data, error }, null, 2) + '\n```' }
    }
    isHidden = !isHidden
    $.ui.invalidate('ui.render')
    return { text: isHidden ? 'cost band hidden' : 'cost band shown' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (isHidden || e.props.hasSurvey) return next(e)
    const { Box, Text } = $.ui.resolve(e)

    let rows
    if (data === null) {
      rows = [Text({ dimColor: true, wrap: 'truncate-end', children: [
            error === 'transcript not found'
              ? 'cost-band: жду первого ответа модели'
              : error
                ? 'cost-band: ' + error
                : 'cost-band: считаю…',
          ] })]
    } else {
      const model = (data.model ?? '?').replace(/^claude-/, '')
      const all = data.main.usd + data.sub.usd
      const hit = data.cacheHit === null ? '—' : Math.round(data.cacheHit * 100) + '%'
      const cool = coolLine(Date.now())
      const unknown = data.unknownModels.length > 0 ? ' · без цены: ' + data.unknownModels.join(', ') : ''
      const top = [
        Text({ bold: true, children: [model] }),
        Text({ children: [' · всего ' + fmtUsd(all)] }),
        Text({ dimColor: true, children: [' · сессия '] }),
        Text({ children: [fmtTokens(tokensOf(data.main)) + ' ' + fmtUsd(data.main.usd)] }),
        Text({ dimColor: true, children: [' · сабагенты (' + data.agents + ') '] }),
        Text({ children: [fmtTokens(tokensOf(data.sub)) + ' ' + fmtUsd(data.sub.usd)] }),
        Text({ dimColor: true, children: [' · кэш ' + hit] }),
      ]
      if (cool !== null) {
        top.push(Text({ dimColor: true, children: [' · '] }))
        top.push(cool.color ? Text({ color: cool.color, children: [cool.text] }) : Text({ children: [cool.text] }))
      }
      if (unknown) top.push(Text({ color: 'yellow', children: [unknown] }))
      rows = [Box({ flexDirection: 'row', children: top })]
    }

    const theirs = await next(e)
    if (theirs) rows.push(theirs)
    return Box({ flexDirection: 'column', children: rows })
  })
}
