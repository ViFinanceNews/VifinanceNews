# Use the latest lightweight Python image
FROM dattran453/base_images_arch:v3

# Set the working directory and permissions
USER root
WORKDIR /search_service

# Copy the application source code
COPY SearchService /search_service/SearchService
COPY ViFinanceCrawLib /search_service/ViFinanceCrawLib
COPY VnCoreNLP /search_service/VnCoreNLP

# Set PYTHONPATH so the modules can be found
ENV PYTHONPATH="/search_service"

# Expose the application's port
EXPOSE 7001

# Use Gunicorn to run the Flask app with increased timeout
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7001", "--timeout", "120", "SearchService.wsgi:app"]

