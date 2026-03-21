"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,  # hours per week available across team
        "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"]
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology", 
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"]
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"], 
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"]
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"]
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"]
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"]
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"]
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"]
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"]
    }
}

# In-memory consultant profiles used for team matching recommendations
consultants = {
    "alice.smith@slalom.com": {
        "name": "Alice Smith",
        "practice_area": "Technology",
        "skill_level": "Expert",
        "certifications": ["AWS Solutions Architect", "Kubernetes Admin"],
        "industry_verticals": ["Healthcare", "Financial Services"],
        "availability": 12
    },
    "bob.johnson@slalom.com": {
        "name": "Bob Johnson",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["Azure Architect Expert"],
        "industry_verticals": ["Retail", "Financial Services"],
        "availability": 10
    },
    "emma.davis@slalom.com": {
        "name": "Emma Davis",
        "practice_area": "Technology",
        "skill_level": "Expert",
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert"],
        "industry_verticals": ["Retail", "Manufacturing"],
        "availability": 14
    },
    "sophia.wilson@slalom.com": {
        "name": "Sophia Wilson",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["Google Analytics"],
        "industry_verticals": ["Healthcare", "Retail"],
        "availability": 8
    },
    "john.brown@slalom.com": {
        "name": "John Brown",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["Docker Certified Associate", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "availability": 9
    },
    "olivia.taylor@slalom.com": {
        "name": "Olivia Taylor",
        "practice_area": "Technology",
        "skill_level": "Proficient",
        "certifications": ["Kubernetes Admin"],
        "industry_verticals": ["Technology", "Healthcare"],
        "availability": 15
    },
    "liam.anderson@slalom.com": {
        "name": "Liam Anderson",
        "practice_area": "Strategy",
        "skill_level": "Expert",
        "certifications": ["Digital Transformation Certificate"],
        "industry_verticals": ["Government", "Healthcare"],
        "availability": 11
    },
    "noah.martinez@slalom.com": {
        "name": "Noah Martinez",
        "practice_area": "Strategy",
        "skill_level": "Advanced",
        "certifications": ["Agile Certified Practitioner"],
        "industry_verticals": ["Financial Services", "Government"],
        "availability": 12
    },
    "ava.garcia@slalom.com": {
        "name": "Ava Garcia",
        "practice_area": "Operations",
        "skill_level": "Expert",
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing"],
        "availability": 7
    },
    "mia.rodriguez@slalom.com": {
        "name": "Mia Rodriguez",
        "practice_area": "Operations",
        "skill_level": "Advanced",
        "certifications": ["Prosci Certified"],
        "industry_verticals": ["Government", "Manufacturing"],
        "availability": 13
    },
    "amelia.lee@slalom.com": {
        "name": "Amelia Lee",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Technology"],
        "availability": 16
    },
    "harper.white@slalom.com": {
        "name": "Harper White",
        "practice_area": "Technology",
        "skill_level": "Proficient",
        "certifications": ["Google UX Design Certificate"],
        "industry_verticals": ["Healthcare", "Retail"],
        "availability": 18
    },
    "ella.clark@slalom.com": {
        "name": "Ella Clark",
        "practice_area": "Technology",
        "skill_level": "Expert",
        "certifications": ["CISSP", "CISM"],
        "industry_verticals": ["Financial Services", "Government"],
        "availability": 6
    },
    "scarlett.lewis@slalom.com": {
        "name": "Scarlett Lewis",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["CompTIA Security+"],
        "industry_verticals": ["Healthcare", "Government"],
        "availability": 12
    },
    "james.walker@slalom.com": {
        "name": "James Walker",
        "practice_area": "Technology",
        "skill_level": "Expert",
        "certifications": ["Microsoft BI Certification", "Power BI Expert"],
        "industry_verticals": ["Retail", "Financial Services"],
        "availability": 10
    },
    "benjamin.hall@slalom.com": {
        "name": "Benjamin Hall",
        "practice_area": "Technology",
        "skill_level": "Advanced",
        "certifications": ["Qlik Sense Certified"],
        "industry_verticals": ["Manufacturing", "Retail"],
        "availability": 14
    },
    "charlotte.young@slalom.com": {
        "name": "Charlotte Young",
        "practice_area": "Operations",
        "skill_level": "Expert",
        "certifications": ["Certified Scrum Master", "SAFe Agilist"],
        "industry_verticals": ["Technology", "Healthcare"],
        "availability": 10
    },
    "henry.king@slalom.com": {
        "name": "Henry King",
        "practice_area": "Operations",
        "skill_level": "Advanced",
        "certifications": ["ICAgile Certified"],
        "industry_verticals": ["Financial Services", "Technology"],
        "availability": 15
    },
    "zoe.thomas@slalom.com": {
        "name": "Zoe Thomas",
        "practice_area": "Technology",
        "skill_level": "Expert",
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Retail", "Financial Services"],
        "availability": 20
    },
    "ethan.moore@slalom.com": {
        "name": "Ethan Moore",
        "practice_area": "Technology",
        "skill_level": "Proficient",
        "certifications": ["Tableau Desktop Specialist"],
        "industry_verticals": ["Retail", "Healthcare"],
        "availability": 20
    }
}


SCORE_WEIGHTS = {
    "skill_level": 35,
    "certifications": 25,
    "availability": 20,
    "practice_area": 10,
    "industry_overlap": 10,
}


SKILL_LEVEL_RANK = {
    "Emerging": 1,
    "Proficient": 2,
    "Advanced": 3,
    "Expert": 4,
}


def _score_skill_level(capability: dict, consultant: dict) -> tuple[float, str]:
    target_level = max(
        capability.get("skill_levels", ["Emerging"]),
        key=lambda level: SKILL_LEVEL_RANK.get(level, 0)
    )
    target_rank = SKILL_LEVEL_RANK.get(target_level, 1)
    consultant_rank = SKILL_LEVEL_RANK.get(consultant.get("skill_level", "Emerging"), 1)
    ratio = min(consultant_rank / max(target_rank, 1), 1)
    points = SCORE_WEIGHTS["skill_level"] * ratio
    reason = (
        f"Skill level {consultant.get('skill_level', 'Emerging')} vs target {target_level}"
    )
    return points, reason


def _score_certifications(capability: dict, consultant: dict) -> tuple[float, str]:
    required = set(capability.get("certifications", []))
    candidate = set(consultant.get("certifications", []))
    if not required:
        return SCORE_WEIGHTS["certifications"], "No required certifications for capability"

    overlap = required.intersection(candidate)
    ratio = len(overlap) / len(required)
    points = SCORE_WEIGHTS["certifications"] * ratio
    reason = f"Certification overlap {len(overlap)}/{len(required)}"
    return points, reason


def _score_availability(consultant: dict) -> tuple[float, str]:
    availability = max(consultant.get("availability", 0), 0)
    ratio = min(availability / 20, 1)
    points = SCORE_WEIGHTS["availability"] * ratio
    reason = f"Availability {availability}h/week"
    return points, reason


def _score_practice_area(capability: dict, consultant: dict) -> tuple[float, str]:
    is_match = capability.get("practice_area") == consultant.get("practice_area")
    points = SCORE_WEIGHTS["practice_area"] if is_match else 0
    reason = "Practice area aligned" if is_match else "Practice area differs"
    return points, reason


def _score_industry_overlap(capability: dict, consultant: dict) -> tuple[float, str]:
    target_industries = set(capability.get("industry_verticals", []))
    consultant_industries = set(consultant.get("industry_verticals", []))
    if not target_industries:
        return SCORE_WEIGHTS["industry_overlap"], "No target industries set"

    overlap = target_industries.intersection(consultant_industries)
    ratio = len(overlap) / len(target_industries)
    points = SCORE_WEIGHTS["industry_overlap"] * ratio
    reason = f"Industry overlap {len(overlap)}/{len(target_industries)}"
    return points, reason


def get_recommendations(capability_name: str, top_n: int = 5) -> list[dict]:
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    capability = capabilities[capability_name]
    existing_team = set(capability.get("consultants", []))
    recommendations = []

    for email, profile in consultants.items():
        if email in existing_team:
            continue

        skill_points, skill_reason = _score_skill_level(capability, profile)
        cert_points, cert_reason = _score_certifications(capability, profile)
        avail_points, avail_reason = _score_availability(profile)
        practice_points, practice_reason = _score_practice_area(capability, profile)
        industry_points, industry_reason = _score_industry_overlap(capability, profile)

        total_score = skill_points + cert_points + avail_points + practice_points + industry_points

        recommendations.append({
            "email": email,
            "name": profile.get("name", email),
            "score": round(total_score, 2),
            "explainability": {
                "skill_level": {"points": round(skill_points, 2), "reason": skill_reason},
                "certifications": {"points": round(cert_points, 2), "reason": cert_reason},
                "availability": {"points": round(avail_points, 2), "reason": avail_reason},
                "practice_area": {"points": round(practice_points, 2), "reason": practice_reason},
                "industry_overlap": {"points": round(industry_points, 2), "reason": industry_reason},
            }
        })

    recommendations.sort(key=lambda item: item["score"], reverse=True)
    return recommendations[:max(top_n, 1)]


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return capabilities


@app.get("/capabilities/{capability_name}/recommendations")
def recommend_consultants(capability_name: str, top_n: int = 5):
    return {
        "capability": capability_name,
        "weights": SCORE_WEIGHTS,
        "recommendations": get_recommendations(capability_name=capability_name, top_n=top_n)
    }


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if email in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )

    # Add consultant
    capability["consultants"].append(email)
    return {"message": f"Registered {email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is registered
    if email not in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Remove consultant
    capability["consultants"].remove(email)
    return {"message": f"Unregistered {email} from {capability_name}"}
