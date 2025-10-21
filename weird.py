import farm

ws = get_world_size()
def main():
	while True:
		clear()
		move(West)
		spawn_drone(gen_drone)
		move(South)
		spawn_drone(gen_drone)
		move(East)
		spawn_drone(gen_drone)
		move(North)
		init()
		gen_drone()
		if num_items(Items.Power) < 100:
			break
	farm.main()

def gen_drone():
	do_a_flip()
	spawn_drone(start_drone)
	start_drone(0)

def start_drone(num = 1):
	direction = [East, North][num]
	rotation = [{East: South, South: West, West: North, North: East}, {East: North, South: East, West: South, North: West}]
	while True:
		migite = rotation[num][direction]
		if move(migite):
			direction = migite
			entity = get_entity_type()
			if entity == Entities.Treasure:
				harvest()
			elif entity == Entities.Grass:
				break
		else:
			direction = rotation[1 - num][direction]
	

def init():
	substance = ws * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	while substance > num_items(Items.Weird_Substance): 
		use_item(Items.Fertilizer)
		while True:
			if can_harvest():
				harvest()
				break
	
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substance)

if __name__ == "__main__":
	main()