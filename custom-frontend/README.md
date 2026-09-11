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

## Upgrade rule

Never change only the runtime image tag. For each Paperless-ngx upgrade:

1. Update the tag and verified commit in `Dockerfile.vaultly`.
2. Recreate the patch against that exact upstream source.
3. Build the image and confirm the patch applies without errors.
4. Test login, document preview, upload, OCR, search, and branding surfaces.
5. Update `PROJECT_LOG.md`, commit, push, and then deploy on the VM.
