import define
import gameObject

# 子弹类
class bullet(gameObject.gameObject):
    def __init__(self, img, init_pos: tuple, size: tuple, screen=None, pos_anchor=...) -> None:
        super().__init__(img, init_pos, size, screen, pos_anchor)
        self.speed = define.BULLET_MOVE_LENGTH
        self.agres = define.BULLET_AGRES            #子弹威力

    def move(self, *args):
        self.changePos((self.x(), self.y()+self.speed), self.getAnchor())
        pos = self.getTopLeftPos()
        if pos[1]+self.height() < 0:
            self.setDestroy(True)


# 飞机类
class plane(gameObject.gameObject):
    def __init__(self, img, init_pos: tuple, size: tuple, screen=None, pos_anchor=...) -> None:
        super().__init__(img, init_pos, size, screen, pos_anchor)
        self.hp = define.PLANE_HP   # 玩家飞机血量

    def move(self, *args):
        # 边界判断
        pos = list((args[0][0]-self.width()/2, args[0][1]-self.height()/2))

        if pos[0] <0:
            pos[0] = 0
        if pos[0]+self.width() > define.WINDOW_WIDTH:
            pos[0] = define.WINDOW_WIDTH-self.width()
        
        if pos[1]<0:
            pos[1] = 0
        if pos[1]+self.height() > define.WINDOW_HEIGHT:
            pos[1] = define.WINDOW_HEIGHT-self.height()

        self.changePos(tuple(pos), gameObject.posAnchor.TOP_LEFT)

    # 开火，参数为子弹pgzero图片对象
    def fire(self, bullet_img):
        pos = self.getTopLeftPos()
        bullet_pos = (pos[0]+self.width()/2, pos[1])
        bull = bullet(bullet_img, bullet_pos, define.BULLET_SIZE, screen = self.screen, pos_anchor=gameObject.posAnchor.BOTTOM)
        return bull


# 敌人类
class enemy(gameObject.gameObject):
    def __init__(self, img, hp, init_pos: tuple, size: tuple, screen=None, pos_anchor=...) -> None:
        super().__init__(img, init_pos, size, screen, pos_anchor)
        self.hp = hp
        self.speed = define.ENEMY_SPEEED
        self.destroy = False

    def move(self, *args):
        if self.destroy == False:
            self.changePos((self.x(), self.y()+self.speed),
                        gameObject.posAnchor.CENTER)
            pos = self.getTopLeftPos()
            if pos[1] > define.WINDOW_HEIGHT:
                self.setDestroy(True)

# 血量类， 用于显示hp
class heart(gameObject.gameObject):
    def __init__(self, img, init_pos: tuple, size: tuple, screen=None, pos_anchor=...) -> None:
        super().__init__(img, init_pos, size, screen, pos_anchor)