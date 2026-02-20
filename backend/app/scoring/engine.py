import math
from app.schemas import ClaimScoreRequest

class ScoringEngine:
    @staticmethod
    def calculate_risk_score(claim: ClaimScoreRequest) -> tuple[float, float, str]:
        """
        Calculate risk score, fraud probability, and decision.
        Returns: (risk_score, fraud_probability, decision)
        """
        risk_score = 0.0
        
        # Amount-based scoring
        if claim.amount < 500:
            risk_score += 5
        elif claim.amount < 5000:
            risk_score += 15
        elif claim.amount < 20000:
            risk_score += 30
        else:
            risk_score += 45
        
        # Incident type scoring
        incident_lower = claim.incident_type.lower()
        if "collision" in incident_lower:
            risk_score += 15
        elif "theft" in incident_lower:
            risk_score += 25
        elif "fire" in incident_lower:
            risk_score += 35
        elif "injury" in incident_lower:
            risk_score += 20
        else:
            risk_score += 10
        
        # History score
        risk_score += claim.history_score * 0.3
        
        # Cap at 100
        risk_score = min(risk_score, 100.0)
        
        # Fraud probability (sigmoid)
        fraud_probability = 1 / (1 + math.exp(-(risk_score - 50) / 10))
        
        # Decision policy
        if fraud_probability < 0.35:
            decision = "APPROVE"
        elif fraud_probability < 0.70:
            decision = "REVIEW"
        else:
            decision = "REJECT"
        
        return risk_score, fraud_probability, decision
    
    @staticmethod
    def generate_template_explanation(
        claim: ClaimScoreRequest,
        risk_score: float,
        fraud_probability: float,
        decision: str
    ) -> str:
        """Generate deterministic template explanation."""
        risk_level = "LOW" if fraud_probability < 0.35 else "MEDIUM" if fraud_probability < 0.70 else "HIGH"
        
        explanation = f"**Risk Level: {risk_level}**\n\n"
        explanation += "**Key Factors:**\n"
        explanation += f"• Claim amount: ${claim.amount:,.2f} (contributes to overall risk assessment)\n"
        explanation += f"• Incident type: {claim.incident_type} (evaluated against historical patterns)\n"
        explanation += f"• Customer history score: {claim.history_score:.1f}/100\n\n"
        explanation += f"**Assessment:**\n"
        explanation += f"• Overall risk score: {risk_score:.2f}/100\n"
        explanation += f"• Fraud probability: {fraud_probability:.1%}\n\n"
        explanation += "**Recommended Action:**\n"
        
        if decision == "APPROVE":
            explanation += "• Auto-approve this claim for fast-track processing\n"
            explanation += "• Estimated processing time: <2 hours\n"
        elif decision == "REVIEW":
            explanation += "• Assign to senior adjuster for manual review\n"
            explanation += "• Request additional documentation if needed\n"
        else:
            explanation += "• Escalate to fraud investigation team\n"
            explanation += "• Conduct thorough verification before proceeding\n"
        
        return explanation
