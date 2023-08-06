from html import escape
from typing import Optional, List, Dict, Union

from fox_orm.fields import int64, pk, default
from fox_orm.model import OrmModel
from pydantic import BaseModel
from telethon.tl.types import User as TgUser


class StateComponent(BaseModel):
    name: str
    params: Dict[str, Union[int, float, str]] = {}

    def __getitem__(self, k):
        return self.params[k]

    def __setitem__(self, k, v):
        self.params[k] = v


class State(BaseModel):
    path: List[StateComponent]

    def back(self):
        if self.path:
            self.path.pop(-1)
        if not self.path:
            self.path.append(StateComponent(name='start'))

    def to(self, component: Union[StateComponent, str], reset: bool = False):
        if isinstance(component, str):
            component = StateComponent(name=component)
        if reset:
            self.path = []
        self.path.append(component)

    @property
    def current(self):
        return self.path[-1] if self.path else None


class User(OrmModel):
    __abstract__ = True

    id: Optional[int64] = pk
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    state: State = default(State(path=[StateComponent(name='start')]))

    async def save(self):
        self.flag_modified('state')
        return await super().save()

    @classmethod
    async def from_tg(cls, tg_user: TgUser):
        if db_user := await cls.get(tg_user.id):
            return db_user
        db_user = cls(id=tg_user.id, first_name=tg_user.first_name,
                      last_name=tg_user.last_name, username=tg_user.username)
        await db_user.save()
        return db_user

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()

    def mention(self, text: Optional[str] = None):
        if text is None:
            text = self.full_name
        return f'<a href="tg://user?id={self.id}">{escape(text)}</a>'
