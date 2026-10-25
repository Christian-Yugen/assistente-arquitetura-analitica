/** Explicit S3 deletion configuration; Forge presigned GET/PUT is not a delete contract. */
import { DeleteObjectCommand, HeadObjectCommand, S3Client } from "@aws-sdk/client-s3";
import type { ObjectStore } from "./physicalRetention";

export function physicalDeletionConfigured(): boolean {
  return Boolean(process.env.MODELGEM_S3_BUCKET && process.env.MODELGEM_S3_REGION &&
    process.env.MODELGEM_S3_ACCESS_KEY_ID && process.env.MODELGEM_S3_SECRET_ACCESS_KEY);
}

export function createPhysicalStore(): ObjectStore {
  if (!physicalDeletionConfigured()) throw new Error("physical_deletion_unavailable");
  const bucket = process.env.MODELGEM_S3_BUCKET!;
  const client = new S3Client({
    region: process.env.MODELGEM_S3_REGION!,
    credentials: {
      accessKeyId: process.env.MODELGEM_S3_ACCESS_KEY_ID!,
      secretAccessKey: process.env.MODELGEM_S3_SECRET_ACCESS_KEY!,
    },
    ...(process.env.MODELGEM_S3_ENDPOINT ? { endpoint: process.env.MODELGEM_S3_ENDPOINT } : {}),
  });
  return {
    async deleteObject(key) { await client.send(new DeleteObjectCommand({ Bucket: bucket, Key: key })); },
    async objectExists(key) {
      try { await client.send(new HeadObjectCommand({ Bucket: bucket, Key: key })); return true; }
      catch (error: unknown) {
        const code = (error as { name?: string; $metadata?: { httpStatusCode?: number } }).name;
        const status = (error as { $metadata?: { httpStatusCode?: number } }).$metadata?.httpStatusCode;
        if (code === "NotFound" || code === "NoSuchKey" || status === 404) return false;
        throw error;
      }
    },
  };
}
