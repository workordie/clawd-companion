// Helpers run inside the real panel (after it has started): find the input box, its footer and the chat
// session the footer component is given (the same way custom.js does: the React fiber's props), and take
// snapshots of the panel's DOM.
;(() => {
  const fiberProps = (node, test, depth = 60) => {
    const key = node && Object.keys(node).find(k => k.startsWith('__reactFiber$'))
    for (let f = key ? node[key] : null, i = 0; f && i < depth; f = f.return, i++) {
      const p = f.memoizedProps
      if (p && typeof p === 'object' && test(p)) return p
    }
    return null
  }
  const RB = (window.RB = {
    fiberProps,
    box: () => document.querySelector('fieldset[class*="inputContainer_"]'),
    footer: () => RB.box()?.querySelector('[class*="inputFooter_"]'),
    props: () => fiberProps(RB.footer(), p => p.session && 'onCompact' in p),
    session: () => RB.props()?.session,
    input: () => document.querySelector('[class*="messageInput_"][contenteditable]'),
    /** The session's own fields: signals (have .value) and their current values. */
    describe() {
      const s = RB.session()
      if (!s) return null
      const out = {}
      for (const k of Object.keys(s)) {
        const v = s[k]
        if (v && typeof v === 'object' && 'value' in v) {
          let val
          try {
            val = v.value
          } catch (e) {
            val = '!' + e.message
          }
          out[k] = val === undefined ? 'undefined' : JSON.stringify(val)?.slice(0, 120)
        }
      }
      return out
    },
    /** An element's box in the panel's CSS px. */
    rect(el) {
      if (typeof el === 'string') el = document.querySelector(el)
      if (!el) return null
      const r = el.getBoundingClientRect()
      return { x: r.left, y: r.top, w: r.width, h: r.height }
    },
    /** Closes notices the panel shows on a first visit (the user has seen them). */
    dismissNotices() {
      // e.g. "Auto mode is enabled" in the empty chat: its own Close button
      let n = 0
      for (const b of document.querySelectorAll('[class*="emptyState_"] button[aria-label="Close"], [class*="emptyState_"] button[aria-label^="Dismiss"]')) {
        b.click()
        n++
      }
      return n
    },
    /**
     * The panel's DOM as it is now: #root's HTML (Clawd taken out: the video draws him), live values copied into
     * attributes so the HTML carries them, the patch's own root variables, and its bubble tail.
     */
    snapshot() {
      for (const inp of document.querySelectorAll('input')) inp.setAttribute('value', inp.value)
      for (const ta of document.querySelectorAll('textarea')) ta.textContent = ta.value
      // where focus and the pointer are: tagged before cloning, found again in the clone (whose children no longer
      // count Clawd), as child-index paths from #root; the video sets the matching data-rb-* attributes
      const live = document.getElementById('root')
      const tags = { focus: document.activeElement !== document.body ? document.activeElement : null,
        hover: [...document.querySelectorAll(':hover')].pop() ?? null, active: [...document.querySelectorAll(':active')].pop() ?? null }
      for (const [k, el] of Object.entries(tags)) if (el && live.contains(el)) el.setAttribute(`data-rb-snap-${k}`, '')
      const root = live.cloneNode(true)
      for (const k of Object.keys(tags)) live.querySelector(`[data-rb-snap-${k}]`)?.removeAttribute(`data-rb-snap-${k}`)
      root.querySelectorAll('.cx-clawd, .cx-clawd-hit').forEach(n => n.remove())
      const paths = {}
      for (const k of Object.keys(tags)) {
        const el = root.querySelector(`[data-rb-snap-${k}]`)
        paths[k] = null
        if (!el) continue
        el.removeAttribute(`data-rb-snap-${k}`)
        const out = []
        for (let n = el; n !== root; n = n.parentElement) out.unshift([...n.parentElement.children].indexOf(n))
        paths[k] = out
      }
      const vars = {}
      const st = document.documentElement.style
      for (let i = 0; i < st.length; i++) if (st[i].startsWith('--cx')) vars[st[i]] = st.getPropertyValue(st[i])
      const extras = [...document.body.children].filter(n => /\bcx-/.test(n.className ?? '')).map(n => n.outerHTML)
      const clawd = document.querySelector('.cx-clawd')
      return {
        ...paths,
        html: root.innerHTML,
        rootAttrs: Object.fromEntries([...live.attributes].map(a => [a.name, a.value])),
        vars,
        extras,
        geometry: {
          box: RB.rect(RB.box()),
          footer: RB.rect(RB.footer()),
          clawd: clawd ? RB.rect(clawd) : null,
          talk: RB.rect('.cx-talk'),
          column: RB.rect('[class*="chatContainer_"]'),
        },
      }
    },
  })
})()
