# refactoring_agent.py

from fast_edit_mode.agent import Agent
import logging

logger = logging.getLogger(__name__)

class RefactoringAgent(Agent):
    def handle_task(self, context):
        code = context['code']
        logger.info(f"{self.name} is refactoring code.")
        try:
            refactored_code = self.orchestrator.ai_interface.refactor_code(code)
            task_info = {
                'agent': self.name,
                'action': 'refactoring',
                'updated_code': refactored_code,
            }
            self.update_context(context, task_info)
            return self.decide_handoff(context)
        except Exception as e:
            logger.error(f"{self.name} failed to refactor code: {e}")
            context['status'] = 'error'
            return None

    def decide_handoff(self, context):
        # Decide whether to hand off to DocumentationAgent
        return 'DocumentationAgent'
