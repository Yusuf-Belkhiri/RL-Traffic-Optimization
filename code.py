import traci
import sumolib
import os


# Set SUMO binary and configuration file path
SUMO_BINARY = "sumo-gui"  # or "sumo" for non-GUI mode
SUMO_CONFIG = "my_simulation.sumocfg"  # path to SUMO config file

# Start SUMO with TraCI
traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])

# Simulation parameters
step = 0
simulation_duration = 1000  # Run the simulation for 1000 steps

# try:
# Run the simulation step-by-step
while step < simulation_duration:
    print(step, " ", simulation_duration)
    traci.simulationStepLegacy()  # Advance one time step in the simulation

    # Example: Retrieve the number of vehicles on the highway
    highway_vehicle_count = len(traci.vehicle.getIDList())
    print(f"Step {step}: Number of vehicles on the highway: {highway_vehicle_count}")

    # # Example: Control a traffic light at a ramp
    # traffic_light_id = "ramp_traffic_light"  # Replace with traffic light ID
    # if step % 20 == 0:  # Every 20 steps, change the traffic light state
    #     current_phase = traci.trafficlight.getPhase(traffic_light_id)
    #     traci.trafficlight.setPhase(traffic_light_id, (current_phase + 1) % traci.trafficlight.getPhaseNumber(traffic_light_id))

    step += 1

# finally:
# Close the TraCI connection at the end
traci.close()
print("Simulation ended.")
