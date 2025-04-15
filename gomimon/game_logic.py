import random

class Monster:
    def __init__(self, name, hp, attack, defense=0):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

    def attack_target(self, target):
        damage = max(0, self.attack - target.defense)
        target.take_damage(damage)
        return f"{self.name} の攻撃！ {target.name} に {damage} のダメージ！"

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return f"{self.name} は {damage} のダメージを受けた。残りHP: {self.hp}/{self.max_hp}"

    def is_alive(self):
        return self.hp > 0

class Battle:
    def __init__(self, monster1, monster2):
        self.monster1 = monster1
        self.monster2 = monster2
        self.log = []
        self.turn = 0

    def simulate_turn(self):
        self.turn += 1
        turn_log = [f"-- ターン {self.turn} --"]

        attacker, defender = (self.monster1, self.monster2) if random.random() < 0.5 else (self.monster2, self.monster1)

        attack_result = attacker.attack_target(defender)
        turn_log.append(attack_result)

        if not defender.is_alive():
            turn_log.append(f"{attacker.name} の勝利！")
            return turn_log

        attacker, defender = defender, attacker
        attack_result = attacker.attack_target(defender)
        turn_log.append(attack_result)

        if not defender.is_alive():
            turn_log.append(f"{attacker.name} の勝利！")
            return turn_log

        return turn_log