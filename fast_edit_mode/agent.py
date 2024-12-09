# agent.py

class Agent:
    def __init__(self, name, orchestrator):
        self.name = name
        self.orchestrator = orchestrator

    def handle_task(self, context):
        raise NotImplementedError("Subclasses must implement handle_task method")

    def update_context(self, context, task_info):
        context['edit_history'].append(task_info)
        context['code'] = task_info['updated_code']
