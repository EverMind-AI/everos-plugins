"""
EverOS SDK v0 (evermemos) — canonical usage reference (15 scenarios).
"""

import os
from datetime import datetime, timezone

from evermemos import EverMemOS, EverMemOSError
from evermemos.types.v0 import (
    MemoryAddResponse,
    MemoryDeleteResponse,
    MemoryGetResponse,
    MemorySearchResponse,
)
from evermemos.types.v0.memories import (
    ConversationMetaCreateResponse,
    ConversationMetaGetResponse,
    ConversationMetaUpdateResponse,
)

USER_ID = "user-alice"
GROUP_ID = "grp-workspace"


# RULE-001/002/004
def create_client() -> EverMemOS:
    return EverMemOS(
        api_key=os.environ.get("EVERMEMOS_API_KEY"),
        base_url=os.environ.get("EVER_MEM_OS_BASE_URL", "https://api.evermind.ai"),
    )


# RULE-011: conversation_meta.create (all params)
def setup_conversation_meta(client: EverMemOS) -> ConversationMetaCreateResponse:
    return client.v0.memories.conversation_meta.create(
        created_at=datetime.now(timezone.utc).isoformat(),
        scene="group_chat",
        default_timezone="Asia/Shanghai",
        llm_custom_setting={
            "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
            "extraction": {"model": "qwen/qwen3-235b-a22b-2507", "provider": "openrouter"},
        },
        description="Dev team technical discussion",
        scene_desc={"description": "Technical discussion group", "type": "work"},
        tags=["work", "technical"],
        user_details={
            USER_ID: {"full_name": "Alice", "role": "user", "custom_role": "developer"},
        },
    )


# RULE-011: conversation_meta.get
def get_conversation_meta(client: EverMemOS) -> ConversationMetaGetResponse:
    response = client.v0.memories.conversation_meta.get()
    if response.result:
        print(f"scene={response.result.scene}, timezone={response.result.default_timezone}")
    return response


# RULE-011: conversation_meta.update
def update_conversation_meta(client: EverMemOS) -> ConversationMetaUpdateResponse:
    return client.v0.memories.conversation_meta.update(
        llm_custom_setting={
            "boundary": {"model": "gpt-4.1-mini", "provider": "openai"},
            "extraction": {"model": "qwen/qwen3-235b-a22b-2507", "provider": "openrouter"},
        },
        default_timezone="UTC",
    )


# RULE-007: add with group + all params
def add_memory(client: EverMemOS) -> MemoryAddResponse:
    return client.v0.memories.add(
        content="I prefer dark mode and vim keybindings",
        create_time=datetime.now(timezone.utc).isoformat(),
        message_id="msg-001",
        sender=USER_ID,
        role="user",
        flush=True,
        group_id=GROUP_ID,
        group_name="Dev Team Chat",
        sender_name="Alice",
    )


# RULE-007: add single-user mode (no group_id) + refer_list
def add_single_user(client: EverMemOS) -> MemoryAddResponse:
    return client.v0.memories.add(
        content="I also like Rust",
        create_time=datetime.now(timezone.utc).isoformat(),
        message_id="msg-002",
        sender=USER_ID,
        role="user",
        refer_list=["msg-001"],
    )


# RULE-010: search with query + group_ids (plural)
def search_with_query(client: EverMemOS) -> MemorySearchResponse:
    response = client.v0.memories.search(
        extra_query={"user_id": USER_ID, "group_ids": GROUP_ID, "query": "dark mode"},
    )
    if response.result and response.result.memories:
        print(f"found {len(response.result.memories)} memories")
        for mem in response.result.memories:
            print(f"  - {getattr(mem, 'summary', None) or getattr(mem, 'episode', 'N/A')}")
    if response.result and response.result.profiles:
        # v0 search ResultProfile: flat per-trait items (item_type + description)
        # NOTE: v1 Profile is completely different (scenario + profile_data) — see RULE-013
        for p in response.result.profiles:
            print(f"  - [{p.item_type}] {p.description}")
    if response.result and response.result.query_metadata:
        qm = response.result.query_metadata
        print(f"  method={qm.retrieve_method}, query={qm.query}")
    return response


# RULE-010 edge: search without query
def search_without_query(client: EverMemOS) -> MemorySearchResponse:
    return client.v0.memories.search(extra_query={"user_id": USER_ID})


# RULE-009: get with group_ids (plural)
def get_episodic(client: EverMemOS) -> MemoryGetResponse:
    response = client.v0.memories.get(
        extra_query={"user_id": USER_ID, "group_ids": GROUP_ID, "memory_type": "episodic_memory"},
    )
    if response.result and response.result.memories:
        print(f"total={response.result.total_count}")
        for mem in response.result.memories:
            print(f"  - {getattr(mem, 'summary', None) or getattr(mem, 'episode', 'N/A')}")
    return response


# RULE-009: get profile
def get_profile(client: EverMemOS) -> MemoryGetResponse:
    response = client.v0.memories.get(extra_query={"user_id": USER_ID, "memory_type": "profile"})
    if response.result and response.result.memories:
        # v0 get ResultMemoryProfileModel: aggregate per user (scenario + profile_data)
        # NOTE: same field names in v1 ProfileItem — no rename needed for get response
        for mem in response.result.memories:
            print(f"  - scenario={mem.scenario}, data={mem.profile_data}")
    return response


# RULE-008 mode 1: delete by memory_id + user_id
def delete_by_id(client: EverMemOS, memory_id: str) -> MemoryDeleteResponse:
    return client.v0.memories.delete(memory_id=memory_id, user_id=USER_ID)


# RULE-008 mode 2: delete by filter (batch)
def delete_by_filter(client: EverMemOS) -> MemoryDeleteResponse:
    return client.v0.memories.delete(user_id=USER_ID, group_id=GROUP_ID)


# RULE-008: delete with legacy id= alias
def delete_legacy_alias(client: EverMemOS) -> MemoryDeleteResponse:
    return client.v0.memories.delete(id="nonexistent-id")


# RULE-011: status.request
def check_status(client: EverMemOS, request_id: str):
    response = client.v0.status.request.get(request_id=request_id)
    print(f"success={response.success}, found={response.found}")
    return response


# RULE-005: exception handling
def handle_errors(client: EverMemOS):
    try:
        client.v0.memories.search(extra_query={"bad_param": "xxx"})
    except EverMemOSError as e:
        print(f"caught: {type(e).__name__}")
