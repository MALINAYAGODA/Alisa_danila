from .MonsterBase import MonsterBase


class Kalmadzilla(MonsterBase):
    def __init__(self):
        super(Kalmadzilla, self).__init__(
            18, 'Кальмадзилла',
            'Ты схвачен, намочен,отфигачен и проглочен. Ты мертв. Мертвее мёртвого. Вопросы?',
            4, 2
        )

    def do_bad_things(self, req, hero):  # он не убежал
        hero["is_alive"] = False
