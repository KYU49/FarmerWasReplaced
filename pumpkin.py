from Utils import move_to, hori_move, get_nearest, can_water
ws = get_world_size()
pumps = [0, 0, ws, ws]	# カボチャが正常に生育していない or 植えられていない座標([x, y]形)を保存
pump_range = [0, 0, 6, 6]

def init(multi = False):
	global pumps
	pumps = []
	move_to(pump_range[0], pump_range[1])
	if multi:
		spawn_drone(init_plant_multi)
	init_plant(multi)
	move_to(pump_range[0], pump_range[1])
	
	up = 1
	right = 1
	for i in range(pump_range[2] * pump_range[3]):
		while not can_harvest() and get_entity_type() == Entities.Pumpkin:
			if can_water():
				use_item(Items.Water)
		if not can_harvest():
			pumps.append([get_pos_x(), get_pos_y()])
			plant(Entities.Pumpkin)
		up, right = hori_move(up, right, pump_range)	

def init_plant(multi=True):
	up = 1
	right = 1
	if multi:
		last = pump_range[2]
	else:
		last = pump_range[2] * pump_range[3]
	for i in range(last):		
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Pumpkin)
		if i != last - 1:
			up, right = hori_move(up, right, pump_range)

def init_plant_multi():
	for _ in range(pump_range[3] - 2):
		move(North)
		spawn_drone(init_plant)
	move(North)
	init_plant()

def start_drone():
	while True:
		if len(pumps) == 0:
			harvest()
			break
		else:
			x = get_pos_x()
			y = get_pos_y()
			index, nearest = get_nearest([x, y], pumps)
			move_to(nearest[0], nearest[1])

			while not can_harvest() and get_entity_type() == Entities.Pumpkin:
				if can_water():
					use_item(Items.Water)
			if can_harvest(): 
				pumps.pop(index)
			else:
				plant(Entities.Pumpkin)
				if can_water():
					use_item(Items.Water)

def pumpkin(pr = None, multi = False):
	global pump_range
	if pr == None:
		pr = [get_pos_x(), get_pos_y()]
	pump_range[0] = pr[0]
	pump_range[1] = pr[1]
	while True:
		init(multi)
		start_drone()

def main():	
	clear()
	pumpkin([0, 0], True)

if __name__ == "__main__":
	main()
	