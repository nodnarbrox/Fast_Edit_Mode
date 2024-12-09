# syntax_agent.py

from fast_edit_mode.agent import Agent
import logging

logger = logging.getLogger(__name__)

class SyntaxCorrectionAgent(Agent):
    def handle_task(self, context):
        code = context['code']
        logger.info(f"{self.name} is correcting syntax.")
        try:
            corrected_code = self.orchestrator.ai_interface.correct_syntax(code)
            task_info = {
                'agent': self.name,
                'action': 'syntax_correction',
                'updated_code': corrected_code,
            }
            self.update_context(context, task_info)
            # Decide if handoff is needed
            return self.decide_handoff(context)
        except Exception as e:
            logger.error(f"{self.name} failed to correct syntax: {e}")
            context['status'] = 'error'
            return None

    def decide_handoff(self, context):
        # Decide whether to hand off to OptimizationAgent
        if 'optimize' in context['code']:
            return 'OptimizationAgent'
        return 'OptimizationAgent'  # Default handoff
