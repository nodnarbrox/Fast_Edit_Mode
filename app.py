import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from fast_edit_mode.utils import load_config
from fast_edit_mode.ai_interface import AIModelInterface
from fast_edit_mode.orchestrator import Orchestrator
from fast_edit_mode.syntax_agent import SyntaxCorrectionAgent
from fast_edit_mode.refactoring_agent import RefactoringAgent
from fast_edit_mode.optimization_agent import OptimizationAgent
from fast_edit_mode.documentation_agent import DocumentationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='web_app.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# CSRF Protection
csrf = CSRFProtect(app)

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "30 per hour"],
    storage_uri="memory://"
)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load configuration
config = load_config()

# Initialize AI Interface
ai_interface = AIModelInterface(config)

# Initialize Orchestrator first
orchestrator = Orchestrator({}, ai_interface)

# Initialize Agents with the orchestrator
agents = {
    'SyntaxCorrectionAgent': SyntaxCorrectionAgent('SyntaxCorrectionAgent', orchestrator),
    'RefactoringAgent': RefactoringAgent('RefactoringAgent', orchestrator),
    'OptimizationAgent': OptimizationAgent('OptimizationAgent', orchestrator),
    'DocumentationAgent': DocumentationAgent('DocumentationAgent', orchestrator)
}

# Update the orchestrator with the agents
orchestrator.agents = agents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("10 per minute")
@csrf.exempt
def upload_code():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the uploaded file
        with open(filepath, 'r') as f:
            code = f.read()
        
        # Use orchestrator to process code
        try:
            # Split code into chunks for parallel processing
            code_chunks = orchestrator.split_code_into_chunks(code)
            orchestrator.process_chunks_in_parallel(code_chunks)
            processed_code = orchestrator.context['code']
            
            # Save processed code
            processed_filename = f'processed_{filename}'
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            with open(processed_filepath, 'w') as f:
                f.write(processed_code)
            
            logger.info(f'Successfully processed file: {filename}')
            
            return jsonify({
                'message': 'File processed successfully',
                'original_filename': filename,
                'processed_filename': processed_filename
            }), 200
        
        except Exception as e:
            logger.error(f'Error processing file: {str(e)}')
            return jsonify({'error': 'Error processing file', 'details': str(e)}), 500
    
    except Exception as e:
        logger.error(f'Upload error: {str(e)}')
        return jsonify({'error': 'Upload failed', 'details': str(e)}), 500

@app.route('/process_instruction', methods=['POST'])
@limiter.limit("10 per minute")
@csrf.exempt
def process_instruction():
    try:
        data = request.get_json()
        
        if not data or 'code' not in data or 'instruction' not in data:
            return jsonify({'error': 'Missing code or instruction'}), 400
        
        code = data['code']
        instruction = data['instruction']
        
        try:
            # Add instruction to context
            orchestrator.context['instruction'] = instruction
            
            # Split code into chunks for parallel processing
            code_chunks = orchestrator.split_code_into_chunks(code)
            orchestrator.process_chunks_in_parallel(code_chunks)
            processed_code = orchestrator.context['code']
            
            # Save processed code
            processed_filename = f'processed_instruction_{hash(instruction)}.py'
            processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
            with open(processed_filepath, 'w') as f:
                f.write(processed_code)
            
            logger.info(f'Successfully processed instruction')
            
            return jsonify({
                'message': 'Code processed successfully based on instruction',
                'processed_filename': processed_filename
            }), 200
        
        except Exception as e:
            logger.error(f'Error processing instruction: {str(e)}')
            return jsonify({'error': 'Error processing instruction', 'details': str(e)}), 500
    
    except Exception as e:
        logger.error(f'Instruction processing error: {str(e)}')
        return jsonify({'error': 'Instruction processing failed', 'details': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True
        )
    except Exception as e:
        logger.error(f'Download error: {str(e)}')
        return jsonify({'error': 'Download failed', 'details': str(e)}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'py', 'js', 'java', 'cpp', 'json', 'xml', 'md', 'txt', 'conf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({'error': 'Rate limit exceeded'}), 429

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
