---
name: everos-sdk-upgrade
description: >
  Migrate EverOS SDK between versions (Python only; Go/TS planned).
  Auto-detects current version, chains rules to target. TRIGGER when: code
  imports evermemos/everos, user mentions upgrade/migrate everos, or
  dependencies contain outdated SDK version.
user-invocable: true
argument-hint: "[target-version, default: latest]"
allowed-tools: Read Grep Glob Edit Bash(python -m py_compile *) Bash(pytest *)
---

# EverOS SDK Migration

Migrate from any SDK version to a target version (default: latest).
Currently supports **Python only**. Go and TypeScript support is planned.

## Step 1: Detect language

Search for EverOS SDK references across all supported languages:

```
Grep pattern="evermemos|everos" glob="*.py"
Grep pattern="evermemos|everos" glob="*.{go,mod}"
Grep pattern="evermemos|everos" glob="*.{ts,json}"
```

Classify by which files contain SDK references (not just by file existence):
- **Python**: `evermemos` or `everos` found in `*.py`, `pyproject.toml`, `requirements.txt` → ✓ **supported**
- **Go**: `evermemos` or `everos` found in `go.mod`, `*.go` → ✗ **not yet supported**
- **TypeScript**: `evermemos` or `everos` found in `package.json`, `*.ts` → ✗ **not yet supported**

NOTE: A project may contain `go.mod` or `package.json` without using the EverOS SDK in
those languages (e.g., mixed repos, frontend tooling). Only flag a language as detected
when SDK import/dependency references are actually found in that language's files.

If Go or TypeScript **SDK usage** is detected, warn the user but **do not stop**:
> "Found EverOS SDK references in Go/TypeScript files — migration for these languages is
> not yet supported. These files will be skipped. Refer to the v1 API documentation for
> manual migration guidance."

Then proceed with Python migration if Python SDK usage is also detected.

## Step 2: Detect current version

Use Grep to search for SDK usage patterns:

```
Grep pattern="evermemos|everos" glob="*.{py,toml,txt}"
```

Determine version from the patterns found:
- `evermemos` + `client.v0.` = **v0**
- `everos` + `client.v1.` = **v1**
- Higher versions: `client.vN.` = **vN**

## Step 3: Determine target version

- If user specified a target (e.g., `/everos-sdk-upgrade v2`), use that.
- Otherwise, find the highest version by scanning rule files (Step 4).

## Step 4: Discover migration path

Use Glob to find rule files for the detected language:

```
Glob pattern="migration/{language}/v*-to-v*.md" path="${CLAUDE_SKILL_DIR}"
```

Each file covers one version hop. Build the chain from current to target.
Example: v0 -> v3 = `v0-to-v1.md` + `v1-to-v2.md` + `v2-to-v3.md`.

If a required rule file is missing, inform the user and stop.

## Step 5: Apply each migration step

For each version hop, read the rule file and apply changes to **all Python files
that contain SDK imports** (as detected in Step 1), **in this order**:

1. **Package dependency** (pyproject.toml / requirements.txt)
2. **Environment variables** (.env, docker-compose, Dockerfile, CI, code, shell)
3. **Import statements** across all source files
4. **Client instantiation** (class/struct name + constructor params)
5. **API call signatures** (follow the rule file — these may be full rewrites)
6. **Type imports** (response/param type renames)
7. **Exception/error class references**

**Wildcard imports**: If code uses `from evermemos.types.v0 import *`, ask the user to
expand it to explicit imports first — wildcard imports make it impossible to reliably
track which types are in use and need renaming.

## Step 6: Suggest package update

After code changes, **tell the user** to update their installed package:

- `pip install everos>=<version>` or `uv sync`

Do NOT auto-run install commands. The user decides when and how to update.

## Step 7: Verify

Syntax-check modified files:

- `python -m py_compile <file>`

If tests exist, run them to verify collection.

### Limitations of syntax checking

Syntax checks (`py_compile`) catch import errors and basic syntax, but
**cannot** detect these common migration errors:

- **Field-level attribute errors**: accessing `p.item_type` on v1 Profile (should be `p.scenario`) — passes syntax check, crashes at runtime
- **Mutually exclusive params**: `delete(memory_id="...", user_id="...")` — valid syntax, 422 at runtime
- **Empty query string**: `search(query="")` — valid syntax, 422 at runtime
- **Return type changes**: `response = delete(...)` then `response.result.count` — valid syntax, AttributeError at runtime

To catch these, the migration agent should also diff the modified code against the v1
example file (Step "Verification examples" below) and verify that field access patterns
match the v1 canonical patterns.

Report a summary: files modified, changes per category, warnings for removed APIs.

## Verification examples

Use Glob to discover all version reference files:

```
Glob pattern="examples/*/v*.{py,go,ts}" path="${CLAUDE_SKILL_DIR}"
```

Each `v{N}.{ext}` is the canonical usage for that major version. To verify migration, diff the output against `v{M}.{ext}`. Example files only exist for major versions. For minor version migrations (e.g., v1→v1.1): the migration rule file (`v1-to-v1.1.md`) is the primary authority; only fall back to the major version example file (`v1.{ext}`) when the rule file does not cover a specific pattern.

## Rules for the migration agent

- Each rule file is self-contained with Before/After code, search patterns, and
  field mappings. Follow the rule file precisely.
- When APIs are **removed** with no replacement, FLAG to the user with a comment
  in the code. Do NOT silently delete.
- Do NOT auto-add new APIs that didn't exist in the source version.
- For complex signature rewrites, restructure carefully — NOT simple find-replace.
