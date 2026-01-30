"""
Mission Objectives and Functional Tree
Based on Chapter 4 - Functional Analysis

This module defines the mission objectives tree and functional decomposition
for autonomous asteroid exploration missions, following MBSE methodology.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class ObjectiveType(Enum):
    """Types of mission objectives"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    FUNCTIONAL = "functional"


class MissionPhase(Enum):
    """Mission phases as defined in ConOps"""
    APPROACH = "approach"
    RENDEZVOUS = "rendezvous"
    HOVERING = "hovering"
    TAG_DESCENT = "tag_descent"
    TAG_SURFACE = "tag_surface"
    TAG_ASCENT = "tag_ascent"
    DEPARTURE = "departure"


@dataclass
class MissionObjective:
    """
    Represents a mission objective in the objectives tree
    
    Attributes:
        id: Unique identifier
        name: Objective name
        description: Detailed description
        type: Objective type (primary, secondary, functional)
        parent: Parent objective ID
        children: List of child objectives
        requirements: Associated requirements
        verification_method: How to verify this objective
    """
    id: str
    name: str
    description: str
    type: ObjectiveType
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    verification_method: Optional[str] = None
    
    def add_child(self, child_id: str):
        """Add a child objective"""
        if child_id not in self.children:
            self.children.append(child_id)
    
    def add_requirement(self, req_id: str):
        """Add an associated requirement"""
        if req_id not in self.requirements:
            self.requirements.append(req_id)


class MissionObjectivesTree:
    """
    Mission objectives tree as defined in Chapter 4, Section 4.1
    
    Main objectives:
    1. Rendezvous and Orbiting/Hovering with the asteroid
    2. Perform Touch-And-Go approach with the asteroid
    3. Departure and return to Earth
    4. Gather scientific data
    """
    
    def __init__(self):
        self.objectives: Dict[str, MissionObjective] = {}
        self._initialize_objectives_tree()
    
    def _initialize_objectives_tree(self):
        """Initialize the complete mission objectives tree"""
        
        # Top-level mission objective
        self.add_objective(
            id="OBJ-0",
            name="Asteroid Sample Return Mission",
            description="Autonomously explore asteroid, collect sample, and return to Earth",
            type=ObjectiveType.PRIMARY
        )
        
        # Primary objectives (Level 1)
        primary_objectives = [
            ("OBJ-1", "Rendezvous and Orbiting/Hovering", 
             "Approach and maintain stable position relative to asteroid"),
            ("OBJ-2", "Touch-And-Go Approach",
             "Perform controlled descent, sample collection, and ascent"),
            ("OBJ-3", "Departure and Earth Return",
             "Execute departure trajectory and return to Earth"),
            ("OBJ-4", "Scientific Data Collection",
             "Gather and transmit scientific measurements")
        ]
        
        for obj_id, name, desc in primary_objectives:
            self.add_objective(
                id=obj_id,
                name=name,
                description=desc,
                type=ObjectiveType.PRIMARY,
                parent="OBJ-0"
            )
        
        # Rendezvous objectives (OBJ-1 children)
        self._add_rendezvous_objectives()
        
        # TAG objectives (OBJ-2 children)
        self._add_tag_objectives()
    
    def _add_rendezvous_objectives(self):
        """Add rendezvous phase functional objectives"""
        
        # Main RDV function
        self.add_objective(
            id="OBJ-1.1",
            name="Manipulate Trajectory Autonomously",
            description="Control spacecraft trajectory and attitude in response to dynamic environment",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-1"
        )
        
        # State estimation
        self.add_objective(
            id="OBJ-1.1.1",
            name="Process Environment Knowledge",
            description="Combine sensor data for precise state estimation",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-1.1",
            requirements=["R-GNC-01", "R-GNC-02"]
        )
        
        # Sub-functions for state estimation
        state_est_functions = [
            ("OBJ-1.1.1.1", "Gather Telemetry Data"),
            ("OBJ-1.1.1.2", "Collect and Transmit Sensor Measurements"),
            ("OBJ-1.1.1.3", "Maintain Position via Active Control"),
            ("OBJ-1.1.1.4", "Perform Internal GNC Checks")
        ]
        
        for obj_id, name in state_est_functions:
            self.add_objective(
                id=obj_id,
                name=name,
                description=f"Function: {name}",
                type=ObjectiveType.FUNCTIONAL,
                parent="OBJ-1.1.1"
            )
        
        # Guidance and control
        self.add_objective(
            id="OBJ-1.1.2",
            name="Absorb Perturbation Torques",
            description="Use reaction wheels to manage angular momentum",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-1.1"
        )
        
        self.add_objective(
            id="OBJ-1.1.3",
            name="Encode Recovery Plans",
            description="Maintain alternative plans for environmental changes",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-1.1"
        )
        
        # Trajectory optimization
        self.add_objective(
            id="OBJ-1.2",
            name="Optimize Trajectory",
            description="Minimize propellant while meeting constraints",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-1"
        )
        
        # Detailed guidance functions
        guidance_functions = [
            ("OBJ-1.2.1", "Minimize Energy for Maneuvers"),
            ("OBJ-1.2.2", "Insert into Desired Orbit Autonomously"),
            ("OBJ-1.2.3", "Obtain Asteroid Position"),
            ("OBJ-1.2.4", "Perform Approach Sequence"),
            ("OBJ-1.2.5", "Localize and Target Asteroid"),
            ("OBJ-1.2.6", "Map Surface Features"),
            ("OBJ-1.2.7", "Detect and Track Target")
        ]
        
        for obj_id, name in guidance_functions:
            self.add_objective(
                id=obj_id,
                name=name,
                description=f"Guidance function: {name}",
                type=ObjectiveType.FUNCTIONAL,
                parent="OBJ-1.2"
            )
    
    def _add_tag_objectives(self):
        """Add Touch-And-Go phase functional objectives"""
        
        # Main TAG function
        self.add_objective(
            id="OBJ-2.1",
            name="Perform Soft Touchdown",
            description="Execute controlled descent, surface contact, and immediate ascent",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-2",
            requirements=["R-GNC-48", "R-GNC-49", "R-GNC-50"]
        )
        
        # TAG descent
        self.add_objective(
            id="OBJ-2.1.1",
            name="Orbit Insertion and Trim",
            description="Insert into proper orbit and perform trim burns",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-2.1"
        )
        
        self.add_objective(
            id="OBJ-2.1.2",
            name="Controlled Descent",
            description="Guide spacecraft to landing point avoiding obstacles",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-2.1"
        )
        
        # Descent sub-functions
        descent_functions = [
            ("OBJ-2.1.2.1", "Obtain Terrain Information", "R-GNC-51"),
            ("OBJ-2.1.2.2", "Compute Surface Normal Vector", None),
            ("OBJ-2.1.2.3", "Control Position and Attitude", "R-GNC-52"),
            ("OBJ-2.1.2.4", "Guide Without Hitting Obstacles", "R-GNC-48"),
            ("OBJ-2.1.2.5", "Stabilize at Touchdown Point", "R-GNC-53"),
            ("OBJ-2.1.2.6", "Control Vertical/Horizontal Velocity", "R-GNC-54")
        ]
        
        for obj_id, name, req in descent_functions:
            obj = self.add_objective(
                id=obj_id,
                name=name,
                description=f"TAG descent function: {name}",
                type=ObjectiveType.FUNCTIONAL,
                parent="OBJ-2.1.2"
            )
            if req:
                obj.add_requirement(req)
        
        # Ascent phase
        self.add_objective(
            id="OBJ-2.1.3",
            name="Ascend from Surface",
            description="Safely depart from asteroid surface",
            type=ObjectiveType.FUNCTIONAL,
            parent="OBJ-2.1"
        )
        
        ascent_functions = [
            ("OBJ-2.1.3.1", "Execute Health Checks"),
            ("OBJ-2.1.3.2", "Compute Attitude During Ascent"),
            ("OBJ-2.1.3.3", "Confirm State Parameters"),
            ("OBJ-2.1.3.4", "Execute Abort if Failure"),
            ("OBJ-2.1.3.5", "Command Safe Trajectory"),
            ("OBJ-2.1.3.6", "Cancel Gravitational Effects")
        ]
        
        for obj_id, name in ascent_functions:
            self.add_objective(
                id=obj_id,
                name=name,
                description=f"Ascent function: {name}",
                type=ObjectiveType.FUNCTIONAL,
                parent="OBJ-2.1.3"
            )
    
    def add_objective(self, id: str, name: str, description: str, 
                     type: ObjectiveType, parent: Optional[str] = None,
                     requirements: Optional[List[str]] = None) -> MissionObjective:
        """Add an objective to the tree"""
        obj = MissionObjective(
            id=id,
            name=name,
            description=description,
            type=type,
            parent=parent,
            requirements=requirements or []
        )
        
        self.objectives[id] = obj
        
        # Update parent's children list
        if parent and parent in self.objectives:
            self.objectives[parent].add_child(id)
        
        return obj
    
    def get_objective(self, obj_id: str) -> Optional[MissionObjective]:
        """Retrieve an objective by ID"""
        return self.objectives.get(obj_id)
    
    def get_children(self, obj_id: str) -> List[MissionObjective]:
        """Get all children of an objective"""
        obj = self.get_objective(obj_id)
        if not obj:
            return []
        return [self.objectives[child_id] for child_id in obj.children 
                if child_id in self.objectives]
    
    def get_objectives_by_phase(self, phase: MissionPhase) -> List[MissionObjective]:
        """Get all objectives for a specific mission phase"""
        phase_map = {
            MissionPhase.RENDEZVOUS: "OBJ-1",
            MissionPhase.TAG_DESCENT: "OBJ-2.1.2",
            MissionPhase.TAG_SURFACE: "OBJ-2.1",
            MissionPhase.TAG_ASCENT: "OBJ-2.1.3",
            MissionPhase.DEPARTURE: "OBJ-3"
        }
        
        root_id = phase_map.get(phase)
        if not root_id:
            return []
        
        # Get root and all descendants
        objectives = []
        to_process = [root_id]
        
        while to_process:
            current_id = to_process.pop(0)
            obj = self.get_objective(current_id)
            if obj:
                objectives.append(obj)
                to_process.extend(obj.children)
        
        return objectives
    
    def print_tree(self, obj_id: str = "OBJ-0", indent: int = 0):
        """Print the objectives tree"""
        obj = self.get_objective(obj_id)
        if not obj:
            return
        
        prefix = "  " * indent
        print(f"{prefix}{obj.id}: {obj.name}")
        if obj.requirements:
            print(f"{prefix}  Requirements: {', '.join(obj.requirements)}")
        
        for child_id in obj.children:
            self.print_tree(child_id, indent + 1)


def main():
    """Example usage"""
    tree = MissionObjectivesTree()
    
    print("=== Mission Objectives Tree ===\n")
    tree.print_tree()
    
    print("\n=== Rendezvous Phase Objectives ===")
    rdv_objectives = tree.get_objectives_by_phase(MissionPhase.RENDEZVOUS)
    for obj in rdv_objectives[:5]:  # Show first 5
        print(f"- {obj.id}: {obj.name}")
    
    print(f"\n=== TAG Descent Objectives ===")
    tag_objectives = tree.get_objectives_by_phase(MissionPhase.TAG_DESCENT)
    for obj in tag_objectives:
        print(f"- {obj.id}: {obj.name}")
        if obj.requirements:
            print(f"  Requirements: {', '.join(obj.requirements)}")


if __name__ == "__main__":
    main()
