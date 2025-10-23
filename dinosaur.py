from Utils import move_to
ws = get_world_size()
dino_range = [0, 0, ws, ws]
tail = []
dir2dxy = {North: [0, 1], South: [0, -1], West: [-1, 0], East: [1, 0]}
apple = [0, 0]
length = 1

# 1. 自分より下にある時、自分とりんごを繋ぐ閉路内に尻尾がなければ、直接行って良い(可能なら横移動、不可能なら下に1歩 → りんごの上まで移動 → 下移動; ただし、自分が1番左にいるときは、右移動から始める)。
# 2. 1において、一番左の列にりんごがある場合は、りんごとの間の閉路に尻尾がなければ、閉路に従って、2列目まで移動、その後一番左の列に入る
# 3. 自分より上にある時、閉路を進み、2列目に行った時に、1列目に尻尾がなければ、1列目に移動、その後閉路を進む。
# 4. 同じ高さのときは無視

def dinosaur():
	global i2xy
	global xy2i
	global i2dir
	global xy2dir
	i2xy, xy2i, i2dir, xy2dir = get_hamiltonian_path()
	while True:
		start_drone()
		break

def start_drone():
	global tail
	global apple
	global length
	move_to(0, 0)
	tail = [[0, 0]]
	index = 0
	
	change_hat(Hats.Dinosaur_Hat)
	apple = measure()

	shortcut = False

	while True:
		d = i2dir[index]
		if shortcut > 0:
			shortcut -= 1
		else:
			x = get_pos_x()
			y = get_pos_y()
			if y > apple[1]:
				if x > apple[0] and apple[0] > 0:
					d = West
				elif x < apple[0]:
					d = East
				else:
					d = South
				if not can_move(d):
					d = South
			elif y < apple[1]:
				if d == East and can_move(South):
					d = South
				elif x == 1:
					d = West
		move_result = move(d)
		if not move_result:
			change_hat(Hats.Brown_Hat)
			return
		x = get_pos_x()
		y = get_pos_y()
		index = xy2i[x][y]
		tail.append([x, y])
		if get_entity_type() == Entities.Apple:
			apple = measure()
			shortcut = not_tail_on_path(x, y, apple[0], apple[1])
			# 一旦これにしてるけど、後半のアルゴリズムは修正の必要がある。
			if len(tail) > 300:
				shortcut = 1024
		else:
			tail.pop(0)

# 自分とりんごを繋ぐハミルトニアン経路の上に、尻尾がないかを判定し、残り何歩でハミルトニアン経路上からなくなるかを判定
#FIXME ハミルトニアン経路上に存在する一番後ろの尻尾まででも良いか？
def not_tail_on_path(x, y, x_apple, y_apple):
	dino_i = xy2i[x][y]
	apple_i = xy2i[x_apple][y_apple]
	count = 0
	# 自機と尻尾の該当位置までの距離と、尻尾の先端からの距離を比べ、該当位置までの距離の方が長かったら、移動後にその位置には決して尻尾がないため、経路上にあっても無視する。
	if dino_i < apple_i:
		for i in range(len(tail)):
			t = tail[i]
			distance = abs(x - t[0]) + abs(y - t[1])
			tail_i = xy2i[t[0]][t[1]]
			if (dino_i < tail_i and tail_i < apple_i) and distance <= i:
				count = i
	else:
		for i in range(len(tail)):
			t = tail[i]
			distance = abs(x - t[0]) + abs(y - t[1])
			tail_i = xy2i[t[0]][t[1]]
			if (dino_i < tail_i or tail_i < apple_i) and distance <= i:
				count = i
	return count


def get_hamiltonian_path():
	w = dino_range[2]
	h = dino_range[3]
	
	xy2dir = []
	xy2i = []
	for i in range(ws):
		xy2dir.append([])
		xy2i.append([])
		for j in range(ws):
			xy2dir[i].append(None)
			xy2i[i].append(0)
	i2xy = []
	i2dir = []
	
	x = 0
	for y in range(ws - 1):
		xy2dir[x][y] = North
		xy2i[x][y] = len(i2xy)
		i2xy.append([0, y])
		i2dir.append(North)
	for x in range(ws - 1):
		xy2dir[x][ws - 1] = East
		xy2i[x][ws - 1] = len(i2xy)
		i2xy.append([x, ws - 1])
		i2dir.append(East)
	for y in range(ws - 2, 0, -2):
		xy2dir[ws - 1][y + 1] = South
		xy2i[ws - 1][y + 1] = len(i2xy)
		i2xy.append([ws - 1, y + 1])
		i2dir.append(South)
		# ←
		for x in range(ws - 1, 1, -1):
			xy2dir[x][y] = West
			xy2i[x][y] = len(i2xy)
			i2xy.append([x, y])
			i2dir.append(West)
		xy2dir[1][y] = South
		xy2i[1][y] = len(i2xy)
		i2xy.append([1, y])
		i2dir.append(South)
		# →
		for x in range(1, ws - 1):
			xy2dir[x][y - 1] = East
			xy2i[x][y - 1] = len(i2xy)
			i2xy.append([x, y - 1])
			i2dir.append(East)
	xy2dir[ws - 1][1] = South
	xy2i[ws - 1][1] = len(i2xy)
	i2xy.append([ws - 1, 1])
	i2dir.append(South)
	for x in range(ws - 1, 0, -1):
		xy2dir[x][0] = West
		xy2i[x][0] = len(i2xy)
		i2xy.append([x, 0])
		i2dir.append(West)

	return i2xy, xy2i, i2dir, xy2dir

def main():
	clear()
	dinosaur()

if __name__ == "__main__":
	main()

