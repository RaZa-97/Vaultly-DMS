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
Barcode configuration. The application plus login screen use Vaultly indigo
`#4338CA` as their primary theme color.

Revision `frontend5` supplies a built-in Vaultly User Guide, points global and
contextual help destinations to matching sections in that guide, and removes
the public tour and upstream version/update footer. Administrator-only health
and diagnostic controls remain available. The customization does not remove
or alter upstream GPL license, copyright, or source notices.

Revision `frontend6` also applies the Vaultly name to the Django administration
header, browser title, and dashboard heading without changing its behavior,
models, or permissions.

Revision `frontend7` expands the bundled Vaultly documentation into a detailed
22-section user and administrator manual and includes a matching downloadable
PDF generated from the same source.

Revision `frontend8` applies the *Vaultly by PBSS* identity. The sidebar brand
regains a mark — the Vaultly vault dial, drawn with the ring in `currentColor`
so it stays legible against either sidebar theme while the V keeps the brand
teal — and reuses the upstream byline slot for `by PBSS`. The application
loading screen, which had still shown the Paperless-ngx leaf and "Paperless-ngx
is loading...", now shows the Vaultly mark and wording. The Django
administration header and index title carry the full `Vaultly by PBSS` name;
the browser title stays `Vaultly Admin`, where the shorter form fits better.

`frontend8` also corrects the Angular primary colour. It had been set to
`hsl(245, 65%, 51%)`, which is `#3E31D3` — close to, but not, the brand indigo.
It is now `hsl(245, 58%, 51%)`, which resolves to `#4338CA`, so the interface
and the logo use the same colour.

Revision `frontend9` removes the remaining user-facing `Paperless-ngx` product
names. The trigger was the upload toast — "Document ... was added to
Paperless-ngx." — but a sweep of the pinned source found 31 strings in total,
including several that are not visible in the browser at all:

- Upload and processing toasts, and the drag-and-drop hint.
- The configuration, personal-settings, system-status, workflows and mail-rule
  screens.
- `environment.appTitle`, the fallback used before the server's `APP_TITLE`
  setting loads.
- Every account page title: sign up, the four password-reset stages, MFA,
  social-account sign in and sign up, and account inactive.
- The transactional email body, and `EMAIL_SUBJECT_PREFIX` /
  `ACCOUNT_EMAIL_SUBJECT_PREFIX`, which set the subject line on messages the
  server sends.
- `MFA_TOTP_ISSUER`, which is the name shown beside the account in a user's
  authenticator app. It is display-only in the `otpauth` URI, so existing
  enrolments keep working.
- The API schema title and the version and system-status endpoint descriptions.

`frontend9` also fixes a packaging gap this exposed. Thirteen of the changed
backend files were never copied into the runtime image, so those edits would
have been applied to the source and then silently dropped at build time. The
Dockerfile now copies the whole `src/documents/templates/` tree instead of
three individual templates, plus `settings.py`, `serialisers.py` and
`documents/views.py`.

Deliberately left alone: `name="author"` meta tags, the GitHub and
docs.paperless-ngx.com links, licence and copyright notices, internal
identifiers such as `PaperlessTask` and `PaperlessConfig`, logger names, log
lines, temp-file prefixes and template paths. Two strings in the update-check
footer also keep the upstream name because the existing patch marks that block
`d-none`, so it never renders.

The patch is now generated mechanically with `git diff` against the pinned
source rather than hand-maintained, and covers 41 files.

## Upgrade rule

Never change only the runtime image tag. For each Paperless-ngx upgrade:

1. Update the tag and verified commit in `Dockerfile.vaultly`.
2. Recreate the patch against that exact upstream source.
3. Build the image and confirm the patch applies without errors.
4. Test login, document preview, upload, OCR, search, and branding surfaces.
5. Update `PROJECT_LOG.md`, commit, push, and then deploy on the VM.
