import random, string
import flet as ft

def view(page,reward_cb):
    level=5
    seq=''.join(random.choice(string.digits) for _ in range(level))
    attempts={'left':3}
    seq_txt=ft.Text(seq,size=40,weight='bold',color='#ff4de1')
    input_f=ft.TextField(label='Введи последовательность',width=320)
    info=ft.Text('3 попытки. Можно в прямом или обратном порядке.',color='white')
    def check(_):
        val=input_f.value.strip()
        ok=val==seq or val==seq[::-1]
        if ok:
            reward_cb(80,8,'Digit Span: успех'); return
        attempts['left']-=1
        info.value=f'Неверно. Осталось: {attempts["left"]}'
        if attempts['left']==0:
            reward_cb(10,1,f'Digit Span: проигрыш, было {seq}')
        page.update()
    return ft.Column([ft.Text('🔢 DIGIT SPAN',size=28,weight='bold',color='#4df0ff'),seq_txt,info,input_f,ft.ElevatedButton('Проверить',on_click=check)])
