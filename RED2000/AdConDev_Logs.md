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
- I was pretty stucked with a refactoring, i have to separate each module type(ESCPOS, Zpl, etc.). I still looking for  faster and easier way to migrate to a new architecture.
- Implemented better barcode support.
- Learned about channels and goroutines in Go.

- I did research a checked some options and the last decition is to make each protocol module a separate go package, but all in one. Protocols behave very differently, so this approach should help in managing their specificities. All of them will be contained within the same repository. Finally, the idea is to create a registry that can handle many printers abstracting the idea of a Point-of-Sale (POS) system.

- Set up pull request and issues in pos-printer repository. All is about the new architecture.
- I should generate the necessary documentation for each protocol module.
- I need to dump the tasks from my diary to backlog items in the github project. It easy to get lost on what is missing.
- I need to check how is github used for project management in a production environment.
- About the new architecture i have started with the ESCPOS basic commands for text and formatting. Those commands only return byte slices and they are concerned to validate input to printers. In the second layer, I plan to implement more complex logic, such autoformatting to active charset corresponding to the Cope Page in printer. Also, better error handling with specific error types.


## Extra Notes
- [Video](https://youtu.be/bi5UxoEVX_E?si=HKV8f-eU13nYogV1) acerca del boot de Puppy Linux. Sirve hasta el minuto 3:45.
- Tutorial a formatear: [Enlace al tutorial](https://www.geekstogo.com/forum/topic/274691-use-puppy-linux-live-cd-to-recover-your-data/)
- Books to Look for:
  - The Art of Concurrency, O'Reilly.
- Words I heard today: Odoo, Endpoint, Business Logic, Kiosko, MVP, VPS, Hash/MD5/SHA256, clientes pesados, criptografía, paginación, Trello, contratos de datos y joins en db.