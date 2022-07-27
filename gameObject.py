from typing import Tuple
from numpy import rec
import pygame
from enum import Enum

# 坐标锚点
class posAnchor(Enum):
    TOP_LEFT = 0        # 左上方
    TOP = 1             # 正上方
    TOP_RIGHT = 2       # 右上方
    LEFT = 3            # 左
    CENTER = 4          # 中心
    RIGHT = 5           # 右
    BOTTOM_LEFT = 6     # 左下方
    BOTTOM = 7          # 正下方
    BOTTOM_RIGHT = 8    # 右下方

# 游戏基类
class gameObject:
    def __init__(self, img, init_pos:tuple, size:tuple, screen = None, pos_anchor=posAnchor.TOP_LEFT) -> None:
        self.img = img          # pgzero图片对象
        self.size = size        # 大小，元组(宽, 高)
        self.screen = screen    # screen
        self.destroy = False    # 用于检测是否被销毁，spiritGroup中的checkDestroy方法检测该属性，为True将从spiritGroup中被移除

        self.__anchor = pos_anchor                                  # 锚
        self.__pos = self.__getTruePos(init_pos, self.__anchor)     # 绘制坐标
        self.__userPos = init_pos                                   # 锚坐标

        # 图片容器对象，需导入pygame
        self.obj = pygame.transform.scale(self.img, self.size)

    # 初始化, 在pgzero update()中调用
    def update(self, screen):
        self.initScreen(screen)
        self.draw()

    # 初始化screen
    def initScreen(self, screen):
        self.screen = screen

    # 绘制
    def draw(self):
        self.screen.blit(self.obj, self.__pos)

    # 更改位置(要求锚点,防止坐标混乱)
    def changePos(self, pos: tuple, pos_anchor):
        self.__pos = self.__getTruePos(pos, pos_anchor)
        self.__userPos = pos

    # 获取宽度
    def width(self):
        return self.size[0]

    # 获取高度
    def height(self):
        return self.size[1]

    # 获取大小尺寸
    def getSize(self):
        return self.size

    # 获取横坐标(锚点坐标)
    def x(self):
        return self.__userPos[0]

    # 获取纵坐标(锚点坐标)
    def y(self):
        return self.__userPos[1]

    # 获取左上角坐标
    def getTopLeftPos(self):
        return self.__pos

    # 获取rect
    def getRect(self):
        return self.obj.get_rect()

    # 获取mask
    def getMask(self):
        return pygame.mask.from_surface(self.obj)

    # 获取锚点
    def getAnchor(self):
        return self.__anchor

    # 更改销毁属性
    def setDestroy(self, choose:bool):
        self.destroy = choose

    # 获得销毁属性
    def getDestroy(self)->bool:
        return self.destroy

    # 碰撞检测
    def collisionDetection(self, other):
        this_pos = self.getTopLeftPos()
        other_pos = other.getTopLeftPos()
        
        this_center_pos = (this_pos[0]+self.width()/2, this_pos[1]+self.height()/2)
        other_center_pos = (other_pos[0]+other.width()/2, other_pos[1]+other.height()/2)

        # 判断矩形相交
        if abs(this_center_pos[0] - other_center_pos[0]) <= (self.width() + other.width())/2 and abs(this_center_pos[1] - other_center_pos[1]) <= (self.height() + other.height())/2:
            return True
        else:
            return False

        def move(*args):
            pass


    # 根据锚和给出坐标，获取左上角坐标
    def __getTruePos(self, pos: tuple, pos_anchor):
        if pos_anchor == posAnchor.TOP_LEFT:
            return pos
        elif pos_anchor == posAnchor.TOP:
            return (pos[0]-self.size[0]/2, pos[1])
        elif pos_anchor == posAnchor.TOP_LEFT:
            return (pos[0]-self.size[0], pos[1])
        elif pos_anchor == posAnchor.LEFT:
            return (pos[0], pos[1]-self.size[1]/2)
        elif pos_anchor == posAnchor.CENTER:
            return (pos[0]-self.size[0]/2, pos[1]-self.size[1]/2)
        elif pos_anchor == posAnchor.RIGHT:
            return (pos[0]-self.size[0], pos[1]-self.size[1]/2)
        elif pos_anchor == posAnchor.BOTTOM_LEFT:
            return (pos[0], pos[1]-self.size[1])
        elif pos_anchor == posAnchor.BOTTOM:
            return (pos[0]-self.size[0]/2, pos[1]-self.size[1])
        elif pos_anchor == posAnchor.BOTTOM_RIGHT:
            return (pos[0]-self.size[0], pos[1]-self.size[1])
        else:
            return None

# 精灵组
class spiritGroup:
    def __init__(self) -> None:
        self.__spiritList = []

    # ----------------------列表操作

    # 追加
    def append(self, spirit: gameObject):
        self.__spiritList.append(spirit)

    # 索引
    def index(self, g_obj: gameObject):
        return self.__spiritList.index(g_obj)

    # 插入
    def insert(self, num):
        self.__spiritList.insert(num)

    # 移除
    def remove(self, g_obj: gameObject):
        self.__spiritList.remove(g_obj)

    # 根据索引移除
    def removeAsIndex(self, num):
        self.remove(self.index(num))

    # 元素个数
    def size(self):
        return len(self.__spiritList)

    # 清空
    def clear(self):
        self.__spiritList.clear()

    # ----------------------运算符重载

    # []
    def __getitem__(self, index) -> gameObject:
        return self.__spiritList[index]

    # in
    def __contains__(self, elem):
        return 

    # +
    def __add__(self, other):
        new_g_obj = spiritGroup()
        for i in self.__spiritList:
            new_g_obj.append(i)
        for i in other:
            new_g_obj.append(i)

        return new_g_obj
    
    # ----------------------基本操作

    # 初始化(draw)
    def update(self, screen):
        for i in self.__spiritList:
            i.update(screen)

    # 绘制
    def draw(self):
        for i in self.__spiritList:
            i.draw()

    # 碰撞检测
    def collisionDetection(self, other, collided = None, args=()):
        for e in self.__spiritList:
            for i in other:
                if e.collisionDetection(i) == True:
                    if collided == None:
                        e.setDestroy(True)
                        i.setDestroy(True)
                    else:
                        collided(e, i, *args)

    # 移动
    def move(self, *args):
        for i in self.__spiritList:
            i.move(*args)

    # 检测元素是否应该被销毁(移除)，并执行
    def checkDestroy(self):
        for i in self.__spiritList:
            if i.getDestroy():
                temp = i
                self.remove(i)
                del i