"""
GNC System Requirements
Based on Chapter 4 - Functional Analysis, Section 4.3

Implements requirements following ECSS-E-ST-60-30C standard with tailoring
for autonomous asteroid exploration missions.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class RequirementType(Enum):
    """Types of requirements"""
    FUNCTIONAL = "functional"
    OPERATIONAL = "operational"
    PERFORMANCE = "performance"
    INTERFACE = "interface"
    SAFETY = "safety"


class VerificationMethod(Enum):
    """Verification methods per ECSS-E-ST-10-02C"""
    TEST = "test"
    ANALYSIS = "analysis"
    REVIEW = "review_of_design"
    INSPECTION = "inspection"


@dataclass
class Requirement:
    """
    System requirement with full traceability
    
    Attributes:
        id: Unique requirement identifier
        text: Requirement statement (shall/should)
        type: Requirement type
        verification: Verification method
        rationale: Why this requirement exists
        parent: Parent requirement ID
        derived_from: Source requirements
        satisfied_by: Design elements that satisfy this
        verified_by: Test cases or analyses
    """
    id: str
    text: str
    type: RequirementType
    verification: VerificationMethod
    rationale: str = ""
    parent: Optional[str] = None
    derived_from: List[str] = field(default_factory=list)
    satisfied_by: List[str] = field(default_factory=list)
    verified_by: List[str] = field(default_factory=list)
    priority: str = "shall"  # shall/should/may
    
    def is_mandatory(self) -> bool:
        """Check if requirement is mandatory"""
        return self.priority == "shall"


class GNCRequirements:
    """
    Complete GNC system requirements database
    
    Organized by subsystem and mission phase:
    - Autonomous requirements (R-AUTO-XX)
    - System requirements (R-SYS-XX)
    - RDV requirements (R-RDV-XX)
    - TAG requirements (R-TAG-XX)
    - GNC functional requirements (R-GNC-XX)
    """
    
    def __init__(self):
        self.requirements: Dict[str, Requirement] = {}
        self._initialize_requirements()
    
    def _initialize_requirements(self):
        """Initialize all GNC requirements"""
        self._add_autonomous_requirements()
        self._add_system_requirements()
        self._add_rdv_requirements()
        self._add_tag_requirements()
        self._add_gnc_functional_requirements()
    
    def _add_autonomous_requirements(self):
        """Autonomous system requirements from Figure 4.16"""
        
        # High-level autonomy requirement
        self.add_requirement(
            id="R-AUTO-01",
            text="The GNC system shall autonomously place the S/C in the appropriate "
                 "trajectory around the orbit with an injection error that ensures no "
                 "collisions and uses the least amount of fuel possible.",
            type=RequirementType.FUNCTIONAL,
            verification=VerificationMethod.ANALYSIS,
            rationale="Primary mission success criterion - autonomous operation required "
                     "due to communication delay with Earth"
        )
        
        self.add_requirement(
            id="R-AUTO-02",
            text="The GNC system shall achieve accurate S/C state estimation relative "
                 "to the target to compute and execute necessary maneuvers to cancel "
                 "deviations in the nominal trajectory.",
            type=RequirementType.FUNCTIONAL,
            verification=VerificationMethod.TEST,
            parent="R-AUTO-01",
            derived_from=["R-AUTO-01"]
        )
        
        self.add_requirement(
            id="R-AUTO-03",
            text="The onboard system shall function independently and produce safe, "
                 "accurate, and verifiable optimal plans for escape safety in the "
                 "event of landing hazards.",
            type=RequirementType.SAFETY,
            verification=VerificationMethod.TEST,
            rationale="Mission survivability - no ground intervention possible"
        )
        
        self.add_requirement(
            id="R-AUTO-04",
            text="The GNC system shall manage resources, schedule and replay onboard "
                 "activities, and avoid safety constraint breaches during descent.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.TEST,
            parent="R-AUTO-03"
        )
    
    def _add_system_requirements(self):
        """System-level GNC requirements from Figure 4.18"""
        
        # Based on ECSS-E-ST-60-30C
        self.add_requirement(
            id="R-SYS-01",
            text="The GNC system shall provide attitude estimation with accuracy "
                 "better than 0.1 degrees (3σ).",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.ANALYSIS,
            rationale="Required for precise pointing during TAG operations"
        )
        
        self.add_requirement(
            id="R-SYS-02",
            text="The GNC system shall provide attitude control with stability "
                 "margin of at least 6 dB.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.ANALYSIS
        )
        
        self.add_requirement(
            id="R-SYS-03",
            text="The navigation system shall estimate translational orbital states "
                 "with position accuracy of 25 m (3σ) and velocity accuracy of "
                 "2.5 cm/s (3σ).",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST,
            rationale="Per OSIRIS-REx mission requirements for TAG operations"
        )
        
        self.add_requirement(
            id="R-SYS-04",
            text="The GNC system shall execute autonomous orbit insertion with "
                 "delta-V accuracy of ±5%.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-SYS-05",
            text="The control system shall limit steady-state pointing error to "
                 "less than 0.5 degrees.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST
        )
    
    def _add_rdv_requirements(self):
        """Rendezvous phase requirements from Figure 4.19 and Table 4.1"""
        
        self.add_requirement(
            id="R-RDV-01",
            text="The spacecraft shall approach from initial position [2500, 200, -50] km "
                 "to final position [20, 0, 0] km within 24 days.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.ANALYSIS,
            rationale="Mission timeline constraint"
        )
        
        self.add_requirement(
            id="R-RDV-02",
            text="The spacecraft shall arrive at home position (20 km) with position "
                 "accuracy of ±2.4 km (3σ).",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.ANALYSIS,
            rationale="From Table 4.1 - RDV Requirements"
        )
        
        self.add_requirement(
            id="R-RDV-03",
            text="The spacecraft shall arrive at home position with velocity accuracy "
                 "of ±0.12 m/s (3σ).",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.ANALYSIS,
            rationale="From Table 4.1 - RDV Requirements"
        )
        
        self.add_requirement(
            id="R-RDV-04",
            text="The spacecraft shall remain within the approach cone with 1° half-angle "
                 "and 1800 km length during rendezvous.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.ANALYSIS,
            rationale="Ensure adequate solar illumination of target"
        )
        
        self.add_requirement(
            id="R-RDV-05",
            text="The total delta-V for rendezvous shall not exceed 3.0 m/s.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.ANALYSIS,
            rationale="Propellant budget constraint"
        )
    
    def _add_tag_requirements(self):
        """Touch-And-Go requirements from Figure 4.17 and Table 4.3"""
        
        # Based on OSIRIS-REx and Marco Polo missions
        self.add_requirement(
            id="R-TAG-01",
            text="The GNC system shall deliver the spacecraft to within 25 meters of "
                 "the TAG site with 98.3% confidence (2.85σ for 2D Gaussian).",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST,
            rationale="OSIRIS-REx mission requirement for sample collection success"
        )
        
        self.add_requirement(
            id="R-TAG-02",
            text="The spacecraft attitude shall be aligned with local vertical within "
                 "10 degrees before touchdown.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.TEST,
            rationale="From Table 4.3 - ensure proper sampling mechanism orientation"
        )
        
        self.add_requirement(
            id="R-TAG-03",
            text="The vertical velocity shall be 10 ± 5 cm/s at touchdown.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST,
            rationale="From Table 4.3 - prevent bounce or excessive impact"
        )
        
        self.add_requirement(
            id="R-TAG-04",
            text="The horizontal velocity shall be less than 5 cm/s at touchdown.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST,
            rationale="From Table 4.3 - minimize lateral drift during contact"
        )
        
        self.add_requirement(
            id="R-TAG-05",
            text="The GNC system shall allow for three TAG attempts within the "
                 "propellant budget.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.ANALYSIS,
            rationale="Mission success probability - allow for contingencies"
        )
    
    def _add_gnc_functional_requirements(self):
        """Detailed GNC functional requirements from Table 3.2"""
        
        # Navigation requirements
        self.add_requirement(
            id="R-GNC-01",
            text="The navigation system shall estimate the full relative state "
                 "(position, velocity, attitude, angular rates) in real-time.",
            type=RequirementType.FUNCTIONAL,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-GNC-02",
            text="Visual information from optical sensors shall be incorporated "
                 "into the navigation system to improve state estimation accuracy.",
            type=RequirementType.FUNCTIONAL,
            verification=VerificationMethod.TEST,
            rationale="Enhanced accuracy for close-proximity operations"
        )
        
        # Guidance requirements
        self.add_requirement(
            id="R-GNC-10",
            text="The guidance system shall generate safe trajectories avoiding "
                 "obstacles with clearance margin of at least 5 meters.",
            type=RequirementType.SAFETY,
            verification=VerificationMethod.ANALYSIS
        )
        
        self.add_requirement(
            id="R-GNC-11",
            text="The guidance system shall recompute trajectories autonomously "
                 "when deviations exceed 10% of nominal values.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.TEST
        )
        
        # Control requirements  
        self.add_requirement(
            id="R-GNC-20",
            text="The control system shall maintain attitude within ±1 degree "
                 "of commanded orientation during thrusting.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-GNC-21",
            text="The control system shall execute maneuvers with thrust vector "
                 "pointing error less than 2 degrees.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST
        )
        
        # Hazard detection requirements
        self.add_requirement(
            id="R-GNC-48",
            text="The GNC system shall guide the S/C to the landing point without "
                 "hitting any obstacles.",
            type=RequirementType.SAFETY,
            verification=VerificationMethod.TEST,
            rationale="Critical safety requirement for TAG operations"
        )
        
        self.add_requirement(
            id="R-GNC-49",
            text="The asteroid shall remain within the field-of-view (FOV) during "
                 "Target Detection and Identification with 99.7% probability.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-GNC-50",
            text="The maximum approach velocity shall ensure that during TDI phase, "
                 "considering position uncertainty, the asteroid remains within FOV.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.ANALYSIS
        )
        
        # State estimation accuracy (from Table 3.2)
        self.add_requirement(
            id="R-GNC-51",
            text="The estimated position and velocity error during descent shall not exceed:\n"
                 "- Vertical position error: 25 m\n"
                 "- Vertical velocity error: 25 mm/s\n"
                 "- Horizontal position error: 30 m\n"
                 "- Horizontal velocity error: 30 mm/s",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST,
            rationale="Hayabusa2 mission heritage"
        )
        
        self.add_requirement(
            id="R-GNC-52",
            text="Visual information collected from optical sensors shall be "
                 "incorporated in the navigation system to improve state estimation.",
            type=RequirementType.FUNCTIONAL,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-GNC-53",
            text="The S/C attitude shall be aligned with the local vertical "
                 "before touchdown.",
            type=RequirementType.OPERATIONAL,
            verification=VerificationMethod.TEST
        )
        
        self.add_requirement(
            id="R-GNC-54",
            text="The S/C velocity shall be within ±8 cm/s horizontal and "
                 "10±5 cm/s vertical before touchdown.",
            type=RequirementType.PERFORMANCE,
            verification=VerificationMethod.TEST
        )
    
    def add_requirement(self, id: str, text: str, type: RequirementType,
                       verification: VerificationMethod, rationale: str = "",
                       parent: Optional[str] = None, 
                       derived_from: Optional[List[str]] = None) -> Requirement:
        """Add a requirement to the database"""
        req = Requirement(
            id=id,
            text=text,
            type=type,
            verification=verification,
            rationale=rationale,
            parent=parent,
            derived_from=derived_from or []
        )
        
        self.requirements[id] = req
        return req
    
    def get_requirement(self, req_id: str) -> Optional[Requirement]:
        """Retrieve a requirement by ID"""
        return self.requirements.get(req_id)
    
    def get_by_type(self, req_type: RequirementType) -> List[Requirement]:
        """Get all requirements of a specific type"""
        return [req for req in self.requirements.values() 
                if req.type == req_type]
    
    def get_by_verification(self, method: VerificationMethod) -> List[Requirement]:
        """Get all requirements verified by a specific method"""
        return [req for req in self.requirements.values() 
                if req.verification == method]
    
    def get_mandatory(self) -> List[Requirement]:
        """Get all mandatory (shall) requirements"""
        return [req for req in self.requirements.values() if req.is_mandatory()]
    
    def export_requirements_matrix(self) -> Dict:
        """Export requirements traceability matrix"""
        matrix = {
            "requirements": [],
            "verification_coverage": {},
            "type_distribution": {}
        }
        
        for req in self.requirements.values():
            matrix["requirements"].append({
                "id": req.id,
                "text": req.text,
                "type": req.type.value,
                "verification": req.verification.value,
                "parent": req.parent,
                "derived_from": req.derived_from
            })
        
        # Verification coverage
        for method in VerificationMethod:
            count = len(self.get_by_verification(method))
            matrix["verification_coverage"][method.value] = count
        
        # Type distribution
        for req_type in RequirementType:
            count = len(self.get_by_type(req_type))
            matrix["type_distribution"][req_type.value] = count
        
        return matrix


def main():
    """Example usage"""
    reqs = GNCRequirements()
    
    print("=== GNC System Requirements ===\n")
    
    print("Autonomous Requirements:")
    for req in [reqs.get_requirement(f"R-AUTO-0{i}") for i in range(1, 5)]:
        if req:
            print(f"\n{req.id}: {req.text[:100]}...")
            print(f"  Type: {req.type.value}")
            print(f"  Verification: {req.verification.value}")
    
    print("\n\nRDV Requirements:")
    for i in range(1, 6):
        req = reqs.get_requirement(f"R-RDV-0{i}")
        if req:
            print(f"\n{req.id}: {req.text[:80]}...")
    
    print("\n\nTAG Requirements:")
    for i in range(1, 6):
        req = reqs.get_requirement(f"R-TAG-0{i}")
        if req:
            print(f"\n{req.id}: {req.text[:80]}...")
    
    print("\n\n=== Requirements Statistics ===")
    matrix = reqs.export_requirements_matrix()
    print(f"\nTotal requirements: {len(matrix['requirements'])}")
    print("\nVerification coverage:")
    for method, count in matrix["verification_coverage"].items():
        print(f"  {method}: {count}")
    print("\nType distribution:")
    for req_type, count in matrix["type_distribution"].items():
        print(f"  {req_type}: {count}")


if __name__ == "__main__":
    main()
