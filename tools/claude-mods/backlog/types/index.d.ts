export type BacklogNode = { id: string; status: string; what: string }
export type BacklogBatch = { n: number; title: string; status: string; prio: string; who: string; nodes: BacklogNode[] }
export type BacklogPile = { slug: string; title: string; batches: BacklogBatch[] }
export type BacklogTree = {
  piles: BacklogPile[]
  counts: Record<string, number>
  error: string
  updatedAt: string
}

declare module 'claude-code' {
  interface PluginState {
    backlog: { tree: Shaped<BacklogTree>; open: Shaped<string[]> }
  }
}
