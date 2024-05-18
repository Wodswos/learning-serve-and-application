
class Item:
    def __init__(self, id, name, description=None):
        self.id = id  # 初始化Item对象的id属性
        self.name = name  # 初始化Item对象的name属性
        self.description = description  # 初始化Item对象的description属性，可省略

    def __repr__(self):
        # 定义对象的字符串表示方法，便于打印和调试
        return f"Item(id={self.id}, name={self.name}, description={self.description})"

class CRUDApp:
    def __init__(self):
        self.items = []  # 初始化一个空列表，用于存储Item对象

    def create_item(self, id, name, description=None):
        # 创建一个Item对象，并将其添加到items列表中
        item = Item(id, name, description)
        self.items.append(item)
        return item  # 返回创建的Item对象

    def read_item(self, id):
        # 根据id读取Item对象
        for item in self.items:
            if item.id == id:
                return item  # 如果找到匹配的id，返回Item对象
        return None  # 如果没有找到匹配的id，返回None

    def update_item(self, id, name=None, description=None):
        # 根据id更新Item对象的name和/或description属性
        for item in self.items:
            if item.id == id:
                if name:
                    item.name = name  # 如果提供了name，更新Item对象的name属性
                if description:
                    item.description = description  # 如果提供了description，更新Item对象的description属性
                return item  # 更新完成后返回Item对象
        return None  # 如果没有找到匹配的id，返回None

    def delete_item(self, id):
        # 根据id删除Item对象
        for index, item in enumerate(self.items):
            if item.id == id:
                return self.items.pop(index)  # 如果找到匹配的id，从列表中移除Item对象并返回
        return None  # 如果没有找到匹配的id，返回None

    def list_items(self):
        # 返回所有存储的Item对象的列表
        return self.items
