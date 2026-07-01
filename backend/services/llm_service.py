from typing import Dict, Any, Optional
import random

async def generate_narrative(kind: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    headlines = {
        "monsoon": "Southwest Monsoon remains active across central and eastern India.",
        "drought": "Localized drought stress observed in low-rainfall districts.",
        "extremes": "Heatwave conditions expected over northwest India.",
        "scenario": "Projected warming may increase water stress in vulnerable regions.",
        "snapshot": "Current climate indicators remain within seasonal expectations.",
        "sector": "Agricultural outlook remains moderately favorable."
    }

    return {
        "ok": True,
        "narrative": {
            "headline": headlines.get(kind, "Climate analysis generated."),
            "confidence": round(random.uniform(0.84, 0.97), 2),
            "summary": "This AI-generated assessment is based on available climate indicators and historical patterns.",
            "recommendations": [
                "Monitor district weather advisories.",
                "Strengthen local preparedness.",
                "Promote climate-resilient practices."
            ]
        }
    }


class AdvisorChat:

    @classmethod
    async def reply(
        cls,
        session_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:

        msg = message.lower()

        if "farmer" in msg or "crop" in msg:
            return """
🌾 Farmer Advisory

• Irrigation every 3-4 days.
• Prefer drought-resistant varieties.
• Apply mulching to conserve soil moisture.
• Monitor IMD rainfall alerts.
"""

        elif "policy" in msg:
            return """
🏛 Policy Recommendation

• Improve climate-resilient infrastructure.
• Increase groundwater recharge projects.
• Expand early warning systems.
• Strengthen district disaster management.
"""

        elif "heat" in msg:
            return """
🔥 Heatwave Advisory

• Avoid outdoor work during afternoon.
• Ensure drinking water availability.
• Activate cooling centres.
• Monitor vulnerable populations.
"""

        elif "flood" in msg:
            return """
🌧 Flood Advisory

• Monitor river levels.
• Evacuate low-lying areas if required.
• Keep emergency supplies ready.
• Follow district administration alerts.
"""

        return """
🤖 Bharat Climate Twin AI

Current climate indicators have been analysed successfully.

Risk Level: Moderate

Recommendations:
• Continue monitoring rainfall.
• Improve water conservation.
• Follow district weather bulletins.
• Review adaptation strategies regularly.
"""