# optimization_agent.py

from fast_edit_mode.agent import Agent
import logging

logger = logging.getLogger(__name__)

class OptimizationAgent(Agent):
    def handle_task(self, context):
        code = context['code']
        logger.info(f"{self.name} is optimizing code.")
        try:
            optimized_code = self.orchestrator.ai_interface.optimize_code(code)
            task_info = {
                'agent': self.name,
                'action': 'optimization',
                'updated_code': optimized_code,
            }
            self.update_context(context, task_info)
            return self.decide_handoff(context)
        except Exception as e:
            logger.error(f"{self.name} failed to optimize code: {e}")
            context['status'] = 'error'
            return None

    def decide_handoff(self, context):
        # Decide whether to hand off to RefactoringAgent
        return 'RefactoringAgent'
