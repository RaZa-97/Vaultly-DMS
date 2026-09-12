"""Replace the remaining user-facing Paperless-ngx product names with Vaultly.

Run against a checkout that already has the existing Vaultly patch applied.
Upstream attribution that is not shown as product naming - author meta tags,
GitHub links, licence notices, template paths, log lines and temp-file
prefixes - is deliberately left alone.
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])

# (path, old, new) - every replacement must match exactly once.
EDITS = [
    # ---------------------------------------------------- upload/consume toasts
    ("src-ui/src/app/app.component.ts",
     "Document ${status.filename} was added to Paperless-ngx.",
     "Document ${status.filename} was added to Vaultly."),
    ("src-ui/src/app/app.component.ts",
     "Document ${status.filename} is being processed by Paperless-ngx.",
     "Document ${status.filename} is being processed by Vaultly."),
    ("src-ui/src/app/app.component.ts",
     "Once you do, Paperless-ngx will start training its machine learning algorithms.",
     "Once you do, Vaultly will start training its machine learning algorithms."),
    ("src-ui/src/app/app.component.ts",
     "Lastly, on behalf of every contributor to this community-supported project, thank you for using Paperless-ngx!",
     "Lastly, thank you for using Vaultly!"),

    # ------------------------------------------------------------- admin screens
    ("src-ui/src/app/components/admin/config/config.component.html",
     "every</strong> user of this install of Paperless-ngx.",
     "every</strong> user of this install of Vaultly."),
    ("src-ui/src/app/components/admin/settings/settings.component.html",
     "Only applies to the Paperless-ngx PDF viewer.",
     "Only applies to the Vaultly PDF viewer."),
    ("src-ui/src/app/components/common/system-status-dialog/system-status-dialog.component.html",
     "<dt i18n>Paperless-ngx Version</dt>",
     "<dt i18n>Vaultly Version</dt>"),
    ("src-ui/src/app/components/manage/workflows/workflows.component.html",
     "customize the behavior of Paperless-ngx when events",
     "customize the behavior of Vaultly when events"),
    ("src-ui/src/app/components/common/edit-dialog/mail-rule-edit-dialog/mail-rule-edit-dialog.component.html",
     "Paperless will only process mails that match",
     "Vaultly will only process mails that match"),

    # --------- fallback app title, used until the server's APP_TITLE setting loads
    ("src-ui/src/environments/environment.ts",
     "appTitle: 'Paperless-ngx',",
     "appTitle: 'Vaultly',"),
    ("src-ui/src/environments/environment.prod.ts",
     "appTitle: 'Paperless-ngx',",
     "appTitle: 'Vaultly',"),

    # ------------------------------------------------- account page head titles
    ("src/documents/templates/account/account_inactive.html",
     '{% trans "Paperless-ngx account inactive" %}',
     '{% trans "Vaultly account inactive" %}'),
    ("src/documents/templates/account/signup.html",
     '{% trans "Paperless-ngx sign up" %}',
     '{% trans "Vaultly sign up" %}'),
    ("src/documents/templates/account/password_reset.html",
     '{% trans "Paperless-ngx reset password request" %}',
     '{% trans "Vaultly reset password request" %}'),
    ("src/documents/templates/account/password_reset_done.html",
     '{% trans "Paperless-ngx reset password sent" %}',
     '{% trans "Vaultly reset password sent" %}'),
    ("src/documents/templates/account/password_reset_from_key.html",
     '{% trans "Paperless-ngx reset password confirmation" %}',
     '{% trans "Vaultly reset password confirmation" %}'),
    ("src/documents/templates/account/password_reset_from_key_done.html",
     '{% trans "Paperless-ngx reset password complete" %}',
     '{% trans "Vaultly reset password complete" %}'),
    ("src/documents/templates/mfa/authenticate.html",
     '{% trans "Paperless-ngx Two-Factor Authentication" %}',
     '{% trans "Vaultly Two-Factor Authentication" %}'),
    ("src/documents/templates/socialaccount/authentication_error.html",
     '{% trans "Paperless-ngx social account sign in" %}',
     '{% trans "Vaultly social account sign in" %}'),
    ("src/documents/templates/socialaccount/login.html",
     '{% trans "Paperless-ngx social account sign in" %}',
     '{% trans "Vaultly social account sign in" %}'),
    ("src/documents/templates/socialaccount/signup.html",
     '{% trans "Paperless-ngx social account sign up" %}',
     '{% trans "Vaultly social account sign up" %}'),

    # ------------------------------- transactional email (password reset, etc.)
    ("src/documents/templates/account/email/base_message.txt",
     '{% blocktrans with site_name="Paperless-ngx" %}Hello from {{ site_name }}!{% endblocktrans %}',
     '{% blocktrans with site_name="Vaultly" %}Hello from {{ site_name }}!{% endblocktrans %}'),
    ("src/documents/templates/account/email/base_message.txt",
     '{% blocktrans with site_name="Paperless-ngx" site_domain=settings.domain %}',
     '{% blocktrans with site_name="Vaultly" site_domain=settings.domain %}'),

    # --------------------------------------------------- API surface and schema
    ("src/documents/serialisers.py",
     'label="Documents are from Paperless-ngx WebUI"',
     'label="Documents are from the Vaultly web interface"'),
    ("src/paperless/settings.py",
     '"TITLE": "Paperless-ngx REST API",',
     '"TITLE": "Vaultly REST API",'),
    ("src/paperless/settings.py",
     '"DESCRIPTION": "OpenAPI Spec for Paperless-ngx",',
     '"DESCRIPTION": "OpenAPI Spec for Vaultly",'),
    ("src/documents/views.py",
     'description="Get the current version of the Paperless-NGX server",',
     'description="Get the current version of the Vaultly server",'),
    ("src/documents/views.py",
     'description="Get the current system status of the Paperless-NGX server",',
     'description="Get the current system status of the Vaultly server",'),

    # ------------------------------------------- email subjects and 2FA issuer
    # Subject prefix on every message the server sends, including password
    # resets and share notifications.
    ("src/paperless/settings.py",
     'EMAIL_SUBJECT_PREFIX: Final[str] = "[Paperless-ngx] "',
     'EMAIL_SUBJECT_PREFIX: Final[str] = "[Vaultly] "'),
    ("src/paperless/settings.py",
     'ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Paperless-ngx] "',
     'ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Vaultly] "'),
    # The issuer shown next to the account in the user's authenticator app.
    # Display-only in the otpauth URI, so existing enrolments keep working.
    ("src/paperless/settings.py",
     'MFA_TOTP_ISSUER = "Paperless-ngx"',
     'MFA_TOTP_ISSUER = "Vaultly"'),
]

failures = []
applied = already = 0
for rel, old, new in EDITS:
    path = ROOT / rel
    if not path.exists():
        failures.append("missing file: %s" % rel)
        continue
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count:
        path.write_text(text.replace(old, new), encoding="utf-8")
        applied += count
        print("  applied  %s: %s" % (rel.split("/")[-1], new[:46]))
    elif new in text:
        already += 1
    else:
        failures.append(
            "neither the old nor the new string is in %s\n      old: %r" % (rel, old)
        )

print("\n%d replacement(s) applied, %d already in place" % (applied, already))
if failures:
    print(
        "\n%d entr(ies) need attention - upstream probably reworded them:"
        % len(failures)
    )
    for f in failures:
        print("  - " + f)
    sys.exit(1)
