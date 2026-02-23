import json

from src.llm.test_generator import generate_test_cases
from src.execution.playwright_executor import execute_login_test
from src.llm.analyzer import BugAnalyzer
from src.agent.vector_memory import save_vector_memory, search_similar_errors

bug_analyzer = BugAnalyzer()


def tool_generate_tests(requirement):

    print("[Tool] Generating test cases")

    return generate_test_cases(requirement)


def tool_execute_tests():

    print("[Tool] Executing test")

    return execute_login_test()


def tool_analyze_failure(error):

    print("[Tool] Analyzing failure")

    return bug_analyzer.analyze(error)


def tool_search_memory(error):

    print("[Tool] Searching memory")

    return search_similar_errors(error)


def tool_save_memory(requirement, error, analysis):

    print("[Tool] Saving memory")

    save_vector_memory(requirement, error, analysis)