/** Provider-neutral physical deletion gate. Does not assume a Forge delete API exists. */
export type DeleteOutcome =
  | { status: 'deleted'; referenceMayBeRemoved: true }
  | { status: 'already_absent'; referenceMayBeRemoved: true }
  | { status: 'retry_required'; referenceMayBeRemoved: false; reason: 'provider_error' | 'unverified' };

export type ObjectStore = {
  deleteObject(key: string): Promise<void>;
  objectExists(key: string): Promise<boolean>;
};

/**
 * Only a verified absence permits clearing the database storage key.
 * Callers MUST enforce owner scope on the database record before invoking this.
 * Repeated invocations are idempotent if the provider treats absent deletes as success.
 */
export async function deleteAndVerifyObject(
  store: ObjectStore,
  key: string,
): Promise<DeleteOutcome> {
  if (!key || key.startsWith('/') || key.includes('..') || key.includes('\\')) {
    return { status: 'retry_required', referenceMayBeRemoved: false, reason: 'unverified' };
  }
  try {
    const existed = await store.objectExists(key);
    if (!existed) return { status: 'already_absent', referenceMayBeRemoved: true };
    await store.deleteObject(key);
    if (await store.objectExists(key)) {
      return { status: 'retry_required', referenceMayBeRemoved: false, reason: 'unverified' };
    }
    return { status: 'deleted', referenceMayBeRemoved: true };
  } catch {
    return { status: 'retry_required', referenceMayBeRemoved: false, reason: 'provider_error' };
  }
}
