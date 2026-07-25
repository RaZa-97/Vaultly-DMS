# Vaultly custom frontend

Vaultly uses the complete Paperless-ngx application and replaces only its
compiled browser frontend. `Dockerfile.vaultly` clones tag `v2.20.15`, verifies
the exact upstream commit, applies `vaultly-2.20.15.patch`, and copies the
compiled result into the official `2.20.15` runtime image.

The patch removes the hard-coded navigation feather and “by Paperless-ngx”
byline, changes the browser and installable-app identity to Vaultly, and uses
the Vaultly SVG favicon. It does not remove or alter the upstream GPL license,
copyright notices, source labels, or project documentation.

## Upgrade rule

Never change only the runtime image tag. For each Paperless-ngx upgrade:

1. Update the tag and verified commit in `Dockerfile.vaultly`.
2. Recreate the patch against that exact upstream source.
3. Build the image and confirm the patch applies without errors.
4. Test login, document preview, upload, OCR, search, and branding surfaces.
5. Update `PROJECT_LOG.md`, commit, push, and then deploy on the VM.

