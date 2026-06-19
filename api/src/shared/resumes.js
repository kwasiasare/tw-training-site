'use strict';

// Private résumé storage on Cloudflare R2 (TW-63). Résumés are PII — they go in a
// dedicated PRIVATE bucket (tw-resumes), never the public videos bucket, and are
// never served publicly. Credentials come from SWA app settings; prefer dedicated
// RESUME_R2_* creds scoped to this bucket, falling back to the shared R2_* creds.

const { S3Client, PutObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');

let client;

function getClient() {
  if (client) return client;
  const accountId = process.env.R2_ACCOUNT_ID;
  const accessKeyId = process.env.RESUME_R2_ACCESS_KEY_ID || process.env.R2_ACCESS_KEY_ID;
  const secretAccessKey = process.env.RESUME_R2_SECRET_ACCESS_KEY || process.env.R2_SECRET_ACCESS_KEY;
  if (!accountId || !accessKeyId || !secretAccessKey) {
    throw new Error('résumé R2 storage is not configured');
  }
  client = new S3Client({
    region: 'auto',
    endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
    credentials: { accessKeyId, secretAccessKey },
  });
  return client;
}

function bucket() {
  return process.env.RESUME_R2_BUCKET || 'tw-resumes';
}

// Store a résumé PDF for a user. Key is namespaced by userId. Returns {bucket,key}.
async function putResume(userId, buffer, stamp) {
  const key = `${userId}/${stamp || Date.now()}.pdf`;
  await getClient().send(new PutObjectCommand({
    Bucket: bucket(),
    Key: key,
    Body: buffer,
    ContentType: 'application/pdf',
  }));
  return { bucket: bucket(), key };
}

async function deleteResume(key) {
  await getClient().send(new DeleteObjectCommand({ Bucket: bucket(), Key: key }));
}

module.exports = { putResume, deleteResume };
