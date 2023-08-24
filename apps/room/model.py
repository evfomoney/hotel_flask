from exts import db


# 房间表
class Room(db.Model):
    """
    [房间表]
        介绍:
            用于记录当前酒店所有的房间, 以房间类型划类

        字段:
            id:int 主键
            room_type:string 非空
            price:Float 价格
            reservers:int 储量(房间剩余量)

    [method]
       用于实现 '/room'的功能

        room_details(cls, **resdict)

    """

    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 房间编号
    room_type = db.Column(db.String(20), nullable=True)  # 房间类型
    price = db.Column(db.Float)  # 价格
    reservers = db.Column(db.Integer, nullable=True)  # 储量, 还差一个自动更新的设置

    @classmethod
    def room_details(cls, resdict: dict):
        # 因为room表是按类型分的, 所以每种类型查询结果只有一条, 如果想要看对应的的用户名, 请移步 用户管理
        tmp = (
            db.session.query(Room)
            .filter(Room.room_type == resdict.get("room_type"))
            .first()
        )
        return tmp
