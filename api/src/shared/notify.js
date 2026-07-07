'use strict';

// Best-effort admin notification (TW-66). When a user requests a custom course,
// email the admin so they can dispatch the generate-course Action. Provider is
// chosen by app settings; if none is configured it's a no-op (the user's request
// still succeeds — notification must never block the flow).
//
// notifyFeedback (TW-133) reuses the same channel for the public
// complaints/suggestions form (see api/src/functions/complaint.js).
//
// Configure ONE of (in SWA app settings):
//   RESEND_API_KEY   (+ optional NOTIFY_FROM, default onboarding@resend.dev)
//   NOTIFY_WEBHOOK_URL  (POST {to,subject,text} — e.g. a Power Automate / Logic App flow)
// Recipient: NOTIFY_EMAIL (default kasare@spreadcomgh.com).

const DEFAULT_TO = 'kasare@spreadcomgh.com';

async function notifyCourseRequest({ userEmail, targetRole, targetSkills } = {}) {
  const to = process.env.NOTIFY_EMAIL || DEFAULT_TO;
  const subject = `New custom course request: ${targetRole || 'unspecified role'}`;
  const text = [
    'A user requested a custom training course.',
    '',
    `User: ${userEmail || '(unknown)'}`,
    `Target role: ${targetRole || '(unspecified)'}`,
    `Skills: ${(targetSkills || []).join(', ') || '(none)'}`,
    '',
    'Next: dispatch the generate-course Action with this role/skills, then review + merge the draft PR.',
  ].join('\n');

  const resendKey = process.env.RESEND_API_KEY;
  if (resendKey) {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { authorization: `Bearer ${resendKey}`, 'content-type': 'application/json' },
      body: JSON.stringify({ from: process.env.NOTIFY_FROM || 'onboarding@resend.dev', to, subject, text }),
    });
    if (!res.ok) throw new Error(`Resend ${res.status}`);
    return { sent: true, via: 'resend' };
  }

  const hook = process.env.NOTIFY_WEBHOOK_URL;
  if (hook) {
    const res = await fetch(hook, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ to, subject, text }),
    });
    if (!res.ok) throw new Error(`webhook ${res.status}`);
    return { sent: true, via: 'webhook' };
  }

  return { sent: false, reason: 'no notification channel configured' };
}

// Simple, permissive email-shape check — only used to decide whether to set a
// reply-to; never used for gating/validation (that happens in complaint.js).
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Best-effort admin notification for the public complaints/suggestions form
// (TW-133). Same two-channel (Resend / webhook) pattern as notifyCourseRequest
// above; a send failure must never block the submitter's success response —
// callers are expected to await this inside their own try/catch.
async function notifyFeedback({ kind, name, email, message } = {}) {
  const to = process.env.NOTIFY_EMAIL || DEFAULT_TO;
  const subject = `New ${kind || 'feedback'} from the AI Career Courses site`;
  const text = [
    `Type: ${kind || 'feedback'}`,
    `Name: ${name || '(not provided)'}`,
    `Email: ${email || '(not provided)'}`,
    '',
    message || '',
  ].join('\n');
  const replyTo = email && EMAIL_RE.test(email) ? email : undefined;

  const resendKey = process.env.RESEND_API_KEY;
  if (resendKey) {
    const payload = { from: process.env.NOTIFY_FROM || 'onboarding@resend.dev', to, subject, text };
    if (replyTo) payload.reply_to = replyTo;
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { authorization: `Bearer ${resendKey}`, 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Resend ${res.status}`);
    return { sent: true, via: 'resend' };
  }

  const hook = process.env.NOTIFY_WEBHOOK_URL;
  if (hook) {
    const payload = { to, subject, text };
    if (replyTo) payload.replyTo = replyTo;
    const res = await fetch(hook, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`webhook ${res.status}`);
    return { sent: true, via: 'webhook' };
  }

  return { sent: false, reason: 'no notification channel configured' };
}

module.exports = { notifyCourseRequest, notifyFeedback };
