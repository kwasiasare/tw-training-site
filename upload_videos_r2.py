"""Upload lesson videos to Cloudflare R2 (S3-compatible API).

Reads R2_* credentials from .env, uploads every .mp4 in site/public/videos/
to the bucket root keyed by filename, so <R2_PUBLIC_BASE>/<filename> resolves.

Idempotent: skips a file if an object of the same size already exists.
Run:  python upload_videos_r2.py
"""
import os
import sys
import pathlib

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

ROOT = pathlib.Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "site" / "public" / "videos"


def load_env(path: pathlib.Path) -> dict:
    env = {}
    if not path.exists():
        sys.exit(f"ERROR: {path} not found")
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def main() -> None:
    env = load_env(ROOT / ".env")
    required = ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY",
                "R2_BUCKET", "R2_PUBLIC_BASE"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        sys.exit(f"ERROR: missing in .env: {', '.join(missing)}")

    bucket = env["R2_BUCKET"]
    endpoint = f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com"

    s3 = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=env["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
        config=Config(signature_version="s3v4", retries={"max_attempts": 5, "mode": "standard"}),
    )

    # --- Connection / auth test ---
    try:
        s3.head_bucket(Bucket=bucket)
        print(f"Connected to R2 bucket '{bucket}' OK.")
    except ClientError as e:
        sys.exit(f"ERROR: cannot access bucket '{bucket}': {e}")

    files = sorted(VIDEO_DIR.glob("*.mp4"))
    if not files:
        sys.exit(f"ERROR: no .mp4 files in {VIDEO_DIR}")
    print(f"Found {len(files)} videos to upload.\n")

    uploaded = skipped = 0
    for i, f in enumerate(files, 1):
        key = f.name
        size = f.stat().st_size
        # Skip if same-size object already present.
        try:
            head = s3.head_object(Bucket=bucket, Key=key)
            if head["ContentLength"] == size:
                print(f"[{i:>2}/{len(files)}] skip (exists) {key}")
                skipped += 1
                continue
        except ClientError:
            pass  # not present -> upload

        s3.upload_file(
            str(f), bucket, key,
            ExtraArgs={"ContentType": "video/mp4", "CacheControl": "public, max-age=31536000, immutable"},
        )
        print(f"[{i:>2}/{len(files)}] up   {key}  ({size/1_048_576:.1f} MB)")
        uploaded += 1

    # --- Verify total objects in bucket ---
    total = 0
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket):
        total += page.get("KeyCount", 0)

    print(f"\nDone. uploaded={uploaded} skipped={skipped} bucket_objects={total}")
    print(f"Public base: {env['R2_PUBLIC_BASE']}")
    if files:
        print(f"Sample URL:  {env['R2_PUBLIC_BASE']}/{files[0].name}")


if __name__ == "__main__":
    main()
