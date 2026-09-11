# Vaultly by PBSS

Vaultly is a self-hosted document management system for small businesses, based on [Paperless-ngx](https://docs.paperless-ngx.com/), delivered in partnership with PBSS.

Surfaces with room carry the full name, **Vaultly by PBSS**. Where space is tight — the browser tab, the sidebar brand slot, `PAPERLESS_APP_TITLE` — the product is **Vaultly** alone. See [`branding/README.md`](branding/README.md) for the asset set and the rules for placing the PBSS badge.

## Project status

Phase 1 is in progress: the local project and Docker Compose stack are being prepared for deployment to an Ubuntu VM through GitHub.

## Docker services

- **Webserver:** the Paperless-ngx application, background workers, OCR pipeline, search, and browser interface.
- **PostgreSQL (`db`):** durable structured storage for users, document metadata, tags, and application state.
- **Redis (`broker`):** the queue used to coordinate background work such as document consumption and scheduled tasks.
- **Gotenberg:** converts Office documents and email content to PDF before Paperless processes them.
- **Tika:** detects and extracts text and metadata from Office documents and email files.

The stack is defined in `docker-compose.yml`. Deployment-specific values belong in an ignored `.env` file created from `.env.example` on the VM.

## Security

Real environment files and runtime data must never be committed. Copy `.env.example` to `.env` only on the deployment machine and replace every placeholder there.
