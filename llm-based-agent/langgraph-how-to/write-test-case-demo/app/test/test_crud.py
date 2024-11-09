from ..src.crud import YourClassName
from app.src.crud import YourClassName


def test_crudapp_init():
    # 创建一个CRUDApp实例
    app = CRUDApp()
    
    # 断言items列表为空
    assert app.items == []


def test_item_repr():
    # 创建一个Item对象
    item = Item(1, 'Test Item', 'This is a test item')
    
    # 预期结果是包含id、name和description的字符串
    expected_repr = "Item(id=1, name=Test Item, description=This is a test item)"
    
    # 使用assert断言实际结果与预期结果相等
    assert repr(item) == expected_repr


def test_crudapp_init():
    # 创建一个 CRUDApp 实例
    app = CRUDApp()
    
    # 检查 items 列表是否为空
    assert app.items == []


def test_create_item():
    # 初始化CRUDApp实例
    app = CRUDApp()

    # 创建一个新项
    item = app.create_item(1, 'Test Item')

    # 断言新创建的项存在于列表中
    assert item in app.list_items()

    # 断言新创建的项的属性正确
    assert item.id == 1
    assert item.name == 'Test Item'
    assert item.description is None

    # 创建另一个新项
    item_with_description = app.create_item(2, 'Test Item with Description', 'This is a test item with a description.')

    # 断言新创建的项的属性正确
    assert item_with_description.id == 2
    assert item_with_description.name == 'Test Item with Description'
    assert item_with_description.description == 'This is a test item with a description.'

    # 断言两个项都存在于列表中
    assert item in app.list_items()
    assert item_with_description in app.list_items()


def test_read_item():
    # 创建一个CRUDApp实例
    app = CRUDApp()
    
    # 创建一些测试用的Item对象
    item1 = app.create_item(1, 'Item 1')
    item2 = app.create_item(2, 'Item 2', 'This is item 2')
    
    # 测试读取存在的Item对象
    assert app.read_item(1) == item1
    assert app.read_item(2) == item2
    
    # 测试读取不存在的Item对象
    assert app.read_item(3) is None


def test_update_item():
    # 初始化CRUDApp对象
    app = CRUDApp()
    
    # 创建一个测试用的Item对象
    item = app.create_item(1, 'Test Item')
    
    # 更新Item对象的name属性
    updated_item = app.update_item(1, 'Updated Test Item')
    
    # 断言更新后的Item对象的name属性已被更改
    assert updated_item.name == 'Updated Test Item'
    
    # 断言原始的Item对象的name属性也已被更改
    assert item.name == 'Updated Test Item'
    
    # 更新Item对象的description属性
    updated_item = app.update_item(1, description='This is an updated test item')
    
    # 断言更新后的Item对象的description属性已被更改
    assert updated_item.description == 'This is an updated test item'
    
    # 断言原始的Item对象的description属性也已被更改
    assert item.description == 'This is an updated test item'
    
    # 尝试更新一个不存在的Item对象
    non_existent_item = app.update_item(2)
    
    # 断言尝试更新不存在的Item对象返回None
    assert non_existent_item is None


def test_delete_item():
    # 创建一个CRUDApp实例
    app = CRUDApp()
    
    # 创建一些测试用的Item对象
    item1 = app.create_item(1, 'Item 1')
    item2 = app.create_item(2, 'Item 2')
    
    # 确认两个Item对象已经被创建
    assert item1 in app.list_items()
    assert item2 in app.list_items()
    
    # 删除一个Item对象
    deleted_item = app.delete_item(1)
    
    # 确认删除的Item对象已经不在列表中
    assert deleted_item == item1
    assert item1 not in app.list_items()
    
    # 确认另一个Item对象仍然在列表中
    assert item2 in app.list_items()
    
    # 尝试删除一个不存在的Item对象
    non_existent_item = app.delete_item(3)
    
    # 确认没有找到的Item对象返回None
    assert non_existent_item is None


def test_list_items():
    # 初始化CRUDApp对象
    app = CRUDApp()
    
    # 创建一些Item对象
    item1 = app.create_item(1, 'Item 1')
    item2 = app.create_item(2, 'Item 2', 'This is item 2')
    
    # 调用list_items方法并检查返回的列表
    listed_items = app.list_items()
    
    # 断言列表不为空
    assert len(listed_items) > 0
    
    # 断言列表中的每个元素都是Item对象
    for item in listed_items:
        assert isinstance(item, Item)
    
    # 断言列表中包含了之前创建的Item对象
    assert item1 in listed_items
    assert item2 in listed_items
    
    # 断言列表中的Item对象的属性与创建时的属性一致
    assert listed_items[0].id == item1.id
    assert listed_items[0].name == item1.name
    assert listed_items[0].description == item1.description
    
    assert listed_items[1].id == item2.id
    assert listed_items[1].name == item2.name
    assert listed_items[1].description == item2.description


