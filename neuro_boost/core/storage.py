import json, sqlite3
from dataclasses import dataclass

@dataclass
class Profile:
    points:int
    coins:int
    upgrades:dict
    hearts:int=5

class Storage:
    def __init__(self, db='neuro_boost.db'):
        self.conn=sqlite3.connect(db)
        self.conn.execute('''CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY CHECK(id=1), points INT DEFAULT 0, coins INT DEFAULT 0, hearts INT DEFAULT 5, upgrades TEXT DEFAULT '{}')''')
        self.conn.execute("INSERT OR IGNORE INTO profile(id, points, coins, hearts, upgrades) VALUES(1,0,0,5,'{}')")
        self.conn.commit()
    def profile(self)->Profile:
        p,c,h,u=self.conn.execute('SELECT points, coins, hearts, upgrades FROM profile WHERE id=1').fetchone()
        return Profile(p,c,json.loads(u or '{}'),h)
    def reward(self, pts, coins):
        self.conn.execute('UPDATE profile SET points=points+?, coins=coins+? WHERE id=1',(pts,coins)); self.conn.commit()
    def spend_heart(self):
        self.conn.execute('UPDATE profile SET hearts=max(0, hearts-1) WHERE id=1'); self.conn.commit()
    def restore_hearts(self):
        self.conn.execute('UPDATE profile SET hearts=5 WHERE id=1'); self.conn.commit()
    def buy(self,key,cost):
        p=self.profile()
        if p.coins<cost:return False
        p.upgrades[key]=p.upgrades.get(key,0)+1
        self.conn.execute('UPDATE profile SET coins=?, upgrades=? WHERE id=1',(p.coins-cost,json.dumps(p.upgrades))); self.conn.commit(); return True
