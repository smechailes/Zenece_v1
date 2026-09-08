import json
import os
from datetime import datetime, timezone

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from routing.routes import register_routes


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///site_config.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ADMIN_TOKEN"] = os.environ.get("ADMIN_TOKEN")

db = SQLAlchemy(app)


class SiteConfig(db.Model):
    __tablename__ = "site_config"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    value_type = db.Column(db.String(20), nullable=False, default="string")
    category = db.Column(db.String(40), nullable=False, default="general")
    is_public = db.Column(db.Boolean, nullable=False, default=True)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


DEFAULT_CONFIG = {
    "theme.primary_color": ("#D4AF37", "color", "theme"),
    "theme.background_color": ("#0B1B2B", "color", "theme"),
    "theme.surface_color": ("#16283D", "color", "theme"),
    "navbar.title": ("ZenEce", "string", "navbar"),
    "navbar.visible": ("true", "boolean", "navbar"),
    "hero.title": ("Nepal's pre-IPO upside, before the crowd gets in.", "string", "hero"),
    "hero.description": (
        "ZenEce buys equity in profitable, listing-track companies years before they reach NEPSE.",
        "string",
        "hero",
    ),
}

ZENECE2_PAGE_DATA = {
    "brand": "ZenEce",
    "nav_links": [
        {"label": "Overview", "href": "#overview"},
        {"label": "Portfolio", "href": "#portfolio"},
        {"label": "Approach", "href": "#approach"},
        {"label": "Team", "href": "#team"},
        {"label": "Updates", "href": "#updates"},
        {"label": "Contact", "href": "#contact"},
    ],
    "hero": {
        "eyebrow": "Confidential · for qualified investors only",
        "title": "Private-market upside before Nepal's next listing wave.",
        "description": "ZenEce evaluates profitable, listing-track businesses years before they reach public markets and brings them into a disciplined, founder-friendly capital structure.",
        "primary_cta": {"label": "Request access", "href": "#contact"},
        "secondary_cta": {"label": "How it works", "href": "#approach"},
        "gallery": [
            {
                "src": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=900&q=80",
                "alt": "Hydropower project landscape",
            },
            {
                "src": "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=900&q=80",
                "alt": "City skyline with investment growth theme",
            },
        ],
    },
    "metrics": [
        {"value": "100", "suffix": " Cr", "label": "NPR total fund size"},
        {"value": "4", "suffix": "", "label": "deals already funded"},
        {"value": "20", "suffix": "%", "label": "target yearly return"},
        {"value": "0", "suffix": "%", "label": "fees & carry"},
    ],
    "overview": {
        "title": "Why founders and investors choose ZenEce",
        "content": "We pair deep local market access with capital discipline, giving early-stage companies long-horizon funding and investors access to pre-IPO upside before the crowd arrives.",
        "bullets": [
            "Direct access to profitable, listing-track opportunities",
            "Capital deployment timed before public-market attention builds",
            "Clear governance with a founder-first operating model",
            "Structured exits designed for repeat, compounding returns",
        ],
    },
    "portfolio": [
        {
            "category": "Agri-processing · IPO-track",
            "name": "Sugar Mill Project",
            "description": "Import substitution, one crush cycle at a time. NPR 170 Cr, 85% complete, COD Dec 2026.",
            "image": "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80",
        },
        {
            "category": "Hydropower · IPO-track",
            "name": "21MW Run-of-River",
            "description": "Thirty years of power, financially closed. NPR 367.5 Cr, 30-yr PPA with NEA.",
            "image": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=900&q=80",
        },
        {
            "category": "Healthcare · IPO-track",
            "name": "Multispecialty Hospital",
            "description": "Three hundred beds, one clear listing path. NPR 1,191 Cr, JCI accreditation target.",
            "image": "https://images.unsplash.com/photo-1538108149393-fbbd81895977?auto=format&fit=crop&w=900&q=80",
        },
        {
            "category": "Healthcare & Education",
            "name": "Teaching Hospital & Cancer Institute",
            "description": "Nineteen years of care, built for scale. 750 beds plus an integrated medical college.",
            "image": "https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=900&q=80",
        },
        {
            "category": "Telecom · Target 2027",
            "name": "Broadband / FTTH Operator",
            "description": "The infrastructure under Nepal's internet. ~485K subscribers, #2 post-merger.",
            "image": "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&w=900&q=80",
        },
        {
            "category": "Hospitality · IPO filed",
            "name": "Branded Hospitality Asset",
            "description": "An international brand, a Nepali address. Operating asset, SEBON process underway.",
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "approach": [
        {
            "step": "01",
            "title": "Buy in early",
            "body": "Take equity stakes in profitable companies, typically 3–5 years before they list, at a low price.",
        },
        {
            "step": "02",
            "title": "Make it list-ready",
            "body": "In-house audit, advisory and merchant-banking teams prepare the company for a clean public listing.",
        },
        {
            "step": "03",
            "title": "Cash out",
            "body": "Exit via IPO or secondary sale, then redeploy into the next opportunity in the pipeline.",
        },
    ],
    "returns": [
        {"label": "Management fee", "value": "None"},
        {"label": "Carried interest", "value": "None"},
        {"label": "Profit to shareholders", "value": "100%, pro-rata", "highlight": True},
    ],
    "scenarios": [
        {"label": "Cautious", "value": "7% / yr · 1.8× money back"},
        {"label": "Base case", "value": "~20% / yr · ~4.0× money back", "highlight": True},
        {"label": "Strong", "value": "30% / yr · 7.0× money back"},
    ],
    "updates": [
        {"date": "August 2026", "tag": "Fundraising", "title": "Capital underway: NPR 75 Cr raise live, founders committed NPR 15 Cr", "href": "#contact"},
        {"date": "August 2026", "tag": "Portfolio", "title": "Financial closure completed for the 21MW hydropower project, 30-yr PPA secured", "href": "#portfolio"},
        {"date": "August 2026", "tag": "Pipeline", "title": "Multispecialty hospital, NPR 1,191 Cr, enters its equity raise stage", "href": "#portfolio"},
    ],
    "team": [
        {
            "name": "Virochan Khanal",
            "role": "FCA · Founder & Managing Director",
            "bio": "15+ years in corporate finance, project financing and capital raising. Chairperson, Miyo Securities.",
            "initials": "VK",
            "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Sanjay Pokhrel",
            "role": "CFA, CA · Founder & Director",
            "bio": "Founder & Director, Garima Capital. US$200Mn+ M&A closed; deal advisory and M&A expert.",
            "initials": "SP",
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Ujjwal Shahi",
            "role": "FCA · Founder, Finance & Governance",
            "bio": "PwC-trained; 15+ years across corporate finance, taxation, investment strategy and audit.",
            "initials": "US",
            "image": "https://images.unsplash.com/photo-1504593811423-6dd665756598?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "contact": {
        "email": "zeneceinvestmentholdings@gmail.com",
        "website": "www.zeneceinvestmentholding.com",
        "location": "Kathmandu, Nepal",
        "note": "By submitting, you confirm you are contacting ZenEce as a qualified investor or professional enquiry.",
    },
}


def serialize_config(setting):
    value = setting.value
    if setting.value_type == "boolean":
        value = value.lower() == "true"
    elif setting.value_type == "integer":
        value = int(value)
    elif setting.value_type == "decimal":
        value = float(value)
    elif setting.value_type == "json":
        value = json.loads(value)
    return value


def public_config():
    return {
        setting.key: serialize_config(setting)
        for setting in SiteConfig.query.filter_by(is_public=True).all()
    }


@app.context_processor
def inject_site_config():
    return {"site_config": public_config()}


def require_admin_token():
    configured_token = app.config["ADMIN_TOKEN"]
    supplied_token = request.headers.get("X-Admin-Token")
    return bool(configured_token and supplied_token == configured_token)


with app.app_context():
    db.create_all()
    for key, (value, value_type, category) in DEFAULT_CONFIG.items():
        if SiteConfig.query.filter_by(key=key).first() is None:
            db.session.add(
                SiteConfig(
                    key=key,
                    value=value,
                    value_type=value_type,
                    category=category,
                )
            )
    db.session.commit()


def get_site_variant(default="default"):
    requested = request.args.get("variant") or request.cookies.get("site_variant") or default
    if requested not in {"default", "zenece2"}:
        return default
    return requested


app.config["PUBLIC_CONFIG"] = public_config
app.config["ZENECE2_PAGE_DATA"] = ZENECE2_PAGE_DATA
app.config["SITE_VARIANT_DEFAULT"] = "default"

register_routes(
    app,
    SiteConfig=SiteConfig,
    db=db,
    public_config=public_config,
    require_admin_token=require_admin_token,
    get_site_variant=get_site_variant,
    ZENECE2_PAGE_DATA=ZENECE2_PAGE_DATA,
)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
    )