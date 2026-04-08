"""
EverOS SDK v1 (everos) — canonical usage reference (15 scenarios).
"""

import os
from datetime import datetime, timezone

from everos import EverOS, EverOSError
from everos.types.v1 import (
    AddResponse,
    GetMemoriesResponse,
    SearchMemoriesResponse,
    SettingsAPIResponse,
)
# RULE-003/011: ConversationMeta types REMOVED, MemoryDeleteResponse → None

USER_ID = "user-alice"
GROUP_ID = "grp-workspace"


# RULE-001/002/004
def create_client() -> EverOS:
    return EverOS(
        api_key=os.environ.get("EVEROS_API_KEY"),
        base_url=os.environ.get("EVER_OS_BASE_URL", "https://api.evermind.ai"),
    )


# RULE-011: conversation_meta.create → settings.update + senders.create
def setup_settings(client: EverOS) -> SettingsAPIResponse:
    """Fields: llm_custom_setting kept, default_timezone→timezone, scene/desc/tags dropped.
    WARNING: v0 was per-group; v1 settings is global singleton."""
    response = client.v1.settings.update(
        llm_custom_setting={
            "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
            "extraction": {"model": "qwen/qwen3-235b-a22b-2507", "provider": "openrouter"},
        },
        timezone="Asia/Shanghai",
    )
    client.v1.senders.create(sender_id=USER_ID, name="Alice")
    # RULE-011: group_name → groups.create (create resources before use)
    client.v1.groups.create(group_id=GROUP_ID, name="Dev Team Chat")
    return response


# RULE-011: conversation_meta.get → settings.retrieve
def get_settings(client: EverOS) -> SettingsAPIResponse:
    response = client.v1.settings.retrieve()
    if response.data:
        print(f"timezone={response.data.timezone}, extraction_mode={response.data.extraction_mode}")
    return response


# RULE-011: conversation_meta.update → settings.update
def update_settings(client: EverOS) -> SettingsAPIResponse:
    return client.v1.settings.update(
        llm_custom_setting={
            "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
            "extraction": {"model": "qwen/qwen3-235b-a22b-2507", "provider": "openrouter"},
        },
        timezone="UTC",
    )


# RULE-007: add rewrite
# NOTE: async_mode=True is needed if v0 code used response.request_id for status polling.
# Without it, response.data.task_id will be None.
def add_memory(client: EverOS) -> AddResponse:
    now = datetime.now(timezone.utc)
    timestamp_ms = int(now.timestamp() * 1000)
    response = client.v1.memories.add(
        messages=[{
            "content": "I prefer dark mode and vim keybindings",
            "role": "user",
            "timestamp": timestamp_ms,
            "sender_id": USER_ID,
        }],
        user_id=USER_ID,
        async_mode=True,  # required to get task_id (was always present as request_id in v0)
    )
    # RULE-007: flush=True → separate flush()
    client.v1.memories.flush(user_id=USER_ID)
    return response


# RULE-007: single-user mode, refer_list dropped
def add_single_user(client: EverOS) -> AddResponse:
    now = datetime.now(timezone.utc)
    timestamp_ms = int(now.timestamp() * 1000)
    return client.v1.memories.add(
        messages=[{
            "content": "I also like Rust",
            "role": "user",
            "timestamp": timestamp_ms,
            "sender_id": USER_ID,
        }],
        user_id=USER_ID,
        # RULE-007: refer_list, message_id → no v1 equivalent
    )


# RULE-010: search with query + group_id (group_ids→group_id)
def search_with_query(client: EverOS) -> SearchMemoriesResponse:
    response = client.v1.memories.search(
        filters={"user_id": USER_ID, "group_id": GROUP_ID},
        query="dark mode",
    )
    if response.data and response.data.episodes:
        print(f"found {len(response.data.episodes)} episodes")
        for ep in response.data.episodes:
            print(f"  - {getattr(ep, 'summary', None) or getattr(ep, 'episode', 'N/A')}")
    if response.data and response.data.profiles:
        for p in response.data.profiles:
            print(f"  - scenario={p.scenario}, data={p.profile_data}")
    if response.data and response.data.query:
        q = response.data.query
        print(f"  method={q.method}, query={q.text}")
    return response


# RULE-010 edge: NEVER query=""
def search_without_query(client: EverOS) -> SearchMemoriesResponse:
    return client.v1.memories.search(
        filters={"user_id": USER_ID},
        query="TODO: specify search query",
    )


# RULE-009: get with group_id (group_ids→group_id)
def get_episodic(client: EverOS) -> GetMemoriesResponse:
    response = client.v1.memories.get(
        filters={"user_id": USER_ID, "group_id": GROUP_ID},
        memory_type="episodic_memory",
    )
    if response.data and response.data.episodes:
        print(f"total={response.data.total_count}")
        for ep in response.data.episodes:
            print(f"  - {getattr(ep, 'summary', None) or getattr(ep, 'episode', 'N/A')}")
    return response


# RULE-009: get profile
def get_profile(client: EverOS) -> GetMemoriesResponse:
    response = client.v1.memories.get(
        filters={"user_id": USER_ID},
        memory_type="profile",
    )
    if response.data and response.data.profiles:
        print(f"total={response.data.total_count}")
        for p in response.data.profiles:
            print(f"  - scenario={p.scenario}, data={p.profile_data}")
    return response


# RULE-008 mode 1: memory_id ALONE
def delete_by_id(client: EverOS, memory_id: str) -> None:
    client.v1.memories.delete(memory_id=memory_id)


# RULE-008 mode 2: filter (batch)
def delete_by_filter(client: EverOS) -> None:
    client.v1.memories.delete(user_id=USER_ID, group_id=GROUP_ID)


# RULE-008: legacy id= → memory_id=
def delete_legacy_alias(client: EverOS) -> None:
    client.v1.memories.delete(memory_id="nonexistent-id")


# RULE-011: status.request.get → tasks.retrieve
def check_task_status(client: EverOS, task_id: str):
    response = client.v1.tasks.retrieve(task_id=task_id)
    print(f"status={response.data.status}")
    return response


# RULE-005: EverMemOSError → EverOSError
def handle_errors(client: EverOS):
    try:
        client.v1.memories.search(filters={"bad_param": "xxx"}, query="test")
    except EverOSError as e:
        print(f"caught: {type(e).__name__}")
