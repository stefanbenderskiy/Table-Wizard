import os

class History:
    def __init__(self,name):
        self.name = name
        self.actions = []
    def add_action(self,action_name, value):
        with open(f"data/histories/{self.name}/{len(self) + 1}.txt", "w") as file:
            file.write(value)
    def get_actions(self):
        return [self.get_action(i) for i in range(len(self.actions))]
    def get_action(self,pos):
        with open(f"data/histories/{self.name}/{self.current}.txt", "r") as file:
            return (self.actions[pos], file.read())
    def get_last_action(self,pos):
        return self.get_action(len(self))
    def __len__(self):
        return len(self.actions)
    def __getitem__(self,pos):
        return self.get_action(pos)