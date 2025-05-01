# Use the latest lightweight Python image
FROM dattran453/base-image:v7

# Set the user and working directory
USER root
WORKDIR /summariser_service

# Copy application source code
COPY SummariserService /summariser_service/SummariserService
COPY ViFinanceCrawLib /summariser_service/ViFinanceCrawLib
COPY VnCoreNLP /summariser_service/VnCoreNLP

# Set PYTHONPATH so the modules can be found
ENV PYTHONPATH="/summariser_service"

# Expose Flask's port
EXPOSE 7002

# Run the app using Gunicorn with a 120-second timeout
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7002", "--timeout", "120", "SummariserService.app:app"]