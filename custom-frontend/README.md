# Vaultly custom frontend

Vaultly uses the complete Paperless-ngx application and replaces only its
compiled browser frontend. `Dockerfile.vaultly` clones tag `v2.20.15`, verifies
the exact upstream commit, applies `vaultly-2.20.15.patch`, and copies the
compiled result into the official `2.20.15` runtime image.

The patch removes the hard-coded navigation feather and “by Paperless-ngx”
bylines, changes the browser, login, and installable-app identity to Vaultly,
and serves the Vaultly SVG favicon. The image copies the patched frontend plus
the narrowly changed Django templates and favicon view into the official
runtime. It also hides the Application Logo and Application Title controls,
which removes the now-empty General Settings tab while preserving OCR and
Barcode configuration. Global documentation menu entries and shared
page-header help links are hidden, and the application plus login screen use
Vaultly indigo `#4338CA` as their primary theme color. It does not remove or
alter the upstream GPL license, copyright notices, source labels, or bundled
project documentation.

## Upgrade rule

Never change only the runtime image tag. For each Paperless-ngx upgrade:

1. Update the tag and verified commit in `Dockerfile.vaultly`.
2. Recreate the patch against that exact upstream source.
3. Build the image and confirm the patch applies without errors.
4. Test login, document preview, upload, OCR, search, and branding surfaces.
5. Update `PROJECT_LOG.md`, commit, push, and then deploy on the VM.
