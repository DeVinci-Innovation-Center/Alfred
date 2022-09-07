from typing import Any, List


class DetectFlag:

    def __init__(self,target_dict:dict={}) -> None:
        self.target_dict=target_dict
        self.flag = False

    def __bool__(self):
        return self.flag

    def set(self, validate=True):
        self.flag = True

    def unset(self):
        self.flag = False

    def toggle(self):
        self.flag = not self.flag

    def update(self,key:int, value:Any)->None:
        self.target_dict.update({key:value})

    def target_exist(self, target_id:int)->bool:
        return target_id in self.target_dict.keys()
