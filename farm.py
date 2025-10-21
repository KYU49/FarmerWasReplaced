import weird
import pumpkin
import cuctus
import sunflower
import companion
from Utils import hori_move, move_to
ws = get_world_size()

def main():
	clear()
	pumpkin.pump_range = [0, 0, 6, 6]
	spawn_drone(pumpkin.pumpkin)
	move_to(7, 0)
	spawn_drone(pumpkin.pumpkin)
	move_to(7, 7)
	spawn_drone(pumpkin.pumpkin)
	move_to(0, 7)
	spawn_drone(pumpkin.pumpkin)
	
	for xy in companion.range_to_center([13, 0, 20, ws]):
		move_to(xy[0], xy[1])
		spawn_drone(companion.companion)
	
	move_to(0, 27)
	sunflower.sf_range = [0, 27, 8, 3]
	spawn_drone(sunflower.sunflower)
	
	move_to(0, 14)
	cuctus.cuctus_range[2] = 11	# 32x32なら、13までいけるけど、ドローンが足りない
	cuctus.cuctus_range[3] = 11
	spawn_drone(cuctus.cuctus)

if __name__ == "__main__":
	main()
