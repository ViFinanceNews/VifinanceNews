FROM dattran453/base_images_arch:v3

# Set the working directory inside the container
USER root 

WORKDIR /analysis_service


# Copy the application source code
COPY AnalysisService /analysis_service/AnalysisService
COPY ViFinanceCrawLib /analysis_service/ViFinanceCrawLib
COPY VnCoreNLP /analysis_service/VnCoreNLP

# Set PYTHONPATH so the modules can be found
ENV PYTHONPATH="/analysis_service"

# Expose Flask's default port
EXPOSE 7003

# Use Gunicorn to run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7003", "--timeout", "120", "AnalysisService.wsgi:app"]