from peewee import MySQLDatabase, Model, IntegerField, TextField, CharField, PrimaryKeyField, DoesNotExist

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'hyperion',
    'password': 'dongjj'
}

db = MySQLDatabase('note', **MYSQL_CONFIG)


class BaseModel(Model):
    class Meta:
        database = db


class Note(BaseModel):
    id = PrimaryKeyField()
    title = CharField()
    content = TextField()
    datetime = CharField()


class Label(BaseModel):
    id = PrimaryKeyField()
    name = CharField()


class NoteLabel(BaseModel):
    id = PrimaryKeyField()
    note_id = IntegerField()
    label_id = IntegerField()


def init_db():
    db.connect()
    print(search("tes"))
    db.close()


"""
Note 
"""


def get_note(note_title):
    note_dict = {"content": "", datetime: ""}
    try:
        note = Note.get(Note.title == note_title)
        note_dict["content"] = note.content
        note_dict["datetime"] = note.datetime
    except DoesNotExist:
        pass
    return note_dict


def save_note(data):
    try:
        Note.get(Note.title == data["title"])
        return_msg = "笔记已存在"
    except DoesNotExist:
        note = Note(title=data["title"], content=data["content"], datetime=data["datetime"])
        note.save()
        return_msg = "保存笔记成功"
    return return_msg


def update_note(data):
    try:
        note_to_update = Note.get(Note.title == data["title"])
        if note_to_update.content != data["content"]:
            note_to_update.content = data["content"]
            note_to_update.datetime = data["datetime"]
            note_to_update.save()
            return_msg = "更新笔记成功"
        else:
            return_msg = "笔记内容相同，没有进行更新"
    except DoesNotExist:
        return_msg = "笔记不存在"
    return return_msg


def delete_note(note_title):
    try:
        note_to_delete = Note.get(Note.title == note_title)
        note_labels = NoteLabel.select().where(NoteLabel.note_id == note_to_delete.id)
        # 检查待删除note是否存在label,如存在同时删除
        if note_labels.exists():
            for note_label in note_labels:
                note_label.delete_instance()
        note_to_delete.delete_instance()
        return_msg = "笔记删除成功"
    except DoesNotExist:
        return_msg = "笔记不存在"
    return return_msg


"""
Label
"""


def get_labels(note_title):
    labels_list = []
    labels = Label.select().join(NoteLabel, on=(NoteLabel.label_id == Label.id)) \
        .join(Note, on=(Note.id == NoteLabel.note_id)) \
        .where(Note.title == note_title)
    if labels.exists():
        for label in labels:
            labels_list.append(label.name)
    return labels_list


def get_all_labels():
    labels = Label.select()
    labels_list = []
    if labels.exists():
        for label in labels:
            labels_list.append(label.name)
    return labels_list


def save_label(data):
    note_title = data["note_title"]
    label_name = data["label_name"]
    return_msg = ""

    try:
        Label.get(Label.name == label_name)
        return_msg += "标签已存在， "
    except DoesNotExist:
        label = Label(name=label_name)
        label.save()
        return_msg += "标签保存成功， "

    try:
        note_id = Note.get(Note.title == note_title).id
        label_id = Label.get(Label.name == label_name).id
        note_label_return = save_notelabel(note_id, label_id)
        return_msg += note_label_return
    except DoesNotExist:
        return_msg += "笔记: {} 不存在".format(note_title)
    return return_msg


def update_label(data):
    label_name = data["label_name"]
    to_change = data["to_change"]
    try:
        label = Label.get(Label.name == label_name)
        if label_name == to_change:
            return_msg = "更改内容与原标签相同"
        else:
            label.name = to_change
            label.save()
            return_msg = "更新标签成功"
    except DoesNotExist:
        return_msg = "标签：{}不存在".format(label_name)
    return return_msg


def delete_label(label_name):
    try:
        label = Label.get(Label.name == label_name)
        label.delete_instance()
        return_msg = "标签删除成功 "
        note_labels = NoteLabel.select().where(NoteLabel.label_id == label.id)
        if note_labels.exists():
            for note_label in note_labels:
                note_label.delete_instance()
            return_msg += " 该标签从笔记移除"
    except DoesNotExist:
        return_msg = "标签不存在"
    return return_msg


def get_menu():
    menu_data = []
    for label in Label.select():
        menu_label_dict = {"name": label.name, "notes": [], "open": False}
        for note_label in NoteLabel.select().where(NoteLabel.label_id == label.id):
            note = Note.get(Note.id == note_label.note_id)
            menu_label_dict["notes"].append(note.title)
        menu_data.append(menu_label_dict)

    result = db.execute_sql("select * from note left outer join notelabel on notelabel.note_id = note.id where notelabel.note_id is null")
    menu_without_label = {"name": "未分类", "notes": [], "open": False}
    for note_without_label in result:
        menu_without_label["notes"].append(note_without_label[1])
    menu_data.append(menu_without_label)
    return menu_data


"""
NoteLabel
"""


def save_notelabel(note_id, label_id):
    try:
        NoteLabel.get(NoteLabel.note_id == note_id, NoteLabel.label_id == label_id)
        return_msg = "笔记标签已存在"
    except DoesNotExist:
        notelabel = NoteLabel(note_id=note_id, label_id=label_id)
        notelabel.save()
        return_msg = "保存笔记标签成功"
    return return_msg

"""
Search
"""


def search(str):
    search_result = []
    result = Note.select().where(Note.content.contains(str))
    for note in result:
        note_dict = {"note_title": note.title, "note_content": note.content}
        search_result.append(note_dict)
    return search_result


if __name__ == '__main__':
    init_db()
