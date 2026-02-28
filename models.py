from pydantic import BaseModel, Field
from typing import Literal, Union, List

class B(BaseModel):
    t: Literal['b']
    b_field: str
    def execute(self): print(f"B: {self.b_field}")

class C(BaseModel):
    t: Literal['c']
    c_field: int
    def execute(self): print(f"C: {self.c_field}")

class D(BaseModel):
    x: Union[B, C] = Field(discriminator='t')

class E(BaseModel):
    d: List[D]
    def execute(self):
        for item in self.d:
            item.x.execute()