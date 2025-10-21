ws = get_world_size()
dino_range = [0, 0, ws, ws]
direction_to_dxy = {North: [0, 1], South: [0, -1], West: [-1, 0], East: [1, 0]}

# 1. 自分より2以上、下にある時、自分とりんごを繋ぐ閉路内に尻尾がなければ、直接行って良い(1歩下 → 横移動 → 下移動; ただし、自分が1番左にいるときは、右移動から始める)。
# 2. 自分より1だけ下にある場合、ハミルトニアン閉路に従う
# 3. 1, 2において、一番左の列にりんごがある場合は、りんごとの間の閉路に尻尾がなければ、閉路に従って、2列目まで移動、その後一番左の列に入る
# 4. 自分より上にある時、閉路を進み、2列目に行った時に、1列目に尻尾がなければ、1列目に移動、その後閉路を進む。
# 5. 同じ高さのときは無視

def dinosaur():
	i2xy, i2dir, xy2dir = get_hamiltonian_path()
	change_hat(Hats.Dinosaur_Hat)
	while True:
		for dir in i2dir:
			move(dir)

def get_hamiltonian_path():
	w = dino_range[2]
	h = dino_range[3]
	
	xy_to_direction = []
	index_to_xy = []
	index_to_direction = []
	
	first_col = []
	for i in range(0, h - 1):
		first_col.append(North)
	first_col.append(East)
	xy_to_direction.append(first_col)
	
	second_col = [West]
	for i in range(1, h):
		second_col.append([South, East][i % 2])
	xy_to_direction.append(second_col)
	
	for _ in range(2, w - 1):
		col = []
		for i in range(0, h):
			col.append([West, East][i % 2])
		xy_to_direction.append(col)
	
	last_col = []
	for i in range(0, h):
		if i % 2 == 0:		
			last_col.append(West)
		else:
			last_col.append(South)
	xy_to_direction.append(last_col)
	x = 0
	y = 0
	for i in range(w * h):
		direction = xy_to_direction[x][y]
		index_to_xy.append([x, y])
		index_to_direction.append(direction)
		x, y += direction_to_dxy[direction]
	return index_to_xy, index_to_direction, xy_to_direction
	

def main():
	clear()
	dinosaur()

if __name__ == "__main__":
	main()

