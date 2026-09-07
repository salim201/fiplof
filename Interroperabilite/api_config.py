# -*- coding: utf-8 -*-
import os
import ConfigParser

INI_PATH = os.path.join(os.path.dirname(__file__), "interop.ini")
DEFAULT_URL = "http://localhost:8001"

def _ensure_ini():
    if not os.path.exists(INI_PATH):
        with open(INI_PATH, "w") as f:
            f.write("[api]\nbase_url = " + DEFAULT_URL + "\n")

def getApiBaseUrl():
    _ensure_ini()
    config = ConfigParser.SafeConfigParser()
    config.read(INI_PATH)
    try:
        return config.get("api", "base_url")
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        return DEFAULT_URL

def setApiBaseUrl(url):
    _ensure_ini()
    config = ConfigParser.SafeConfigParser()
    config.read(INI_PATH)
    if not config.has_section("api"):
        config.add_section("api")
    config.set("api", "base_url", url)
    with open(INI_PATH, "w") as f:
        config.write(f)
