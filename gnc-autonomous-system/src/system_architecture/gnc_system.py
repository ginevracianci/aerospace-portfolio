"""
GNC System Architecture
Based on Chapter 5 - System Architecture Definition

Implements the complete GNC system following the Hayabusa2 heritage architecture
with autonomous guidance, navigation, and control capabilities.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


class GNCMode(Enum):
    """GNC operational modes"""
    SAFE = "safe"
    CRUISE = "cruise"
    APPROACH = "approach"
    PROXIMITY = "proximity"
    TAG_DESCENT = "tag_descent"
    TAG_SURFACE = "tag_surface"
    TAG_ASCENT = "tag_ascent"


class ControlAuthority(Enum):
    """Control authority levels"""
    GROUND = "ground"
    AUTONOMOUS = "autonomous"
    HYBRID = "hybrid"


@dataclass
class GNCState:
    """
    Complete GNC state vector
    
    Attributes:
        position: [x, y, z] in LVLH frame [m]
        velocity: [vx, vy, vz] in LVLH frame [m/s]
        attitude: Quaternion [q0, q1, q2, q3]
        angular_rate: [wx, wy, wz] [rad/s]
        timestamp: Time [s]
    """
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))
    attitude: np.ndarray = field(default_factory=lambda: np.array([1, 0, 0, 0]))
    angular_rate: np.ndarray = field(default_factory=lambda: np.zeros(3))
    timestamp: float = 0.0
    
    def __post_init__(self):
        """Ensure arrays are numpy arrays"""
        self.position = np.asarray(self.position)
        self.velocity = np.asarray(self.velocity)
        self.attitude = np.asarray(self.attitude)
        self.angular_rate = np.asarray(self.angular_rate)


@dataclass
class GNCCommand:
    """
    GNC control commands
    
    Attributes:
        thrust_vector: [Fx, Fy, Fz] [N]
        torque_vector: [Tx, Ty, Tz] [Nm]
        reaction_wheel_speeds: [w1, w2, w3, w4] [rad/s]
        timestamp: Time [s]
    """
    thrust_vector: np.ndarray = field(default_factory=lambda: np.zeros(3))
    torque_vector: np.ndarray = field(default_factory=lambda: np.zeros(3))
    reaction_wheel_speeds: np.ndarray = field(default_factory=lambda: np.zeros(4))
    timestamp: float = 0.0


class GNCSystem:
    """
    Main GNC System Architecture
    
    Implements the functional architecture from Figure 5.2, including:
    - Navigation filter for state estimation
    - Guidance logic for trajectory generation
    - Control modules for attitude and orbit control
    
    Based on Hayabusa mission heritage (Figure 5.1).
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize GNC system
        
        Args:
            config: Configuration dictionary with system parameters
        """
        self.config = config or self._default_config()
        
        # GNC mode and authority
        self.mode = GNCMode.SAFE
        self.authority = ControlAuthority.GROUND
        
        # State variables
        self.current_state = GNCState()
        self.desired_state = GNCState()
        self.last_command = GNCCommand()
        
        # Subsystem interfaces (to be connected)
        self.navigation = None
        self.guidance = None
        self.control = None
        self.sensors = None
        self.actuators = None
        
        # Performance monitoring
        self.performance_log = {
            'position_error': [],
            'velocity_error': [],
            'attitude_error': [],
            'control_effort': [],
            'timestamps': []
        }
    
    def _default_config(self) -> Dict:
        """Default configuration following mission requirements"""
        return {
            # Mission parameters (from Table 4.1, Table 4.3)
            'rdv_arrival_position': np.array([20.0, 0.0, 0.0]),  # km
            'rdv_position_tolerance': 2.4,  # km (3σ)
            'rdv_velocity_tolerance': 0.12,  # m/s (3σ)
            'tag_landing_accuracy': 25.0,  # m
            'tag_attitude_tolerance': 10.0,  # degrees
            'tag_vertical_velocity': 0.10,  # m/s
            'tag_horizontal_velocity': 0.05,  # m/s
            
            # Control parameters
            'control_frequency': 10.0,  # Hz
            'navigation_frequency': 5.0,  # Hz
            'guidance_frequency': 1.0,  # Hz
            
            # Safety parameters
            'min_safe_distance': 50.0,  # m
            'max_approach_velocity': 0.5,  # m/s
            'abort_altitude': 100.0,  # m
            
            # Performance requirements (from R-SYS requirements)
            'attitude_accuracy': 0.1,  # degrees (3σ)
            'position_accuracy': 25.0,  # m (3σ)
            'velocity_accuracy': 0.025,  # m/s (3σ)
        }
    
    def initialize_subsystems(self, navigation, guidance, control,
                             sensors, actuators):
        """
        Connect GNC subsystems
        
        Args:
            navigation: Navigation filter instance
            guidance: Guidance module instance
            control: Control module instance
            sensors: Sensor suite instance
            actuators: Actuator suite instance
        """
        self.navigation = navigation
        self.guidance = guidance
        self.control = control
        self.sensors = sensors
        self.actuators = actuators
    
    def set_mode(self, mode: GNCMode):
        """
        Change GNC operational mode
        
        Args:
            mode: New GNC mode
        """
        print(f"GNC Mode transition: {self.mode.value} -> {mode.value}")
        self.mode = mode
        
        # Mode-specific initialization
        if mode == GNCMode.TAG_DESCENT:
            self._initialize_tag_descent()
        elif mode == GNCMode.PROXIMITY:
            self._initialize_proximity_operations()
    
    def set_authority(self, authority: ControlAuthority):
        """
        Set control authority level
        
        Args:
            authority: Control authority (ground/autonomous/hybrid)
        """
        self.authority = authority
        print(f"Control authority: {authority.value}")
    
    def _initialize_tag_descent(self):
        """Initialize TAG descent phase"""
        # Set conservative limits for descent
        self.config['max_approach_velocity'] = 0.1  # m/s
        print("TAG descent initialized - entering autonomous control")
    
    def _initialize_proximity_operations(self):
        """Initialize proximity operations"""
        self.config['max_approach_velocity'] = 0.3  # m/s
        print("Proximity operations initialized")
    
    def guidance_cycle(self, target_state: GNCState) -> GNCState:
        """
        Execute guidance cycle
        
        Generates desired trajectory based on current and target states.
        
        Args:
            target_state: Desired final state
            
        Returns:
            Commanded state for next time step
        """
        if self.guidance is None:
            return self.current_state
        
        # Guidance generates desired state trajectory
        commanded_state = self.guidance.compute_command(
            current=self.current_state,
            target=target_state,
            mode=self.mode
        )
        
        self.desired_state = commanded_state
        return commanded_state
    
    def navigation_cycle(self, sensor_data: Dict) -> GNCState:
        """
        Execute navigation cycle
        
        Estimates current state from sensor measurements.
        
        Args:
            sensor_data: Dictionary of sensor measurements
            
        Returns:
            Estimated current state
        """
        if self.navigation is None:
            return self.current_state
        
        # Navigation estimates state from sensor data
        estimated_state = self.navigation.update(
            sensor_data=sensor_data,
            previous_state=self.current_state
        )
        
        self.current_state = estimated_state
        return estimated_state
    
    def control_cycle(self) -> GNCCommand:
        """
        Execute control cycle
        
        Computes control commands to track desired state.
        
        Returns:
            Control commands for actuators
        """
        if self.control is None:
            return GNCCommand()
        
        # Control computes commands to minimize state error
        command = self.control.compute_command(
            current_state=self.current_state,
            desired_state=self.desired_state,
            mode=self.mode
        )
        
        self.last_command = command
        return command
    
    def execute_gnc_loop(self, sensor_data: Dict, target_state: GNCState,
                        dt: float) -> Tuple[GNCState, GNCCommand]:
        """
        Execute complete GNC loop
        
        This is the main control loop that executes:
        1. Navigation: Estimate current state
        2. Guidance: Compute desired state
        3. Control: Generate commands
        
        Args:
            sensor_data: Current sensor measurements
            target_state: Target state to achieve
            dt: Time step [s]
            
        Returns:
            Tuple of (estimated_state, control_command)
        """
        # 1. Navigation: State estimation
        current_state = self.navigation_cycle(sensor_data)
        
        # 2. Guidance: Trajectory generation
        desired_state = self.guidance_cycle(target_state)
        
        # 3. Control: Command generation
        command = self.control_cycle()
        
        # 4. Log performance
        self._log_performance(dt)
        
        # 5. Safety checks
        if not self._safety_check():
            command = self._generate_safe_command()
        
        return current_state, command
    
    def _safety_check(self) -> bool:
        """
        Perform safety checks
        
        Returns:
            True if safe to continue, False if abort needed
        """
        # Check distance to target
        distance = np.linalg.norm(self.current_state.position)
        if distance < self.config['min_safe_distance']:
            if self.mode not in [GNCMode.TAG_DESCENT, GNCMode.TAG_SURFACE]:
                print(f"WARNING: Too close to target: {distance:.1f} m")
                return False
        
        # Check velocity magnitude
        velocity = np.linalg.norm(self.current_state.velocity)
        if velocity > self.config['max_approach_velocity']:
            print(f"WARNING: Velocity too high: {velocity:.3f} m/s")
            return False
        
        return True
    
    def _generate_safe_command(self) -> GNCCommand:
        """
        Generate safe abort command
        
        Returns:
            Command to move spacecraft to safe state
        """
        print("Generating SAFE command - aborting maneuver")
        
        # Point away from target and apply thrust
        abort_direction = self.current_state.position / \
                         np.linalg.norm(self.current_state.position)
        
        return GNCCommand(
            thrust_vector=abort_direction * 5.0,  # 5 N away from target
            torque_vector=np.zeros(3),
            timestamp=self.current_state.timestamp
        )
    
    def _log_performance(self, dt: float):
        """Log current performance metrics"""
        pos_error = np.linalg.norm(
            self.current_state.position - self.desired_state.position
        )
        vel_error = np.linalg.norm(
            self.current_state.velocity - self.desired_state.velocity
        )
        
        # Attitude error (simple quaternion difference magnitude)
        att_error = np.linalg.norm(
            self.current_state.attitude - self.desired_state.attitude
        )
        
        control_effort = np.linalg.norm(self.last_command.thrust_vector)
        
        self.performance_log['position_error'].append(pos_error)
        self.performance_log['velocity_error'].append(vel_error)
        self.performance_log['attitude_error'].append(att_error)
        self.performance_log['control_effort'].append(control_effort)
        self.performance_log['timestamps'].append(self.current_state.timestamp)
    
    def check_requirements_compliance(self) -> Dict[str, bool]:
        """
        Check if current performance meets requirements
        
        Returns:
            Dictionary of requirement IDs and compliance status
        """
        compliance = {}
        
        if len(self.performance_log['position_error']) == 0:
            return compliance
        
        # R-SYS-03: Position accuracy 25 m (3σ)
        recent_pos_errors = self.performance_log['position_error'][-100:]
        pos_std = np.std(recent_pos_errors)
        compliance['R-SYS-03-position'] = pos_std * 3 <= 25.0
        
        # R-SYS-03: Velocity accuracy 2.5 cm/s (3σ)
        recent_vel_errors = self.performance_log['velocity_error'][-100:]
        vel_std = np.std(recent_vel_errors)
        compliance['R-SYS-03-velocity'] = vel_std * 3 <= 0.025
        
        # R-SYS-01: Attitude accuracy 0.1 deg (3σ)
        recent_att_errors = self.performance_log['attitude_error'][-100:]
        att_std = np.std(recent_att_errors)
        compliance['R-SYS-01'] = att_std * 3 <= np.radians(0.1)
        
        return compliance
    
    def get_performance_summary(self) -> Dict:
        """
        Get summary of GNC performance
        
        Returns:
            Dictionary with performance statistics
        """
        if len(self.performance_log['timestamps']) == 0:
            return {}
        
        return {
            'mission_duration': self.performance_log['timestamps'][-1],
            'mean_position_error': np.mean(self.performance_log['position_error']),
            'std_position_error': np.std(self.performance_log['position_error']),
            'mean_velocity_error': np.mean(self.performance_log['velocity_error']),
            'std_velocity_error': np.std(self.performance_log['velocity_error']),
            'total_control_effort': np.sum(self.performance_log['control_effort']),
            'requirements_compliance': self.check_requirements_compliance()
        }


def main():
    """Example GNC system setup"""
    
    print("=== GNC System Architecture Demo ===\n")
    
    # Initialize GNC system
    gnc = GNCSystem()
    
    print("Configuration:")
    for key, value in gnc.config.items():
        if isinstance(value, np.ndarray):
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {value}")
    
    print("\n=== Mode Transitions ===")
    gnc.set_mode(GNCMode.CRUISE)
    gnc.set_mode(GNCMode.APPROACH)
    gnc.set_mode(GNCMode.TAG_DESCENT)
    
    print("\n=== Authority Levels ===")
    gnc.set_authority(ControlAuthority.GROUND)
    gnc.set_authority(ControlAuthority.AUTONOMOUS)
    
    # Simulate some state updates
    gnc.current_state.position = np.array([1000.0, 100.0, -50.0])
    gnc.current_state.velocity = np.array([0.5, 0.1, -0.05])
    
    print(f"\nCurrent State:")
    print(f"  Position: {gnc.current_state.position} m")
    print(f"  Velocity: {gnc.current_state.velocity} m/s")
    
    # Safety check
    print(f"\nSafety check: {'PASS' if gnc._safety_check() else 'FAIL'}")
    
    print("\n=== GNC System Ready ===")


if __name__ == "__main__":
    main()
