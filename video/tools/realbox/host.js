// In-page stand-in for the VS Code side of the Claude Code panel: acquireVsCodeApi(), and answers to the
// requests the panel sends at start-up, posted back the way the extension does ({type:'from-extension'}).
// Values are what a signed-in user with default settings would see; HOST.state / HOST.config can be
// edited before the panel script runs.
;(() => {
  // the panel picks tips and spinner words at random: seed it, so every capture is the same
  let seed = 0x5eed1e55
  Math.random = () => {
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
  const sent = (window.__sent = [])
  const HOST = (window.HOST = {
    state: {
      defaultCwd: '/Users/you/playground',
      authStatus: { authMethod: 'claudeai', email: null, subscriptionType: 'max' },
      gatewaySignIns: [],
      openNewInTab: false,
      showTerminalBanner: false,
      showReviewUpsellBanner: false,
      isOnboardingEnabled: false,
      isOnboardingDismissed: true,
      loginPromptDisabled: false,
      modelSetting: 'default',
      thinkingLevel: undefined,
      allowDangerouslySkipPermissions: true, // Bypass is in the user's mode menu
      initialPermissionMode: 'auto', // the screenshot's "● Auto"
      artifactAutoOpen: false,
      platform: 'darwin',
      speechToTextEnabled: true,
      speechToTextMicDenied: false,
      marketplaceType: 'vscode',
      useCtrlEnterToSend: false,
      ctrlJInsertsNewline: false,
      scrollToBottomOnSend: true,
      showMessageTimestamps: false,
      focusViewEnabled: true,
      spellcheckEnabled: false,
      spellcheckUserWords: [],
      bookmarksSupported: false,
      chromeMcpState: { status: 'disconnected' },
      browserIntegrationSupported: false,
      debuggerMcpState: { status: 'inactive' },
      jupyterMcpState: { status: 'inactive' },
      remoteControlState: { status: 'disconnected' },
      settings: {},
      claudeSettings: { effective: {}, sources: [], errors: [] },
      experimentGates: { tengu_auto_mode_state: 'enabled' }, // Auto is in the user's mode menu
      remoteControlAutoEnableDefault: false,
      remoteControlAutoConnectDefault: false,
      remoteControlAvailable: true,
      sweptStaleChannels: false,
    },
    // the CLI's model list (get_claude_state): the user's model, its effort levels, Auto mode
    config: {
      models: [
        {
          value: 'default',
          displayName: 'Fable 5.2',
          description: 'Most capable for complex work',
          supportsEffort: true,
          supportedEffortLevels: ['low', 'medium', 'high', 'xhigh', 'max'],
          supportsAutoMode: true,
          supportsFastMode: false,
        },
      ],
    },
    // extra answers by request type: (request) => response. As the extension answers them with nothing set up:
    answers: {
      engine_ui_state: () => ({ type: 'engine_ui_state_response', available: false }), // no plugin surface
    },
    unhandled: [],
  })
  // the user has sent messages before, so the placeholder is the focus hint, not the first-run one
  try {
    localStorage.setItem('claude-vscode-first-run-bypassed', 'true')
  } catch {}
  const post = message => window.postMessage({ type: 'from-extension', message }, '*')
  HOST.post = post
  HOST.respond = (requestId, response) => setTimeout(() => post({ type: 'response', requestId, response }), 0)
  /** A message from the CLI for the panel's chat (the extension forwards them as io_message). */
  HOST.io = message => post({ type: 'io_message', channelId: HOST.channelId, message, done: false })
  /** Claude's reply to the prompt and the end of the turn, as the CLI streams them (Agent SDK message shapes). */
  HOST.reply = (text, { ms = 18000 } = {}) => {
    const now = new Date().toISOString()
    HOST.io({ type: 'assistant', uuid: 'a-' + Date.now(), session_id: 'session-1', parent_tool_use_id: null, timestamp: now,
      message: { id: 'msg_1', type: 'message', role: 'assistant', model: 'default', content: [{ type: 'text', text }], stop_reason: 'end_turn',
        usage: { input_tokens: 1200, output_tokens: 90, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 } } })
    HOST.io({ type: 'result', subtype: 'success', is_error: false, duration_ms: ms, duration_api_ms: ms, num_turns: 1, result: text,
      session_id: 'session-1', total_cost_usd: 0.02, usage: { input_tokens: 1200, output_tokens: 90 }, uuid: 'r-' + Date.now() })
  }
  let nextId = 1
  /** A request from the host to the panel (as the extension sends them), e.g. engine_surface_state. */
  HOST.request = (channelId, request) => post({ type: 'request', channelId, requestId: `host-${nextId++}`, request })
  function handle(msg) {
    if (msg.type === 'launch_claude') {
      // the CLI starts for this channel; no plugin draws in this build (as the extension tells the panel)
      HOST.channelId = msg.channelId
      setTimeout(() => HOST.request(msg.channelId, { type: 'engine_surface_state', available: false }), 0)
      return
    }
    if (msg.type !== 'request') return
    const r = msg.request
    if (r.type === 'init') return HOST.respond(msg.requestId, { type: 'init_response', state: HOST.state })
    if (r.type === 'get_claude_state') return HOST.respond(msg.requestId, { type: 'get_claude_state_response', config: HOST.config })
    if (HOST.answers[r.type]) {
      const res = HOST.answers[r.type](r, msg) // undefined: answered later (HOST.respond)
      if (res !== undefined) HOST.respond(msg.requestId, res)
      return
    }
    HOST.unhandled.push(r.type)
  }
  let state
  const api = Object.freeze({
    postMessage(message) {
      sent.push(message)
      handle(message)
    },
    getState: () => state,
    setState: s => (state = s),
  })
  window.acquireVsCodeApi = () => api
})()
