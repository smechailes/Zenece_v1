import json
import math
import re

from flask import jsonify, make_response, redirect, render_template, request, session, url_for


ALLOWED_VALUE_TYPES = {"string", "color", "boolean", "integer", "decimal", "json"}
COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$")


def validate_setting(key, setting_data, setting, setting_types):
    if not isinstance(setting_data, dict):
        return "Each setting must be an object."
    if "value" not in setting_data:
        return f"Missing value for {key}."

    value_type = setting_data.get("value_type", setting_types.get(key, "string"))
    if not isinstance(value_type, str) or value_type not in ALLOWED_VALUE_TYPES:
        return f"Unsupported value type for {key}."

    value = setting_data["value"]
    if value_type == "string" and not isinstance(value, str):
        return f"String value required for {key}."
    if value_type == "color" and (
        not isinstance(value, str) or not COLOR_PATTERN.fullmatch(value)
    ):
        return f"Invalid color value for {key}."
    if value_type == "boolean" and not isinstance(value, bool):
        return f"Boolean value required for {key}."
    if value_type == "integer" and (
        not isinstance(value, int) or isinstance(value, bool)
    ):
        return f"Integer value required for {key}."
    if value_type == "decimal" and (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(value)
    ):
        return f"Decimal value required for {key}."
    if value_type == "json":
        try:
            json.dumps(value, allow_nan=False)
        except (TypeError, ValueError):
            return f"JSON-compatible value required for {key}."

    if "category" in setting_data and not isinstance(setting_data["category"], str):
        return f"Category must be a string for {key}."
    if "is_public" in setting_data and not isinstance(setting_data["is_public"], bool):
        return f"is_public must be boolean for {key}."
    return None


def serialize_setting_value(value, value_type):
    if value_type == "json":
        return json.dumps(value)
    if value_type == "boolean":
        return str(value).lower()
    return str(value)


def register_routes(
    app,
    SiteSetting,
    NavLink,
    User,
    db,
    public_config,
    get_nav_links,
    require_admin_token,
    get_site_variant,
    ZENECE2_PAGE_DATA,
    allowed_config_keys,
    setting_types,
):
    def admin_authorized():
        return bool(session.get("admin_user_id") or require_admin_token())

    def require_admin_access():
        if admin_authorized():
            return None
        if request.accept_mimetypes.accept_html and request.method == "GET":
            return redirect(url_for("admin_login"))
        return jsonify({"error": "Admin authorization required."}), 401

    @app.get("/")
    @app.get("/site/<variant>")
    @app.get("/zenece2")
    def home(variant=None):
        selected_variant = variant or get_site_variant()
        if request.path == "/zenece2":
            selected_variant = "zenece2"

        template_name = "index.html" if selected_variant == "default" else "zenece2.html"
        response = make_response(
            render_template(
                template_name,
                page={
                    "title": "ZenEce Investment Holdings — Pre-IPO capital, disciplined exits",
                    "brand": "ZenEce",
                    "location": "Kathmandu",
                    "email": "zeneceinvestmentholdings@gmail.com",
                    "confidentiality": "Confidential · For qualified investors only",
                },
                selected_variant=selected_variant,
                zenece2_data=ZENECE2_PAGE_DATA if selected_variant == "zenece2" else None,
            )
        )
        response.set_cookie("site_variant", selected_variant, max_age=60 * 60 * 24 * 30)
        return response

    @app.get("/api/site-config")
    def site_config_api():
        return jsonify(public_config())

    @app.get("/admin")
    def admin_dashboard():
        access_error = require_admin_access()
        if access_error:
            return access_error
        return render_template(
            "admin.html",
            nav_links=get_nav_links(include_hidden=True),
        )

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if request.method == "GET":
            return render_template("admin_login.html")

        payload = request.get_json(silent=True) or request.form
        username = payload.get("username", "")
        password = payload.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return jsonify({"error": "Invalid admin credentials."}), 401
        session["admin_user_id"] = user.id
        return jsonify({"authenticated": True})

    @app.post("/admin/logout")
    def admin_logout():
        session.pop("admin_user_id", None)
        return jsonify({"authenticated": False})

    @app.post("/admin/settings")
    def update_settings():
        access_error = require_admin_access()
        if access_error:
            return access_error

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return jsonify({"error": "A non-empty JSON object is required."}), 400

        unknown_keys = set(payload) - allowed_config_keys
        if unknown_keys:
            return jsonify({"error": f"Unsupported setting: {sorted(unknown_keys)[0]}."}), 400

        settings = {
            key: SiteSetting.query.filter_by(key=key).first()
            for key in payload
        }
        for key, setting_data in payload.items():
            error = validate_setting(key, setting_data, settings[key], setting_types)
            if error:
                return jsonify({"error": error}), 400

        updated = []
        for key, setting_data in payload.items():
            setting = settings[key]
            if setting is None:
                setting = SiteSetting(key=key, value="")
                db.session.add(setting)

            value_type = setting_data.get("value_type", setting_types.get(key, "string"))
            value = serialize_setting_value(setting_data["value"], value_type)

            setting.value = value
            updated.append(key)

        db.session.commit()
        return jsonify({"updated": updated, "config": public_config()})

    @app.post("/admin/nav")
    def update_navigation():
        access_error = require_admin_access()
        if access_error:
            return access_error

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "A JSON object is required."}), 400
        links = payload.get("links")
        if not isinstance(links, list):
            return jsonify({"error": "links must be an array."}), 400

        try:
            normalized = []
            for index, link_data in enumerate(links):
                if not isinstance(link_data, dict):
                    raise ValueError("Each navigation link must be an object.")
                title = link_data.get("title")
                url = link_data.get("url")
                if not isinstance(title, str) or not title.strip():
                    raise ValueError("Navigation titles are required.")
                if not isinstance(url, str) or not url.strip():
                    raise ValueError("Navigation URLs are required.")
                normalized.append((link_data.get("id"), title.strip(), url.strip(), index, bool(link_data.get("is_visible", True))))
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        existing = {link.id: link for link in NavLink.query.all()}
        retained_ids = {link_id for link_id, *_ in normalized if isinstance(link_id, int)}
        for link_id, title, url, order_index, is_visible in normalized:
            link = existing.get(link_id) if isinstance(link_id, int) else None
            if link is None:
                link = NavLink()
                db.session.add(link)
            link.title = title
            link.url = url
            link.order_index = order_index
            link.is_visible = is_visible
        for link_id, link in existing.items():
            if link_id not in retained_ids:
                db.session.delete(link)
        db.session.commit()
        return jsonify({"nav_links": get_nav_links(include_hidden=True)})
