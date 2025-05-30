#!/bin/bash

# Color definitions
RED="[0;31m"
GREEN="[0;32m"
YELLOW="[1;33m"
BLUE="[0;34m"
NC="[0m" # No Color

# Log file
LOG_FILE="logs/manage.log"
mkdir -p logs

# Logging function
log() {
    local level=$1
    local message=$2
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "${timestamp} [${level}] ${message}" >> "${LOG_FILE}"
    case $level in
        "INFO")
            echo -e "${BLUE}${timestamp}${NC} [${GREEN}${level}${NC}] ${message}"
            ;;
        "WARNING")
            echo -e "${BLUE}${timestamp}${NC} [${YELLOW}${level}${NC}] ${message}"
            ;;
        "ERROR")
            echo -e "${BLUE}${timestamp}${NC} [${RED}${level}${NC}] ${message}"
            ;;
    esac
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log "ERROR" "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Check required environment variables
check_env() {
    if [ ! -f .env ]; then
        log "ERROR" ".env file not found"
        exit 1
    fi

    required_vars=("POSTGRES_USER" "POSTGRES_PASSWORD" "POSTGRES_DB")
    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" .env; then
            log "ERROR" "Required environment variable ${var} not found in .env"
            exit 1
        fi
    done
}

# Initialize database
init_db() {
    log "INFO" "Initializing database..."
    docker-compose exec backend python scripts/init_db.py
    if [ $? -eq 0 ]; then
        log "INFO" "Database initialized successfully"
    else
        log "ERROR" "Database initialization failed"
        exit 1
    fi
}

# Check service health
check_health() {
    local service=$1
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps $service | grep -q "Up"; then
            log "INFO" "${service} is healthy"
            return 0
        fi
        log "INFO" "Waiting for ${service} to be ready... (${attempt}/${max_attempts})"
        sleep 2
        ((attempt++))
    done

    log "ERROR" "${service} failed to start"
    return 1
}

# Start services
start() {
    check_docker
    check_env
    
    log "INFO" "Starting services..."
    docker-compose up -d
    
    services=("db" "backend" "frontend" "caddy")
    for service in "${services[@]}"; do
        check_health $service || exit 1
    done
    
    log "INFO" "All services started successfully"
    log "INFO" "Application is available at https://cloud-splitter.localhost"
}

# Stop services
stop() {
    log "INFO" "Stopping services..."
    docker-compose down
    log "INFO" "Services stopped"
}

# Restart services
restart() {
    stop
    start
}

# Show service status
status() {
    docker-compose ps
}

# Monitor services
monitor() {
    log "INFO" "Monitoring services..."
    docker stats
}

# View service logs
logs() {
    local service=$1
    local lines=${2:-100}
    
    if [ -z "$service" ]; then
        log "ERROR" "Service name required"
        exit 1
    fi
    
    docker-compose logs --tail=$lines -f $service
}

# Show help
show_help() {
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  monitor     Monitor service resources"
    echo "  logs        View service logs (args: service_name [num_lines])"
    echo "  init-db     Initialize database"
    echo "  help        Show this help message"
}

# Main script
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    monitor)
        monitor
        ;;
    logs)
        logs $2 $3
        ;;
    init-db)
        init_db
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
