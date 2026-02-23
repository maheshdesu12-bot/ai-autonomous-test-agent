class PlannerAgent:

    def create_plan(self):

        print("[Planner] Creating execution plan")

        return [
            {
                "name": "register",
                "agent": "register_agent",
                "depends_on": None
            },
            {
                "name": "login",
                "agent": "login_agent",
                "depends_on": "register"
            }
        ]