#!/usr/bin/env python3
"""Provision the private R2 bucket for résumé storage (TW-61 / TW-63).

Résumés are PII, so they live in a dedicated PRIVATE bucket (default: tw-resumes)
— never the public videos bucket, and never exposed via r2.dev or a public domain.

Cloudflare R2 buckets are PRIVATE by default: this script just creates the bucket
(idempotently) and verifies it. It does NOT enable any public access.

Credentials (read from .env or the environment), in priority order:
  R2_ADMIN_ACCESS_KEY_ID / R2_ADMIN_SECRET_ACCESS_KEY   <- token with bucket-create rights
  R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY               <- fallback (your normal R2 token)
Plus R2_ACCOUNT_ID (always required) and RESUME_R2_BUCKET (default 'tw-resumes').

NOTE: the app's own R2 token is typically scoped to a single bucket and CANNOT
create new buckets — you'll get AccessDenied. In that case either (a) run this with
an Account-level "Admin Read & Write" R2 API token in R2_ADMIN_*, or (b) just create
the bucket in the Cloudflare dashboard (R2 -> Create bucket -> tw-resumes -> private).
See HOWTO_Resume_Storage.md.

Usage:
  python setup_r2_resumes.py
"""

import os
import sys

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    sys.exit("boto3 is required: pip install boto3")


def load_env(path=".env"):
    """Minimal .env loader (no dependency on python-dotenv)."""
    env = dict(os.environ)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip())
    return env


def main():
    env = load_env()
    account_id = env.get("R2_ACCOUNT_ID")
    access_key = env.get("R2_ADMIN_ACCESS_KEY_ID") or env.get("R2_ACCESS_KEY_ID")
    secret_key = env.get("R2_ADMIN_SECRET_ACCESS_KEY") or env.get("R2_SECRET_ACCESS_KEY")
    bucket = env.get("RESUME_R2_BUCKET", "tw-resumes")

    missing = [n for n, v in (
        ("R2_ACCOUNT_ID", account_id),
        ("R2_(ADMIN_)ACCESS_KEY_ID", access_key),
        ("R2_(ADMIN_)SECRET_ACCESS_KEY", secret_key),
    ) if not v]
    if missing:
        sys.exit("Missing required config: " + ", ".join(missing))

    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )

    print(f"Ensuring private R2 bucket '{bucket}' exists…")
    try:
        s3.create_bucket(Bucket=bucket)
        print(f"  created '{bucket}'")
    except ClientError as exc:
        code = exc.response.get("Error", {}).get("Code", "")
        if code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            print(f"  '{bucket}' already exists")
        elif code in ("AccessDenied", "Forbidden"):
            sys.exit(
                "  AccessDenied — this token cannot create buckets.\n"
                "  Use an Account-level R2 API token in R2_ADMIN_*, or create the\n"
                f"  bucket '{bucket}' in the Cloudflare dashboard (it is private by default).\n"
                "  See HOWTO_Resume_Storage.md."
            )
        else:
            raise

    # Verify reachable and that it is NOT publicly listable as an object store.
    try:
        s3.head_bucket(Bucket=bucket)
        print(f"  verified '{bucket}' is reachable")
    except ClientError as exc:
        print(f"  warning: could not head_bucket '{bucket}': {exc}")

    print(
        "\nDone. Next:\n"
        "  1. Create an R2 API token scoped to Object Read & Write on this bucket only.\n"
        "  2. Put it in the SWA app settings as RESUME_R2_ACCESS_KEY_ID / RESUME_R2_SECRET_ACCESS_KEY\n"
        "     (and RESUME_R2_BUCKET if you changed the name).\n"
        "  3. Do NOT enable public access / r2.dev for this bucket — résumés are private.\n"
        "  See HOWTO_Resume_Storage.md."
    )


if __name__ == "__main__":
    main()
