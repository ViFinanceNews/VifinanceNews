# Use the latest lightweight Python image
FROM dattran453/base-image:v7

# Set the working directory inside the container
WORKDIR /logging_service

# Copy the rest of the application source code (only after dependencies are installed)
COPY LoggingService /logging_service/LoggingService
COPY ViFinanceCrawLib /logging_service/ViFinanceCrawLib

# Set PYTHONPATH so the module can be found
ENV PYTHONPATH="/logging_service"

# Expose Flask's default port
EXPOSE 7004

# Use a more efficient CMD
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7004", "--timeout", "120", "LoggingService.app:app"]