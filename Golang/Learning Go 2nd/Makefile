# Variables
BINARY_NAME=learning-go
SOURCE_DIR=.
BUILD_DIR=bin

# Default target
all: build

# Build the Go application
build:
	@echo "Building the project..."
	@if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)
	@go build -o $(BUILD_DIR)/$(BINARY_NAME) $(SOURCE_DIR)

# Run the Go application
run: build
	@echo "Running the project..."
	@$(BUILD_DIR)/$(BINARY_NAME)

# Test the Go application
test:
	@echo "Running tests..."
	@go test ./...

# Clean the build artifacts
clean:
	@echo "Cleaning the build directory..."
	@rm -rf $(BUILD_DIR)

# Install dependencies (if any)
deps:
	@echo "Installing dependencies..."
	@go mod tidy

# Format the Go code
fmt:
	@echo "Formatting the code..."
	@go fmt ./...

# Lint the Go code
lint:
	@echo "Linting the code..."
	@golangci-lint run

# Show help message
help:
	@echo "Usage:"
	@echo "  make [target]"
	@echo
	@echo "Targets:"
	@echo "  all      - Default target (build)"
	@echo "  build    - Build the Go application"
	@echo "  run      - Run the Go application"
	@echo "  test     - Test the Go application"
	@echo "  clean    - Clean the build artifacts"
	@echo "  deps     - Install dependencies"
	@echo "  fmt      - Format the Go code"
	@echo "  lint     - Lint the Go code"
	@echo "  help     - Show this help message"

# Phony targets (not real files)
.PHONY: all build run test clean deps fmt lint help