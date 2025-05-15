# Image Processing Service with Django and Celery

![Django](https://img.shields.io/badge/Django-3.2-green)
![Celery](https://img.shields.io/badge/Celery-5.2-blue)
![Redis](https://img.shields.io/badge/Redis-6.2-red)
![Docker](https://img.shields.io/badge/Docker-20.10-lightblue)

A scalable image processing service that:
- Accepts image uploads via POST requests
- Processes images asynchronously with Celery
- Returns random results (1-1000) after 20-second simulation
- Provides real-time status updates
- Supports bulk processing (100 images at once)

## Features

- **Asynchronous Processing**: Celery handles long-running tasks
- **Real-time Status**: Polling endpoint for progress updates
- **Bulk Processing**: Test endpoint for sending 100 images
- **Result Tracking**: Stores all results in PostgreSQL
- **Modern Stack**: Django, Celery, Redis, Docker
- **Monitoring**: Flower for Celery task monitoring

## Prerequisites

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.12 (optional for local development)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-processing-service.git
   cd image-processing-service