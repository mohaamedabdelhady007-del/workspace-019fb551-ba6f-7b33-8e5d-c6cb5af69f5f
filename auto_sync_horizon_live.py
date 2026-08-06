import base64
import fnmatch
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

STORE_URL = os.environ.get("SHOPIFY_STORE", "rvsdgy-e1.myshopify.com")
THEME_NAME_HINT = os.environ.get("SHOPIFY_THEME_NAME", "Horizon")
BRANCH = os.environ.get("SHOPIFY_SYNC_BRANCH", "arena/019fd49b-workspace-019fb551-ba6f-7b33-8")
POLL_SECONDS = int(os.environ.get("SHOPIFY_SYNC_INTERVAL", "8"))
STATE_FILE = Path(".shopify_live_sync_state.json")
REPO_ROOT = Path(__file__).resolve().parent
REMOTE_REF = f"origin/{BRANCH}"

SYNC_PROFILE = os.environ.get("SHOPIFY_SYNC_PROFILE", "homepage").strip().lower()

SYNC_PATTERNS_BY_PROFILE = {
    "homepage": [
        "shopify-theme/sections/d99-home-grid.liquid",
        "shopify-theme/templates/index.json",
    ],
    "all": [
        "shopify-theme/sections/d99-*.liquid",
        "shopify-theme/templates/index.json",
        "shopify-theme/templates/product*.json",
        "shopify-theme/templates/collection.json",
        "shopify-theme/templates/cart.json",
        "shopify-theme/templates/page*.json",
        "shopify-theme/assets/d99-*",
        "shopify-theme/layout/theme.liquid",
        "shopify-theme/sections/header.liquid",
        "shopify-theme/sections/footer.liquid",
    ],
}

SYNC_PATTERNS = SYNC_PATTERNS_BY_PROFILE.get(SYNC_PROFILE, SYNC_PATTERNS_BY_PROFILE["homepage"])

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm"
}


def run(*args, text=True, check=True):
    return subprocess.run(args, cwd=REPO_ROOT, check=check, capture_output=True, text=text)


def git_fetch():
    run("git", "fetch", "origin", BRANCH)


def git_rev_parse(ref):
    return run("git", "rev-parse", ref).stdout.strip()


def git_diff_names(old_ref, new_ref):
    result = run("git", "diff", "--name-only", old_ref, new_ref, "--", "shopify-theme")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def git_ls_tree(ref):
    result = run("git", "ls-tree", "-r", "--name-only", ref, "shopify-theme")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def git_show_bytes(ref, path):
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=False,
    )
    return result.stdout


def matches_sync_patterns(path):
    return any(fnmatch.fnmatch(path, pattern) for pattern in SYNC_PATTERNS)


def read_token():
    candidates = [Path.home() / ".shopify_token", Path("/home/user/.shopify_token")]
    for path in candidates:
        if path.exists():
            token = path.read_text(encoding="utf-8").strip()
            if token:
                return token
    raise RuntimeError("No Shopify token found. Save it to ~/.shopify_token first.")


def request_json(url, token, method="GET", payload=None):
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def get_live_theme(token):
    url = f"https://{STORE_URL}/admin/api/2026-07/themes.json"
    themes = request_json(url, token)["themes"]
    for theme in themes:
        if theme.get("role") == "main" and THEME_NAME_HINT.lower() in theme.get("name", "").lower():
            return theme
    for theme in themes:
        if theme.get("role") == "main":
            return theme
    raise RuntimeError("Could not find a live theme to update.")


def upload_asset(token, theme_id, path, content_bytes):
    key = path.replace("shopify-theme/", "", 1)
    ext = Path(path).suffix.lower()
    url = f"https://{STORE_URL}/admin/api/2026-07/themes/{theme_id}/assets.json"

    if ext in BINARY_EXTENSIONS:
        payload = {
            "asset": {
                "key": key,
                "attachment": base64.b64encode(content_bytes).decode("utf-8")
            }
        }
    else:
        payload = {
            "asset": {
                "key": key,
                "value": content_bytes.decode("utf-8")
            }
        }

    try:
        request_json(url, token, method="PUT", payload=payload)
        print(f"  ↑ {key}")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Failed uploading {key}: HTTP {exc.code} :: {details}") from exc


def read_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def write_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def changed_files_for_sync(last_synced_ref, current_ref):
    if not last_synced_ref:
        return [path for path in git_ls_tree(current_ref) if matches_sync_patterns(path)]
    return [path for path in git_diff_names(last_synced_ref, current_ref) if matches_sync_patterns(path)]


def sync_once():
    token = read_token()
    theme = get_live_theme(token)
    state = read_state()

    git_fetch()
    remote_commit = git_rev_parse(REMOTE_REF)
    last_synced = state.get("last_synced_commit")

    files = changed_files_for_sync(last_synced, remote_commit)
    if not files:
        print(f"No theme changes to sync. Live theme remains: {theme['name']} (ID {theme['id']})")
        state["last_synced_commit"] = remote_commit
        state["theme_id"] = theme["id"]
        write_state(state)
        return

    print(f"Syncing {len(files)} changed file(s) to live theme: {theme['name']} (ID {theme['id']})")
    print(f"Commit: {remote_commit}")
    for path in files:
        content = git_show_bytes(remote_commit, path)
        upload_asset(token, theme["id"], path, content)

    state["last_synced_commit"] = remote_commit
    state["theme_id"] = theme["id"]
    write_state(state)
    print("Sync complete.\n")


def watch_loop():
    print(
        f"Watching branch '{BRANCH}' every {POLL_SECONDS}s and syncing profile '{SYNC_PROFILE}' "
        f"to live theme '{THEME_NAME_HINT}'..."
    )
    print("Leave this terminal open. Any new commit I push will be pulled and uploaded automatically.\n")
    while True:
        try:
            sync_once()
        except Exception as exc:
            print(f"SYNC ERROR: {exc}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    if "--once" in sys.argv:
        sync_once()
    else:
        watch_loop()
