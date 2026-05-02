import random, time
import flet as ft

def view(page,reward_cb):
    nums=list(range(1,26)); random.shuffle(nums)
    need={'n':1}; started={'t':None}
    info=ft.Text('Нажимай 1→25. Ошибка = -1 попытка (до 5).',color='white')
    lives={'left':5}
    grid=ft.GridView(max_extent=80,spacing=6,run_spacing=6,child_aspect_ratio=1)
    def tap(v,b):
        if started['t'] is None: started['t']=time.time()
        if v==need['n']:
            b.bgcolor='#4df0ff'; b.color='black'; need['n']+=1
            if need['n']==26:
                sec=max(1,time.time()-started['t']); pts=max(60,int(320-sec*20)); reward_cb(pts,pts//12,'Schulte: done')
        else:
            lives['left']-=1; info.value=f'Ошибка. Жизни: {lives["left"]}'
            if lives['left']<=0: reward_cb(15,1,'Schulte: fail')
        page.update()
    for n in nums:
        b=ft.TextButton(str(n),on_click=lambda e,v=n,bb=None:None)
        b.on_click=lambda e,v=n,bb=b:tap(v,bb)
        grid.controls.append(ft.Container(b,bgcolor='#172035',border_radius=10,padding=4))
    return ft.Column([ft.Text('🔲 SCHULTE BLITZ',size=28,weight='bold',color='#4df0ff'),info,grid],expand=True)
