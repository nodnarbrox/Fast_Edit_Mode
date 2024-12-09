# documentation_agent.py

from fast_edit_mode.agent import Agent
import logging

logger = logging.getLogger(__name__)

class DocumentationAgent(Agent):
    def handle_task(self, context):
        code = context['code']
        logger.info(f"{self.name} is adding documentation.")
        try:
            documented_code = self.orchestrator.ai_interface.add_documentation(code)
            task_info = {
                'agent': self.name,
                'action': 'documentation',
                'updated_code': documented_code,
            }
            self.update_context(context, task_info)
            return self.decide_handoff(context)
        except Exception as e:
            logger.error(f"{self.name} failed to add documentation: {e}")
            context['status'] = 'error'
            return None

    def decide_handoff(self, context):
        # This is the last agent in the chain
        return None
