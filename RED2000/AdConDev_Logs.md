# Mental Notes / Backlog Items
## 07/08/2025 - 12/08/2025
### Repository Improvements
- Create templates for issues, bugs, and feature requests.
- Set up CI workflows:
  - Test and build on multiple OS.
  - Run simple linters.
  - Ensure compliance with Conventional Commits 1.0.0.
- Configure Dependabot:
  - Periodic update checks.
  - Automerge updates to `dev` and open PRs for review.
- Automate PR tagging:
  - Tag based on modified files and PR size.
  - Add a greeting comment for PR authors.
- Automate releases:
  - Format and define releases based on commit types and PR descriptions.
- Implement stale PR/issue closer:
  - Close items after a period of inactivity.

### Secondary GitHub Tasks
- Configure commit instructions for better commit messages and Copilot usage.
- Set up linters:
  - Commit message linter.
  - Code linters for Goland (local) and GH Actions.
- Add documentation:
  - Contribution guide, code of conduct, setup instructions, and development process.
- Pending tasks:
  - Translate `pr-template`.
  - Investigate `renovate.json`.
  - Update `README.md`.

### PosPrinter and Daemon Separation
- Split the repository:
  - Create a new repo for core logic.
- Explore implementations:
  - Daemon listening to WebSocket for print commands.
  - REST API for protocol-agnostic, lightweight local use.
- Develop a simple API using Gin:
  - Prioritize performance and lightweight design.
- Avoid ticket constructors in Golang:
  - Use JSON for ticket data.
  - Translate JSON commands to Golang functions.
- Research:
  - JSON ticket representation tools (e.g., Parzibyte).
  - WebSocket and REST API communication feasibility.
- Microservices:
  - Split into at least two services: Printing and Daemon.
  - Evaluate gRPC for inter-service communication.
- Containers:
  - Assess containerization impact on connectors.

### Pending Development Tasks
- Investigate codepage issues:
  - Suspect printer issues.
  - Test with a disk reader (possible firmware update).
- Complete ESCPOS functions:
  - Integrate documented commands.
  - Separate responsibilities after removing base commands.
- Refactor:
  - Use Copilot for suggestions.
  - Review all TODOs and FIXMEs in the code.

## 13/08/2025 - 15/08/2025

## Pending TODOs and FIXMEs

- Review all TODOs and FIXMEs in the codebase.
  - Most of them are related to unfinished ESCPOS command implementations.
  - Many of them required specific types to validate inputs.
- I need a plan to test the entire commands without the need of a physical printer, maybe os.stdout io.writer could help.
- I have to reduce boilerplate code when using the final commands, a nice improvement could be a middleware approach to commands.
- Making sure every function have it's proper declaration related to being private or public.
- I worked on codebase fragmentation to improve modularity and separation of concerns. Then, the main core logic to print could be imported from the new repo, making it even more public.
- I keep reviewing the overall architecture since I didn't realize how different protocols were from each other. So, the same print command can work, but what about CutLabel, since ESCPOS don't have a direct equivalent?

## 18/08/2025 - 22/08/2025
- I was pretty stuck with a refactor; I need to separate each module type (ESCPOS, ZPL, etc.). I'm still looking for a faster, easier way to migrate to the new architecture.
- Implemented better barcode support.
- Learned more about channels and goroutines in Go.

- I researched and evaluated several options; the final decision is to make each protocol module a separate Go package, but keep them all in the same repository. Protocols behave very differently, so this approach should help manage their specificities. The plan is to create a registry to handle multiple printers and abstract the Point-of-Sale (POS) concept.

- Set up pull requests and issues in the pos-printer repository; these track the new architecture work.
- I should generate the necessary documentation for each protocol module.
- I need to move diary tasks into backlog items in the GitHub project — it's easy to lose track of what's missing.
- I need to review how GitHub is used for project management in production.

- Regarding the new architecture, I started with ESCPOS basic commands for text and formatting. These commands return byte slices and focus on validating input for printers. In a second layer I plan to implement more complex logic: auto-formatting to the active charset corresponding to the printer code page, and improved error handling with specific error types.

- Learning about stack, heap and garbage collection in Golang. Also migrating to Go 1.25.
- The new architecture is going well, for now i have visualized that i need 2 version of ESCPOS, Standard and Page Mode, which could be handled by the same codebase with different configurations. Page Mode commands will be ignored for now.
- Basic commands done:
  - Printing 

## Extra Notes
- [Video](https://youtu.be/bi5UxoEVX_E?si=HKV8f-eU13nYogV1) acerca del boot de Puppy Linux. Sirve hasta el minuto 3:45.
- Tutorial a formatear: [Enlace al tutorial](https://www.geekstogo.com/forum/topic/274691-use-puppy-linux-live-cd-to-recover-your-data/)
- Books to Look for:
  - The Art of Concurrency, O'Reilly.
- Words I heard today: Odoo, Endpoint, Business Logic, Kiosko, MVP, VPS, Hash/MD5/SHA256, clientes pesados, criptografía, paginación, Trello, procesamiento en db de prod, deslindarse inmediatamente, DNS, VMS, Podman y Containers, Exponential Backoff.