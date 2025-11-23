import importlib
import sys

import pytest


def test_insecure_secret_key_for_prod_env_fails(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.delenv("SECRET_KEY", raising=False)

    sys.modules.pop("app.core.config", None)

    with pytest.raises(ValueError):
        importlib.import_module("app.core.config")
