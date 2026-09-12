# python/m3/m3.2_homework.py
"""M3.2 Homework: Bundle a Reference File Into Your Skill.

THE IDEA
The lab's two skills (qualify-lead and draft-pitch) are each a single flat
SKILL.md file with everything inline. But the lesson also covered a third
stage of progressive disclosure: a skill can point to supporting files (a
reference doc, a template, a script) that live alongside SKILL.md and that
the agent only reads when it actually needs them, instead of stuffing
everything into the system prompt up front. This homework asks you to write
a skill for a topic or workflow YOU pick (not sales) that bundles a SECOND
file with details the agent needs but that aren't in SKILL.md itself, then
confirm from the trace that the agent actually called `read_file` on that
second file before answering, rather than guessing.

WHAT YOU FILL IN
  TODO 1: write your own SKILL.md content. It must instruct the agent to
    read a `reference.md` file (in the same skill directory) for specific
    details it needs, and must NOT restate those details inline. The `name`
    field in your frontmatter must exactly match SKILL_NAME below.
  TODO 2: write reference.md's content: the specific facts, numbers, or
    template your skill's instructions point to and depend on.
  TODO 3: write a system prompt and a user question that should activate
    your skill.

RUN
  cd python
  uv run ./m3/m3.2_homework.py
"""

import tempfile
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend

from models import model

# This name becomes the skill's directory name. It must exactly match the
# `name:` field you write in the frontmatter inside build_skill_md() below.
SKILL_NAME = "workout-planner"
REFERENCE_PATH = f"/skills/{SKILL_NAME}/reference.md"


# ════════════════════════════════════════════════════════════════════════
# TODO 1: Write your own SKILL.md content.
#
# Requirements:
#   - YAML frontmatter with `name` (must equal SKILL_NAME above) and
#     `description` (a specific sentence describing WHEN to use this skill).
#   - Steps that tell the agent to open `reference.md` (in this same skill
#     directory) for the specific details it needs to do the task well.
#   - Do NOT put those details in SKILL.md itself; if the agent could do
#     the task correctly without ever reading reference.md, this doesn't
#     exercise progressive disclosure.
#
# Example shape (delete this and write your own):
#   return """---
#   name: your-skill-name
#   description: Use when the user wants to ...
#   ---
#
#   # Your Skill Title
#
#   **Step 1: ...**: ...
#   **Step 2: ...**: before proceeding, read reference.md in this skill's
#     directory for the exact ... to use. Do not guess these.
#   """
# ════════════════════════════════════════════════════════════════════════

def build_skill_md() -> str:
    return """---
name: workout-planner
description: Use when the user wants a structured workout plan for a specific day or goal.
---

    # Workout Planner

    Build a single-session workout plan tailored to the user's goal and available time.

    **Step 1: Goal**: Ask what the user is training for today (strength, hypertrophy,
    endurance, or mobility) if it isn't already clear from their message.

    **Step 2: Constraints**: Confirm how much time they have and what equipment is
    available (bodyweight only, dumbbells, a full gym).

    **Step 3: Look up the numbers**: Before writing sets and reps, read `reference.md`
    in this skill's directory for the exact sets/reps/rest table for the stated
    goal. Do not guess these numbers; they vary by goal and this skill's rubric is
    specific about them.

    **Step 4: Warm-up**: Always include a 5-minute warm-up appropriate to the goal.

    **Step 5: Main block**: Write 4-6 exercises using the sets/reps/rest from
    reference.md that fit the stated goal, time, and equipment.

    **Step 6: Cool-down**: End with 2-3 minutes of stretching relevant to the muscles
    worked.

    ## Output

    Present the plan as a numbered list: warm-up, main block (with sets/reps/rest
    per reference.md), then cool-down. Keep the whole plan realistic for the time
    the user gave you.
    
    """


# ════════════════════════════════════════════════════════════════════════
# TODO 2: Write reference.md's content.
#
# This should contain the specific facts your SKILL.md pointed to and
# depends on: a rubric, a set of numbers, a template, a checklist. Specific
# enough that an answer produced without reading it would visibly differ
# from one produced with it.
# ════════════════════════════════════════════════════════════════════════

def build_reference_md() -> str:
    return """# Sets / Reps / Rest Rubric

    Use the row matching the user's stated goal. Do not deviate from these
    numbers; they're calibrated for a single 20-30 minute session.

    | Goal        | Sets | Reps      | Rest between sets |
    |-------------|------|-----------|--------------------|
    | Strength    | 4-5  | 4-6       | 90-120 seconds     |
    | Hypertrophy | 3-4  | 8-12      | 60-90 seconds      |
    | Endurance   | 2-3  | 15-20     | 30-45 seconds      |
    | Mobility    | 2-3  | 30-60s hold (not reps) | 15-30 seconds |
    """


# Write the skill to a scratch directory so it's discoverable through a
# FilesystemBackend, the same mechanism the lab uses for python/m3/skills/.
_tmp_root = Path(tempfile.mkdtemp(prefix="m3_2_homework_"))
_skill_dir = _tmp_root / "skills" / SKILL_NAME
_skill_dir.mkdir(parents=True, exist_ok=True)
(_skill_dir / "SKILL.md").write_text(build_skill_md())
(_skill_dir / "reference.md").write_text(build_reference_md())

backend = FilesystemBackend(root_dir=str(_tmp_root), virtual_mode=True)
print(f"Skill files written to: {_skill_dir}")


# ════════════════════════════════════════════════════════════════════════
# TODO 3: Write a system prompt and a triggering question.
#
# SYSTEM_PROMPT: give the agent a persona of your choosing (a name, a
# voice, anything you want).
# USER_QUESTION: a question that should match your skill's `description`
# closely enough that the agent activates it.
# ════════════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are Coach Goggins, an ex navy seal, you can be very mean and harsh, but want the best for your clients. 
Keep your tone encouraging and practical. But be mean and harsh when necessary."""
USER_QUESTION = "I have 45 minutes and just a pair of dumbbells. Give me a workout focused on strength."

agent = create_deep_agent(
    model=model,
    name="Homework_Agent",
    backend=backend,
    skills=["/skills"],
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke({"messages": [{"role": "user", "content": USER_QUESTION}]})
print(result["messages"][-1].content)

read_calls = [
    call
    for msg in result["messages"]
    for call in getattr(msg, "tool_calls", [])
    if call["name"] == "read_file"
]
reference_was_read = any(call["args"].get("file_path") == REFERENCE_PATH for call in read_calls)
print(f"\n--- Did the agent read {REFERENCE_PATH}? {reference_was_read} ---")
if not reference_was_read:
    print(
        "It didn't. Either SKILL.md isn't clearly telling it to, or the "
        "task is answerable without the details in reference.md."
    )
