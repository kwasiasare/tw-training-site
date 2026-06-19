'use strict';

// Best-effort admin notification (TW-66). When a user requests a custom course,
// email the admin so they can dispatch the generate-course Action. Provider is
// chosen by app settings; if none is configured it's a no-op (the user's request
// still succeeds — notification must never block the flow).
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

module.exports = { notifyCourseRequest };
