from Utils import move_to, can_water
ws = get_world_size()
comp_center = []

def range_to_center(comp_range):
	results = []
	w = comp_range[2]
	h = comp_range[3]
	
	if w < 7 or h < 7:
		return []
	for i in range(6, w, 8):
		for j in range(6, h, 7):
			results.append([comp_range[0] + i - 3, comp_range[1] + j - 3])
			if 0 <= i + 1 - 3 and i + 1 + 3 <= w and 0 <= j - 3 and j + 3 <= h:
				results.append([comp_range[0] + i + 1, comp_range[1] + j])
				
	return results

def companion(cr = None, wtp = [Entities.Carrot, Entities.Carrot, Entities.Carrot, Entities.Grass, Entities.Tree]):
	global comp_center
	if cr == None:
		cr = [get_pos_x(), get_pos_y()]
	comp_center = cr
	move_to(comp_center[0], comp_center[1])
	gt = get_ground_type()
	while True:
		for w in wtp:
			if w == Entities.Grass and gt == Grounds.Soil:
				till()
				gt = Grounds.Grassland
			if w != Entities.Grass and gt == Grounds.Grassland:
				till()
				gt = Grounds.Soil
				
			plant(w)
			plant_type, (x, y) = get_companion()
			move_to(x, y)
			if plant_type == Entities.Grass and get_ground_type() == Grounds.Soil:
				till()
			if plant_type != Entities.Grass and get_ground_type() == Grounds.Grassland:
				till()
			plant(plant_type)
			move_to(comp_center[0], comp_center[1])
			while not can_harvest():
				if can_water():
					use_item(Items.Water)
				if w == Entities.Tree:
					move(North)
					harvest()
					move(West)
					move(South)
					harvest()
					move(East)
					move(South)
					harvest()
					move(East)
					move(North)
					harvest()
					move(West)
			harvest()

def main():
	clear()
	for xy in range_to_center([0, 0, ws, ws]):
		move_to(xy[0], xy[1])
		spawn_drone(companion)

if __name__ == "__main__":
	main()