# Cloud-Splitter Web Service

## Overview
Cloud-Splitter Web Service is a modern web application that provides audio processing and visualization capabilities, transforming the original TUI-based Cloud-Splitter into a feature-rich web platform. The service enables users to process audio files with real-time visualization and interactive controls.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-12.0.0-blue)](https://nextjs.org)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.2.0-brightgreen)](https://vuejs.org)

## Features
- Advanced audio processing and stem splitting
- Real-time 10-band audio spectrum analyzer
- Music-reactive background effects
- Interactive file management
- Real-time processing status updates
- Cross-platform compatibility

## Architecture
The project consists of two main components:
1. Backend Service (FastAPI)
2. Frontend Application (Next.js + Vue.js)

### Technology Stack
- **Backend**:
  - FastAPI
  - PostgreSQL
  - WebSocket
  - Python Audio Libraries

- **Frontend**:
  - Next.js
  - TypeScript
  - Vue.js
  - Web Audio API

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Docker (optional)

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/cbwinslow/cloud-splitter.git
cd cloud-splitter/web
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Start the backend server
uvicorn app.main:app --reload
```

3. Set up the frontend:
```bash
# Install dependencies
cd ../frontend
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your configuration

# Start the development server
npm run dev
```

4. Access the development environment:
- Backend API: http://localhost:8000
- Frontend App: http://localhost:3000
- API Documentation: http://localhost:8000/docs

### Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Access the containerized application:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Development Guidelines

### Code Structure

```
web/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── public/
│   ├── styles/
│   └── package.json
└── docs/
    ├── README.md
    ├── SRS.md
    └── PROJECT_PLAN.md
```

### Coding Standards
- Backend: Follow PEP 8 guidelines
- Frontend: Follow TypeScript best practices
- Use ESLint and Prettier for code formatting
- Write comprehensive tests for new features
- Maintain documentation for all APIs

### Git Workflow
1. Create a feature branch from `develop`
2. Make changes and commit with clear messages
3. Write/update tests
4. Submit PR for review
5. Address review comments
6. Merge to `develop` after approval

### Testing
- Backend:
```bash
cd backend
pytest
```

- Frontend:
```bash
cd frontend
npm test
```

## API Documentation

### REST API
- Complete API documentation available at `/docs` endpoint
- OpenAPI specification at `/openapi.json`

### WebSocket API
- Real-time updates for processing status
- Audio visualization data streaming
- Connection details in API documentation

## Deployment

### Production Build
1. Backend:
```bash
cd backend
python scripts/build.py
```

2. Frontend:
```bash
cd frontend
npm run build
```

### Deployment Options
- Docker Compose (recommended)
- Manual deployment
- Cloud platforms (AWS, GCP, Azure)

Refer to `deployment.md` for detailed instructions.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please read `CONTRIBUTING.md` for details on our code of conduct and development process.

## Monitoring and Maintenance

### Health Checks
- Backend: `/health`
- Frontend: `/api/health`

### Logging
- Backend logs: `backend/logs/`
- Frontend logs: Available in browser console
- Production logs: Configured via environment variables

### Performance Monitoring
- API response times
- WebSocket connection status
- Resource usage metrics
- Error rates and types

## Support and Communication
- GitHub Issues for bug reports and feature requests
- Project Discord channel for discussions
- Regular team meetings (see PROJECT_PLAN.md)

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Original Cloud-Splitter TUI developers
- Open source audio processing libraries
- Community contributors

## Security
Report security vulnerabilities to security@cloud-splitter.com

## Version History
See CHANGELOG.md for version history and migration guides.

