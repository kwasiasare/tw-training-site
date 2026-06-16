# 🔐 How to set up Microsoft Entra External ID (authentication)

This wires user accounts (register / login / logout) into the site via Azure Static Web Apps'
built-in auth, using **Microsoft Entra External ID** (CIAM) as a custom OpenID Connect provider.

**Who does what:** you create the external tenant + app in the Azure portal (steps below) and
hand back four values. Then Claude upgrades the SWA to Standard, sets the secrets, wires the
config, and verifies the login flow.

**Cost:** Entra External ID is free under 50,000 monthly active users. The only cost is the SWA
**Standard** plan (~$9/month), which is required for custom auth providers.

---

## What you'll hand back
At the end you'll give Claude these four values:
1. **Tenant subdomain** — e.g. `twtraining` (from `twtraining.ciamlogin.com`)
2. **Directory (tenant) ID** — a GUID
3. **Application (client) ID** — a GUID
4. **Client secret value** — a string (shown only once)

---

## Step 1 — Create an external tenant
1. Go to the **Microsoft Entra admin center**: <https://entra.microsoft.com>.
2. **Identity → Overview → Manage tenants → Create**.
3. Choose **External** (this is the CIAM / customer-facing tenant type), click **Continue**.
4. Give it a name (e.g. "TW Training") and a domain/subdomain (e.g. `twtraining`), pick a location, **Create**.
5. Switch into the new tenant (top-right tenant switcher). Note its **subdomain** and **Directory (tenant) ID** (Overview page).

## Step 2 — Register the application
1. In the external tenant: **Applications → App registrations → New registration**.
2. **Name:** `TW Training Website`.
3. **Supported account types:** *Accounts in this organizational directory only*.
4. **Redirect URI:** platform **Web**, value:
   ```
   https://gray-river-01e111b0f.7.azurestaticapps.net/.auth/login/entraExternalId/callback
   ```
   *(This is the production SWA host. If we test on a preview host first, we'll add that callback too.)*
5. Click **Register**. Copy the **Application (client) ID**.

## Step 3 — Create a client secret
1. In the app: **Certificates & secrets → Client secrets → New client secret**.
2. Description `swa`, expiry 12–24 months, **Add**.
3. **Copy the secret _Value_ now** (not the Secret ID) — it's shown only once.

## Step 4 — Create a sign-up / sign-in user flow
1. In the external tenant: **External Identities → User flows → New user flow**.
2. Name it (e.g. `signupsignin`), select **Email with password** (and any social providers you want later).
3. Choose the user attributes to collect (e.g. Display Name, Email).
4. **Create**, then open the flow → **Applications → Add application** → select `TW Training Website`.

## Step 5 — Confirm the OIDC metadata URL
The provider's well-known configuration URL is:
```
https://<subdomain>.ciamlogin.com/<tenant-id>/v2.0/.well-known/openid-configuration
```
Open it in a browser to confirm it returns JSON (issuer, authorization_endpoint, etc.).

## Step 6 — Hand the four values to Claude
Give Claude: **subdomain**, **tenant ID**, **client ID**, **client secret value**. Do **not** paste
the secret into the repo — it goes into SWA application settings (never committed).

---

## What Claude does next (automated)
1. `az staticwebapp update --sku Standard` (the approved tier upgrade).
2. Set SWA app settings `ENTRA_CLIENT_ID` and `ENTRA_CLIENT_SECRET` (secrets, never in git).
3. Add the custom OIDC provider to `staticwebapp.config.json`:
   ```json
   "auth": {
     "identityProviders": {
       "customOpenIdConnectProviders": {
         "entraExternalId": {
           "registration": {
             "clientIdSettingName": "ENTRA_CLIENT_ID",
             "clientCredential": { "clientSecretSettingName": "ENTRA_CLIENT_SECRET" },
             "openIdConnectConfiguration": {
               "wellKnownOpenIdConfiguration": "https://<subdomain>.ciamlogin.com/<tenant-id>/v2.0/.well-known/openid-configuration"
             }
           },
           "login": { "scopes": ["openid", "profile", "email"] }
         }
       }
     }
   }
   ```
4. Deploy to a preview, sign in end-to-end, then merge to production.

## How it behaves
- **Lessons stay public** — sign-in is additive (for accounts/progress, which arrives with TW-4).
- Login: `/.auth/login/entraExternalId`; logout: `/.auth/logout`; identity: `/.auth/me`.
- Roles: authenticated users get the built-in `authenticated` role; an `administrator` role can be
  assigned later (for the admin dashboard, TW-6).

## Security notes
- The client secret lives only in SWA application settings — never in the repo.
- Rotate it in **Certificates & secrets**; update the `ENTRA_CLIENT_SECRET` app setting after.
