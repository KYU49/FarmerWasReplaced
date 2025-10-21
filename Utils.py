ws = get_world_size()
def move_to(x, y):
	dx = x - get_pos_x()
	dy = y - get_pos_y()
	if dx > 0:
		for _ in range(dx):
			move(East)
	else:
		for _ in range(abs(dx)):
			move(West)
	if dy > 0:
		for _ in range(dy):
			move(North)
	else:
		for _ in range(abs(dy)):
			move(South)

def hori_move(go_up, go_right, area):
	x = get_pos_x()
	y = get_pos_y()
	if area[3] > 1:
		if y + go_up > area[1] + area[3] - 1:
			go_up = -1
		elif y + go_up < area[1]:
			go_up = 1
	else:
		go_up = 0
	if x + go_right > area[0] + area[2] - 1:
		y += go_up
		go_right = -1
	elif x + go_right < area[0]:
		y += go_up
		go_right = 1
	elif area[2] > 1:
		x += go_right
	move_to(x, y)
	return (go_up, go_right)
	
def vert_move(go_up, go_right, area):
	x = get_pos_x()
	y = get_pos_y()
	if area[2] > 1:
		if x + go_right > area[0] + area[2] - 1:
			go_right = -1
		elif x + go_right < area[0]:
			go_right = 1
	else:
		go_right = 0
	if y + go_up > area[1] + area[3] - 1:
		x += go_right
		go_up = -1
	elif y + go_up < area[1]:
		x += go_right
		go_up = 1
	elif area[3] > 1:
		y += go_up
	move_to(x, y)	
	return (go_up, go_right)

# currentに入れた[x, y]がtargetの[[x1, y1], [x2, y2], ...]のどれに一番近いか返す。
def get_nearest(current, target):
	index = 0
	nearest = target[0]
	distance = ws * 2
	for i in range(len(target)):
		t = target[i]
		temp_dist = abs(t[0] - current[0]) + abs(t[1] - current[1])
		# 現在いる位置は返さない (リストが1つだけなら返す)
		if distance > temp_dist and temp_dist != 0:
			distance = temp_dist
			nearest = t
			index = i
	return index, nearest

# 1単位の水よりも地面が乾いていたら水をやる
def can_water():
	if get_water() < 0.75:
		return True
	return False