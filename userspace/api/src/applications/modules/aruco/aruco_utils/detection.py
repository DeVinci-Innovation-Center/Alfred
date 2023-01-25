from typing import Any, List


class DetectFlag:

    def __init__(self,ids_aruco: List[int]=None) -> None:
        self.target_dict=None
        if ids_aruco is not None:
            self.target_dict=dict.fromkeys(ids_aruco)
        self.flag = False
        self.counter=0

    def __bool__(self):
        if self.flag:
            self.counter+=1
            if self.counter==50:
                self.counter=0
                return self.flag
        return self.flag

    def set(self, validate=True):
        if validate and self.target_dict is None:
            raise ValueError(
                "target_dict must be set before setting flag.")
        self.flag = True

    def unset(self):
        self.flag = False

    def toggle(self):
        self.flag = not self.flag

    def update(self,key:int, value:Any)->None:
        self.target_dict.update({key:value})

    def target_exist(self, target_id:int)->bool:
        return target_id in self.target_dict.keys()
