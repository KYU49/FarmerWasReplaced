from Utils import move_to, vert_move, can_water, get_nearest
ws = get_world_size()
sf_range = [0, 0, 3, 6]
sf_measure = [[], [], [], [], [], [], [], [], []]	# 15, 14, ..., 8, 7枚のひまわりの座標
index = 0

# まず、花びら7枚のひまわりを9本生成
# 別のエリアにひまわりを植え、[長さ15 - 7 + 1の配列]の[枚数-1]の位置にその座標を保存
# 植え終えたら配列を順に回して、別のエリアのひまわりを全て回収
	
def init():
	move_to(sf_range[0], sf_range[1])
	sunflws_count = 0
	go_up = 1
	go_right = 1
	for i in range( sf_range[2] * sf_range[3] ):
		while can_water():
			use_item(Items.Water)
		sunflws_count += 1
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Sunflower)
		while measure() > 7:
			use_item(Items.Fertilizer)
			use_item(Items.Fertilizer)
			while not can_harvest():
				pass
			harvest()
			plant(Entities.Sunflower)
		if sunflws_count >= 9:
			x = get_pos_x()
			y = get_pos_y()
			return [x, y, go_up, go_right]
		go_up, go_right = vert_move(go_up, go_right, sf_range)
			
def my_plant(nines_xy):
	global sf_measure
	move_to(nines_xy[0], nines_xy[1])
	go_up = nines_xy[2]
	go_right = nines_xy[3]
	for i in range( sf_range[2] * sf_range[3] - 9):
		go_up, go_right = vert_move(go_up, go_right, sf_range)
		x = get_pos_x()
		y = get_pos_y()
		while can_water():
			use_item(Items.Water)
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Sunflower)
		sf_measure[15 - measure()].append([x, y])
				
def my_harvest():
	global sf_measure
	x = get_pos_x()
	y = get_pos_y()
	for mai in sf_measure:
		while len(mai) > 0:
			index, xy = get_nearest([x, y], mai)
			move_to(xy[0], xy[1])
			x, y = xy
			mai.pop(index)
			while not can_harvest():
				pass
			harvest()

def sunflower(sr = None):
	global sf_range
	if sr == None:
		sr = [get_pos_x(), get_pos_y()]
	sf_range[0] = sr[0]
	sf_range[1] = sr[1]
	nines_xy = init()
	while True:
		my_plant(nines_xy)
		move_to(nines_xy[0], nines_xy[1])
		my_harvest()

def main():	
	clear()
	sunflower()

if __name__ == "__main__":
	main()
	