#!/bin/bash

# Docker Build and Run Scripts for SugarGlitch RealOps

set -e

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

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "Docker is available and running"
}

# Build the Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t sugarglitch-realops:latest .
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Run the container
run_container() {
    print_status "Running Docker container..."
    docker run --rm -it \
        --name sugarglitch-realops-temp \
        -v "$(pwd)/logs:/app/logs" \
        -v "$(pwd)/databases:/app/databases" \
        -v "$(pwd)/extractions:/app/extractions" \
        -v "$(pwd)/results:/app/results" \
        sugarglitch-realops:latest "$@"
}

# Run with docker-compose
run_compose() {
    print_status "Starting services with docker-compose..."
    docker-compose up -d
    if [ $? -eq 0 ]; then
        print_success "Services started successfully"
        print_status "Use 'docker-compose logs -f' to view logs"
        print_status "Use 'docker-compose down' to stop services"
    else
        print_error "Failed to start services"
        exit 1
    fi
}

# Stop docker-compose services
stop_compose() {
    print_status "Stopping docker-compose services..."
    docker-compose down
    print_success "Services stopped"
}

# Clean up Docker resources
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker system prune -f
    docker volume prune -f
    print_success "Cleanup completed"
}

# Show help
show_help() {
    echo "SugarGlitch RealOps Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build           Build the Docker image"
    echo "  run [args]      Run the container with optional arguments"
    echo "  compose         Start services with docker-compose"
    echo "  stop            Stop docker-compose services"
    echo "  cleanup         Clean up unused Docker resources"
    echo "  shell           Open a shell in the container"
    echo "  logs            Show container logs"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 run tools/generate_dm_timeline.py"
    echo "  $0 compose"
    echo "  $0 shell"
}

# Open shell in container
run_shell() {
    print_status "Opening shell in container..."
    docker run --rm -it \
        --name sugarglitch-realops-shell \
        -v "$(pwd)/logs:/app/logs" \
        -v "$(pwd)/databases:/app/databases" \
        -v "$(pwd)/extractions:/app/extractions" \
        -v "$(pwd)/results:/app/results" \
        --entrypoint /bin/bash \
        sugarglitch-realops:latest
}

# Show logs
show_logs() {
    if docker-compose ps | grep -q "sugarglitch-realops"; then
        docker-compose logs -f sugarglitch-realops
    else
        print_error "Container is not running. Start it with: $0 compose"
    fi
}

# Main script logic
main() {
    case "${1:-help}" in
        "build")
            check_docker
            build_image
            ;;
        "run")
            check_docker
            shift
            run_container "$@"
            ;;
        "compose")
            check_docker
            run_compose
            ;;
        "stop")
            check_docker
            stop_compose
            ;;
        "cleanup")
            check_docker
            cleanup
            ;;
        "shell")
            check_docker
            run_shell
            ;;
        "logs")
            check_docker
            show_logs
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run the main function with all arguments
main "$@"
