import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    """
    引数で与えられたRectが画面内か外かを判定する
    引数：こうかとんRect　or 爆弾Rect
    戻り値：真理値タプル(縦、横)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def game_over_screen(screen): #ゲームオーバー画面を表示する関数

    #黒色の半透明の四角の描画
    brack_out = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(brack_out, (0), (0, 0, WIDTH, HEIGHT))
    brack_out.set_alpha(200)
    screen.blit(brack_out, [0, 0])

    #ゲームオーバーの文字の描画
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, [WIDTH//2-150, HEIGHT//2-50])

    #泣いている２匹のこうかとんの描画
    KK_cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    KK_cry_rct = KK_cry_img.get_rect()
    KK_cry_rct.center = WIDTH//2+200, HEIGHT//2-25
    screen.blit(KK_cry_img, KK_cry_rct)
    KK_cry_rct.center = WIDTH//2-200, HEIGHT//2-25
    screen.blit(KK_cry_img, KK_cry_rct)

    pg.display.update()
    time.sleep(5)
    return


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #爆弾用の空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    DELTA = {
        pg.K_UP:(0, -5), 
        pg.K_DOWN:(0, +5), 
        pg.K_LEFT:(-5, 0), 
        pg.K_RIGHT:(+5, 0),
            }
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            game_over_screen(screen=screen)
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横にはみ出てる
            vx *= -1
        if not tate: #縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
