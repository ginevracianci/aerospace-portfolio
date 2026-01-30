"""
Sensor Suite for GNC System
Based on Chapter 5, Section 5.1 - State-of-the-art GNC technologies

Implements sensor models for:
- Inertial Measurement Unit (IMU)
- Star Tracker
- Sun Sensor
- Optical Camera
- LIDAR/Altimeter
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum


class SensorType(Enum):
    """Types of GNC sensors"""
    IMU = "imu"
    STAR_TRACKER = "star_tracker"
    SUN_SENSOR = "sun_sensor"
    OPTICAL_CAMERA = "optical_camera"
    LIDAR = "lidar"
    ALTIMETER = "altimeter"


@dataclass
class SensorMeasurement:
    """
    Generic sensor measurement
    
    Attributes:
        sensor_type: Type of sensor
        data: Measurement data
        timestamp: Measurement time [s]
        valid: Whether measurement is valid
        uncertainty: Measurement uncertainty (standard deviation)
    """
    sensor_type: SensorType
    data: np.ndarray
    timestamp: float
    valid: bool = True
    uncertainty: Optional[np.ndarray] = None


class IMU:
    """
    Inertial Measurement Unit
    
    Combines 3 accelerometers and 3 gyroscopes for 6-DOF motion sensing.
    Used for attitude propagation between star tracker updates.
    
    From Chapter 5: "Accelerometers and gyroscopes measure changes in velocity
    and angle, respectively... IMU may be employed for attitude propagation
    between star tracker updates if the control system needs precise knowledge."
    """
    
    def __init__(self, noise_accel: float = 1e-4, noise_gyro: float = 1e-6,
                 bias_accel: np.ndarray = None, bias_gyro: np.ndarray = None):
        """
        Initialize IMU
        
        Args:
            noise_accel: Accelerometer noise std [m/s²]
            noise_gyro: Gyroscope noise std [rad/s]
            bias_accel: Accelerometer bias [m/s²]
            bias_gyro: Gyroscope bias [rad/s]
        """
        self.noise_accel = noise_accel
        self.noise_gyro = noise_gyro
        self.bias_accel = bias_accel if bias_accel is not None else np.zeros(3)
        self.bias_gyro = bias_gyro if bias_gyro is not None else np.zeros(3)
        
        # Measurement history for bias estimation
        self.accel_history = []
        self.gyro_history = []
    
    def measure(self, true_acceleration: np.ndarray, true_angular_rate: np.ndarray,
                timestamp: float) -> SensorMeasurement:
        """
        Simulate IMU measurement
        
        Args:
            true_acceleration: True specific force [m/s²]
            true_angular_rate: True angular velocity [rad/s]
            timestamp: Measurement time [s]
            
        Returns:
            Combined IMU measurement (acceleration + angular rate)
        """
        # Add noise and bias to accelerometer
        accel_noise = np.random.normal(0, self.noise_accel, 3)
        measured_accel = true_acceleration + self.bias_accel + accel_noise
        
        # Add noise and bias to gyroscope
        gyro_noise = np.random.normal(0, self.noise_gyro, 3)
        measured_gyro = true_angular_rate + self.bias_gyro + gyro_noise
        
        # Store history
        self.accel_history.append(measured_accel)
        self.gyro_history.append(measured_gyro)
        
        # Combine measurements [ax, ay, az, wx, wy, wz]
        data = np.concatenate([measured_accel, measured_gyro])
        uncertainty = np.concatenate([
            np.full(3, self.noise_accel),
            np.full(3, self.noise_gyro)
        ])
        
        return SensorMeasurement(
            sensor_type=SensorType.IMU,
            data=data,
            timestamp=timestamp,
            uncertainty=uncertainty
        )


class StarTracker:
    """
    Star Tracker
    
    Provides precise 3-axis attitude by comparing digital images with star catalog.
    
    From Chapter 5: "Through the comparison of a digital picture with an onboard
    star catalog, a star tracker may yield a precise approximation of the absolute
    three-axis attitude... numerous stars are identified and tracked, and a
    three-axis attitude is provided numerous times per second."
    """
    
    def __init__(self, noise_attitude: float = np.radians(0.001)):
        """
        Initialize star tracker
        
        Args:
            noise_attitude: Attitude measurement noise [rad] (~0.001° typical)
        """
        self.noise_attitude = noise_attitude
        self.update_rate = 5.0  # Hz (typical for star trackers)
    
    def measure(self, true_attitude: np.ndarray, 
                timestamp: float) -> SensorMeasurement:
        """
        Measure spacecraft attitude
        
        Args:
            true_attitude: True attitude quaternion [q0, q1, q2, q3]
            timestamp: Measurement time [s]
            
        Returns:
            Attitude measurement
        """
        # Add noise to quaternion (simplified model)
        noise = np.random.normal(0, self.noise_attitude, 4)
        measured_attitude = true_attitude + noise
        
        # Normalize quaternion
        measured_attitude = measured_attitude / np.linalg.norm(measured_attitude)
        
        return SensorMeasurement(
            sensor_type=SensorType.STAR_TRACKER,
            data=measured_attitude,
            timestamp=timestamp,
            uncertainty=np.full(4, self.noise_attitude)
        )


class SunSensor:
    """
    Sun Sensor
    
    Determines Sun orientation within spacecraft body frame.
    
    From Chapter 5: "To determine the Sun's orientation within a spacecraft's
    body frame, sun sensors are employed... The Sun is highly bright and clearly
    recognizable, therefore problem detection and recovery commonly employ Sun sensors."
    """
    
    def __init__(self, noise_angle: float = np.radians(0.5)):
        """
        Initialize sun sensor
        
        Args:
            noise_angle: Angular measurement noise [rad] (~0.5° typical)
        """
        self.noise_angle = noise_angle
        self.fov = np.radians(120)  # Field of view [rad]
    
    def measure(self, sun_direction_body: np.ndarray,
                timestamp: float) -> SensorMeasurement:
        """
        Measure sun direction in body frame
        
        Args:
            sun_direction_body: True sun direction unit vector in body frame
            timestamp: Measurement time [s]
            
        Returns:
            Sun direction measurement
        """
        # Check if sun is in FOV
        z_body = np.array([0, 0, 1])
        angle_from_z = np.arccos(np.dot(sun_direction_body, z_body))
        
        valid = angle_from_z < (self.fov / 2)
        
        if not valid:
            return SensorMeasurement(
                sensor_type=SensorType.SUN_SENSOR,
                data=np.zeros(3),
                timestamp=timestamp,
                valid=False
            )
        
        # Add noise
        noise = np.random.normal(0, self.noise_angle, 2)
        
        # Convert to azimuth/elevation (simplified)
        azimuth = np.arctan2(sun_direction_body[1], sun_direction_body[0]) + noise[0]
        elevation = np.arcsin(sun_direction_body[2]) + noise[1]
        
        # Reconstruct unit vector
        measured_direction = np.array([
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation)
        ])
        
        return SensorMeasurement(
            sensor_type=SensorType.SUN_SENSOR,
            data=measured_direction,
            timestamp=timestamp,
            valid=True,
            uncertainty=np.full(3, self.noise_angle)
        )


class OpticalCamera:
    """
    Optical Navigation Camera
    
    Provides line-of-sight measurements to asteroid for relative navigation.
    
    From Chapter 5: "Relative or absolute estimates of the spacecraft's location,
    velocity, and attitude are produced based on observations from several sensors.
    Surface optical measurements are typically included during small body descent."
    """
    
    def __init__(self, focal_length: float = 0.1, pixel_size: float = 5e-6,
                 resolution: Tuple[int, int] = (1024, 1024)):
        """
        Initialize optical camera
        
        Args:
            focal_length: Focal length [m]
            pixel_size: Pixel size [m]
            resolution: Image resolution (width, height) [pixels]
        """
        self.focal_length = focal_length
        self.pixel_size = pixel_size
        self.resolution = resolution
        self.fov = 2 * np.arctan(resolution[0] * pixel_size / (2 * focal_length))
    
    def measure(self, target_position_body: np.ndarray,
                timestamp: float) -> SensorMeasurement:
        """
        Measure line-of-sight to target
        
        Args:
            target_position_body: Target position in body frame [m]
            timestamp: Measurement time [s]
            
        Returns:
            Line-of-sight unit vector measurement
        """
        # Convert to unit vector
        distance = np.linalg.norm(target_position_body)
        los_direction = target_position_body / distance
        
        # Check if in FOV (simplified - assume camera points along +Z)
        z_body = np.array([0, 0, 1])
        angle_from_z = np.arccos(np.dot(los_direction, z_body))
        
        valid = angle_from_z < (self.fov / 2)
        
        if not valid:
            return SensorMeasurement(
                sensor_type=SensorType.OPTICAL_CAMERA,
                data=np.zeros(3),
                timestamp=timestamp,
                valid=False
            )
        
        # Pixel noise (1 pixel typical)
        angular_noise = self.pixel_size / self.focal_length
        noise = np.random.normal(0, angular_noise, 2)
        
        # Add noise to azimuth/elevation
        azimuth = np.arctan2(los_direction[1], los_direction[0]) + noise[0]
        elevation = np.arcsin(los_direction[2]) + noise[1]
        
        # Reconstruct direction
        measured_los = np.array([
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation)
        ])
        
        return SensorMeasurement(
            sensor_type=SensorType.OPTICAL_CAMERA,
            data=measured_los,
            timestamp=timestamp,
            valid=True,
            uncertainty=np.full(3, angular_noise)
        )


class LIDAR:
    """
    LIDAR (Light Detection and Ranging)
    
    Provides range and surface normal measurements for proximity operations.
    
    From Hayabusa2 (Chapter 4): "A laser range finder (LRF) system is activated...
    The LRF system produces the attitude perpendicular to the local surface."
    """
    
    def __init__(self, range_noise: float = 0.1, max_range: float = 5000.0):
        """
        Initialize LIDAR
        
        Args:
            range_noise: Range measurement noise [m]
            max_range: Maximum measurement range [m]
        """
        self.range_noise = range_noise
        self.max_range = max_range
    
    def measure(self, target_distance: float, surface_normal: np.ndarray,
                timestamp: float) -> SensorMeasurement:
        """
        Measure range and surface normal
        
        Args:
            target_distance: True distance to target [m]
            surface_normal: Surface normal unit vector
            timestamp: Measurement time [s]
            
        Returns:
            Range + surface normal measurement [range, nx, ny, nz]
        """
        valid = target_distance <= self.max_range
        
        if not valid:
            return SensorMeasurement(
                sensor_type=SensorType.LIDAR,
                data=np.zeros(4),
                timestamp=timestamp,
                valid=False
            )
        
        # Measure range with noise
        measured_range = target_distance + np.random.normal(0, self.range_noise)
        
        # Surface normal with small angular noise
        normal_noise = np.random.normal(0, np.radians(1), 3)
        measured_normal = surface_normal + normal_noise
        measured_normal = measured_normal / np.linalg.norm(measured_normal)
        
        # Combine: [range, nx, ny, nz]
        data = np.concatenate([[measured_range], measured_normal])
        
        return SensorMeasurement(
            sensor_type=SensorType.LIDAR,
            data=data,
            timestamp=timestamp,
            valid=True,
            uncertainty=np.array([self.range_noise, 
                                 np.radians(1), np.radians(1), np.radians(1)])
        )


class SensorSuite:
    """
    Complete sensor suite for GNC system
    
    Manages all sensors and provides unified interface for measurements.
    """
    
    def __init__(self):
        """Initialize complete sensor suite"""
        self.imu = IMU()
        self.star_tracker = StarTracker()
        self.sun_sensor = SunSensor()
        self.optical_camera = OpticalCamera()
        self.lidar = LIDAR()
        
        self.measurements = {}
    
    def get_all_measurements(self, spacecraft_state: dict, 
                           timestamp: float) -> dict:
        """
        Get measurements from all sensors
        
        Args:
            spacecraft_state: Dictionary with true spacecraft state
            timestamp: Current time [s]
            
        Returns:
            Dictionary of measurements from all sensors
        """
        measurements = {}
        
        # IMU
        measurements['imu'] = self.imu.measure(
            spacecraft_state['acceleration'],
            spacecraft_state['angular_rate'],
            timestamp
        )
        
        # Star Tracker
        measurements['star_tracker'] = self.star_tracker.measure(
            spacecraft_state['attitude'],
            timestamp
        )
        
        # Sun Sensor
        if 'sun_direction' in spacecraft_state:
            measurements['sun_sensor'] = self.sun_sensor.measure(
                spacecraft_state['sun_direction'],
                timestamp
            )
        
        # Optical Camera
        if 'target_position_body' in spacecraft_state:
            measurements['optical_camera'] = self.optical_camera.measure(
                spacecraft_state['target_position_body'],
                timestamp
            )
        
        # LIDAR
        if 'target_distance' in spacecraft_state:
            measurements['lidar'] = self.lidar.measure(
                spacecraft_state['target_distance'],
                spacecraft_state.get('surface_normal', np.array([0, 0, 1])),
                timestamp
            )
        
        self.measurements = measurements
        return measurements


def main():
    """Example sensor suite usage"""
    print("=== GNC Sensor Suite Demo ===\n")
    
    # Initialize sensors
    suite = SensorSuite()
    
    # Simulate spacecraft state
    state = {
        'acceleration': np.array([0.01, 0.005, -0.002]),  # m/s²
        'angular_rate': np.array([0.001, -0.0005, 0.0002]),  # rad/s
        'attitude': np.array([1, 0, 0, 0]),  # quaternion
        'sun_direction': np.array([0.5, 0.3, 0.8]) / np.linalg.norm([0.5, 0.3, 0.8]),
        'target_position_body': np.array([100, 50, 200]),  # m
        'target_distance': 223.6,  # m
        'surface_normal': np.array([0, 0, 1])
    }
    
    # Get measurements
    measurements = suite.get_all_measurements(state, timestamp=0.0)
    
    print("Sensor Measurements:")
    for sensor_name, meas in measurements.items():
        print(f"\n{sensor_name.upper()}:")
        print(f"  Valid: {meas.valid}")
        if meas.valid:
            print(f"  Data: {meas.data}")
            if meas.uncertainty is not None:
                print(f"  Uncertainty: {meas.uncertainty}")


if __name__ == "__main__":
    main()
