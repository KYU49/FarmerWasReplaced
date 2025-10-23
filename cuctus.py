from Utils import hori_move, vert_move, move_to

ws = get_world_size()
cuctus_range = [0, 0, ws, ws]
drones = []
def swap_hori():
	x = get_pos_x()
	if x < cuctus_range[0] + cuctus_range[2] - 1 and measure() > measure(East):
		swap(East)
		return True
	return False
		
def swap_vert():
	y = get_pos_y()
	if y < cuctus_range[1] + cuctus_range[3] - 1 and measure() > measure(North):
		swap(North)
		return True
	return False

def vert_drone():
	start = cuctus_range[1]
	end = cuctus_range[1] + cuctus_range[3] - 2
	x = get_pos_x()
	while start < end:
		new_end = start
		move_to(x, start)
		for i in range(start, end + 1):
			if swap_vert():
				new_end = i + 1
			if i < end:
				move(North)
		end = min(new_end, end)
		
		new_start = end
		move_to(x, end)
		for i in range(end, start - 1, -1):
			if swap_vert():
				new_start = i - 1
			if i > start:
				move(South)
		start = max(new_start, start)
		
	
def hori_drone():
	start = cuctus_range[0]
	end = cuctus_range[0] + cuctus_range[2] - 2
	y = get_pos_y()
	while start < end:
		new_start = end
		move_to(end, y)
		for i in range(end, start - 1, -1):
			if swap_hori():
				new_start = i - 1
			if i > start:
				move(West)
		start = max(new_start, start)
		
		new_end = start
		move_to(start, y)
		for i in range(start, end + 1):
			if swap_hori():
				new_end = i + 1
			if i < end:
				move(East)
		end = min(end, new_end)

def plant_drone():
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Cactus)
	for i in range(cuctus_range[2] - 1):
		move(East)
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)
	
def init():
	move_to(cuctus_range[0], cuctus_range[1])
	for i in range(cuctus_range[3] - 1):
		spawn_drone(plant_drone)
		move(North)
	plant_drone()

def start_hori_swap():
	global drones
	for i in range(cuctus_range[3] - 1):
		drones.append(spawn_drone(hori_drone))
		move(South)
	hori_drone()

def start_vert_swap():
	global drones
	for i in range(cuctus_range[2] - 1):
		drones.append(spawn_drone(vert_drone))
		move(East)
	vert_drone()

def cuctus(cr = None):
	global cuctus_range
	if cr == None:
		cr = [get_pos_x(), get_pos_y()]
	cuctus_range[0] = cr[0]
	cuctus_range[1] = cr[1]
	while True:
		init()
		start_hori_swap()
		wait_all_drones()
		move_to(cuctus_range[0], cuctus_range[1])
		start_vert_swap()
		wait_all_drones()
		harvest()
		break

def wait_all_drones():
	global drones
	while len(drones) > 0:
		for i in range(len(drones) - 1, -1, -1):
			if has_finished(drones[i]):
				drones.pop(i)

def main():
	clear()
	cuctus()

if __name__ == "__main__":
	main()