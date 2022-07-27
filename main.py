import random
import pgzrun
import define
import actors
import pygame, sys

# 窗口基本配置, pgzero会调用此处的变量来设置窗口
TITLE = define.WINDOW_TITLE
WIDTH = define.WINDOW_WIDTH
HEIGHT = define.WINDOW_HEIGHT

# 图片映射字典
images_dict = {
    'plane': images.plane,
    'bullet': images.bullet,
    'enemy': images.enemy,
    'heart': images.heart
}

# 子弹组
bullet_list = actors.gameObject.spiritGroup()
# 敌人组
enemy_list = actors.gameObject.spiritGroup()
# 血量显示组
heart_list = actors.gameObject.spiritGroup()

# 角色飞机
plane = actors.plane(images_dict['plane'], (define.WINDOW_WIDTH/2, define.WINDOW_HEIGHT*3/4),
                     (define.BLOCK_SIZE, define.BLOCK_SIZE), pos_anchor=actors.gameObject.posAnchor.CENTER)

# 生成敌人时间间隔
enemy_time = 0
# 游戏得分
player_scores = 0

# -------------------------------------------------游戏控制----------------------------------- #
# 随机生成敌人
def creatEnemy():
    global enemy_time
    if enemy_time <= 0:
        # 此处血量随机1-2
        enemy_list.append(actors.enemy(images_dict['enemy'], random.randint(1,2),
            (random.randint(5, define.WINDOW_WIDTH-define.BLOCK_SIZE), 0), (define.BLOCK_SIZE, define.BLOCK_SIZE), 
            pos_anchor=actors.gameObject.posAnchor.TOP_LEFT))
        enemy_time = define.ENEMY_CREATE_TIME
    else:
        enemy_time -= 1

# 显示血量
def showHp():
    hp = plane.hp
    i = 0
    heart_list.clear()
    while i<hp:
        he = actors.heart(images_dict['heart'], (i*define.HEART_SIZE, 0), (define.HEART_SIZE,
                          define.HEART_SIZE), pos_anchor=actors.gameObject.posAnchor.TOP_LEFT)
        heart_list.append(he)
        i+=1

# 得分
def getScores():
    global player_scores
    player_scores += 1

# 游戏结束
def gameOver():
    global player_scores
    pygame.quit()
    print('Game Over')
    print('Your scores are {}'.format(player_scores))
    sys.exit()

# 子弹碰撞敌机的回调函数
# 默认的碰撞检测直接将对象删除，如果给敌人设置血量根据子弹威力来扣血则需要外部提供回调函数
def bulletCollidedEnemy(bullet: actors.bullet, enemy: actors.enemy, getScore):
    enemy.hp -= bullet.agres
    bullet.setDestroy(True)         #销毁子弹
    # 根据血量判断敌人是否销毁
    if enemy.hp <= 0:
        enemy.setDestroy(True)
        getScore()                 # 得分

# 敌机与玩家碰撞
# 玩家飞机没有精灵组，所以直接写碰撞事件在Update()中调用
def enemyCollidedPlane():
    # 遍历并检测碰撞
    for i in enemy_list:
        if i.collisionDetection(plane):
            plane.hp -= 1           #扣血
            i.setDestroy(True)
            # 检测是否血量归零以结束游戏
            if plane.hp == 0:
                gameOver()

# -------------------------------------------------pgzero内置----------------------------------- #

def update():
    plane.update(screen)

    bullet_list.update(screen)
    bullet_list.move()

    creatEnemy()
    enemy_list.update(screen)
    enemy_list.move()
    enemy_list.checkDestroy()


    showHp()
    heart_list.update(screen)

    bullet_list.collisionDetection(enemy_list, collided=bulletCollidedEnemy, args=(getScores,))
    bullet_list.checkDestroy()

    enemyCollidedPlane()

def draw():
    screen.fill(define.BG_COLOR)

    plane.draw()
    bullet_list.draw()
    enemy_list.draw()
    heart_list.draw()

def on_mouse_move(pos):
    plane.move(pos)

def on_key_down(key):
    # 空格飞机发射子弹
    if key == keys.SPACE:
        bullet_list.append(plane.fire(images_dict['bullet']))

# -------------------------------------------------运行-----------------------------------#
pgzrun.go()
