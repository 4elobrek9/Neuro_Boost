import random
import flet as ft
from neuro_boost.core.storage import Storage
from neuro_boost.games import memory, digits, schulte

SHOP=[('focus','Фокус++',30,'+10% к очкам (позже)'),('audio','Аудио-пак',50,'бит-режимы и эффекты'),('energy','Energy refill',25,'восстановить жизни')]


def run():
    ft.app(target=main)


def main(page: ft.Page):
    page.title='Neuro Boost WOW'
    page.theme_mode=ft.ThemeMode.DARK
    page.bgcolor='#090b12'
    page.padding=12
    page.window.width=1280
    page.window.height=840
    store=Storage()

    profile_txt=ft.Text('',size=16,color='white')
    content=ft.AnimatedSwitcher(duration=350,transition=ft.AnimatedSwitcherTransition.SCALE,expand=True)

    def refresh():
        p=store.profile()
        profile_txt.value=f'🏆 {p.points}  💰 {p.coins}  ❤️ {p.hearts}/5'
        page.update()

    def reward(points,coins,msg):
        store.reward(points,coins)
        dlg=ft.AlertDialog(title=ft.Text('Результат'),content=ft.Text(f'{msg}\n+{points} очков / +{coins} монет'))
        page.dialog=dlg; dlg.open=True
        refresh()

    def home():
        cards=[]
        for t,d in [('Visual Arena','Мемори, Фотоаппарат, Найди отличия'),('Audio Lab','Цифры, Снежный ком, ритмы'),('Logic Core','Шульте, Sudoku, Chess-lite')]:
            cards.append(ft.Container(ft.Column([ft.Text(t,size=22,weight='bold'),ft.Text(d)],tight=True),padding=16,bgcolor='#151b2e',border_radius=16,ink=True,on_click=lambda e:None))
        return ft.Column([
            ft.Text('NEURO BOOST // STOP SCROLLING',size=34,weight='bold',color='#4df0ff'),
            ft.Text('ВАУ-дизайн + ограниченные попытки + экономика + будущий онлайн режим',color='#ff4de1'),
            ft.Row(cards,wrap=True,spacing=12),
        ])

    def shop_view():
        rows=[]
        for k,title,cost,desc in SHOP:
            def buy(e,key=k,c=cost):
                if key=='energy':
                    if store.buy(key,c): store.restore_hearts(); refresh(); return
                ok=store.buy(key,c)
                page.snack_bar=ft.SnackBar(ft.Text('Куплено!' if ok else 'Недостаточно монет')); page.snack_bar.open=True; refresh()
            rows.append(ft.Container(ft.Row([ft.Column([ft.Text(title,weight='bold'),ft.Text(desc,size=12)]),ft.ElevatedButton(f'Купить {cost}',on_click=buy)]),padding=10,bgcolor='#151b2e',border_radius=12))
        return ft.Column([ft.Text('🛒 Магазин',size=28,weight='bold',color='#4df0ff'),*rows])

    def set_view(factory):
        content.content=factory()
        page.update()

    rail=ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=110,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME,label='Хаб'),
            ft.NavigationRailDestination(icon=ft.Icons.GRID_VIEW,label='Мемори'),
            ft.NavigationRailDestination(icon=ft.Icons.HEARING,label='Цифры'),
            ft.NavigationRailDestination(icon=ft.Icons.APPS,label='Шульте'),
            ft.NavigationRailDestination(icon=ft.Icons.SHOP,label='Шоп'),
        ],
        on_change=lambda e:[set_view([home,lambda:memory.view(page,reward),lambda:digits.view(page,reward),lambda:schulte.view(page,reward),shop_view][e.control.selected_index]), refresh()]
    )

    hero=ft.Container(ft.Row([ft.Icon(ft.Icons.BOLT,color='#4df0ff',size=34),ft.Text('Neuro Boost',size=30,weight='bold')]),padding=8)
    page.add(ft.Row([rail,ft.VerticalDivider(width=1,color='#253253'),ft.Column([hero,profile_txt,content],expand=True)] ,expand=True))
    set_view(home)
    refresh()
