import random
import flet as ft

def view(page, reward_cb):
    symbols=list('AABBCCDDEEFFGGHH'); random.shuffle(symbols)
    first={'i':None}; opened=set(); attempts={'left':18}
    status=ft.Text('Найди пары. Попыток: 18', color='white')
    grid=ft.GridView(expand=1,max_extent=90,child_aspect_ratio=1,spacing=8,run_spacing=8)
    buttons=[]
    def end(win):
        pts=160+attempts['left']*8 if win else 20
        reward_cb(pts,max(1,pts//12),f'Мемори: {"победа" if win else "поражение"}')
    def click(i):
        if i in opened or attempts['left']<=0:return
        buttons[i].text=symbols[i]
        if first['i'] is None:
            first['i']=i; page.update(); return
        j=first['i']; first['i']=None
        if i!=j and symbols[i]==symbols[j]:
            opened.update({i,j})
            if len(opened)==len(symbols): end(True)
        else:
            attempts['left']-=1
            status.value=f'Не совпало. Попыток: {attempts["left"]}'
            buttons[i].text='?'; buttons[j].text='?'
            if attempts['left']==0:end(False)
        page.update()
    for i in range(len(symbols)):
        b=ft.ElevatedButton('?',height=80,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),on_click=lambda e,k=i:click(k))
        buttons.append(b); grid.controls.append(b)
    return ft.Column([ft.Text('🎴 MEMORI X',size=28,weight='bold',color='#4df0ff'),status,grid], expand=True)
