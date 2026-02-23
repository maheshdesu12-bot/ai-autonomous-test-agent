import json

from src.agent.tools import (
    tool_generate_tests,
    tool_execute_tests,
    tool_analyze_failure,
    tool_search_memory,
    tool_save_memory
)


class AutonomousAgent:

    def run(self, goal):

        print("\n[Agent] Goal:", goal)

        # =========================
        # Step 1: Generate tests
        # =========================
        print("[Tool] Generating test cases")

        test_cases_raw = tool_generate_tests(goal)

        try:
            test_cases = json.loads(test_cases_raw)
        except Exception:
            test_cases = test_cases_raw


        # =========================
        # Step 2: Execute tests
        # =========================
        print("[Tool] Executing test")

        execution = tool_execute_tests()

        error = execution.get("error")

        # =========================
        # Step 3: Decision branch
        # =========================

        if error and error != "no error":

            print("[Agent] Error detected")

            # Search memory
            print("[Tool] Searching memory")

            similar = tool_search_memory(error)

            if similar:
                print("[Agent] Found similar failure in memory")
            else:
                print("[Agent] No similar failure found")


            # Analyze failure
            print("[Tool] Analyzing failure")

            analysis = tool_analyze_failure(error)


            # Save memory
            print("[Tool] Saving memory")

            tool_save_memory(goal, error, analysis)

            memory_saved = True

        else:

            print("[Agent] Test passed successfully")

            similar = []
            analysis = None
            memory_saved = False


        # =========================
        # Final result
        # =========================

        final_result = {

            "goal": goal,
            "test_cases": test_cases,
            "execution": execution,
            "error": error,
            "analysis": analysis,
            "memory_saved": memory_saved
        }


        return final_result


# =========================
# Run agent
# =========================

if __name__ == "__main__":

    agent = AutonomousAgent()

    result = agent.run("User login with email and password")

    print("\nFINAL RESULT:\n")

    print(json.dumps(result, indent=2))