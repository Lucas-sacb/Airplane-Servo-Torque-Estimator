# -*- coding: utf-8 -*-
"""
RC Aircraft Control Surface Servo Torque Estimator

This script calculates the estimated hinge torque required for the servos of an
RC aircraft's control surfaces (ailerons, elevator, and rudder).

The calculation is based on the standard aerodynamic hinge moment formula:
Torque = q * S * c_bar * C_h

by lucas-santos Adelphi 2021
"""

import math

# --- 1. CONSTANTS ---
# Conversion factor from Newton-meters (N.m) to kilogram-centimeters (kg-cm)
NM_TO_KGCM = 10.1972

# --- 2. HELPER FUNCTIONS ---

def get_user_input(prompt_text, default_value, input_type=float):
    """
    Prompts the user for an input, providing a default value.
    Returns the user's input or the default if nothing is entered.
    """
    try:
        user_value = input(f"{prompt_text} [e.g., {default_value}]: ")
        if user_value == "":
            return input_type(default_value)
        return input_type(user_value)
    except ValueError:
        print(f"Invalid input. Using default value: {default_value}")
        return input_type(default_value)

def calculate_trapezoid_area(root_chord, tip_chord, span):
    """Calculates the area of a trapezoidal wing or surface."""
    return (root_chord + tip_chord) * span / 2.0

def calculate_mean_aerodynamic_chord(root_chord, tip_chord):
    """Calculates the Mean Aerodynamic Chord (MAC) for a trapezoidal surface."""
    return (root_chord + tip_chord) / 2.0

def calculate_hinge_torque(dynamic_pressure, surface_area, mean_chord, hinge_coeff):
    """
    Calculates the hinge moment (torque) for a control surface.
    The result is converted to kg-cm, a common unit for RC servos.
    """
    torque_nm = dynamic_pressure * surface_area * mean_chord * abs(hinge_coeff)
    torque_kg_cm = torque_nm * NM_TO_KGCM
    return torque_nm, torque_kg_cm

def process_surface(name, defaults, dynamic_pressure):
    """
    Processes a single control surface: gets inputs, calculates, and returns results.
    """
    print(f"\n--- {name} Parameters {defaults['note']} ---")
    
    hinge_coeff = get_user_input(f"{name} Hinge Moment Coefficient (Ch)", defaults['ch'])
    span = get_user_input(f"{name} span in meters", defaults['span'])
    root_chord = get_user_input(f"{name} root chord in meters", defaults['root_chord'])
    tip_chord = get_user_input(f"{name} tip chord in meters", defaults['tip_chord'])

    area = calculate_trapezoid_area(root_chord, tip_chord, span)
    mean_chord = calculate_mean_aerodynamic_chord(root_chord, tip_chord)
    
    torque_nm, torque_kgcm = calculate_hinge_torque(
        dynamic_pressure, area, mean_chord, hinge_coeff
    )
    
    # Return all results in a dictionary for easy access
    return {"name": name, "ch": hinge_coeff, "torque_nm": torque_nm, "torque_kgcm": torque_kgcm}

# --- 3. MAIN EXECUTION FUNCTION ---

def run_servo_torque_estimation():
    """
    Main function to guide the user through the calculation process.
    """
    print("--- RC Servo Torque Estimator ---")
    print("Enter the flight conditions and aircraft parameters in the specified units.")

    # --- Flight Conditions ---
    print("\n--- Flight Conditions ---")
    air_density = get_user_input("Air density (rho) in kg/m^3", 1.225)
    velocity = get_user_input("Aircraft velocity (V) in m/s", 18.0)
    
    dynamic_pressure = 0.5 * air_density * (velocity ** 2)
    print(f"\nCalculated Dynamic Pressure (q): {dynamic_pressure:.2f} N/m^2")

    # --- Surface Data and Calculations ---
    # A dictionary to hold default values for each surface
    surface_defaults = {
        "Aileron":  {"ch": -0.15, "span": 0.924, "root_chord": 0.110, "tip_chord": 0.050, "note": "(Single Aileron)"},
        "Elevator": {"ch": -0.10, "span": 0.318, "root_chord": 0.225, "tip_chord": 0.225, "note": "(One Half of the Elevator)"},
        "Rudder":   {"ch": -0.10, "span": 0.308, "root_chord": 0.200, "tip_chord": 0.150, "note": ""}
    }

    results = []
    for name, defaults in surface_defaults.items():
        surface_result = process_surface(name, defaults, dynamic_pressure)
        results.append(surface_result)

    # --- Display Results ---
    print("\n--- ESTIMATED SERVO TORQUE REQUIREMENTS ---")
    for res in results:
        print(f"\nFor the {res['name']} (using Ch = {res['ch']}):")
        print(f"  - Required Torque: {res['torque_nm']:.4f} N.m")
        print(f"  - Required Torque: {res['torque_kgcm']:.2f} kg-cm")
    
    print("\nDisclaimer: This is a theoretical estimation. Always choose a servo with a safety margin (e.g., 1.5x to 2x the estimated torque).")

# --- 4. SCRIPT EXECUTION ---

if __name__ == "__main__":
    run_servo_torque_estimation()
