import xml.etree.ElementTree as ElementTree


class HistoryParsingError(Exception):
    pass


class HistoryStoringError(Exception):
    pass


class Action:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_content(self):
        return self.content


class History:
    def __init__(self):
        self.current_pos = 0
        self.actions = []

    def get_action(self, pos):
        return self.actions[pos]

    def add_action(self, action: Action):
        if self.current_pos == len(self.actions) - 1:
            self.actions.append(action)
        else:
            self.actions = self.actions[:self.current_pos + 1] + [action]
        self.current_pos += 1

    def remove_action(self, pos):
        if 0 < pos < len(self.actions) - 1:
            del self.actions[pos]
            self.current_pos = pos

    def get_actions(self):
        return [self.get_action(i) for i in range(len(self.actions))]

    def get_current_action(self):
        return self.actions[self.current_pos]
    def undo(self):
        self.current_pos = min(self.current_pos - 1, 0)
        return self.get_current_action()
    def redo(self):
        self.current_pos = max(self.current_pos + 1, len(self.actions) - 1)
        return self.get_current_action()
    def set_current_pos(self, pos):
        if 0 <= pos <= len(self.actions):
            self.current_pos = pos
    def get_current_pos(self):
        return self.current_pos
    def last(self):
        return self.actions[-1]
    def clear(self):
        self.actions.clear()
    def store(self, filename):
        root = ElementTree.Element('history')
        for action in self.actions:
            element = ElementTree.Element("action", {"name": action})
            element.text = action.get_content()
            root.append(element)
        tree = ElementTree.ElementTree(root)
        try:
            tree.write(filename)
        except Exception as e:
            raise HistoryStoringError(f"Error while storing history to {filename}. Error: {e}")

    @staticmethod
    def load(filename):
        history = History()
        try:
            tree = ElementTree.parse(filename)
            root = tree.getroot()
            for item in root.findall("action"):
                try:
                    content = item.text
                    name = item.attrib['name']
                    action = Action(name, content)
                    history.add_action(action)
                except Exception:
                    return HistoryParsingError('Invalid action content')
            return history
        except Exception as e:
            return HistoryParsingError('Error while parsing history to {filename}. Error: : ' + str(e))

    def __len__(self):
        return len(self.actions)

    def __getitem__(self, pos):
        return self.get_action(pos)

    def __delitem__(self, pos):
        del self.actions[pos]

    def __iter__(self):
        return iter(self.actions)

    def __eq__(self, other):
        return self.name == other.name and self.actions == other.actions
