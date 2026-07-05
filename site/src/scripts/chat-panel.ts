// Shared chat-UI logic (TW-117) — message log, send, Enter-to-send, 401/403 ->
// sign-in link. Factored out of Tutor.astro's inline script so the new global
// ChatWidget can reuse the exact same tested interaction pattern instead of
// forking a second copy.
//
// Tutor.astro's markup/styles/behavior must stay byte-for-byte identical from
// the user's perspective (TW-117 refactor constraint), and it already ships
// with its own fixed `data-tutor-*` attribute names and `.tutor-msg` CSS classes
// that this refactor must not rename. The new widget uses its own namespaced
// `.cw-*` markup/classes (no shared IDs or global state — see ChatWidget.astro).
// To let ONE implementation serve both without either markup changing, this
// module accepts two small, additive, optional knobs beyond the primary shape:
// `selectors` (which data-attributes to query under `root`) and
// `msgClassPrefix` (which CSS class each message bubble gets). It also accepts
// `initialHistory`/`onHistoryChange`, used only by the widget to persist
// conversation history across page navigation (Tutor does not use them).

export type Role = 'user' | 'assistant';
export type Msg = { role: Role; content: string };
export type AddMsg = (cls: string, text: string) => HTMLElement;

export interface ChatPanelSelectors {
  log: string;
  form: string;
  input: string;
  send: string;
}

const DEFAULT_SELECTORS: ChatPanelSelectors = {
  log: '[data-log]',
  form: '[data-form]',
  input: '[data-input]',
  send: '[data-send]',
};

export interface AttachChatPanelOpts {
  root: HTMLElement;
  endpoint: string;
  buildBody: (history: Msg[]) => unknown;
  onReply?: (data: any, addMsg: AddMsg) => void;
  maxHistory?: number;
  signInMessage?: string;
  /** 422 copy — defaults to the chatbot's "couldn't answer that" wording. */
  cannotAnswerMessage?: string;
  /** 429 copy — defaults to the chatbot's "sending messages quickly" wording. */
  rateLimitedMessage?: string;
  /** data-attribute selectors to query under `root` (defaults to [data-log] etc). */
  selectors?: Partial<ChatPanelSelectors>;
  /** CSS class prefix applied to each message bubble (default 'msg'). */
  msgClassPrefix?: string;
  /** Prior conversation to seed the log with on attach (widget-only; persisted history). */
  initialHistory?: Msg[];
  /** Called after every history mutation, with the (already maxHistory-trimmed) history. */
  onHistoryChange?: (history: Msg[]) => void;
}

const DEFAULT_CANNOT_ANSWER = "I couldn't answer that one — try asking a different question about our courses.";
const DEFAULT_RATE_LIMITED = "You're sending messages quickly — please wait a minute.";
const DEFAULT_GENERIC_ERROR = 'Something went wrong. Please try again in a moment.';
const DEFAULT_NETWORK_ERROR = 'Network error. Please try again.';

export function attachChatPanel(opts: AttachChatPanelOpts): { ask(q: string): Promise<void> } {
  const {
    root,
    endpoint,
    buildBody,
    onReply,
    maxHistory = 8,
    signInMessage = 'Please sign in to continue.',
    cannotAnswerMessage = DEFAULT_CANNOT_ANSWER,
    rateLimitedMessage = DEFAULT_RATE_LIMITED,
    selectors,
    msgClassPrefix = 'msg',
    initialHistory,
    onHistoryChange,
  } = opts;

  const sel: ChatPanelSelectors = { ...DEFAULT_SELECTORS, ...selectors };
  const log = root.querySelector<HTMLElement>(sel.log);
  const form = root.querySelector<HTMLFormElement>(sel.form);
  const input = root.querySelector<HTMLTextAreaElement>(sel.input);
  const send = root.querySelector<HTMLButtonElement>(sel.send);

  const history: Msg[] = [];

  function addMsg(cls: string, text: string): HTMLElement {
    const el = document.createElement('div');
    el.className = `${msgClassPrefix} ${cls}`;
    el.textContent = text; // plain text only — never innerHTML (XSS prevention)
    if (log) {
      log.appendChild(el);
      log.scrollTop = log.scrollHeight;
    }
    return el;
  }

  function emitHistoryChange() {
    if (onHistoryChange) onHistoryChange(history.slice(-maxHistory));
  }

  // Replay any persisted history into the visible log on attach (widget only).
  if (initialHistory && initialHistory.length) {
    for (const m of initialHistory) {
      if (!m || (m.role !== 'user' && m.role !== 'assistant')) continue;
      if (typeof m.content !== 'string' || !m.content) continue;
      history.push({ role: m.role, content: m.content });
      addMsg(m.role === 'user' ? 'user' : 'bot', m.content);
    }
  }

  async function ask(question: string): Promise<void> {
    const q = (question || '').trim();
    if (!q) return;

    addMsg('user', q);
    history.push({ role: 'user', content: q });
    emitHistoryChange();
    const pending = addMsg('bot', 'Thinking…');
    send?.setAttribute('disabled', 'true');
    input?.setAttribute('disabled', 'true');

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(buildBody(history.slice(-maxHistory))),
      });

      if (res.status === 401 || res.status === 403) {
        const back = encodeURIComponent(location.pathname);
        pending.className = `${msgClassPrefix} err`;
        pending.textContent = signInMessage;
        const a = document.createElement('a');
        a.href = '/.auth/login/entraExternalId?post_login_redirect_uri=' + back;
        a.textContent = ' Sign in';
        pending.appendChild(a);
        history.pop();
        emitHistoryChange();
        return;
      }

      if (res.status === 422) {
        pending.className = `${msgClassPrefix} err`;
        pending.textContent = cannotAnswerMessage;
        history.pop();
        emitHistoryChange();
        return;
      }

      if (res.status === 429) {
        pending.className = `${msgClassPrefix} err`;
        pending.textContent = rateLimitedMessage;
        history.pop();
        emitHistoryChange();
        return;
      }

      const data = res.ok ? await res.json().catch(() => null) : null;
      if (data && typeof data.reply === 'string') {
        pending.textContent = data.reply;
        history.push({ role: 'assistant', content: data.reply });
        emitHistoryChange();
        if (onReply) onReply(data, addMsg);
      } else {
        pending.className = `${msgClassPrefix} err`;
        pending.textContent = DEFAULT_GENERIC_ERROR;
        history.pop();
        emitHistoryChange();
      }
    } catch (e) {
      pending.className = `${msgClassPrefix} err`;
      pending.textContent = DEFAULT_NETWORK_ERROR;
      history.pop();
      emitHistoryChange();
    } finally {
      send?.removeAttribute('disabled');
      input?.removeAttribute('disabled');
      input?.focus();
    }
  }

  if (form && input) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = (input.value || '').trim();
      if (!q) return;
      input.value = '';
      ask(q);
    });
    // Enter to send, Shift+Enter for newline.
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        form.requestSubmit();
      }
    });
  }

  return { ask };
}
