# RC Servo Torque Estimator

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A command-line Python script designed to provide a theoretical estimate of the hinge torque required for the control surface servos of an RC aircraft (ailerons, elevator, and rudder).

---

## Table of Contents

- [About The Project](#about-the-project)
- [The Physics Behind the Calculation](#the-physics-behind-the-calculation)
- [How to Use](#how-to-use)
- [Input Parameters Explained](#input-parameters-explained)
- [Understanding the Output](#understanding-the-output)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [License](#license)

## About The Project

Choosing a servo with the appropriate torque is critical for the safety and performance of any RC aircraft. An under-powered servo can lead to control surface "blowback" at high speeds, resulting in a loss of control. A grossly overpowered servo adds unnecessary weight and cost.

This tool helps you move from guesswork to a data-driven decision by providing a baseline torque estimation based on key aerodynamic principles and aircraft dimensions.

## The Physics Behind the Calculation

The script estimates the servo torque by calculating the **Hinge Moment** of the control surface. This is the rotational force that the airflow exerts on the surface at its hinge line, which the servo must counteract.

The core formula used is:

$$ T = q \cdot S \cdot \bar{c} \cdot C_h $$

Where each component is:

| Variable | Symbol | Description |
| :--- | :---: | :--- |
| **Torque** | $T$ | The final hinge moment in Newton-meters (N·m), which the servo must overcome. |
| **Dynamic Pressure** | $q$ | The kinetic energy of the airflow, calculated as $q = 0.5 \cdot \rho \cdot V^2$. Here, $\rho$ (rho) is the air density and $V$ is the aircraft's velocity. |
| **Surface Area**| $S$ | The area of the movable part of the control surface (e.g., the aileron itself, not the entire wing). |
| **Mean Chord**| $\bar{c}$ | The average chord (width) of the movable control surface. |
| **Hinge Moment Coefficient** | $C_h$| A non-dimensional coefficient that depends on the airfoil shape, angle of attack, and control surface deflection angle. This is the most complex variable to determine without wind tunnel data. The script uses a conservative, general-purpose estimate (**-0.1** by default), which is a reasonable starting point for typical RC model flight envelopes. |


## How to Use

1.  **Download the Script:**
    Save the `servo_torque_estimator.py` file to your computer.

2.  **Run from the Terminal:**
    Open a terminal or command prompt, navigate to the directory where you saved the file, and run the script using Python:
    ```bash
    python servo_torque_estimator.py
    ```

3.  **Follow the Prompts:**
    The script will interactively ask for flight conditions and the dimensions of your aircraft's control surfaces. For each prompt, a default value is suggested in brackets `[e.g., ...]`.
    - To use your own value, type it in and press `Enter`.
    - To accept the suggested default value, simply press `Enter`.

## Input Parameters Explained

| Parameter | Prompt Text | Unit | Description |
| :--- | :--- | :--- | :--- |
| **Air Density** | `Air density (rho)` | kg/m³ | Density of the air. `1.225` is standard for sea level. |
| **Aircraft Velocity**| `Aircraft velocity (V)` | m/s | The maximum expected speed of your aircraft. Torque increases with the square of velocity. |
| **Hinge Moment Coeff.**| `Hinge Moment Coefficient (Ch)`| - | A non-dimensional factor. `-0.1` is a safe starting estimate for general sport flying. |
| **Span** | `... span` | meters| The length of the control surface from end to end. For the elevator, this is one half. |
| **Root Chord** | `... root chord` | meters | The width of the control surface at the end closest to the fuselage. |
| **Tip Chord** | `... tip chord` | meters | The width of the control surface at the end furthest from the fuselage. |

**Important:** All measurements must be for the **movable portion** of the control surface only, not the entire wing or stabilizer.

## Understanding the Output

The script provides the estimated torque in two common units:
* **N·m (Newton-meters):** The standard SI unit for torque.
* **kg-cm (kilogram-centimeters):** The most common unit used in RC servo specifications.

### The Golden Rule: Safety Margin
The results are a **theoretical minimum**. Real-world factors like linkage friction, propeller wash, and aggressive maneuvers will increase the required torque.

**Always choose a servo with a rating of 1.5x to 2x the estimated torque.** For example, if the script estimates 5 kg-cm, you should choose a servo rated for 7.5 kg-cm to 10 kg-cm.

### Ailerons vs. Elevator
* **Ailerons:** The calculation is for a **single aileron**. You will need **two servos**, each meeting the calculated torque requirement.
* **Elevator:** The calculation is for **one half of the elevator**.
    * If you use **one servo** for both halves, **multiply the result by 2**.
    * If you use **two servos** (one for each half), use the calculated value for **each servo**.

## Disclaimer

This is a theoretical tool for estimation purposes only. The accuracy of the output is entirely dependent on the accuracy of the input values and the generic nature of the Hinge Moment Coefficient. The author is not responsible for any damage to equipment or property resulting from the use of this script. Always err on the side of caution and prioritize safety in your aircraft's construction.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` file for more information.
