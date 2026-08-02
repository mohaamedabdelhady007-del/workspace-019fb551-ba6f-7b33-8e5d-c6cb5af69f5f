#!/usr/bin/env python3
"""
package_omni_themes.py
======================
Zip each generated OMNI UK theme so it can be uploaded manually via
Shopify Admin -> Online Store -> Themes -> Upload theme (or for backup).

Usage:  python3 package_omni_themes.py
Outputs: omni-uk-themes/<theme>.zip for each theme.
"""

import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
THEMES_DIR = os.path.join(ROOT, "omni-uk-themes")

SKIP = {"__pycache__"}


def zip_theme(name):
    src = os.path.join(THEMES_DIR, name)
    out = os.path.join(THEMES_DIR, f"{name}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, _, files in os.walk(src):
            for fn in files:
                full = os.path.join(dp, fn)
                rel = os.path.relpath(full, src)
                if rel.split(os.sep)[0] in SKIP:
                    continue
                z.write(full, rel)
    print(f"  {out}  ({os.path.getsize(out)//1024} KB)")


def main():
    if not os.path.isdir(THEMES_DIR):
        raise SystemExit("omni-uk-themes/ not found. Run generate_omni_themes.py first.")
    print("Zipping OMNI UK themes:")
    for name in sorted(os.listdir(THEMES_DIR)):
        full = os.path.join(THEMES_DIR, name)
        if os.path.isdir(full) and not name.endswith(".zip"):
            zip_theme(name)


if __name__ == "__main__":
    main()
