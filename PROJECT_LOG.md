# Vaultly Project Log

## Current State

- **Built:** Initial repository foundation plus a version-pinned Paperless-ngx Docker Compose stack using PostgreSQL, Redis, Gotenberg, and Tika; Step 3 non-secret settings are selected for admin `Rasanga926`, timezone `Asia/Colombo`, and English/Sinhala/Tamil/Simplified Chinese OCR.
- **Pushed:** `origin/main` includes the Step 2 stack and the selected non-secret Step 3 deployment settings; no password or generated secret is stored in Git.
- **VM:** Nothing deployed or running yet.
- **Next:** Run the provided Step 3 commands on the Ubuntu VM, then report the Git clone and `docker compose config --quiet` results before starting the stack.

## History

### 2026-07-18 — Phase 1, Step 3: deployment settings selected

- Selected initial administrator username `Rasanga926` and timezone `Asia/Colombo`.
- Selected multilingual OCR using `eng+sin+tam+chi_sim`, with additional container language packages `sin tam chi-sim` for Sinhala, Tamil, and Simplified Chinese; English is bundled by default.
- Kept the administrator password, database password, and Paperless secret out of the log and repository; they will be entered or generated only on the VM.
- Reason: prepare exact, secrets-safe VM commands without guessing user-specific settings.

### 2026-07-18 — Phase 1, Step 2: Compose stack committed and pushed

- Static checks confirmed all five services are defined, every Compose interpolation variable exists in `.env.example`, no image uses a floating `latest` tag, and all secret fields contain placeholders.
- Docker is not installed on the Windows development machine, so runtime Compose validation is deferred to the Ubuntu VM before startup.
- Created and pushed commit `cad0281` (`feat: add Paperless Docker Compose stack`) to `origin/main`.
- Reason: publish a reviewed deployment definition for the Git-based transfer workflow and leave the project ready for VM configuration.

### 2026-07-18 — Phase 1, Step 2: Compose stack prepared

- Added `docker-compose.yml`, adapted from the current official Paperless-ngx PostgreSQL + Tika template.
- Configured Paperless-ngx `2.20.15`, PostgreSQL `18.4`, Redis `8.8.0`, Gotenberg `8.25`, and Apache Tika `3.2.3.0` as five cooperating services.
- Routed database credentials, the application secret, initial admin credentials, timezone, OCR language, user mapping, and host port through the ignored `.env` file.
- Expanded `.env.example` with every deployment value required by this Compose stack, using placeholders for all secrets and user-specific values, plus an optional field for installing non-default OCR language packs.
- Documented what each container does in `README.md`.
- Reason: create a reproducible, secrets-safe deployment definition that can be transferred to the Ubuntu VM through GitHub.

### 2026-07-18 — Phase 1, Step 1: first GitHub push completed

- Pushed local `main` to `https://github.com/RaZa-97/Vaultly-DMS.git` and configured it to track `origin/main`.
- Confirmed GitHub accepted commits `638c755` and `683d438`.
- Reason: establish GitHub as the transfer point between Windows development and the Ubuntu VM deployment.

### 2026-07-18 — Phase 1, Step 1: initial commit created

- Created commit `638c755` (`chore: initialize Vaultly project`) after confirming the environment template contains placeholders only and the ignore rules protect `.env` and runtime data.
- Reason: preserve the reviewed project foundation as an auditable checkpoint before publishing it to the private GitHub repository.

### 2026-07-18 — Phase 1, Step 1: initial project files

- Added the Vaultly README and established this log as the project source of truth.
- Added ignore rules for secrets, Paperless-ngx runtime data, backups, editor files, and operating-system clutter.
- Added a placeholder-only `.env.example`; the real `.env` will exist only on the Ubuntu VM.
- Initialized Git on the `main` branch, configured the repository-local commit identity, and connected `origin` to `https://github.com/RaZa-97/Vaultly-DMS.git`.
- Reason: establish a safe, documented foundation before the first GitHub push.
