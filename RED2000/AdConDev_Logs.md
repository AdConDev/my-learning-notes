# Development Backlog and Notes

## Week of 07/08/2025 - 12/08/2025

### Repository Improvements
- **Templates & Workflows**
  - Create templates for issues, bugs, and feature requests
  - Set up CI workflows:
    - Test and build on multiple OS
    - Run simple linters
    - Ensure compliance with Conventional Commits 1.0.0
  - Implement stale PR/issue closer (auto-close after inactivity)

- **Dependency Management**
  - Configure Dependabot:
    - Periodic update checks
    - Automerge updates to `dev` and open PRs for review

- **PR Automation**
  - Automate PR tagging based on modified files and PR size
  - Add greeting comments for PR authors
  - Automate releases based on commit types and PR descriptions

### Documentation & Code Quality
- Configure commit instructions for better messages and Copilot usage
- Set up linters:
  - Commit message linter
  - Code linters for Goland (local) and GH Actions
- Add documentation:
  - Contribution guide
  - Code of conduct
  - Setup instructions
  - Development process

### Pending GitHub Tasks
- Translate `pr-template`
- Investigate `renovate.json`
- Update `README.md`

### Architecture: PosPrinter and Daemon Separation
- **Repository Structure**
  - Split repository: create new repo for core logic
  
- **Service Implementation**
  - Explore implementations:
    - Daemon listening to WebSocket for print commands
    - REST API for protocol-agnostic, lightweight local use
  - Develop simple API using Gin (prioritize performance and lightweight design)
  
- **Ticket Handling**
  - Use JSON for ticket data instead of ticket constructors
  - Translate JSON commands to Golang functions
  
- **Research Areas**
  - JSON ticket representation tools (e.g., Parzibyte)
  - WebSocket and REST API communication feasibility
  
- **Microservices Approach**
  - Split into at least two services: Printing and Daemon
  - Evaluate gRPC for inter-service communication
  - Assess containerization impact on connectors

### Development Tasks
- Investigate codepage issues:
  - Suspect printer issues
  - Test with disk reader (possible firmware update needed)
- Complete ESCPOS functions:
  - Integrate documented commands
  - Separate responsibilities after removing base commands
- Refactor code:
  - Use Copilot for suggestions
  - Review all TODOs and FIXMEs

## Week of 13/08/2025 - 15/08/2025

### Code Review and Refactoring
- Review all TODOs and FIXMEs in the codebase:
  - Most relate to unfinished ESCPOS command implementations
  - Many require specific types to validate inputs
- Develop testing strategy for commands without physical printer (investigate os.stdout as io.writer)
- Reduce boilerplate code with middleware approach to commands
- Ensure proper public/private function declarations
- Improve modularity and separation of concerns
- Review architecture differences between protocols (e.g., ESCPOS vs ZPL command equivalents)

## Week of 18/08/2025 - 22/08/2025

### Architecture and Implementation
- **Module Separation**
  - Implement separate modules for different protocols (ESCPOS, ZPL, etc.)
  - Create each protocol module as separate Go package within same repository
  - Design registry to handle multiple printers and abstract POS concept
  
- **Implementation Progress**
  - Improved barcode support
  - Started ESCPOS basic commands for text and formatting
  - Planning second layer for complex logic:
    - Auto-formatting to active charset for printer code page
    - Improved error handling with specific error types
  
- **Project Management**
  - Set up PRs and issues in pos-printer repository for tracking
  - Need to generate documentation for each protocol module
  - Move diary tasks into GitHub project backlog items
  - Review GitHub project management best practices

### Technical Learning
- Deepened knowledge of channels and goroutines in Go
- Learning about stack, heap, and garbage collection in Golang
- Migrating slowly to Go 1.25

### Architecture Progress
- Identified need for two ESCPOS versions: Standard and Page Mode
  - Can be handled by same codebase with different configurations
  - Page Mode commands postponed for now
- Basic commands implemented:
  - Printing
  - Line Spacing

## Week of 25/08/2025 - 29/08/2025

### Testing and Delivery
- Implemented robust testing for basic commands:
  - Printing
  - Line Spacing
- Planning to replicate testing approach for all commands
- Investigating PDF/image generation as additional protocol option for receipt delivery
- Focusing on delivering working prototype ASAP
- Need to consolidate backlog items from laptop notes to GitHub Project
- Established weekly policy to push to remote branches with open PRs every Friday

#### 1. **Dependency Injection Testing**
**Purpose**: Verify that your code works with any implementation of an interface
- Tests flexibility and substitutability
- Ensures loose coupling
- Validates the Liskov Substitution Principle

#### 2. **Fake Implementation Testing**
**Purpose**: Test behavior with stateful simulations
- Tracks accumulated state over multiple operations
- Simulates real-world behavior without real hardware
- Useful for integration testing

#### 3. **Interface Composition Testing**
**Purpose**: Verify that composite interfaces work correctly
- Tests that a type implements multiple interfaces
- Validates interface embedding
- Ensures polymorphic behavior

#### 4. **Mock Testing**
**Purpose**: Verify interactions and behavior
- Tracks method calls
- Controls return values
- Simulates error conditions