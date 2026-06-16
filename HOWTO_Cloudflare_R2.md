# 🎬 How to set up Cloudflare R2 for course videos

This is the **one task blocking deployment**. R2 hosts the 65 lesson videos (≈273 MB) with
**zero egress fees**, so the Astro site on Azure Static Web Apps stays small and cheap. Once the
five `R2_*` keys are in `.env`, Claude uploads the videos, rebuilds the site to load them from R2,
and deploys.

**Time:** ~10 minutes. **Cost:** free tier (10 GB storage, 1M writes/mo) easily covers this.

---

## Step 1 — Create a Cloudflare account
1. Go to <https://dash.cloudflare.com/sign-up> and sign up (or log in).
2. Verify your email. No domain or credit card is required for R2's free tier.

## Step 2 — Enable R2
1. In the dashboard left sidebar, click **R2 Object Storage**.
2. Click **Enable R2** / **Purchase R2**. You may be asked for a payment method to guard against
   overages — the free allowance (10 GB stored, 1M Class-A + 10M Class-B ops/month) is plenty here.

## Step 3 — Create the bucket
1. Click **Create bucket**.
2. **Bucket name:** `tw-course-videos`  *(must match `R2_BUCKET` in `.env`)*.
3. **Location:** Automatic is fine. Click **Create bucket**.

## Step 4 — Make the bucket publicly readable (r2.dev dev URL)
The site loads videos over plain HTTPS, so the bucket needs public read access.
1. Open the `tw-course-videos` bucket → **Settings** tab.
2. Under **Public access → R2.dev subdomain**, click **Allow Access** and confirm.
3. Cloudflare shows a **Public R2.dev Bucket URL** like:
   `https://pub-xxxxxxxxxxxxxxxxxxxxxxxx.r2.dev`
   **Copy it** — this is your `R2_PUBLIC_BASE`.

> 💡 *Optional, recommended later:* connect a custom domain (e.g. `videos.yourdomain.com`) under
> **Settings → Custom Domains** for nicer URLs and Cloudflare CDN caching. The r2.dev URL is fine
> to launch with.

## Step 5 — Create an API token (S3 credentials)
The upload script uses the S3-compatible API via `boto3`.
1. On the main **R2** page, click **Manage R2 API Tokens** (top-right) → **Create API token**.
2. **Token name:** `tw-course-upload`.
3. **Permissions:** **Object Read & Write**.
4. **Specify bucket(s):** restrict to `tw-course-videos` (least privilege).
5. Click **Create API Token**. Cloudflare shows **once**:
   - **Access Key ID** → `R2_ACCESS_KEY_ID`
   - **Secret Access Key** → `R2_SECRET_ACCESS_KEY`
   **Copy both now** — the secret is not shown again.

## Step 6 — Find your Account ID
1. On the **R2** overview page (or any Cloudflare dashboard page), the **Account ID** is shown in
   the right-hand sidebar / under the account menu. It's a 32-char hex string.
2. This is `R2_ACCOUNT_ID`. The S3 endpoint the script builds is
   `https://<R2_ACCOUNT_ID>.r2.cloudflarestorage.com`.

## Step 7 — Fill in `.env`
Open `.env` in the project root and add (alongside the existing Azure keys):
```
R2_ACCOUNT_ID=your32charhexaccountid
R2_ACCESS_KEY_ID=youraccesskeyid
R2_SECRET_ACCESS_KEY=yoursecretaccesskey
R2_BUCKET=tw-course-videos
R2_PUBLIC_BASE=https://pub-xxxxxxxxxxxxxxxxxxxxxxxx.r2.dev
```
`.env` is git-ignored — never commit it. (`.env.example` documents these keys for anyone cloning.)

## Step 8 — Tell Claude "done"
Claude then automatically:
1. Uploads all 65 MP4s from `site/public/videos/` to the R2 bucket (boto3, S3 API).
2. Rebuilds the site with `PUBLIC_VIDEO_CDN_BASE=<R2_PUBLIC_BASE>` so `<VideoEmbed>` points at R2.
3. Strips `dist/videos` so nothing heavy is bundled into the SWA deploy.
4. Runs `az staticwebapp create` (Free tier) and deploys `dist` → returns your live URL.

---

## ✅ Quick verification
After Step 4 you can sanity-check public access: upload any small file in the bucket UI, then open
`<R2_PUBLIC_BASE>/<filename>` in a browser — it should download/play. If you get **Access Denied**,
the r2.dev public access toggle (Step 4) isn't enabled.

## 🔒 Security notes
- The API token is scoped to **one bucket** with read/write only — it can't touch the rest of your account.
- If a key ever leaks, revoke it under **Manage R2 API Tokens** and create a new one.
- Public read is intentional for now (videos are course content). When auth lands (TW-3/TW-5), switch
  to **signed URLs**: make the bucket private and generate short-lived presigned GET links per user.

## 💸 Cost expectation
- Storage: 273 MB ≪ 10 GB free tier → **$0**.
- Egress: **$0 on R2 always** (this is the whole reason for R2 over Azure Blob).
- Uploads: ~65 writes, far under 1M/month free → **$0**.
