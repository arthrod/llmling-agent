"""Tests for ACPAgentAPI request defaults."""

from __future__ import annotations

from typing import TYPE_CHECKING

from acp.agent.acp_agent_api import ACPAgentAPI
from acp.schema import LoadSessionResponse, NewSessionResponse


if TYPE_CHECKING:
    from acp.schema import LoadSessionRequest, NewSessionRequest


class _StubConnection:
    def __init__(self) -> None:
        self.new_session_request: NewSessionRequest | None = None
        self.load_session_request: LoadSessionRequest | None = None

    async def new_session(self, params: NewSessionRequest) -> NewSessionResponse:
        self.new_session_request = params
        return NewSessionResponse(session_id="sess-1")

    async def load_session(self, params: LoadSessionRequest) -> LoadSessionResponse:
        self.load_session_request = params
        return LoadSessionResponse()


async def test_new_session_defaults_to_empty_mcp_servers() -> None:
    connection = _StubConnection()
    api = ACPAgentAPI(connection)

    await api.new_session("/tmp")

    assert connection.new_session_request is not None
    assert connection.new_session_request.mcp_servers == []


async def test_load_session_defaults_to_empty_mcp_servers() -> None:
    connection = _StubConnection()
    api = ACPAgentAPI(connection)

    await api.load_session("sess-1", "/tmp")

    assert connection.load_session_request is not None
    assert connection.load_session_request.mcp_servers == []
