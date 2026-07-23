# Vaultly Project Log

## Current State

- **Built:** Initial repository foundation plus a version-pinned Paperless-ngx Docker Compose stack using PostgreSQL, Redis, Gotenberg, and Tika; Step 3 non-secret settings are selected for admin `Rasanga926`, timezone `Asia/Colombo`, and English/Sinhala/Tamil/Simplified Chinese OCR.
- **Pushed:** `origin/main` includes the Step 2 stack and the selected non-secret Step 3 deployment settings; no password or generated secret is stored in Git.
- **VM:** Phase 1 Step 6 is complete: `vaultly-ocr-test.png` uploaded and persisted, preview rendering works, OCR extracted all test text exactly, and full-text search returned the document. Vaultly's core document workflow is proven.
- **Next:** Commit and push the validated Step 7 branding and accumulated deployment log, then pull and apply the branding on the VM.

## History

### 2026-07-23 — Phase 1, Step 7: branding and Git state validated

- Parsed all four SVG assets successfully as valid XML.
- Reconstructed the missing local `.git` metadata, fetched the existing private `origin/main` history, and reattached local `main` without overwriting working files.
- Rebuilt the index and confirmed only `.gitignore`, the accumulated project log, and new branding files differ from `origin/main`; existing Compose, README, and environment-template content is unchanged.
- Reason: ensure the branding checkpoint is structurally valid, secrets-safe, and based on the existing repository history before commit and push.

### 2026-07-23 — Phase 1, Step 7: local credential file protected

- Detected an untracked root-level file named `ACCESS TOKENS & LOGIN CREDENTIALS.txt` while reconstructing Git metadata.
- Did not open or stage the file, and added its exact path to `.gitignore`.
- Reason: enforce the standing rule that access tokens and login credentials must never be committed or pushed.

### 2026-07-23 — Phase 1, Step 7: Vaultly SVG branding created

- Added a transparent primary wordmark using deep indigo `#4338CA` and teal `#14B8A6`, with a vault dial whose hands form the letter V.
- Added a simplified 32×32 SVG favicon designed for legibility at 16 px.
- Added single-color light-on-dark versions of both the wordmark and favicon, plus a concise branding asset guide.
- Reason: establish a scalable, repository-owned product identity before applying it in Paperless-ngx.

### 2026-07-23 — Phase 1, Step 6: search smoke test passed

- Searched for unique OCR-extracted text and confirmed Vaultly returned `vaultly-ocr-test`.
- The Phase 1 smoke test now verifies upload, persistent media storage, preview generation, OCR, indexing, and full-text retrieval end to end.
- Reason: prove the deployed DMS performs its core document-ingestion and discovery workflow successfully.

### 2026-07-23 — Phase 1, Step 6: OCR extraction verified

- Opened the ingested document's Content tab and confirmed OCR extracted `VAULTLY OCR SMOKE TEST`, `Silver Elephant 926`, and `Invoice Reference VLT-2026-0723` exactly.
- Upload, persistent media storage, preview generation, and English OCR are now verified.
- Full-text search indexing remains to be tested.
- Reason: distinguish successful text extraction from merely displaying the uploaded image.

### 2026-07-23 — Phase 1, Step 6: test document ingested

- Uploaded the non-sensitive image `vaultly-ocr-test.png` through the Windows browser.
- Vaultly created document `vaultly-ocr-test` and rendered its one-page preview correctly.
- OCR text extraction and search results still need separate verification.
- Reason: confirm browser upload, ingestion, persistent media storage, and preview generation before testing OCR/search.

### 2026-07-23 — Phase 1, Step 5: browser access and login verified

- Opened `http://192.168.56.105:8000` from the Windows host successfully.
- Logged in as administrator `Rasanga926` and reached the Paperless-ngx dashboard.
- The dashboard reports Paperless-ngx is running and currently contains zero documents.
- Reason: confirm end-to-end VM networking, web-service availability, and administrator authentication before document ingestion.

### 2026-07-23 — Phase 1, Step 5: VM access address identified

- Inspected the VM's IPv4 interfaces and identified `192.168.56.105/24` on `enp0s3` as the VirtualBox host-only address reachable from Windows.
- Identified `10.0.3.15/24` on `enp0s8` as the NAT-side address; Docker's `172.17.0.1` and `172.18.0.1` addresses are internal container networks.
- Reason: select the correct browser URL without changing the working VirtualBox network configuration.

### 2026-07-23 — Phase 1, Step 4: startup logs verified clean

- Paperless completed database migrations, created superuser `Rasanga926`, passed Django system checks, initialized its search index, and started Granian, Celery worker, Celery beat, and the consume-directory watcher.
- Confirmed Paperless-ngx `2.20.15` is listening on port `8000` and connected to Redis.
- PostgreSQL `18.4` completed its expected one-time initialization restart and reports ready to accept connections.
- Found no application traceback, fatal database error, or restart loop; Phase 1 Step 4 is complete.
- Reason: verify functional service initialization before exposing the login workflow to the user.

### 2026-07-23 — Phase 1, Step 4: Vaultly stack started

- Ran `docker compose up -d` successfully and pulled all five pinned images.
- Created the Vaultly network and persistent Redis, PostgreSQL, Paperless data, and media volumes.
- Started broker, database, Gotenberg, Tika, and webserver containers; `docker compose ps` shows all Up and the webserver healthy on `0.0.0.0:8000`.
- Startup logs still need review before Step 4 is marked clean.
- Reason: launch the complete document-management stack for the first time on the persistent VM.

### 2026-07-23 — Phase 1, Step 3: Compose validation passed

- Replaced the interpolation-affected administrator password with a 20-character value containing no dollar sign.
- Verified only its length, then reran `docker compose config --quiet` successfully with no warnings or errors.
- Phase 1 Step 3 is complete on the persistent replacement VM; no containers have been started.
- Reason: establish a complete, correctly parsed secret-bearing configuration before first startup.

### 2026-07-23 — Phase 1, Step 3: Compose exposed password interpolation issue

- Ran `docker compose config --quiet`; it returned repeated warnings about an unset variable rather than validating silently.
- Diagnosed an unescaped dollar sign in an `.env` secret, most likely the chosen administrator password, which Compose treats as variable interpolation and substitutes with blank text.
- No secret fragment was recorded and no containers were started.
- Reason: replace the affected credential before startup so the actual administrator password is passed intact.

### 2026-07-23 — Phase 1, Step 3: non-root Docker access verified

- Added `vboxuser` to the Docker group and rebooted the persistent clone to apply membership.
- Confirmed `groups` includes `docker` and non-root `docker ps` succeeds with an empty container list.
- Docker, clipboard autostart, repository, and VM state all survived the reboot.
- Reason: establish the intended routine Compose workflow without `sudo` before validating or starting Vaultly.

### 2026-07-23 — Phase 1, Step 3: restored Docker runtime verified

- Confirmed `docker.service` is active, Docker Engine reports `29.6.2`, and Compose reports `5.3.1`.
- Confirmed `vboxuser` currently belongs only to `vboxuser` and `sudo`, so non-root Docker socket access is not yet available.
- Reason: verify runtime health and identify the remaining access step before Compose validation.

### 2026-07-23 — Phase 1, Step 3: Docker stack restored persistently

- Installed Docker Engine and CLI `29.6.2`, containerd `2.2.6`, Buildx `0.35.0`, and Compose `5.3.1` on the persistent replacement VM.
- Installation completed without errors and enabled Docker, its socket, and containerd for system startup.
- Runtime health and non-root user access still need verification; no Vaultly containers are running.
- Reason: complete reconstruction of the missing container runtime on storage proven to survive restarts.

### 2026-07-23 — Phase 1, Step 3: Docker repository restored

- Restored Docker's official stable `resolute`/`amd64` APT source on the persistent VM.
- Refreshed APT successfully and downloaded Docker's signed package index without warnings or errors.
- Reason: make the official Docker Engine and Compose packages available for persistent installation.

### 2026-07-23 — Phase 1, Step 3: Docker signing key restored

- Restored Docker's official signing key at `/etc/apt/keyrings/docker.asc` and verified APT-readable permissions.
- Docker's stable source and packages still need restoration.
- Reason: authenticate packages before re-adding Docker's repository on the persistent VM.

### 2026-07-23 — Phase 1, Step 3: Docker prerequisites restored

- Confirmed `ca-certificates` is current and reinstalled `curl 8.18.0` successfully on persistent storage.
- Docker's signing key, APT source, and packages still need restoration.
- Reason: rebuild the trusted-download prerequisites for Docker's official installation method.

### 2026-07-23 — Phase 1, Step 3: Docker rebuild boundary verified

- Confirmed no `.env` assignment retains a `replace-with` placeholder.
- Confirmed `curl`, `/etc/apt/keyrings/docker.asc`, and `/etc/apt/sources.list.d/docker.sources` are absent in the replacement clone.
- Reason: resume the official Docker installation from its true starting point without assuming rolled-back system changes survived.

### 2026-07-23 — Phase 1, Step 3: persistent VM environment completed

- Securely set a new 16-character administrator password in the ignored VM-only `.env`.
- Verified only its length; the password was not displayed, shared, or recorded in Git.
- All required `.env` values are now populated, pending a final placeholder check and Compose validation.
- Reason: complete reconstruction of the secret-bearing configuration on verified persistent storage.

### 2026-07-23 — Phase 1, Step 3: VM-generated secrets restored

- Generated a new random 64-character PostgreSQL password and 96-character Paperless application secret directly on the persistent VM.
- Verified only their lengths; neither value was displayed, shared, or recorded in Git.
- The administrator password remains the final `.env` placeholder.
- Reason: replace credentials lost in the snapshot rollback with unique secrets stored only on persistent VM storage.

### 2026-07-23 — Phase 1, Step 3: non-secret environment settings restored

- Restored and verified port `8000`, UID/GID `1000`, administrator username `Rasanga926`, and timezone `Asia/Colombo`.
- Restored and verified OCR settings `eng+sin+tam+chi_sim` with additional packages `sin tam chi-sim`.
- Database, application, and administrator secret values remain placeholders.
- Reason: reconstruct known-safe deployment values before generating new credentials on persistent storage.

### 2026-07-23 — Phase 1, Step 3: environment template restored

- Copied `.env.example` to the ignored `~/vaultly/.env` on the persistent replacement VM without error.
- Reconfirmed the Ubuntu account UID and GID are both `1000`.
- All secret fields remain placeholders and no containers are running.
- Reason: rebuild the VM-only configuration safely after the snapshot rollback.

### 2026-07-23 — Phase 1, Step 3: repository restored on persistent VM

- Authenticated to GitHub and cloned the private `origin/main` repository successfully into persistent `~/vaultly`.
- Verified `.env.example`, `.git`, `.gitignore`, `PROJECT_LOG.md`, `README.md`, and `docker-compose.yml` are present.
- The real `.env` and Docker installation still need reconstruction; no secrets from the rolled-back VM will be reused.
- Reason: restore the Git-based deployment source after stabilizing the replacement VM.

### 2026-07-23 — Phase 1, Step 3: automatic clipboard startup verified

- Rebooted `Ubuntu-Vaultly`, logged in, waited for desktop startup, and confirmed host-to-guest paste worked without manually launching `VBoxClient`.
- The clone now has both persistent storage and reliable automatic clipboard integration.
- Reason: finish stabilizing the replacement VM before recreating repository, secrets, and Docker state.

### 2026-07-23 — Phase 1, Step 3: clipboard autostart configured

- Created `~/.config/autostart/vboxclient-clipboard.desktop` in `Ubuntu-Vaultly`.
- Configured it to launch `/usr/bin/VBoxClient --clipboard` three seconds after GNOME desktop login, allowing the XWayland session to initialize first.
- Verified the saved desktop-entry contents; reboot behavior still needs confirmation.
- Reason: make bidirectional clipboard reliable without a manual terminal command after every login.

### 2026-07-23 — Phase 1, Step 3: clipboard daemon startup issue identified

- After a clean restart, VirtualBox bidirectional clipboard was enabled but paste did not work.
- Manually started Guest Additions `VBoxClient --clipboard`; its log showed Guest Additions `7.2.6` in an XWayland session, and clipboard paste immediately worked.
- The current fix lasts only for the login session; automatic desktop startup still needs configuration.
- Reason: distinguish the VirtualBox permission setting from the guest-side clipboard process and prepare a persistent login-time fix.

### 2026-07-23 — Phase 1, Step 3: cloned VM persistence verified

- Created a marker file in `Ubuntu-Vaultly`, flushed it to disk, performed a clean shutdown, restarted the same clone, and confirmed the file survived.
- The clone now has verified persistent storage in addition to working clipboard and Git.
- The original `Ubuntu-Desktop` remains powered off as a fallback; no VM or snapshot has been deleted.
- Reason: establish a reliable storage foundation before recreating secrets, Docker, or future document data.

### 2026-07-23 — Phase 1, Step 3: cloned VM boot and clipboard verified

- Started `Ubuntu-Vaultly` successfully.
- Verified bidirectional host-to-guest terminal paste and confirmed Git `2.53.0` is installed.
- Shutdown persistence is the remaining clone-safety check before deployment reconstruction.
- Reason: confirm the full clone retained the working Guest Additions/clipboard setup and Git prerequisite.

### 2026-07-23 — Phase 1, Step 3: independent VM clone created

- Created `Ubuntu-Vaultly` as a full clone of the working clipboard/Git state with new network-adapter MAC addresses.
- The clone shows only Current State, eliminating the old snapshot tree as a source of accidental rollback.
- Preserved the original `Ubuntu-Desktop` VM powered off as a fallback; nothing was deleted.
- The new clone still requires clipboard and disk-persistence verification before deployment is reconstructed.
- Reason: isolate Vaultly on an independent virtual disk while retaining the difficult-to-reproduce Guest Additions/clipboard configuration.

### 2026-07-23 — Phase 1, Step 3: VirtualBox snapshot rollback identified

- Verified the attached virtual disk is a normal dynamically allocated VDI, not an immutable medium.
- Inspected the snapshot tree: `Clean State` → `After Clipboard and Git Installed` → `Current State (changed)`.
- The restored VM contents align with the four-day-old `After Clipboard and Git Installed` snapshot, explaining why Git survived while all later work disappeared.
- No snapshots were modified or deleted.
- Reason: establish that named snapshots are historical checkpoints and that new work must remain in `Current State` rather than restoring an older checkpoint.

### 2026-07-23 — Phase 1, Step 3: VM persistence test failed

- Created a harmless marker file, flushed filesystem writes, and shut Ubuntu down cleanly.
- After a normal VM start, the marker file was absent, proving that changes are reverted across power cycles.
- Deployment remains paused because secrets, containers, and future documents would be lost on every restart in this state.
- Reason: require reliable persistent storage before repeating the repository clone, `.env` creation, or Docker installation.

### 2026-07-23 — Phase 1, Step 3: restored snapshot state identified

- Verified the current root filesystem is writable `ext4` on `/dev/sda2`; the VM is not running from Ubuntu live media.
- Verified Git `2.53.0` remains installed, while `~/vaultly` does not exist and Docker is not installed.
- The boundary of surviving changes strongly indicates an older VirtualBox snapshot was restored after the crash.
- The VM must pass a simple clean-shutdown persistence test before secrets or deployment setup are repeated.
- Reason: distinguish a one-time snapshot rollback from an immutable/non-persistent disk before recreating work.

### 2026-07-23 — Phase 1, Step 3: VM persistence failure reported

- After manually restarting the VM, the user reported that changes made during the session no longer appear.
- Potential causes include booting an Ubuntu live image, automatic snapshot restoration, an immutable VirtualBox disk, or starting a different VM/disk; the cause is not yet established.
- Deployment work is paused to avoid repeating Git/Docker setup and secret creation on storage that may be discarded again.
- No Vaultly containers were ever started.
- Reason: treat persistent storage as a hard prerequisite before reconstructing the VM deployment.

### 2026-07-23 — Phase 1, Step 3: VM restarted after VirtualBox error

- The Ubuntu VM encountered an unspecified VirtualBox error during the requested reboot and was started again manually.
- No Vaultly containers were running at the time, so no application or document workload was interrupted.
- Post-restart Docker health and group membership still need verification before deployment continues.
- Reason: record the unexpected VM event and pause further changes until the current boot is checked.

### 2026-07-23 — Phase 1, Step 3: Docker group membership assigned

- Added `vboxuser` to the privileged `docker` group for the planned non-root Compose workflow.
- The `newgrp` utility is not installed, so the existing desktop login cannot refresh its group membership in place; a reboot or full logout/login is required.
- No Vaultly containers are running.
- Reason: enable routine Docker commands without `sudo` while avoiding an unnecessary package installation solely to refresh the current shell.

### 2026-07-23 — Phase 1, Step 3: Docker runtime verified

- Confirmed `docker.service` is active.
- Confirmed the Docker CLI reports Engine `29.6.2` and the Compose plugin reports `5.3.1`.
- Non-root access for `vboxuser` still needs configuration; no test or Vaultly containers have been started.
- Reason: verify the daemon and command-line components before granting user access or running workloads.

### 2026-07-23 — Phase 1, Step 3: official Docker stack installed

- Installed Docker Engine and CLI `29.6.2`, containerd `2.2.6`, Buildx `0.35.0`, and Docker Compose plugin `5.3.1` from Docker's official stable Ubuntu repository.
- The packages enabled `docker.service`, `docker.socket`, and `containerd.service` for system startup without installation errors.
- Docker runtime health and non-root access still need verification; no Vaultly containers are running.
- Reason: restore the missing VM prerequisite using the official supported package channel and record the exact installed versions.

### 2026-07-23 — Phase 1, Step 3: Docker repository verified

- Refreshed APT successfully and downloaded the signed `amd64` package index from Docker's official stable `resolute` repository without warnings or errors.
- Docker packages are now available for installation; Docker Engine itself is not installed yet.
- Reason: confirm repository compatibility and trust before making the system-level Docker installation.

### 2026-07-23 — Phase 1, Step 3: Docker APT source registered

- Added Docker's official stable Ubuntu APT source using the VM-detected codename `resolute` and architecture `amd64`.
- Verified the source references Docker's installed signing key; repository availability for this Ubuntu release still needs confirmation through `apt update`.
- Reason: configure the official package channel before installing Docker Engine and Compose.

### 2026-07-23 — Phase 1, Step 3: Docker signing key installed

- Downloaded Docker's official Ubuntu repository signing key to `/etc/apt/keyrings/docker.asc`.
- Verified the key file exists and is world-readable for APT; Docker Engine itself is not installed yet.
- Reason: allow Ubuntu to authenticate packages obtained from Docker's official repository.

### 2026-07-23 — Phase 1, Step 3: Docker installation prerequisites prepared

- Updated Ubuntu's package information, confirmed `ca-certificates` was already current, and installed `curl 8.18.0`.
- Docker Engine itself is not installed yet and no containers are running.
- Reason: prepare the trusted-download tools required by Docker's official Ubuntu APT-repository installation method.

### 2026-07-23 — Phase 1, Step 3: Docker prerequisite missing on VM

- Confirmed that no `.env` assignment still uses a `replace-with` placeholder.
- Attempted `docker compose config --quiet`, but Ubuntu reported `docker: command not found`.
- Verified that `command -v docker` returns nothing and no `docker*` or `containerd*` Debian packages are installed, so this is a missing prerequisite rather than a PATH or package-conflict problem.
- No Compose validation or container startup occurred.
- Reason: pause deployment and inspect the supposedly preinstalled Docker prerequisite rather than selecting an Ubuntu-suggested replacement without verification.

### 2026-07-23 — Phase 1, Step 3: admin password strengthened

- Replaced the insufficient 9-character administrator password with a 16-character password in the ignored VM-only `.env`.
- Verified only its length; the password was not displayed, shared, or recorded in Git.
- The VM environment file now has values for all required settings and secrets, pending Compose validation.
- Reason: meet the minimum credential requirement before validating or starting the deployment.

### 2026-07-23 — Phase 1, Step 3: admin password requires replacement

- Inserted the chosen administrator password into the ignored VM-only `.env` without displaying or recording its value.
- Length-only verification reported 9 characters, below the required 16-character minimum, so deployment validation and startup remain paused.
- Reason: correct the weak credential before Vaultly is exposed on the VM network.

### 2026-07-23 — Phase 1, Step 3: Paperless application secret generated

- Generated a random 96-character Paperless application secret directly on the VM and inserted it into the ignored `.env`.
- Verified only its presence and length; the secret was not displayed, shared, or recorded in Git.
- Reason: protect Vaultly's sessions and other security-sensitive application data with a unique VM-only key.

### 2026-07-23 — Phase 1, Step 3: database password generated

- Generated a random 64-character PostgreSQL password directly on the VM and inserted it into the ignored `.env`.
- Verified only its presence and length; the password was not displayed, shared, or recorded in Git.
- Reason: secure the database with a unique VM-only credential.

### 2026-07-23 — Phase 1, Step 3: non-secret VM settings configured

- Set and verified port `8000`, UID/GID `1000`, administrator username `Rasanga926`, and timezone `Asia/Colombo` in the ignored VM-only `.env`.
- Set and verified OCR for English, Sinhala, Tamil, and Simplified Chinese using `eng+sin+tam+chi_sim` and additional packages `sin tam chi-sim`.
- The database password, Paperless secret key, and administrator password remain placeholders; no secret was displayed or recorded.
- Reason: verify all safe deployment values separately before generating VM-only credentials.

### 2026-07-23 — Phase 1, Step 3: VM environment file created

- Copied `.env.example` to the Git-ignored `~/vaultly/.env` on the Ubuntu VM without errors.
- Confirmed the Ubuntu account's UID and GID are both `1000`; these values still need to be placed in `.env`.
- No secret values were recorded in Git or the project log, and no containers are running.
- Reason: prepare the VM-only configuration location and verify filesystem ownership mapping before adding deployment settings.

### 2026-07-23 — Phase 1, Step 3: private repository cloned on Ubuntu VM

- Authenticated to GitHub using a repository-scoped personal access token and cloned `origin/main` successfully into `~/vaultly`.
- Verified that `.env.example`, `.git`, `.gitignore`, `PROJECT_LOG.md`, `README.md`, and `docker-compose.yml` are present on the VM.
- The real `.env` has not been created and no containers are running yet.
- Reason: establish the Git-based transfer path before creating VM-only secrets or starting services.

### 2026-07-23 — Phase 1, Step 3: Git installed on Ubuntu VM

- Installed Git `2.53.0` successfully on the Ubuntu VM.
- Enabled bidirectional VirtualBox shared clipboard and verified terminal paste using `Ctrl+Shift+V`.
- Confirmed that cloning the private repository with the GitHub account password fails because GitHub does not support password authentication for Git operations.
- No Vaultly files have been cloned and no services are running yet.
- Reason: record the verified VM prerequisite and the private-repository authentication blocker before choosing a secure authentication method.

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
