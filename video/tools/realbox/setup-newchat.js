// A brand-new chat for the same user: what the panel has before Claude's first reply. Nothing about the
// conversation yet: no prompt-cache record (the footer shows no cache clock), no context used (the ring says 0%).
// The user's own settings as in their screenshot: Remote Control on, Ultracode offered, effort High.
;(() => {
  const s = RB.session()
  s.reportedUltracodeAvailable.value = true
  s.effortLevel.value = 'high'
  const conn = s.connection.value
  const byChannel = new Map(conn.remoteControlStateByChannel.value ?? [])
  byChannel.set(s.claudeChannelIdSignal.value, { status: 'connected', sessionUrl: 'https://claude.ai/code' })
  conn.remoteControlStateByChannel.value = byChannel
})()
