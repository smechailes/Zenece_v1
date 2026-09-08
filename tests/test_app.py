def test_public_routes_render_distinct_variants(client):
    default_response = client.get("/?variant=default")
    alternate_response = client.get("/?variant=zenece2")

    assert default_response.status_code == 200
    assert b"z2-hero" not in default_response.data
    assert alternate_response.status_code == 200
    assert b"z2-hero" in alternate_response.data


def test_site_config_endpoint_returns_seeded_config(client):
    response = client.get("/api/site-config")

    assert response.status_code == 200
    assert response.json["navbar.visible"] is True
    assert response.json["theme.primary_color"] == "#D4AF37"


def test_admin_settings_requires_token(client):
    response = client.post(
        "/admin/settings",
        json={"hero.title": {"value": "Unauthorized", "value_type": "string"}},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Admin authorization required."}


def test_admin_settings_updates_with_valid_token(client):
    response = client.post(
        "/admin/settings",
        headers={"X-Admin-Token": "test-admin-token"},
        json={"hero.title": {"value": "Updated title", "value_type": "string"}},
    )

    assert response.status_code == 200
    assert response.json["updated"] == ["hero.title"]
    assert response.json["config"]["hero.title"] == "Updated title"


def test_admin_settings_rejects_unknown_key(client):
    response = client.post(
        "/admin/settings",
        headers={"X-Admin-Token": "test-admin-token"},
        json={"unknown.key": {"value": "value", "value_type": "string"}},
    )

    assert response.status_code == 400
    assert "Unsupported setting" in response.json["error"]


def test_admin_settings_rejects_invalid_values(client):
    invalid_payloads = [
        {"theme.primary_color": {"value": "#ggg", "value_type": "color"}},
        {"theme.primary_color": {"value": "#12345", "value_type": "color"}},
        {"navbar.visible": {"value": "true", "value_type": "boolean"}},
        {"hero.title": {"value": 123, "value_type": "string"}},
        {"hero.title": {"value": "value", "value_type": "unsupported"}},
    ]

    for payload in invalid_payloads:
        response = client.post(
            "/admin/settings",
            headers={"X-Admin-Token": "test-admin-token"},
            json=payload,
        )
        assert response.status_code == 400


def test_missing_route_returns_json_error(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json == {"error": "Resource not found."}


def test_admin_login_creates_session_and_dashboard_is_protected(client):
    unauthenticated = client.get("/admin", headers={"Accept": "text/html"})
    assert unauthenticated.status_code == 302
    assert unauthenticated.location.endswith("/admin/login")

    login = client.post(
        "/admin/login",
        json={"username": "admin", "password": "test-password"},
    )
    assert login.status_code == 200

    dashboard = client.get("/admin")
    assert dashboard.status_code == 200
    assert b"Navigation links" in dashboard.data


def test_admin_nav_updates_order_and_visibility(client):
    response = client.post(
        "/admin/nav",
        headers={"X-Admin-Token": "test-admin-token"},
        json={
            "links": [
                {"id": 1, "title": "Start", "url": "#hero", "is_visible": True},
                {"id": 2, "title": "Hidden", "url": "#hidden", "is_visible": False},
            ]
        },
    )

    assert response.status_code == 200
    assert [link["title"] for link in response.json["nav_links"]] == ["Start", "Hidden"]
    assert response.json["nav_links"][1]["is_visible"] is False
