class BonusBase:  # бонус
    def __init__(self, title, additional_title, price, mini_text=None):
        self.title = title
        self.additional_title = additional_title
        self.price = price
        if mini_text is None:
            self.mini_text = 'без объяснения'
        else:
            self.mini_text = mini_text

    def use_bonus(self, req, hero):  # используем бонус, улучшаем героя
        pass
