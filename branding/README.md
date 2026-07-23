# Vaultly branding

- `vaultly-logo.svg`: primary transparent-background wordmark using deep indigo `#4338CA` and teal `#14B8A6`.
- `vaultly-favicon.svg`: simplified square mark designed to remain legible at 16 px.
- `vaultly-logo-dark.svg`: single-color `#F8FAFC` wordmark for dark backgrounds.
- `vaultly-favicon-dark.svg`: single-color favicon for dark backgrounds.

The circular dial, four index marks, and central hub evoke a vault mechanism. The dial's hands form the letter **V**.

`docker-compose.yml` mounts this directory read-only at Paperless's `/media/logo`
directory. The supported `PAPERLESS_APP_LOGO=/logo/vaultly-logo.svg` setting
selects the primary wordmark without modifying the container image.
