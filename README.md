# Fast Edit Mode
cd "C:\path_to_project directory" ; python "C:path_to_\fast_edit_mode\scripts\run_fast_edit.py" -fix --config fast_edit_mode/config.yaml functions/ivrFlow.js functions/ivrFlow_edited.js


step 1: edit the config.yaml file according to your project structure and requirements.\
step 2: run the command: cd "C:\\path_to_project directory" ; python "C:\\path_to_\\fast_edit_mode\\scripts\\run_fast_edit.py" -fix --config fast\_edit\_mode/config.yaml functions/ivrFlow.js functions/ivrFlow\_edited.js

example of actual command cd "C:\Users\USERNAME\Desktop\build\Sonivo - Ai SAAS call center - v1\upload_this" ; python "C:\Users\USERNAME\Desktop\build\fast_edit_mode\scripts\run_fast_edit.py" -fix --config fast_edit_mode/config.yaml functions/ivrFlow.js functions/ivrFlow_edited.js
## Overview
Fast Edit Mode is an intelligent code editing and optimization tool designed to assist developers in improving and refactoring their code. The tool leverages multiple AI agents to provide comprehensive code analysis, documentation, and optimization capabilities.

## Project Structure
- `fast_edit_mode/`: Core package directory
  - `agent.py`: Base agent class
  - `ai_interface.py`: Interface for AI interactions
  - `documentation_agent.py`: Agent for generating documentation
  - `optimization_agent.py`: Agent for code optimization
  - `orchestrator.py`: Coordinates different agents
  - `refactoring_agent.py`: Agent for code refactoring
  - `syntax_agent.py`: Agent for syntax analysis
  - `utils.py`: Utility functions
  - `config.yaml`: Configuration file

- `scripts/`: Utility scripts
  - `run_fast_edit.py`: Script to run the tool

## Prerequisites
- Python 3.8+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nodnarbrox/Fast_Edit_Mode.git
cd fast-edit-mode
```

2. Install the package:
```bash
pip install -e .
```

## Usage Examples

### Basic Command Usage
```bash
# Run the main script
python scripts/run_fast_edit.py

# Optimize a specific Python file
python scripts/run_fast_edit.py --optimize path/to/your/script.py

# Generate documentation for a file
python scripts/run_fast_edit.py --document path/to/your/script.py

# Perform syntax analysis
python scripts/run_fast_edit.py --syntax-check path/to/your/script.py

# Refactor code
python scripts/run_fast_edit.py --refactor path/to/your/script.py
```

### Advanced Usage
```bash
# Run multiple operations on a file
python scripts/run_fast_edit.py --optimize --document --syntax-check path/to/your/script.py

# Specify custom configuration
python scripts/run_fast_edit.py --config custom_config.yaml path/to/your/script.py

# Verbose output mode
python scripts/run_fast_edit.py --verbose path/to/your/script.py
```

## Configuration Examples
In `fast_edit_mode/config.yaml`:
```yaml
# Example configuration
optimization:
  level: high
  ignore_patterns:
    - "*.test.py"
    - "vendor/*"

documentation:
  format: markdown
  include_type_hints: true

syntax:
  strict_mode: true
  max_line_length: 120
```

## Features
- Code Optimization
- Syntax Analysis
- Documentation Generation
- Code Refactoring

## Troubleshooting
- Ensure you have the latest version of Python
- Check that all dependencies are installed
- Verify your configuration file syntax
- Use the `--verbose` flag for detailed error messages

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
[Specify your license here]

## Contact
[Your contact information or project maintainer's details]
