"""
translate.py — Reverie API proxy routes
Registers blueprint: translate_bp
"""

import os
import requests as http_requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# If you created utils.py in Week 1, uncomment the line below:
# from utils import translate_via_reverie 

translate_bp = Blueprint("translate", __name__)

REVERIE_API_KEY = os.getenv("REVERIE_API_KEY")
REVERIE_APP_ID  = os.getenv("REVERIE_APP_ID")
REVERIE_BASE    = "https://revapi.reverieinc.com/"

def _reverie_headers(src_lang: str = "en", tgt_lang: str = "hi") -> dict:
    return {
        "REV-API-KEY":    REVERIE_API_KEY,
        "REV-APP-ID":     REVERIE_APP_ID,
        "REV-APPNAME":    "localization",
        "REV-APPVERSION": "3.0",
        "domain":         "ecommerce",
        "Content-Type":   "application/json",
        "src_lang":       src_lang,
        "tgt_lang":       tgt_lang
    }

# ─────────────────────────────────────────────
# Translation — NO @jwt_required
# ─────────────────────────────────────────────

@translate_bp.route("/", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    
    # Check JSON body first, then headers, then default to en->hi
    src_lang = data.get("src_lang") or request.headers.get("src_lang") or "en"
    tgt_lang = data.get("tgt_lang") or request.headers.get("tgt_lang") or "hi"

    texts = data.get("data", [])

    # The Echo-Chamber Check
    if src_lang == tgt_lang:
        return jsonify({
            "responseList": [{"inString": t, "outString": t} for t in texts]
        })

    body = {
        "data":          texts,
        "enableNmt":     data.get("enableNmt", True),
        "enableLookup":  data.get("enableLookup", True),
    }
    
    if data.get("nmtMask") or data.get("nmtMaskTerms"):
        body["nmtMask"]      = True
        body["nmtMaskTerms"] = data.get("nmtMaskTerms", [])

    try:
        resp = http_requests.post(
            REVERIE_BASE,
            json=body,
            headers=_reverie_headers(src_lang, tgt_lang),
            timeout=20,
        )
        resp.raise_for_status()
        return jsonify(resp.json()), resp.status_code
    except http_requests.RequestException as e:
        print(f"Reverie API Error: {e}")
        return jsonify({"error": str(e)}), 502

# ─────────────────────────────────────────────
# Transliteration — No Auth Required
# ─────────────────────────────────────────────

@translate_bp.route("/transliterate", methods=["POST"])
def transliterate():
    data = request.get_json(force=True)
    src_lang = data.get("src_lang") or request.headers.get("src_lang") or "en"
    tgt_lang = data.get("tgt_lang") or request.headers.get("tgt_lang") or "hi"

    body = {"data": data.get("data", []), "isBulk": True, "ignoreTaggedEntities": True}

    try:
        resp = http_requests.post(
            "https://revapi.reverieinc.com/transliterate",
            json=body,
            headers=_reverie_headers(src_lang, tgt_lang),
            timeout=20,
        )
        resp.raise_for_status()
        return jsonify(resp.json()), resp.status_code
    except http_requests.RequestException as e:
        return jsonify({"error": str(e)}), 502

# ─────────────────────────────────────────────
# STT token & File-based STT — Requires Auth
# ─────────────────────────────────────────────

@translate_bp.route("/stt-token", methods=["GET"])
@jwt_required()
def stt_token():
    return jsonify({
        "api_key": REVERIE_API_KEY,
        "app_id":  REVERIE_APP_ID,
    })

@translate_bp.route("/stt", methods=["POST"])
@jwt_required()
def stt_file():
    audio = request.files.get("audio_file")
    lang  = request.form.get("lang", "hi")
    domain = request.form.get("domain", "ecommerce")

    if not audio:
        return jsonify({"error": "audio_file is required"}), 400

    try:
        resp = http_requests.post(
            "https://revapi.reverieinc.com/stt",
            files={"audio_file": (audio.filename, audio.stream, audio.content_type)},
            data={"lang": lang, "domain": domain},
            headers={
                "REV-API-KEY": REVERIE_API_KEY,
                "REV-APP-ID":  REVERIE_APP_ID,
            },
            timeout=30,
        )
        resp.raise_for_status()
        return jsonify(resp.json()), resp.status_code
    except http_requests.RequestException as e:
        return jsonify({"error": str(e)}), 502