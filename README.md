# Cloud Splitter

## Service Management

The project includes a comprehensive management script (`scripts/manage.sh`) to help with Docker service operations and monitoring. Here's how to use it:

### Basic Usage

```bash
# Make the script executable
chmod +x scripts/manage.sh

# Start all services
./scripts/manage.sh start

# Stop all services
./scripts/manage.sh stop

# Restart all services
./scripts/manage.sh restart

# Check service status
./scripts/manage.sh status
```

### Monitoring and Logs

```bash
# Monitor service status and resource usage
./scripts/manage.sh monitor

# View logs for a specific service
./scripts/manage.sh logs backend    # Last 100 lines
./scripts/manage.sh logs frontend 200  # Last 200 lines
```

### Database Management

```bash
# Initialize database and run migrations
./scripts/manage.sh init-db
```

### Additional Features

- Automatic environment validation
- Service health checking
- Colored logging with timestamps
- Resource usage monitoring
- Database migration support

### Requirements

- Docker
- Docker Compose
- Bash shell

### Logs

Logs are stored in the `logs/` directory:
- Service logs are handled by Docker Compose
- Management script logs are stored in `logs/manage.log`

For more information about available commands:
```bash
./scripts/manage.sh help
```

# Cloud Splitter

A comprehensive audio processing toolkit featuring both a modern web interface and a TUI-based tool for downloading, processing, and visualizing audio stems from videos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js-black)](https://nextjs.org)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com)
[![WebSocket: Ready](https://img.shields.io/badge/WebSocket-Ready-blue)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## Features

### Web Interface
- 🎵 Real-time audio processing and visualization
- 📊 10-band spectrum analyzer with Matrix theme
- 🌟 Music-reactive background effects
- 🎹 Audio stem separation (vocals, drums, bass, other)
- 🔄 Real-time WebSocket updates
- 📱 Responsive design

### TUI Application
- 🎼 Download videos/audio using yt-dlp
- 🎸 Process audio through multiple stem separators
- 📂 Batch processing support
- ⚙️ Flexible configuration options
- 📁 Intelligent file organization

## System Requirements

- Python 3.8+
- Node.js 16+ (for web interface)
- PostgreSQL 13+ (for web interface)
- FFmpeg
- ROCm (AMD GPUs) or CUDA (NVIDIA GPUs)

## Quick Start

### Web Interface Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/cbwinslow/cloud-splitter.git
   cd cloud-splitter
   ```

2. Set up the backend:
   ```bash
   cd web/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .env\Scriptsctivate
   pip install -r requirements.txt
   python scripts/setup.py
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   npm run setup-env
   ```

4. Start the development servers:
   ```bash
   # Terminal 1 - Backend
   cd web/backend
   source venv/bin/activate
   uvicorn app.main:app --reload

   # Terminal 2 - Frontend
   cd web/frontend
   npm run dev
   ```

Visit `http://localhost:3000` to access the web interface.

### TUI Application Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .env\Scriptsctivate  # Windows
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Launch the TUI:
   ```bash
   cloud-splitter tui
   ```

## Project Structure

```
cloud-splitter/
├── web/                   # Web interface components
│   ├── frontend/         # Next.js frontend application
│   │   ├── components/   # React components
│   │   ├── contexts/     # Context providers
│   │   ├── hooks/        # Custom hooks
│   │   ├── pages/        # Next.js pages
│   │   ├── services/     # Frontend services
│   │   └── styles/       # Theme and styles
│   └── backend/          # FastAPI backend service
│       ├── app/          # Application code
│       ├── tests/        # Backend tests
│       └── scripts/      # Utility scripts
├── src/                  # TUI application source
├── docs/                 # Documentation
├── scripts/              # Project scripts
└── tests/               # Integration tests
```

## Configuration

### Web Interface
- Frontend configuration in `web/frontend/.env.local`
- Backend configuration in `web/backend/.env`

### TUI Application
Configuration file location:
- Linux/Mac: `~/.config/cloud-splitter/config.toml`
- Windows: `%APPDATA%## Security

This project takes security seriously and implements several measures to maintain code security:

### Automated Security Tools
- Weekly dependency updates via Dependabot
- Automated security scanning via GitHub Actions
- CodeQL analysis for JavaScript and Python
- Snyk vulnerability scanning
- Regular npm audit and pip-audit checks

### Security Documentation
- Comprehensive security policy in SECURITY.md
- Known issues tracking and mitigation strategies
- Clear vulnerability reporting guidelines

### Best Practices
- Regular dependency updates
- Production/development environment separation
- Secure configuration management
- Input validation
- Proper error handling

For more details, see [SECURITY.md](SECURITY.md).


