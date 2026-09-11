# Vaultly branding

The product is **Vaultly by PBSS**. Vaultly is the primary identity; PBSS is a
secondary attribution mark that appears only where there is room for it.

## Generating the assets

Every SVG here is produced by `build-branding.py`. Edit the script, never the
SVGs — hand edits are overwritten on the next run.

```
pip install fonttools
python branding/build-branding.py
```

The Inter variable font is downloaded to `branding/.cache/` on first run and is
Git-ignored.

## The mark

A teal V, shaped like a vault-dial pointer, inside an indigo dial ring cut by
four index notches. The whole mark is defined once in a 64-unit box and scaled
everywhere else, so the favicon and the logo are the same drawing.

The notches are a stroke dash pattern rather than separate tick shapes. They
read as dial machining at display sizes and close up optically below about
24 px, so the mark simplifies to a clean ring instead of breaking into
fragments in a browser tab.

## The wordmark

Inter, instanced at `wght 650` / `opsz 32`, tracked −1.2%, emitted as outlined
vector paths.

Outlining is deliberate, not decorative. The logo is served to browsers through
an `<img>` tag, so a live SVG `<text>` element resolves fonts on the *viewer's*
machine — the same file would render in Inter, Segoe UI, or Arial depending on
who opened it. Outlines remove the dependency entirely.

Inter is licensed under the SIL Open Font License 1.1, which permits embedding
and derived outlines.

## Palette

| Colour | Hex | Role |
| --- | --- | --- |
| Indigo | `#4338CA` | Brand core; also the application's UI primary |
| Indigo light / deep | `#4F46E5` / `#3730A3` | Dial ring gradient |
| Teal | `#14B8A6` | Brand secondary |
| Teal light / deep | `#2DD4BF` / `#0D9488` | V gradient |
| Slate | `#64748B` | Byline on light backgrounds |
| PBSS blue | `#005D9B` | Partner mark only — never applied to Vaultly elements |

## Asset index

| File | Contents | Use on |
| --- | --- | --- |
| `vaultly-logo.svg` | Mark + wordmark | Light surfaces |
| `vaultly-logo-dark.svg` | Mark + wordmark, single colour | Dark surfaces |
| `vaultly-lockup-full.svg` | + `BY PBSS` superscript + PBSS badge | Light surfaces |
| `vaultly-lockup-full-dark.svg` | as above, single colour | Indigo and dark surfaces |
| `vaultly-lockup-compact.svg` | Mark + wordmark, no PBSS | Light surfaces |
| `vaultly-lockup-compact-dark.svg` | Mark + wordmark, no PBSS | Dark surfaces |
| `vaultly-mark.svg` | Mark alone | Nav badge, app icon |
| `vaultly-mark-dark.svg` | Mark alone, single colour | Nav badge on dark |
| `vaultly-favicon.svg` | Mark, optically boosted ×1.10 | Browser tab, manifest |
| `vaultly-favicon-dark.svg` | Mark, optically boosted, single colour | Browser tab on dark |

`vaultly-lockup-compact.svg` is byte-identical to `vaultly-logo.svg` by design.
`vaultly-logo.svg` is the filename already wired into `docker-compose.yml` and
`PAPERLESS_APP_LOGO`; `vaultly-lockup-compact.svg` is the named variant for use
alongside `vaultly-lockup-full.svg`.

## The PBSS badge

| File | Variant | Use on |
| --- | --- | --- |
| `pbss-badge-white.png` | Plain white disc, transparent exterior | Indigo, dark, and photographic surfaces |
| `pbss-badge-white-ring.png` | Same disc with a grey rim | White and light surfaces, where the plain disc would disappear |
| `pbss-logo-original-square.png` | Unprocessed source | Reference only — not used in the product |

Use these files as supplied. Do not recolour, re-cut, or restore a background.

**Resolution ceiling.** Both badges are 200 × 200 px rasters. They are placed at
44 px in the lockups — a 4.5× downscale, so they stay sharp. **Nothing may place
the badge above ~96 px.** A surface that needs it larger needs a vector PBSS
file first; scaling the raster up will visibly degrade.

On any surface whose background changes with the viewer's theme, prefer the
ringed variant: the rim gives the disc definition on light backgrounds and stays
unobtrusive on dark ones.

## Deployment

`docker-compose.yml` mounts the login logo and the favicon read-only into the
static root that Paperless serves. `PAPERLESS_APP_LOGO` selects the mounted
file, so branding changes do not require rebuilding the container image.

The PBSS badge is embedded in the lockup SVGs as a base64 data URI rather than
referenced as a separate file. This is required, not a convenience: an SVG
loaded through an `<img>` tag cannot fetch external images, and
`PAPERLESS_APP_LOGO` points at a single static file.
