from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver

from models import model

m3_dir = Path(__file__).parent
backend = FilesystemBackend(root_dir=str(m3_dir), virtual_mode=True)
THREAD = {"configurable": {"thread_id": "scratch_agent_skills"}}

agent = create_deep_agent(
    model=model,
    name="Sales_Assistant",
    backend=backend,
    checkpointer=MemorySaver(),
    skills=["/skills"],
    system_prompt="You are a sales assistant.",
)

print("================================================")
print("Qualifying a lead\n")
result = agent.invoke({"messages": [{"role": "user", "content": "Qualify this lead: Acme Corp, 200-person logistics company. I spoke with Sarah Chen, VP of Sales: she's the decision maker. They have $45k budgeted for CRM this year. Main pain: deals are slipping through the cracks due to poor pipeline visibility. They want a solution live by end of Q3."}]}, config=THREAD)
print(result["messages"][-1].content)


print("================================================")
print("Drafting a pitch\n")
result = agent.invoke({"messages": [{"role": "user", "content": "Draft a pitch for the Acme Corp lead that we qualified earlier."}]}, config=THREAD)
print(result["messages"][-1].content)