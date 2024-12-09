#!/usr/bin/env python3

import argparse
import logging
import os
from fast_edit_mode.orchestrator import Orchestrator
from fast_edit_mode.ai_interface import AIModelInterface
from fast_edit_mode.syntax_agent import SyntaxCorrectionAgent
from fast_edit_mode.optimization_agent import OptimizationAgent
from fast_edit_mode.refactoring_agent import RefactoringAgent
from fast_edit_mode.documentation_agent import DocumentationAgent
from fast_edit_mode.utils import load_config, setup_logging

def apply_fixes(orchestrator):
    """Apply fixes using the orchestrator."""
    context = orchestrator.context
    for agent_name, agent in orchestrator.agents.items():
        if isinstance(agent, SyntaxCorrectionAgent):
            agent.handle_task(context)

def main():
    parser = argparse.ArgumentParser(description="Fast Edit Mode: Multi-Agent Code Editing")
    parser.add_argument('input', help='Path to the input file')
    parser.add_argument('output', help='Path to save the edited output file')
    parser.add_argument('--config', default='fast_edit_mode/config.yaml', help='Path to config file')
    parser.add_argument('-fix', action='store_true', help='Apply fixes to the code')
    args = parser.parse_args()

    # Load configuration with correct path
    config = load_config(args.config)
    setup_logging(config)
    logger = logging.getLogger(__name__)

    # Initialize AI interface
    ai_interface = AIModelInterface(config)

    # Initialize orchestrator (agents will be initialized inside)
    orchestrator = Orchestrator({}, ai_interface)

    # Initialize agents
    orchestrator.agents = {
        'SyntaxCorrectionAgent': SyntaxCorrectionAgent('SyntaxCorrectionAgent', orchestrator),
        'OptimizationAgent': OptimizationAgent('OptimizationAgent', orchestrator),
        'RefactoringAgent': RefactoringAgent('RefactoringAgent', orchestrator),
        'DocumentationAgent': DocumentationAgent('DocumentationAgent', orchestrator),
    }

    # Read the input file
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        logger.error(f"Failed to read input file: {e}")
        print("Failed to read input file.")
        return

    # Check if the file is large and needs chunking
    if len(code.split('\n')) > 1000:
        # Split code into chunks and process in parallel
        code_chunks = orchestrator.split_code_into_chunks(code)
        orchestrator.process_chunks_in_parallel(code_chunks)
    else:
        # Process code without chunking
        orchestrator.start_process(code)

    # Apply fixes if the -fix flag is provided
    if args.fix:
        apply_fixes(orchestrator)

    # Write the output file
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(orchestrator.context['code'])
        logger.info(f"Editing completed successfully. Output saved to {args.output}")
        print(f"Editing completed successfully. Output saved to {args.output}")
    except Exception as e:
        logger.error(f"Failed to write output file: {e}")
        print("Failed to write output file.")

if __name__ == "__main__":
    main()
