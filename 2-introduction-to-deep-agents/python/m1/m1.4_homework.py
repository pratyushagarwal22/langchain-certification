# python/m1/m1.4_homework.py
"""M1.4 Homework: Scope the Agent to One Domain.

THE IDEA
Lab 1 had you swap personas (pirate, cowboy, Shakespeare) on top of the
butler system prompt, which only changes the agent's voice. This homework
uses `system_prompt` differently: instead of persona, write a constraint
that scopes the agent to a single domain of your choosing (cooking,
houseplants, retro video games, personal finance, etc.) and
instructs it to refuse or redirect anything outside that domain.

There's no single correct domain here, that's the point. What matters is
that the refusal actually holds, not just that the agent sounds like
something.

WHAT YOU FILL IN
  TODO 1: write your own SYSTEM_PROMPT string that scopes the agent to a
    single domain of your choosing and tells it to refuse or redirect
    anything outside that domain (no persona/voice requirement here,
    just the scope + refusal instruction).
  TODO 2: invoke the agent with two test prompts, one inside your domain
    and one clearly outside it, and print both responses so you can see
    whether the refusal actually held.

RUN
  cd python
  uv run ./m1/m1.4_homework.py
"""

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

from deepagents import create_deep_agent
from models import model


# ════════════════════════════════════════════════════════════════════════
# TODO 1: Write a system prompt that scopes the agent to one domain and
# tells it to refuse or redirect anything outside that domain.
#
# Requirements:
#   - Pick one domain (a subject, not a persona).
#   - State clearly what the agent should do when asked about something
#     outside that domain (e.g. say it can't help, redirect back to the
#     domain, ask a domain-relevant follow-up).
#
# Example shape (delete this and write your own):
#   SYSTEM_PROMPT = (
#       "You only answer questions about ... . If asked about anything "
#       "else, ... ."
#   )
# ════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = (
  # Domain Specific System Prompt
  "You only answer questions about elephants. If asked about anything else, you will refuse to answer and redirect the user to the elephant domain. Ending with a joke about elephants, and a question about the user's favourite animal."
)


agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    name="Homework_Agent",
)


# ════════════════════════════════════════════════════════════════════════
# TODO 2: Run one in-domain prompt and one out-of-domain prompt through
# the agent and print both responses, so you can check whether the
# refusal actually held.
# ════════════════════════════════════════════════════════════════════════

def run_test_prompts():
    """TODO 2: invoke `agent` with one in-domain prompt and one
    out-of-domain prompt, and print each response."""
    
    result = agent.invoke({"messages": [{"role" : "user", "content" : "Which elephant is the largest in the world?"}]})

    print(result["messages"][-1].content)

    result = agent.invoke({"messages": [{"role": "user", "content": "What is the capital of France?"}]})

    print(result["messages"][-1].content)


run_test_prompts()
