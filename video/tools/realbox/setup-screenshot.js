// The state of the user's own footer in their screenshot (out/realbox/ref-user-box.png): a resumed chat (tokens
// known, context window not yet: the ring shows "–"), its prompt cache expired ("cold"), Remote Control on, Ultracode
// offered, effort High (the slider's middle step, charts-green), Auto mode.
;(() => {
  const s = RB.session()
  s.reportedUltracodeAvailable.value = true
  s.effortLevel.value = 'high'
  // Remote Control is read per channel from the connection
  const conn = s.connection.value
  const byChannel = new Map(conn.remoteControlStateByChannel.value ?? [])
  byChannel.set(s.claudeChannelIdSignal.value, { status: 'connected', sessionUrl: 'https://claude.ai/code' })
  conn.remoteControlStateByChannel.value = byChannel
  s.promptCacheRecord.value = { messageId: 'm1', anchorAt: Date.now() - 3 * 3600e3, ttl: '5m', recacheTokens: 20000 }
  s.usageData.value = { totalTokens: 52000, totalCost: 0, contextWindow: 0, maxOutputTokens: 0 }
})()
