import json

from flask import jsonify, make_response, render_template, request


def register_routes(app, SiteConfig, db, public_config, require_admin_token, get_site_variant, ZENECE2_PAGE_DATA):
    @app.get("/")
    @app.get("/site/<variant>")
    @app.get("/zenece2")
    def home(variant=None):
        selected_variant = variant or get_site_variant()
        if request.path == "/zenece2":
            selected_variant = "zenece2"

        template_name = "index.html" if selected_variant == "default" else "zenece2.html"
        css_file = "css/site.css" if selected_variant == "default" else "css/zenece2.css"
        js_file = "js/site.js" if selected_variant == "default" else "js/zenece2.js"

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
                site_config=public_config(),
                selected_variant=selected_variant,
                css_file=css_file,
                js_file=js_file,
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
        return render_template("admin.html")

    @app.post("/admin/settings")
    def update_settings():
        if not require_admin_token():
            return jsonify({"error": "Admin authorization required."}), 401

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return jsonify({"error": "A non-empty JSON object is required."}), 400

        updated = []
        for key, setting_data in payload.items():
            if not isinstance(key, str) or not isinstance(setting_data, dict):
                return jsonify({"error": "Each setting must be an object."}), 400
            if "value" not in setting_data:
                return jsonify({"error": f"Missing value for {key}."}), 400

            setting = SiteConfig.query.filter_by(key=key).first()
            if setting is None:
                setting = SiteConfig(key=key, value="", category="general")
                db.session.add(setting)

            value_type = setting_data.get("value_type", setting.value_type)
            if value_type not in {"string", "color", "boolean", "integer", "decimal", "json"}:
                return jsonify({"error": f"Unsupported value type for {key}."}), 400
            value = setting_data["value"]
            if value_type == "color" and (
                not isinstance(value, str)
                or not value.startswith("#")
                or len(value) not in {4, 7}
            ):
                return jsonify({"error": f"Invalid color value for {key}."}), 400
            if value_type == "json":
                value = json.dumps(value)
            elif value_type == "boolean":
                if not isinstance(value, bool):
                    return jsonify({"error": f"Boolean value required for {key}."}), 400
                value = str(value).lower()
            else:
                value = str(value)

            setting.value = value
            setting.value_type = value_type
            setting.category = setting_data.get("category", setting.category)
            setting.is_public = bool(setting_data.get("is_public", setting.is_public))
            updated.append(key)

        db.session.commit()
        return jsonify({"updated": updated, "config": public_config()})
