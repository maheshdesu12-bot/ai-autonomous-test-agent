from src.execution.parallel_executor import run_parallel_tests
from src.reporting.test_reporter import save_test_report


class OrchestratorAgent:

    def run(self):

        print("[Orchestrator] Running parallel tests")

        results = run_parallel_tests()

        for agent, result in results.items():

            save_test_report(agent, result)

        return results


if __name__ == "__main__":

    agent = OrchestratorAgent()

    results = agent.run()

    print(results)