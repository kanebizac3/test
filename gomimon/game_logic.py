import random
from .models import UserGomimon

class Monster:
    def __init__(self, name, hp, maxhp, attack, defense=0):
        self.name = name
        self.hp = hp
        self.maxhp = maxhp
        self.attack = attack
        self.defense = defense

    def attack_target(self, target):
        damage = max(0, self.attack - target.defense)
        # target.take_damage(damage)
        return damage, f"{self.name} の攻撃！ {target.name} に {damage} のダメージ！"

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return f"{self.name} は {damage} のダメージを受けた。残りHP: {self.hp}/{self.maxhp}"

    def is_alive(self):
        return self.hp > 0

class Battle:
    def __init__(self, monster1, monster2):
        self.monster1 = monster1
        self.monster2 = monster2
        self.log = []
        self.turn = 0

    def simulate_turnA(self, attacker, defender):
        self.turn += 1
        turn_log = [f"-- ターン {self.turn} --"]
        damage, attack_result = attacker.attack_target(defender)
        turn_log.append(attack_result)
        damage_result = defender.take_damage(damage)
        turn_log.append(damage_result)

        if not defender.is_alive():
            turn_log.append(f"{attacker.name} の勝利！")
            return turn_log
        
        return turn_log

    def simulate_turnB(self, attacker, defender):
        turn_log = []
        attacker, defender = defender, attacker
        damage, attack_result = attacker.attack_target(defender)
        turn_log.append(attack_result)
        damage_result = defender.take_damage(damage)
        turn_log.append(damage_result)

        if not defender.is_alive():
            turn_log.append(f"{attacker.name} の勝利！")
            return turn_log

        return turn_log
    

def get_level_from_experience_exponential(experience, base_exp=10):
    """
    経験値が2倍になると一つレベルアップするアルゴリズムで、現在の経験値からレベルを判定する。
    """
    level = 1
    required_exp = 0
    next_level_exp = base_exp
    while experience >= next_level_exp:
        required_exp = next_level_exp
        level += 1
        next_level_exp = base_exp * (2 ** (level - 1))
        if next_level_exp == base_exp: # レベル2の時のnext_level_expの計算を修正
            next_level_exp = base_exp * 2
        elif level > 2:
            next_level_exp = base_exp * (2 ** (level - 2)) * 2


    return level

def level_up_gomimon(user_gomimon):
    """
    ゴミモンをレベルアップさせ、ステータスをランダムに増加させる。

    Args:
        user_gomimon (UserGomimon): レベルアップさせる UserGomimon モデルのインスタンス。

    Returns:
        UserGomimon: レベルアップ後の UserGomimon モデルのインスタンス (保存は別途行う必要があります)。
    """
    if isinstance(user_gomimon, UserGomimon):
        user_gomimon.gomimon_level += 1
        user_gomimon.gomimon_atack += random.randint(1, 3)
        user_gomimon.gomimon_defence += random.randint(1, 2)
        user_gomimon.gomimon_maxhp += random.randint(5, 10)
        user_gomimon.gomimon_hp = user_gomimon.gomimon_maxhp # HPを最大値まで回復させる (レベルアップ時)
        return user_gomimon
    else:
        raise TypeError("引数 'user_gomimon' は UserGomimon モデルのインスタンスである必要があります。")


