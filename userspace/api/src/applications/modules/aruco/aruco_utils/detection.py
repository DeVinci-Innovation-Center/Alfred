from typing import Any, Optional


class DetectFlag:

    def __init__(self,target_dict: Optional[dict]=None) -> None:
        self.target_dict=target_dict
        self.flag = False

    def __bool__(self):
        return self.flag

    def set(self, validate=True):
        if validate and self.target_dict is not None:
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
