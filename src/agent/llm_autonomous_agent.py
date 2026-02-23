import json

from src.agent.llm_decision import decide_next_tool

from src.agent.tools import (
    tool_generate_tests,
    tool_execute_tests,
    tool_analyze_failure,
    tool_search_memory,
    tool_save_memory
)


TOOLS = {

    "generate_tests": tool_generate_tests,
    "execute_tests": tool_execute_tests,
    "analyze_failure": tool_analyze_failure,
    "search_memory": tool_search_memory,
    "save_memory": tool_save_memory

}


class LLMAutonomousAgent:

    def run(self, goal):

        print("\n[Agent] Goal:", goal)

        context = ""

        state = {}

        for step in range(10):

            # Call LLM ONLY ONCE
            tool_name = decide_next_tool(goal, context)

            print(f"\n[Agent] LLM selected tool: {tool_name}")

            if tool_name == "done":
                print("\n[Agent] Goal complete.")

                break

            if tool_name not in TOOLS:
                print("[Agent] Unknown tool. Stopping.")

                break

            try:

                if tool_name == "generate_tests":

                    result = TOOLS[tool_name](goal)

                    try:
                        state["test_cases"] = json.loads(result)
                    except:
                        state["test_cases"] = result


                elif tool_name == "execute_tests":

                    result = TOOLS[tool_name]()

                    state["execution"] = result
                    state["error"] = result.get("error")


                elif tool_name == "search_memory":

                    result = TOOLS[tool_name](state.get("error"))

                    state["memory"] = result


                elif tool_name == "analyze_failure":

                    result = TOOLS[tool_name](state.get("error"))

                    state["analysis"] = result


                elif tool_name == "save_memory":

                    TOOLS[tool_name](
                        goal,
                        state.get("error"),
                        state.get("analysis")
                    )

                    state["memory_saved"] = True


            except Exception as e:

                print(f"[Agent] Tool failed: {e}")

                break

            # Update context for LLM
            context = json.dumps(state, indent=2)

        return state


if __name__ == "__main__":

    agent = LLMAutonomousAgent()

    result = agent.run("User login with email and password")

    print("\nFINAL STATE:\n")

    print(json.dumps(result, indent=2))