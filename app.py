"""Compatibility entry point for the original python app.py command and WSGI server (Render)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "aclproject2-main" / "aclproject2-main"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Load the Flask WSGI instance from the project directory
spec = importlib.util.spec_from_file_location("knee_backend", APP_DIR / "app.py")
if spec and spec.loader:
    knee_backend = importlib.util.module_from_spec(spec)
    sys.modules["knee_backend"] = knee_backend
    spec.loader.exec_module(knee_backend)
    app = getattr(knee_backend, "app", None)
    init_db = getattr(knee_backend, "init_db", lambda: None)
    try:
        init_db()
    except Exception:
        pass
else:
    raise RuntimeError(f"Cannot load application from {APP_DIR / 'app.py'}")

if __name__ == "__main__":
    from web import main
    raise SystemExit(main())