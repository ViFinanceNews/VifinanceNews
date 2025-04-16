from flask import Flask, request, jsonify
from datetime import datetime
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os

app = Flask(__name__)

# Configure logging with Azure Application Insights
try:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Retrieve instrumentation key from environment variable
    instrumentation_key = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
    if not instrumentation_key:
        raise ValueError("APPINSIGHTS_INSTRUMENTATIONKEY not set")
    
    azure_handler = AzureLogHandler(
        connection_string=f'InstrumentationKey={instrumentation_key}'
    )
    logger.addHandler(azure_handler)
    
    # Console output for development
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s')
    )
    logger.addHandler(stream_handler)
    
except Exception as e:
    print(f"Failed to configure Azure logging: {str(e)}")

# Supported services
VALID_SERVICES = {
    'SearchService',
    'AuthenticationService',
    'AnalysisService',
    'SummariseService'
}

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": list(VALID_SERVICES)
    })

# Log endpoint for general messages
@app.route('/log', methods=['POST'])
def log_message():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['service_name', 'event_type', 'message', 'severity']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        # Validate service_name
        service_name = data['service_name']
        if service_name not in VALID_SERVICES:
            return jsonify({"error": f"Invalid service_name. Must be one of {VALID_SERVICES}"}), 400
            
        event_type = data['event_type']
        message = data['message']
        severity = data['severity'].upper()
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Custom dimensions for Application Insights
        custom_dimensions = {
            'service_name': service_name,
            'event_type': event_type,
            'timestamp': timestamp
        }
        
        # Log based on severity
        if severity == 'DEBUG':
            logger.debug(message, extra={'custom_dimensions': custom_dimensions})
        elif severity == 'INFO':
            logger.info(message, extra={'custom_dimensions': custom_dimensions})
        elif severity == 'WARNING':
            logger.warning(message, extra={'custom_dimensions': custom_dimensions})
        elif severity == 'ERROR':
            logger.error(message, extra={'custom_dimensions': custom_dimensions})
        elif severity == 'CRITICAL':
            logger.critical(message, extra={'custom_dimensions': custom_dimensions})
        else:
            return jsonify({"error": "Invalid severity level"}), 400
            
        return jsonify({
            "status": "success",
            "message": "Log recorded",
            "timestamp": timestamp,
            "service_name": service_name
        }), 200
        
    except Exception as e:
        logger.exception(f"Error processing log: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Exception logging endpoint
@app.route('/exception', methods=['POST'])
def log_exception():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['service_name', 'error']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        service_name = data['service_name']
        if service_name not in VALID_SERVICES:
            return jsonify({"error": f"Invalid service_name. Must be one of {VALID_SERVICES}"}), 400
            
        error_message = data['error']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        custom_dimensions = {
            'service_name': service_name,
            'timestamp': timestamp
        }
        
        logger.exception(
            error_message,
            extra={'custom_dimensions': custom_dimensions}
        )
        
        return jsonify({
            "status": "success",
            "message": "Exception recorded",
            "timestamp": timestamp,
            "service_name": service_name
        }), 200
        
    except Exception as e:
        logger.exception(f"Error processing exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Event logging endpoint
@app.route('/event', methods=['POST'])
def log_event():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['service_name', 'event_name']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
            
        service_name = data['service_name']
        if service_name not in VALID_SERVICES:
            return jsonify({"error": f"Invalid service_name. Must be one of {VALID_SERVICES}"}), 400
            
        event_name = data['event_name']
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        custom_dimensions = {
            'service_name': service_name,
            'event_name': event_name,
            'timestamp': timestamp
        }
        
        logger.info(
            f"Event: {event_name}",
            extra={'custom_dimensions': custom_dimensions}
        )
        
        return jsonify({
            "status": "success",
            "message": "Event recorded",
            "timestamp": timestamp,
            "service_name": service_name
        }), 200
        
    except Exception as e:
        logger.exception(f"Error processing event: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)