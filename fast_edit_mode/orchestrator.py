# orchestrator.py

import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, agents, ai_interface):
        self.agents = agents  # Dictionary of agent instances
        self.ai_interface = ai_interface
        self.context = {
            'code': '',
            'edit_history': [],
            'metadata': {},
            'status': 'pending',
        }

    def start_process(self, code):
        self.context['code'] = code
        current_agent_name = 'SyntaxCorrectionAgent'
        while current_agent_name:
            agent = self.agents[current_agent_name]
            logger.info(f"Current agent: {current_agent_name}")
            next_agent_name = agent.handle_task(self.context)
            if self.context.get('status') == 'error':
                logger.error("Process terminated due to an error.")
                break
            current_agent_name = next_agent_name

    def split_code_into_chunks(self, code, chunk_size=1000):
        # Split code into chunks based on the chunk size
        lines = code.split('\n')
        chunks = []
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

    def process_chunks_in_parallel(self, code_chunks):
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(self.process_chunk, chunk) for chunk in code_chunks]
            results = [future.result() for future in futures]
        # Combine results and update context
        combined_code = '\n'.join(results)
        self.context['code'] = combined_code
        self.context['metadata']['chunk_processing'] = True
        self.context['metadata']['processed_chunks'] = results

    def process_chunk(self, chunk):
        # Create a separate context for the chunk
        chunk_context = {
            'code': chunk,
            'edit_history': [],
            'metadata': {},
            'status': 'pending',
        }
        current_agent_name = 'SyntaxCorrectionAgent'
        while current_agent_name:
            agent = self.agents[current_agent_name]
            logger.info(f"Processing chunk with {current_agent_name}")
            next_agent_name = agent.handle_task(chunk_context)
            if chunk_context.get('status') == 'error':
                logger.error("Chunk processing terminated due to an error.")
                break
            current_agent_name = next_agent_name
        return chunk_context['code']
