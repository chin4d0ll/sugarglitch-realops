#!/bin/bash

# Docker Compose Management Script for SugarGlitch RealOps
# Usage: ./docker-scripts.sh [start|stop|restart|logs|build|status|clean]

set -e

PROJECT_NAME="sugarglitch-realops"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if docker-compose is available
check_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
        print_error "docker-compose is not available. Please install docker-compose."
        exit 1
    fi
}

# Determine compose command
get_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        echo "docker-compose"
    else
        echo "docker compose"
    fi
}

# Main functions
start_services() {
    print_status "Starting SugarGlitch RealOps services..."
    check_docker
    check_compose
    
    COMPOSE_CMD=$(get_compose_cmd)
    
    # Create data directory if it doesn't exist
    mkdir -p ./data
    
    # Start services
    $COMPOSE_CMD -f $COMPOSE_FILE up -d
    
    print_success "Services started successfully!"
    print_status "Database: postgresql://sguser:sgpass@localhost:5432/sgdb"
    print_status "Use '$0 logs' to view logs"
    print_status "Use '$0 status' to check service status"
}

stop_services() {
    print_status "Stopping SugarGlitch RealOps services..."
    check_docker
    check_compose
    
    COMPOSE_CMD=$(get_compose_cmd)
    $COMPOSE_CMD -f $COMPOSE_FILE down
    
    print_success "Services stopped successfully!"
}

restart_services() {
    print_status "Restarting SugarGlitch RealOps services..."
    stop_services
    sleep 2
    start_services
}

view_logs() {
    check_docker
    check_compose
    
    COMPOSE_CMD=$(get_compose_cmd)
    
    if [ -n "$2" ]; then
        print_status "Viewing logs for service: $2"
        $COMPOSE_CMD -f $COMPOSE_FILE logs -f "$2"
    else
        print_status "Viewing logs for all services (Ctrl+C to exit)..."
        $COMPOSE_CMD -f $COMPOSE_FILE logs -f
    fi
}

build_services() {
    print_status "Building SugarGlitch RealOps services..."
    check_docker
    check_compose
    
    COMPOSE_CMD=$(get_compose_cmd)
    $COMPOSE_CMD -f $COMPOSE_FILE build --no-cache
    
    print_success "Build completed successfully!"
}

check_status() {
    check_docker
    check_compose
    
    COMPOSE_CMD=$(get_compose_cmd)
    
    print_status "Service Status:"
    $COMPOSE_CMD -f $COMPOSE_FILE ps
    
    echo ""
    print_status "Container Health:"
    docker ps --filter "name=sugarglitch" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

clean_all() {
    print_warning "This will remove all containers, networks, and volumes!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        check_docker
        check_compose
        
        COMPOSE_CMD=$(get_compose_cmd)
        
        print_status "Stopping and removing all services..."
        $COMPOSE_CMD -f $COMPOSE_FILE down -v --remove-orphans
        
        print_status "Removing images..."
        docker rmi $(docker images -q --filter "reference=*sugarglitch*") 2>/dev/null || true
        
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Help function
show_help() {
    echo "SugarGlitch RealOps Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  logs [svc]  View logs (optionally for specific service: app, db)"
    echo "  build       Build/rebuild all services"
    echo "  status      Show service status"
    echo "  clean       Remove all containers, networks, and volumes"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start              # Start all services"
    echo "  $0 logs app           # View app logs only"
    echo "  $0 logs db            # View database logs only"
    echo "  $0 build              # Rebuild services"
}

# Main script logic
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        view_logs "$@"
        ;;
    build)
        build_services
        ;;
    status)
        check_status
        ;;
    clean)
        clean_all
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
