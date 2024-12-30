import traci
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import math



def get_distance(pos1, pos2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)





def get_nearest_vehicle_distance(junction_id, edge_id):
    """
    Get the smallest distance between a junction (traffic light) and the nearest vehicle on a specific edge.

    Returns:
    - Smallest distance to the nearest vehicle or 150 if no vehicles are on the edge.
    """
    # Get the position of the junction
    junction_position = traci.junction.getPosition(junction_id)
    
    # Get the list of vehicle IDs on the specified edge
    vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
    
    if not vehicle_ids:
        return float(150)       # No vehicles on the edge
    
    # Calculate distances from the junction to each vehicle
    distances = []
    for vehicle_id in vehicle_ids:
        vehicle_position = traci.vehicle.getPosition(vehicle_id)
        distance = get_distance(junction_position, vehicle_position)
        distances.append(distance)
    
    # Return the smallest distance
    return min(distances)





def update_live_plot(fig, ax, line, values):
    line.set_xdata(range(len(values)))
    line.set_ydata(values)

    ax.relim()
    ax.autoscale_view()

    plt.draw()
    plt.pause(0.01)
    clear_output(wait=True)
    display(fig)