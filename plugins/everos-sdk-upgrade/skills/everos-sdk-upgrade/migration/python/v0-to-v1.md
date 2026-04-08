# Migration Rules: evermemos (v0) -> everos (v1)

This file contains every breaking change between the two SDK versions.
Apply rules in the order listed.

## Contents

- RULE-001: Package Dependency (rename evermemos -> everos)
- RULE-002: Environment Variables (EVERMEMOS_API_KEY -> EVEROS_API_KEY)
- RULE-003: Import Statements (module + type renames)
- RULE-004: Client Class (EverMemOS -> EverOS)
- RULE-005: Exception Classes (EverMemOSError -> EverOSError)
- RULE-006: Resource Path (.v0. -> .v1.)
- RULE-007: memories.add() — **COMPLETE REWRITE** (single msg -> batch array)
- RULE-008: memories.delete() (HTTP method + return type change)
- RULE-009: memories.get() — **COMPLETE REWRITE** (no params -> filters DSL)
- RULE-010: memories.search() — **COMPLETE REWRITE** (no params -> filters + query)
- RULE-011: Removed Resources — conversation_meta field-by-field migration + status.request → tasks.retrieve
- RULE-012: New v1 Features (informational)
- RULE-013: Response Structure Rewrite (.result->.data, .memories->.episodes, add .request_id->.data.task_id)
- Quick Reference: Search-and-Replace Checklist

---

## RULE-001: Package Dependency

### Change Type: BREAKING - Package Rename

**Before (v0):**
```
# pyproject.toml
dependencies = ["evermemos>=0.3.0"]

# requirements.txt
evermemos>=0.3.0
evermemos==0.3.13
```

**After (v1):**
```
# pyproject.toml
dependencies = ["everos>=0.1.0"]

# requirements.txt
everos>=0.1.0
everos==0.1.1
```

### Search Patterns:
- `evermemos` in pyproject.toml, requirements*.txt, setup.py, setup.cfg, Pipfile

### Steps:
1. FIND: `evermemos` in dependency declarations
2. REPLACE: with `everos`
3. Update version constraints to `>=0.1.0`

---

## RULE-002: Environment Variables

### Change Type: BREAKING - Env Var Rename

**Before (v0):**
```bash
EVERMEMOS_API_KEY=sk-xxx
EVER_MEM_OS_BASE_URL=https://api.evermind.ai
```

**After (v1):**
```bash
EVEROS_API_KEY=sk-xxx
EVER_OS_BASE_URL=https://api.evermind.ai
```

### Search Patterns:
- `EVERMEMOS_API_KEY` -> `EVEROS_API_KEY`
- `EVER_MEM_OS_BASE_URL` -> `EVER_OS_BASE_URL`

### Steps:
1. Search all files: .env, .env.*, docker-compose*.yml, Dockerfile, *.py, *.sh, CI configs
2. FIND: `EVERMEMOS_API_KEY` REPLACE: `EVEROS_API_KEY`
3. FIND: `EVER_MEM_OS_BASE_URL` REPLACE: `EVER_OS_BASE_URL`

---

## RULE-003: Import Statements

### Change Type: BREAKING - Module Rename

**Before (v0):**
```python
import evermemos
from evermemos import EverMemOS, AsyncEverMemOS
from evermemos import EverMemOSError
from evermemos.types.v0 import MemoryAddResponse, MemoryGetResponse, MemorySearchResponse, MemoryDeleteResponse
from evermemos.types.v0 import MemoryType, Metadata
from evermemos.types.v0.memories import (
    ConversationMetaCreateResponse,
    ConversationMetaUpdateResponse,
    ConversationMetaGetResponse,
)
from evermemos.types.v0.status import RequestGetResponse
```

**After (v1):**
```python
import everos
from everos import EverOS, AsyncEverOS
from everos import EverOSError
from everos.types.v1 import AddResponse, GetMemoriesResponse, SearchMemoriesResponse
from everos.types.v1 import (
    ContentItemParam, MessageItemParam, FlushResponse,
    EpisodeItem, ProfileItem, RawMessageDto,
)
# NOTE: ConversationMeta types are REMOVED in v1 - no direct replacement
# NOTE: Status types are REMOVED in v1 - no direct replacement
```

### Search Patterns (regex):
- `^import evermemos` -> `import everos`
- `^from evermemos` -> `from everos`
- `evermemos\.` -> `everos.`
- `\.types\.v0` -> `.types.v1`
- `\.resources\.v0` -> `.resources.v1`

### Type Rename Mapping:

| v0 Type | v1 Type | Notes |
|---------|---------|-------|
| `MemoryAddResponse` | `AddResponse` | |
| `MemoryGetResponse` | `GetMemoriesResponse` | |
| `MemorySearchResponse` | `SearchMemoriesResponse` | |
| `MemoryDeleteResponse` | *(returns None)* | v1 delete returns None |
| `MemoryType` | *(removed)* | Use Literal types inline |
| `Metadata` | *(removed)* | |
| `ConversationMetaCreateResponse` | **REMOVED** | No v1 equivalent |
| `ConversationMetaUpdateResponse` | **REMOVED** | No v1 equivalent |
| `ConversationMetaGetResponse` | **REMOVED** | No v1 equivalent |
| `RequestGetResponse` | **REMOVED** | Use `GetTaskStatusResponse` for async tasks |

### Steps:
1. FIND all `import evermemos` / `from evermemos` and REPLACE with `everos`
2. FIND `.types.v0` REPLACE `.types.v1`
3. FIND `.resources.v0` REPLACE `.resources.v1`
4. Rename type references per mapping table
5. FLAG any ConversationMeta or Status type usage to user

---

## RULE-004: Client Class

### Change Type: BREAKING - Class Rename

**Before (v0):**
```python
from evermemos import EverMemOS, AsyncEverMemOS

client = EverMemOS(api_key="sk-xxx")
async_client = AsyncEverMemOS(api_key="sk-xxx")

# Or with env var (auto-inferred from EVERMEMOS_API_KEY)
client = EverMemOS()
```

**After (v1):**
```python
from everos import EverOS, AsyncEverOS

client = EverOS(api_key="sk-xxx")
async_client = AsyncEverOS(api_key="sk-xxx")

# Or with env var (auto-inferred from EVEROS_API_KEY)
client = EverOS()
```

### Search Patterns:
- `EverMemOS(` -> `EverOS(`
- `AsyncEverMemOS(` -> `AsyncEverOS(`
- `EverMemOS` (as type hint) -> `EverOS`
- `AsyncEverMemOS` (as type hint) -> `AsyncEverOS`

### Steps:
1. FIND: `EverMemOS` REPLACE: `EverOS` (all occurrences including type hints)
2. FIND: `AsyncEverMemOS` REPLACE: `AsyncEverOS`

---

## RULE-005: Exception Classes

### Change Type: BREAKING - Exception Rename

**Before (v0):**
```python
from evermemos import EverMemOSError
try:
    ...
except EverMemOSError as e:
    ...
```

**After (v1):**
```python
from everos import EverOSError
try:
    ...
except EverOSError as e:
    ...
```

### Search Patterns:
- `EverMemOSError` -> `EverOSError`

---

## RULE-006: Resource Path (v0 -> v1)

### Change Type: BREAKING - Namespace Change

**Before (v0):**
```python
client.v0.memories.add(...)
client.v0.memories.get()
client.v0.memories.search()
client.v0.memories.delete(...)
client.v0.memories.conversation_meta.create(...)
client.v0.status.request.get(...)
```

**After (v1):**
```python
client.v1.memories.add(...)
client.v1.memories.get(...)
client.v1.memories.search(...)
client.v1.memories.delete(...)
# conversation_meta -> REMOVED
# status.request -> REMOVED (use client.v1.tasks.retrieve(task_id) for async tasks)
```

### Search Patterns:
- `\.v0\.` -> `.v1.`
- `client.v0` -> `client.v1`

### Steps:
1. FIND: `.v0.` REPLACE: `.v1.` in all API call chains
2. FLAG any `.conversation_meta.` usage - REMOVED in v1
3. FLAG any `.status.request.` usage - REMOVED in v1

---

## RULE-007: memories.add() - COMPLETE REWRITE

### Change Type: BREAKING - Signature Rewrite

This is the most complex change. v0 accepts single message fields; v1 accepts a
batch messages array with a completely different structure.

**Before (v0):**
```python
response = client.v0.memories.add(
    content="Hello, how are you?",
    create_time="2024-01-15T10:30:00+08:00",
    message_id="msg-001",
    sender="user-123",
    role="user",
    flush=True,
    group_id="grp-001",
    group_name="My Group",
    sender_name="Alice",
    refer_list=["msg-000"],
)
# response: MemoryAddResponse
```

**After (v1):**
```python
response = client.v1.memories.add(
    messages=[
        {
            "content": "Hello, how are you?",
            "role": "user",
            "timestamp": 1705285800000,  # unix ms, was ISO 8601 string
            "sender_id": "user-123",     # was "sender"
        }
    ],
    user_id="user-123",                  # explicit, was inferred from "sender"
    session_id=None,                     # new field
    # async_mode=True,                   # optional: async processing
)
# response: AddResponse
#
# For flushing, call separately:
# client.v1.memories.flush(user_id="user-123")
```

### Field Mapping:

| v0 Field | v1 Equivalent | Notes |
|----------|---------------|-------|
| `content` (str) | `messages[].content` (str or list[ContentItemParam]) | Moved into message object. v1 also supports multimodal content. |
| `create_time` (ISO 8601 str) | `messages[].timestamp` (int, unix ms) | **Format change**: ISO string -> unix milliseconds integer |
| `message_id` (str) | *(removed)* | No equivalent in v1 - SDK handles dedup internally |
| `sender` (str) | `messages[].sender_id` (str) + top-level `user_id` (str) | **Split**: sender -> sender_id in message, and explicit user_id at top level |
| `role` (str) | `messages[].role` ("user" \| "assistant") | Moved into message object |
| `flush` (bool) | *(removed)* | Use separate `client.v1.memories.flush(user_id=...)` call |
| `group_id` (str) | *(removed from add)* | Use `client.v1.memories.group.add()` for group memory |
| `group_name` (str) | *(removed)* | Use `client.v1.groups.create(group_id=..., name=...)` |
| `sender_name` (str) | *(removed from add)* | Use `client.v1.senders.create(sender_id=..., name=...)` |
| `refer_list` (list[str]) | *(removed)* | No equivalent in v1 |
| *(new)* | `session_id` (str, top-level) | Optional session context for memory grouping |
| *(new)* | `async_mode` (bool, top-level) | Set `True` to get `task_id` in response (needed for `tasks.retrieve` polling, see RULE-011) |

### IMPORTANT: async_mode and task_id

v0 always returned `request_id` in `MemoryAddResponse`. v1 only returns `task_id` in
`AddResponse.data.task_id` when `async_mode=True` is set. If your v0 code used
`response.request_id` for status polling, you MUST add `async_mode=True`:

```python
# v0: request_id always available
response = client.v0.memories.add(content="...", sender="user-123", role="user")
request_id = response.request_id  # always present

# v1: task_id requires async_mode=True
response = client.v1.memories.add(messages=[...], user_id="user-123", async_mode=True)
task_id = response.data.task_id   # only present with async_mode=True
```

### Conversion helper for timestamp:

```python
from datetime import datetime

# v0: ISO 8601 string
v0_time = "2024-01-15T10:30:00+08:00"

# v1: unix milliseconds
v1_timestamp = int(datetime.fromisoformat(v0_time).timestamp() * 1000)
# Result: 1705285800000
```

### Migration Steps:
1. Identify all `client.v0.memories.add(...)` calls
2. Extract the field values from the flat call
3. Restructure into `messages=[{...}]` array format
4. Convert `create_time` ISO string to `timestamp` unix milliseconds
5. Rename `sender` to `sender_id` inside message, add `user_id` at top level
6. If `flush=True` was used, add a separate `client.v1.memories.flush()` call after add
7. If `group_id` was used, switch to `client.v1.memories.group.add()` instead
8. Remove `message_id`, `group_name`, `sender_name`, `refer_list` (no v1 equivalents)

### Group Memory: memories.group.add()

If v0 code used `group_id` in `memories.add()`, v1 requires a **separate API**:
`client.v1.memories.group.add()`. The message structure (`GroupMessageItemParam`) differs
from personal memory (`MessageItemParam`):

- `sender_id` is **Required** per message (personal memory makes it optional)
- `group_id` is a **Required** top-level param (not in the message)
- `group_meta` is optional metadata dict (new in v1)

```python
# v0: group memory via memories.add(group_id=...)
client.v0.memories.add(
    content="Team standup notes",
    sender=USER_ID,
    role="user",
    group_id="grp-001",
    group_name="Dev Team",
    sender_name="Alice",
)

# v1: group memory via memories.group.add()
client.v1.groups.create(group_id="grp-001", name="Dev Team")   # create group first
client.v1.senders.create(sender_id=USER_ID, name="Alice")      # create sender first
client.v1.memories.group.add(
    group_id="grp-001",
    messages=[{
        "content": "Team standup notes",
        "role": "user",
        "sender_id": USER_ID,          # REQUIRED for group messages
        "timestamp": 1705285800000,
    }],
)
```

---

## RULE-008: memories.delete()

### Change Type: BREAKING - HTTP Method + Params + Return Type

**Before (v0):**
```python
# HTTP DELETE /api/v0/memories
response = client.v0.memories.delete(
    memory_id="mem-001",
    user_id="user-123",
    group_id="grp-001",
    id="mem-001",          # alias for memory_id
    event_id="mem-001",    # alias for memory_id
)
# response: MemoryDeleteResponse
```

**After (v1):**
```python
# HTTP POST /api/v1/memories/delete
# IMPORTANT: v1 has TWO mutually exclusive delete modes:

# Mode 1 - By ID (memory_id ONLY, no other fields allowed):
client.v1.memories.delete(memory_id="mem-001")

# Mode 2 - By filters (user_id and/or group_id, optional sender_id/session_id):
client.v1.memories.delete(
    user_id="user-123",
    group_id="grp-001",
    sender_id="sender-1",  # optional filter
    session_id="sess-1",   # optional filter
)
# returns None (not a response object)
```

### CRITICAL: Mutually Exclusive Delete Modes

v1 enforces strict separation:
- **By ID**: `memory_id` only — passing `user_id`, `group_id`, `sender_id`, or `session_id` alongside will raise 422
- **By filters**: `user_id` and/or `group_id` required — `memory_id` must NOT be present

v0 allowed mixing `memory_id` with `user_id`; v1 does NOT.

**When v0 code mixes both** (e.g., `delete(memory_id=x, user_id=y, group_id=z)`):
prefer the **memory_id-only** path and discard the filter params, as ID-based deletion
is more specific. Add a comment explaining the change.

### Field Mapping:

| v0 Field | v1 Equivalent | Notes |
|----------|---------------|-------|
| `memory_id` | `memory_id` | Same, but must be used ALONE (no other fields) |
| `user_id` | `user_id` | Same, but must NOT be combined with memory_id |
| `group_id` | `group_id` | Same, but must NOT be combined with memory_id |
| `id` | *(removed)* | Was alias for memory_id, just use memory_id |
| `event_id` | *(removed)* | Was alias for memory_id, just use memory_id |
| *(new)* | `sender_id` | Filter mode only |
| *(new)* | `session_id` | Filter mode only |

### CRITICAL: Return Type Change — MemoryDeleteResponse → None

v0 `delete()` returned `MemoryDeleteResponse` with `.result.count` and `.result.filters`.
v1 `delete()` returns **`None`**. Any code that accesses the return value will raise `AttributeError`.

```python
# v0: return value is usable
response = client.v0.memories.delete(user_id="user-123")
print(f"deleted {response.result.count} memories")  # works

# v1: returns None — accessing response will crash
client.v1.memories.delete(user_id="user-123")  # returns None
# response.result.count  ← AttributeError!
```

If v0 code stores or uses the delete response, remove those references entirely.

### Steps:
1. FIND: `client.v0.memories.delete(` REPLACE: `client.v1.memories.delete(`
2. Remove `id=` and `event_id=` params, use `memory_id=` instead
3. **If `memory_id` is present, REMOVE all other params** (user_id, group_id, etc.)
4. If only filter params (user_id, group_id) were used without memory_id, keep them
5. **If return value was captured** (`response = client.v0.memories.delete(...)`), remove the assignment or change to bare call — v1 returns `None`
6. **Remove all response field access** (`.result.count`, `.result.filters`, `.status`, `.message`) — these no longer exist
7. Update any type hints from `MemoryDeleteResponse` to `None`

---

## RULE-009: memories.get() - COMPLETE REWRITE

### Change Type: BREAKING - Signature Rewrite

**Before (v0):**
```python
# GET /api/v0/memories (no parameters)
response = client.v0.memories.get()
# response: MemoryGetResponse
```

**After (v1):**
```python
# POST /api/v1/memories/get (with filters DSL)
response = client.v1.memories.get(
    filters={"user_id": "user-123"},
    memory_type="episodic_memory",  # "episodic_memory" | "profile" | "agent_case" | "agent_skill"
    page=1,
    page_size=20,
    rank_by="timestamp",
    rank_order="desc",
)
# response: GetMemoriesResponse
```

### Note on extra_query pattern:

Some v0 users pass filters via `extra_query` since v0 SDK doesn't expose params:

```python
# v0 with extra_query workaround:
response = client.v0.memories.get(
    extra_query={"user_id": "user-123", "group_ids": "grp-workspace", "memory_type": "episodic_memory"},
)

# v1 (params are first-class):
response = client.v1.memories.get(
    filters={"user_id": "user-123", "group_id": "grp-workspace"},
    memory_type="episodic_memory",
)
```

Extract values from `extra_query` dict and map to v1's named parameters.

### CRITICAL: group_ids → group_id rename

v0 server uses `group_ids` (**plural**, `List[str]`).
v1 filters DSL uses `group_id` (**singular**, supports both string and `{"in": [...]}` array).

| v0 extra_query key | v1 filters key | Notes |
|-------------------|----------------|-------|
| `user_id` | `user_id` | Same |
| `group_ids` | `group_id` | **RENAMED**: plural → singular |
| `memory_type` | *(named param)* | Extracted to top-level `memory_type=` param |

```python
# v0: group_ids (plural, accepts string or list)
extra_query={"group_ids": "grp-workspace"}
extra_query={"group_ids": ["grp-1", "grp-2"]}

# v1: group_id (singular, use "in" operator for multiple)
filters={"group_id": "grp-workspace"}
filters={"group_id": {"in": ["grp-1", "grp-2"]}}
```

### Steps:
1. FIND: `client.v0.memories.get(` (with or without extra_query)
2. If `extra_query` was used:
   - Extract `user_id` → `filters={"user_id": ...}`
   - **Rename `group_ids` → `group_id`** in filters dict
   - If `group_ids` was a list, convert to `{"group_id": {"in": [...]}}`
   - Extract `memory_type` → top-level named param
3. REPLACE: with `client.v1.memories.get(filters={...}, memory_type="...")`
4. The user MUST provide `filters` (at minimum `user_id` or `group_id`) and `memory_type`
5. **NEVER use `group_ids` in v1 filters** — server rejects it with 422

---

## RULE-010: memories.search() - COMPLETE REWRITE

### Change Type: BREAKING - Signature Rewrite

**Before (v0):**
```python
# GET /api/v0/memories/search (no parameters in SDK, likely query params)
response = client.v0.memories.search()
# response: MemorySearchResponse
```

**After (v1):**
```python
# POST /api/v1/memories/search
response = client.v1.memories.search(
    filters={"user_id": "user-123"},
    query="what did we discuss yesterday",
    method="hybrid",          # "keyword" | "vector" | "hybrid" | "agentic"
    memory_types=["episodic_memory", "profile"],
    top_k=10,
    radius=0.7,
    include_original_data=False,
)
# response: SearchMemoriesResponse
```

### Note on extra_query pattern:

```python
# v0 with extra_query workaround:
response = client.v0.memories.search(
    extra_query={"user_id": "user-123", "group_ids": "grp-workspace", "query": "dark mode"},
)

# v1 (params are first-class):
response = client.v1.memories.search(
    filters={"user_id": "user-123", "group_id": "grp-workspace"},  # group_ids → group_id
    query="dark mode",
)
```

### CRITICAL: group_ids → group_id rename (same as RULE-009)

v0 uses `group_ids` (plural); v1 uses `group_id` (singular). See RULE-009 for details.

```python
# v0: group_ids (plural)
extra_query={"group_ids": ["grp-1", "grp-2"]}

# v1: group_id (singular, "in" operator for multiple)
filters={"group_id": {"in": ["grp-1", "grp-2"]}}
```

### New v1 search parameters (not present in v0)

These parameters are new in v1 and have no v0 equivalent. Do NOT auto-add during migration,
but document them in comments if the v0 code was filtering by memory type or needed raw data:

| v1 Parameter | Type | Notes |
|---|---|---|
| `memory_types` | `List[Literal["episodic_memory", "profile", "raw_message", "agent_memory"]]` | Filter search to specific memory types. **Note**: plural `memory_types` (search) vs singular `memory_type` (get, RULE-009) |
| `include_original_data` | `bool` | When `True`, response includes `.data.original_data` with raw source documents |
| `method` | `"keyword" \| "vector" \| "hybrid" \| "agentic"` | Search algorithm selection, defaults to hybrid |
| `top_k` | `int` | Maximum results to return |
| `radius` | `float` | Cosine similarity threshold (0.0–1.0), not an absolute distance |

### CRITICAL: query parameter

v1 SDK defines `query` as `Required[str]`, but the server rejects empty strings
(`query=""` → 422 "String should have at least 1 character"). Two safe approaches:

1. If the v0 code had a query string (in extra_query or elsewhere), use it directly
2. If no query can be inferred, FLAG to the user with a `TODO` comment — do NOT
   use `query=""` as a placeholder. This is a **migration-incomplete** state: report it
   in the summary as requiring user action before the code is production-ready. Example:

```python
response = client.v1.memories.search(
    filters={"user_id": USER_ID},
    query="TODO: specify search query",  # REQUIRED, must not be empty
)
```

### Steps:
1. FIND: `client.v0.memories.search(` (with or without extra_query)
2. If `extra_query` was used:
   - Extract `user_id` → `filters={"user_id": ...}`
   - **Rename `group_ids` → `group_id`** in filters dict (see RULE-009)
   - Extract `query` → top-level named param
3. REPLACE: with `client.v1.memories.search(filters={...}, query="...")`
4. The user MUST provide `filters` at minimum
5. **NEVER use `query=""`** — server rejects empty strings with 422
6. If no query can be inferred from the v0 code, use a descriptive TODO placeholder and mark the migration as **incomplete** in the summary

---

## RULE-011: Removed Resources — conversation_meta & status.request

### conversation_meta — field-by-field migration

v0 `conversation_meta.create()` / `.update()` / `.get()` are entirely removed. Fields are split across different v1 APIs.

#### conversation_meta Field Migration Table

| v0 conversation_meta field | v1 destination | Migration approach |
|--------------------------|---------|---------|
| `scene` ("group_chat" / "assistant") | **DROPPED** | v1 distinguishes implicitly: personal via `client.v1.memories.add()`, group via `client.v1.memories.group.add()` |
| `llm_custom_setting` (boundary/extraction/extra) | **Migrated to settings** | `client.v1.settings.update(llm_custom_setting={...})`, structure identical (boundary/extraction/extra) |
| `default_timezone` | **Migrated to settings** | `client.v1.settings.update(timezone="Asia/Shanghai")` |
| `description` | **DROPPED** | No v1 equivalent, remove |
| `scene_desc` | **DROPPED** | No v1 equivalent, remove |
| `tags` | **DROPPED** | No v1 equivalent, remove |
| `user_details` | **PARTIAL** | See WARNING below — data loss |
| `created_at` | **DROPPED** | v1 settings manages timestamps automatically |

#### WARNING: user_details Data Loss

v0 `user_details` contained rich user metadata per user:
```python
user_details={"user_001": {"full_name": "Alice", "role": "user", "custom_role": "developer", "extra": {...}}}
```

v1 `senders.create()` only accepts **`sender_id` + `name`**. The following fields are **permanently lost** with no v1 equivalent:
- `role` — no replacement
- `custom_role` — no replacement
- `extra` — no replacement

FLAG this to the user during migration with a comment listing the dropped fields:
```python
# WARNING: v0 user_details fields lost in migration:
#   role="user", custom_role="developer", extra={...}
#   v1 senders only supports sender_id + name
client.v1.senders.create(sender_id="user_001", name="Alice")
```

#### Migration Code Examples

**Before (v0) — conversation_meta.create:**

```python
client.v0.memories.conversation_meta.create(
    created_at="2025-01-15T10:00:00+00:00",
    scene="group_chat",
    default_timezone="Asia/Shanghai",
    llm_custom_setting={
        "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
        "extraction": {"model": "qwen3-235b", "provider": "openrouter"},
    },
    description="Tech discussion",
    tags=["work", "technical"],
    user_details={
        "user_001": {"full_name": "Alice", "role": "user", "custom_role": "developer"},
    },
)
```

**After (v1) — split into settings + groups:**

```python
# 1. llm_custom_setting + timezone → settings API (global config, set once)
client.v1.settings.update(
    llm_custom_setting={
        "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
        "extraction": {"model": "qwen3-235b", "provider": "openrouter"},
    },
    timezone="Asia/Shanghai",
)

# 2. scene → implicit (no explicit setting needed)
#    personal: client.v1.memories.add(messages=[...], user_id="...")
#    group: client.v1.memories.group.add(group_id="...", messages=[...])

# 3. user_details → partially replaced by senders resource
#    v0 user_details had full_name, role, custom_role, extra
#    v1 senders only keeps sender_id + name (maps to v0 sender + full_name)
#    role/custom_role/extra have no v1 equivalent, dropped
#    Example:
#    client.v1.senders.create(sender_id="user_001", name="Alice")

# 4. description, tags, scene_desc, created_at → dropped, remove
```

#### IMPORTANT: Scope Change

v0 `conversation_meta` was **per-group scoped** (each group could have independent config, with fallback to default).

v1 `settings` is a **global singleton** (no group_id scoping, entire space shares one config).

If user's v0 code set different `llm_custom_setting` for different group_ids, v1 cannot migrate directly — must consolidate into one global config. FLAG this to the user during migration.

**Multi-group consolidation guidance:**

If v0 code calls `conversation_meta.create()` or `.update()` multiple times with different
`llm_custom_setting` for different groups, the migration agent MUST:

1. Identify all distinct `llm_custom_setting` configs across groups
2. If they are identical → use the single config in `settings.update()`
3. If they differ → **do NOT auto-pick one**. Add a `# TODO: MANUAL REVIEW REQUIRED` comment
   listing ALL group configs, and leave the `settings.update()` call with a placeholder.
   The user MUST manually decide which config to use as the global default.
4. This is a **migration-incomplete** state — report it in the summary as requiring user action

```python
# TODO: MANUAL REVIEW REQUIRED — v0 had per-group llm_custom_setting:
#   grp-001: boundary=gpt-4.1-mini, extraction=qwen3-235b
#   grp-002: boundary=claude-sonnet-4-5-20250514, extraction=gpt-4.1
# v1 settings is a global singleton — you must manually choose one config:
client.v1.settings.update(
    llm_custom_setting={  # FILL IN: choose from configs above
        "boundary": {"model": "...", "provider": "..."},
        "extraction": {"model": "...", "provider": "..."},
    },
)
```

**Before (v0) — conversation_meta.update:**

```python
client.v0.memories.conversation_meta.update(
    llm_custom_setting={...},
    default_timezone="UTC",
)
```

**After (v1):**

```python
client.v1.settings.update(
    llm_custom_setting={...},
    timezone="UTC",
)
```

**Before (v0) — conversation_meta.get:**

```python
meta = client.v0.memories.conversation_meta.get()
```

**After (v1):**

```python
settings = client.v1.settings.retrieve()
# settings.data contains llm_custom_setting, timezone, extraction_mode, etc.
```

#### Migration Steps:

1. FIND: `conversation_meta.create(` or `conversation_meta.update(`
2. Extract `llm_custom_setting` and `default_timezone` params
3. REPLACE: with `client.v1.settings.update(llm_custom_setting=..., timezone=...)`
4. FIND: `conversation_meta.get()`
5. REPLACE: with `client.v1.settings.retrieve()`
6. Remove `scene`, `description`, `scene_desc`, `tags`, `user_details`, `created_at` params
7. Add comment explaining `scene` is now implicit via API choice

#### Migrating group_name from v0 add()

v0 `memories.add(group_name="Dev Team Chat")` requires pre-creating group in v1:

```python
# v1: create/update group first (group_name → groups.create name)
client.v1.groups.create(group_id="grp-workspace", name="Dev Team Chat")

# Then use group.add for group memory ingestion
client.v1.memories.group.add(group_id="grp-workspace", messages=[...])
```

---

### status.request — migrated to tasks.retrieve

**Before (v0):**

```python
response = client.v0.status.request.get(request_id="req-123")
# response: RequestGetResponse(success, data, found, message, request_id, status)
```

**After (v1):**

```python
response = client.v1.tasks.retrieve(task_id="task-123")
# response: GetTaskStatusResponse(data: TaskStatusResult(status, task_id))
# status: "processing" | "success" | "failed"
```

#### Field Mapping

| v0 RequestGetResponse | v1 GetTaskStatusResponse | Notes |
|----------------------|-------------------------|-------|
| `request_id` (param) | `task_id` (param) | Param renamed |
| `status` ("queued"/"success"/...) | `data.status` ("processing"/"success"/"failed") | Value changed: "queued" → "processing" |
| `success` (bool) | *(removed)* | Use status to determine |
| `found` (bool) | *(removed)* | Not found throws exception |
| `data` (dict) | *(removed)* | v1 does not return detailed execution data |
| `message` (str) | *(removed)* | v1 does not return message text |

#### Note: task_id Source Change

v0's `request_id` came from `MemoryAddResponse.request_id`.
v1's `task_id` comes from `AddResponse.data.task_id` (requires `async_mode=True` to be returned).

```python
# v1: use async_mode to get task_id
response = client.v1.memories.add(messages=[...], user_id="...", async_mode=True)
task_id = response.data.task_id

# Then poll
status = client.v1.tasks.retrieve(task_id=task_id)
```

#### Migration Steps:

1. FIND: `client.v0.status.request.get(request_id=`
2. REPLACE: `client.v1.tasks.retrieve(task_id=`
3. Update response field access: `response.status` → `response.data.status`
4. Update status value checks: `"queued"` → `"processing"`
5. If code depends on `response.success` / `response.found` / `response.message`, replace with `response.data.status` check

---

## RULE-012: New v1 Features (informational, do NOT auto-add)

These resources are new in v1. Do NOT add them during migration unless the user
explicitly asks. List them in the migration summary for awareness:

| Resource | Purpose |
|----------|---------|
| `client.v1.memories.flush()` | Trigger boundary detection (replaces v0 `flush=True` param) |
| `client.v1.memories.agent.add()` / `.flush()` | Agent trajectory memory |
| `client.v1.memories.group.add()` / `.flush()` | Group memory (replaces v0 group_id in add) |
| `client.v1.groups.create/retrieve/patch()` | Group CRUD |
| `client.v1.senders.create/retrieve/patch()` | Sender CRUD |
| `client.v1.settings.retrieve/update()` | Global settings |
| `client.v1.tasks.retrieve()` | Async task status |
| `client.v1.object.sign()` | Multimodal pre-signed upload |
| Multimodal content in messages | `content` can be `list[ContentItemParam]` with image/audio/doc/pdf types |

---

## RULE-013: Response Structure Rewrite

### Change Type: BREAKING - Response Wrapper + Field Renames

Two changes: (1) top-level accessor `.result` → `.data`, and (2) field names
inside the response are renamed.

**Before (v0):**
```python
# get response (MemoryGetResponse)
response = client.v0.memories.get()
memories = response.result.memories      # list of memory objects
total = response.result.total_count
count = response.result.count

# search response (MemorySearchResponse)
response = client.v0.memories.search()
memories = response.result.memories      # list of memory objects
profiles = response.result.profiles
```

**After (v1):**
```python
# get response (GetMemoriesResponse -> GetMemResponse)
response = client.v1.memories.get(filters={...}, memory_type="episodic_memory")
episodes = response.data.episodes        # was .memories, now .episodes
profiles = response.data.profiles        # was nested in .memories, now top-level
agent_cases = response.data.agent_cases  # new field
agent_skills = response.data.agent_skills  # new field
total = response.data.total_count
count = response.data.count

# search response (SearchMemoriesResponse -> SearchMemoriesResponseData)
response = client.v1.memories.search(filters={...}, query="...")
episodes = response.data.episodes        # was .memories, now .episodes
profiles = response.data.profiles        # top-level, not nested
agent_memory = response.data.agent_memory  # new field
raw_messages = response.data.raw_messages  # new field
```

### Field Rename Mapping:

| v0 field | v1 field | Notes |
|----------|----------|-------|
| `.result` | `.data` | Top-level wrapper rename |
| `.result.memories` | `.data.episodes` | **Renamed**: memories → episodes |
| `.result.profiles` | `.data.profiles` | Kept, but now top-level in search response |
| `.result.total_count` | `.data.total_count` | Same for **get** only. **search** response has no total_count in v1 |
| `.result.count` | `.data.count` | Same for **get** only |
| *(new)* | `.data.agent_cases` | New in v1 get |
| *(new)* | `.data.agent_skills` | New in v1 get |
| *(new)* | `.data.agent_memory` | New in v1 search |
| *(new)* | `.data.raw_messages` | New in v1 search (replaces v0 `.result.pending_messages`) |
| `.result.pending_messages` | `.data.raw_messages` | **Renamed**: pending_messages → raw_messages |
| `.result.query_metadata` | `.data.query` | **Renamed + restructured**: QueryMetadata → Query |
| `.result.metadata` | *(removed)* | v0 Metadata object not present in v1 responses |

### Add response field changes:

```python
# v0 add response (MemoryAddResponse)
response.request_id   # str
response.message      # str
response.status       # str

# v1 add response (AddResponse -> AddResult)
response.data.task_id        # str (was request_id)
response.data.message        # str
response.data.status         # "accumulated" | "extracted" (was free-form str)
response.data.message_count  # int (new)
```

### Search Patterns:
- `.result.` → `.data.` (in SDK response contexts)
- `.result.memories` or `.data.memories` → `.data.episodes`
- `.result.profiles` → `.data.profiles`
- `.result.pending_messages` → `.data.raw_messages`
- `.result.query_metadata` → `.data.query`
- `.request_id` (on add response) → `.data.task_id`

### Steps:
1. FIND: `.result.` REPLACE: `.data.` (in SDK response access chains)
2. FIND: `.memories` (on response data objects) REPLACE: `.episodes`
3. FIND: `.data.total_count` — keep as-is (unchanged)
4. Be careful not to replace `.result` or `.memories` in non-SDK contexts

### Object-Level Field Changes

The tables above cover **container-level** renames (`.result` → `.data`, `.memories` → `.episodes`).
Below are the **field-level** changes inside each object type. Code that accesses individual
attributes on Episode/Profile/Query/PendingMessage objects WILL break if these are not migrated.

#### Search Response: Profile Object — COMPLETE RESTRUCTURE

v0 `ResultProfile` is a **flat, per-trait item** (one object per explicit_info or implicit_trait).
v1 `Profile` is an **aggregate per user/group** with all traits collected into `profile_data`.

| v0 `ResultProfile` field | v1 `Profile` field | Notes |
|---|---|---|
| `item_type` ("explicit_info" / "implicit_trait") | **REMOVED** | v1 aggregates all items into `profile_data` dict |
| `category` | **REMOVED** | Nested inside `profile_data["explicit_info"]` |
| `description` | **REMOVED** | Nested inside `profile_data` values |
| `trait_name` | **REMOVED** | Nested inside `profile_data["implicit_traits"]` |
| `score` | `score` | Kept (search relevance score) |
| *(new)* | `id` | MongoDB ObjectId |
| *(new)* | `group_id` | Group scope |
| *(new)* | `memcell_count` | Number of underlying MemCells |
| *(new)* | `profile_data` | `Dict` with `explicit_info` + `implicit_traits` keys |
| *(new)* | `scenario` | `"solo"` or `"team"` |
| *(new)* | `user_id` | Owner user ID |

**Migration example:**

```python
# v0: iterate flat per-trait items
for p in response.result.profiles:
    print(f"[{p.item_type}] {p.description}")

# v1: iterate aggregate profile objects
for p in response.data.profiles:
    print(f"[{p.scenario}] {p.profile_data}")
```

#### Get Response: Profile Object — Field Removals

v0 `ResultMemoryProfileModel` → v1 `ProfileItem`. Core fields kept, metadata fields removed.

| v0 `ResultMemoryProfileModel` field | v1 `ProfileItem` field | Notes |
|---|---|---|
| `id` | `id` | Kept |
| `group_id` | `group_id` | Kept (now Optional) |
| `user_id` | `user_id` | Kept (now Optional) |
| `memcell_count` | `memcell_count` | Kept |
| `profile_data` | `profile_data` | Kept |
| `scenario` | `scenario` | Kept |
| `cluster_ids` | **REMOVED** | Internal clustering, not exposed |
| `confidence` | **REMOVED** | |
| `created_at` | **REMOVED** | |
| `last_updated_cluster` | **REMOVED** | |
| `updated_at` | **REMOVED** | |
| `version` | **REMOVED** | |

#### Episode Object — Field Removals & Additions

v0 `ResultMemoryEpisodicMemoryModel` (get) / `ResultMemoryEpisodeMemory` (search) → v1 `EpisodeItem` / `Episode`.

| v0 field | v1 field | Notes |
|---|---|---|
| `id` | `id` | Kept (now required) |
| `episode` | `episode` | Kept |
| `summary` | `summary` | Kept |
| `subject` | `subject` | Kept |
| `type` | `type` | Kept |
| `timestamp` | `timestamp` | Kept |
| `user_id` | `user_id` | Kept |
| `group_id` | `group_id` | Kept |
| `parent_id` | `parent_id` | Kept |
| `parent_type` | `parent_type` | Kept |
| `participants` | `participants` | Kept |
| `score` | `score` | Kept (search only) |
| `memory_type` | **REMOVED** | v1 uses separate lists instead of union type |
| `episode_id` | **REMOVED** | Get response only; use `id` |
| `extend` | **REMOVED** | |
| `group_name` | **REMOVED** | Use groups API |
| `keywords` | **REMOVED** | |
| `linked_entities` | **REMOVED** | |
| `ori_event_id_list` | **REMOVED** | |
| `original_data` | **REMOVED** | Available at response level via `include_original_data` param |
| `user_name` | **REMOVED** | Use senders API |
| `vector` / `vector_model` | **REMOVED** | Internal, not exposed |
| `start_time` / `end_time` / `location` | **REMOVED** | Get response only |
| `metadata` | **REMOVED** | |
| *(new)* | `session_id` | Session context |
| *(new)* | `sender_ids` | Get response only — list of sender IDs |
| *(new)* | `atomic_facts` | Search only — expanded `EpisodeAtomicFact` list |

#### v0 Union Type → v1 Separate Lists

v0 stored all memory types in a single `result.memories` union list (`ResultMemoryProfileModel | ResultMemoryEpisodicMemoryModel | ResultMemoryEventLogModel | ResultMemoryForesightModel`).

v1 separates them into distinct typed lists:
- `.data.episodes` — episodic memories (was `EpisodicMemoryModel` in v0)
- `.data.profiles` — user/group profiles (was `ProfileModel` in v0 get; separate `profiles` in v0 search)
- `.data.agent_cases` — agent task cases (**new in v1**)
- `.data.agent_skills` — agent reusable skills (**new in v1**)

**v0 types with NO v1 equivalent:**
- `ResultMemoryEventLogModel` (get) / `ResultMemoryEventLog` (search) → **subsumed** by `EpisodeAtomicFact` nested inside `Episode.atomic_facts` in search results
- `ResultMemoryForesightModel` (get) / `ResultMemoryForesight` (search) → **REMOVED**, no v1 equivalent

#### PendingMessage → RawMessageDto — Field Renames & Removals

v0 `ResultPendingMessage` → v1 `RawMessageDto`.

| v0 `ResultPendingMessage` field | v1 `RawMessageDto` field | Notes |
|---|---|---|
| `id` | `id` | Kept |
| `request_id` | `request_id` | Kept |
| `content` | `content_items` | **RENAMED** + type: `str` → `List[Dict]` (multimodal) |
| `sender` | `sender_id` | **RENAMED** |
| `created_at` | `created_at` | Kept |
| `group_id` | `group_id` | Kept |
| `message_id` | `message_id` | Kept |
| `sender_name` | `sender_name` | Kept |
| `updated_at` | `updated_at` | Kept |
| `group_name` | **REMOVED** | |
| `message_create_time` | **REMOVED** | |
| `refer_list` | **REMOVED** | |
| `user_id` | **REMOVED** | |
| *(new)* | `session_id` | Session identifier |
| *(new)* | `timestamp` | Event timestamp |

#### QueryMetadata → Query — Restructured (10+ fields → 3)

v0 `ResultQueryMetadata` → v1 `Query`. Most fields collapsed into `filters_applied`.

| v0 `ResultQueryMetadata` field | v1 `Query` field | Notes |
|---|---|---|
| `retrieve_method` | `method` | **RENAMED** |
| `query` | `text` | **RENAMED** |
| `current_time` | **REMOVED** | |
| `end_time` | **REMOVED** | |
| `group_ids` | **REMOVED** | Moved into `filters_applied` dict |
| `memory_types` | **REMOVED** | Moved into `filters_applied` dict |
| `radius` | **REMOVED** | Moved into `filters_applied` dict |
| `start_time` | **REMOVED** | |
| `top_k` | **REMOVED** | Moved into `filters_applied` dict |
| `user_id` | **REMOVED** | Moved into `filters_applied` dict |
| *(new)* | `filters_applied` | Dict containing all applied filters |

**Migration example:**

```python
# v0
qm = response.result.query_metadata
print(f"method={qm.retrieve_method}, query={qm.query}, top_k={qm.top_k}")

# v1
q = response.data.query
print(f"method={q.method}, query={q.text}, filters={q.filters_applied}")
```

---

## Quick Reference: Search-and-Replace Checklist

For simple renames, these can be applied project-wide:

| Find | Replace | Scope |
|------|---------|-------|
| `evermemos` | `everos` | All files |
| `EverMemOS` | `EverOS` | *.py |
| `AsyncEverMemOS` | `AsyncEverOS` | *.py |
| `EverMemOSError` | `EverOSError` | *.py |
| `EVERMEMOS_API_KEY` | `EVEROS_API_KEY` | All files |
| `EVER_MEM_OS_BASE_URL` | `EVER_OS_BASE_URL` | All files |
| `.v0.` | `.v1.` | *.py (in API call chains) |
| `.types.v0` | `.types.v1` | *.py |
| `.resources.v0` | `.resources.v1` | *.py |
| `MemoryAddResponse` | `AddResponse` | *.py |
| `MemoryGetResponse` | `GetMemoriesResponse` | *.py |
| `MemorySearchResponse` | `SearchMemoriesResponse` | *.py |
| `MemoryDeleteResponse` | `None` | *.py (type hints only) |
| `.result.` | `.data.` | *.py (response access) |
| `.data.memories` | `.data.episodes` | *.py (response field rename) |
| `group_ids` | `group_id` | *.py (in filters/extra_query dicts — **plural→singular**) |

### Object-level field renames (in response access code):

| Find | Replace | Context |
|------|---------|---------|
| `p.item_type` | `p.scenario` | Search response Profile — **complete restructure**, see RULE-013 |
| `p.description` | `p.profile_data` | Search response Profile — type also changes: `str` → `Dict` |
| `p.category` | *(remove)* | Search response Profile — nested in `profile_data` |
| `p.trait_name` | *(remove)* | Search response Profile — nested in `profile_data` |
| `.query_metadata` | `.query` | Search response — `ResultQueryMetadata` → `Query` |
| `qm.retrieve_method` | `q.method` | Query object field rename |
| `qm.query` | `q.text` | Query object field rename |
| `qm.top_k` | `q.filters_applied` | Query object — moved into filters dict |
| `.pending_messages` | `.raw_messages` | Search response container rename |
| `pm.content` | `pm.content_items` | RawMessage — type: `str` → `List[Dict]` |
| `pm.sender` | `pm.sender_id` | RawMessage field rename |
| `pm.refer_list` | *(remove)* | RawMessage — no v1 equivalent |
| `pm.message_create_time` | *(remove)* | RawMessage — no v1 equivalent |
| `mem.memory_type` | *(remove)* | Episode — v1 uses separate lists, no union discriminator |
| `mem.episode_id` | `ep.id` | Episode — use `id` in v1 |

### Additional naming changes (in context-specific code):

| v0 | v1 | Context |
|----|-----|--------|
| `sender` (param) | `sender_id` (in message dict) | memories.add param → message-level field |
| `sender_name` (param) | `name` (in senders.create) | memories.add → senders.create |
| `group_name` (param) | `name` (in groups.create) | memories.add → groups.create |
| `default_timezone` | `timezone` | conversation_meta → settings |
| `create_time` (ISO str) | `timestamp` (int ms) | memories.add param → message-level field |
| `request_id` (response) | `data.task_id` (response) | add response field |
| `flush` (bool param) | `flush()` (separate method) | memories.add → memories.flush() |
| `.result.pending_messages` | `.data.raw_messages` | search response |
| `.result.query_metadata` | `.data.query` | search response |
| `retrieve_method` (query) | `method` (named param) | search extra_query → search param |
| `response.success` / `.found` | `response.data.status` | status.request → tasks.retrieve |

**These are NOT simple renames** (require manual restructuring):
- `memories.add()` parameters -> see RULE-007
- `memories.get()` parameters -> see RULE-009
- `memories.search()` parameters -> see RULE-010
- `conversation_meta.*` calls -> REMOVED, see RULE-011
- `status.request.*` calls -> REMOVED, see RULE-011
