import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { BacklogTree } from '../types'

// The pane of the forge's backlog. Data: `python -B tools/backlog_tree.py` in the session's folder (the one reader,
// built on tools/piles.py). No timer: the tree is read at session start, after this session writes plans/piles, and on «обновить».
const SCRIPT = 'tools/backlog_tree.py'
const PANE = 'backlog'
const TITLE = 'Бэклог'
const EMPTY: BacklogTree = { piles: [], counts: {}, error: '', updatedAt: '' }
const READY_TEXT = 'готовься к компакту'

const tree = atom({ plugin: 'backlog', key: 'tree' } as const, EMPTY, { shape: 'tree-2' })
const open = atom({ plugin: 'backlog', key: 'open' } as const, [] as string[], { shape: 'open-1' })

const PRIO_COLOR: Record<string, string> = { 'П1': '#e5534b', 'П2': '#e0a030', 'П3': '#5b8def' }

async function refresh($: any): Promise<void> {
  try {
    const ran = await $.process.run(['python', '-B', SCRIPT], { timeoutMs: 120000 })
    if (ran.exitCode !== 0) {
      await update($, tree, t => ({ ...t, error: (ran.stderr || `${SCRIPT} failed`).slice(-400) }))
      return
    }
    const data = JSON.parse(ran.stdout)
    await update($, tree, () => ({
      piles: data.piles ?? [],
      counts: data.counts ?? {},
      error: '',
      updatedAt: new Date().toLocaleTimeString(),
    }))
  } catch (err) {
    await update($, tree, t => ({ ...t, error: String(err).slice(0, 400) }))
  }
}

function toggle(list: string[], key: string): string[] {
  return list.includes(key) ? list.filter(k => k !== key) : [...list, key]
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const started = await next(e)
    // Only in a checkout of the forge: elsewhere the mod stays silent.
    if (!(await $.fs.exists(SCRIPT))) return started
    await $.command.register({ name: 'backlog', description: 'Открыть панель «Бэклог»' })
    void $.ui.open({ id: PANE, title: TITLE })
    void refresh($)
    return started
  })

  on('command.run', { command: 'backlog' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })
    void refresh($)
    return { text: 'Панель «Бэклог» открыта.' }
  })

  // This session's own write to the backlog redraws the pane once, right after the call.
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    const input = JSON.stringify((e as any).input ?? {})
    if (input.includes('plans/piles') || input.includes('plans\\\\piles') || input.includes('piles.py close')) void refresh($)
    return ran
  })

  // One line above the prompt: the open nodes by priority, «Открыть» for the pane and /compact. It puts itself BELOW
  // what the plugins beneath draw (cost-band puts itself above), so the cost line stays first whichever runs first.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const below = await next(e)
    if (e.props?.hasSurvey) return below
    const t = await read($, tree)
    if (!t.piles.length && !t.error) return below
    const { Box, Text, Button } = $.ui.resolve(e)
    return (
      <Box flexDirection="column">
        {below}
        <Box flexDirection="row">
          <Text dimColor>Бэклог:{' '}</Text>
          {['П1', 'П2', 'П3'].filter(p => t.counts[p]).map(p => (
            <Text color={PRIO_COLOR[p]} weight="semibold">{p} {t.counts[p]}{'  '}</Text>
          ))}
          <Button
            key="backlog-open"
            label="Открыть"
            onPress={() => {
              void $.ui.open({ id: PANE, title: TITLE })
              void refresh($)
            }}
          />
          <Box flexGrow={1} />
          {/* A plugin's prompt waits for the running turn to end: it is queued, never an interrupt. */}
          <Button
            key="backlog-ready"
            label="Be ready to compact"
            onPress={async () => {
              try {
                await $.prompt.submit({ text: READY_TEXT, asUser: true })
              } catch (err) {
                $.ui.toast(`Be ready to compact: ${String((err as Error)?.message ?? err)}`)
              }
            }}
          />
          <Button
            key="backlog-compact"
            label="/compact"
            onPress={async () => {
              try {
                await $.command.run({ command: 'compact', args: '' })
              } catch (err) {
                $.ui.toast(`/compact: ${String((err as Error)?.message ?? err)}`)
              }
            }}
          />
        </Box>
      </Box>
    )
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e)
    const t = await read($, tree)
    const opened = await read($, open)
    const flip = (key: string) => () => void update($, open, list => toggle(list, key))
    const total = Object.values(t.counts).reduce((a, b) => a + b, 0)
    const byPrio = ['П1', 'П2', 'П3']
      .filter(p => t.counts[p])
      .map(p => (
        <Text color={PRIO_COLOR[p]} weight="semibold">
          {p} {t.counts[p]}{'  '}
        </Text>
      ))

    return (
      <Box flexDirection="column">
        <Box flexDirection="row">
          <Text weight="semibold">Открыто узлов: {total}{'  '}</Text>
          {byPrio}
        </Box>
        <Box flexDirection="row">
          <Text dimColor size="caption">обновлено {t.updatedAt || '—'}{'  '}</Text>
          <Button key="refresh" plain onPress={() => void refresh($)}>обновить</Button>
        </Box>
        {t.error && <Text color="#e5534b">{t.error}</Text>}
        {t.piles.map(pile => {
          const pk = `p:${pile.slug}`
          const isOpen = opened.includes(pk)
          const nodes = pile.batches.reduce((a, b) => a + b.nodes.length, 0)
          return (
            <Box flexDirection="column" key={pk}>
              <Button key={pk} plain onPress={flip(pk)}>
                {isOpen ? '▾ ' : '▸ '}
                <Text weight="semibold">{pile.slug}</Text>
                <Text dimColor> — {pile.title} · {pile.batches.length} п. · {nodes} у.</Text>
              </Button>
              {isOpen &&
                pile.batches.map(batch => {
                  const bk = `b:${pile.slug}/${batch.n}`
                  const bOpen = opened.includes(bk)
                  const color = PRIO_COLOR[batch.prio] ?? '#999999'
                  return (
                    <Box flexDirection="column" key={bk} paddingLeft={2}>
                      <Button key={bk} plain onPress={flip(bk)}>
                        {bOpen ? '▾ ' : '▸ '}
                        <Text color={color} weight="semibold">{batch.prio || '—'} </Text>
                        <Text color={color}>пачка {batch.n}</Text>
                        <Text dimColor> · {batch.nodes.length} у. · {batch.status}{batch.who && batch.who !== '—' ? ` · ${batch.who}` : ''}</Text>
                      </Button>
                      {bOpen && <Text dimColor size="caption">{batch.title}</Text>}
                      {bOpen &&
                        batch.nodes.map(node => (
                          <Box flexDirection="row" key={`${bk}:${node.id}`} paddingLeft={2}>
                            <Text mono color={color}>{node.id}{' '}</Text>
                            <Text dimColor>{node.status}{' '}</Text>
                            <Text>{node.what}</Text>
                          </Box>
                        ))}
                    </Box>
                  )
                })}
            </Box>
          )
        })}
      </Box>
    )
  })
}
