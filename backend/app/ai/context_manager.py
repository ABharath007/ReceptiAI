from contextvars import ContextVar

from app.ai.context import AgentContext


_context: ContextVar[AgentContext | None] = ContextVar(
    "agent_context",
    default=None
)


def set_context(context: AgentContext):
    return _context.set(context)


def get_context() -> AgentContext:
    context = _context.get()

    if context is None:
        raise RuntimeError("Agent context has not been initialized.")

    return context


def reset_context(token) -> None:
    _context.reset(token)