from exts import db
from apps.room import Room


# 记录表
class Records(db.Model):
    """
    [记录表]
        描述:
            用于登记入住信息, 如: 插入/修改/删除 入住信息
        字段:
            id:int 主键
            room_id:int 外键
            user_name:str 外键
            rztime:str, {不由用户填入, 系统自动填入}
            room_style: str, {不由用户填入, 由系统查询后, 由room表得出}
            price:float 非空
            tele:str

            backinterface: user, room

            unique: room_id and user_name
    [note]
         允许多个用户为相同的user_name, 区分不同的 记录数据依靠: (room_id, user_name)

    [methods]
        主要用于实现 '/admin'的功能实现

        create_rc(cls, **resdict)

        modify_rc()

        delete_rc()

        all_detail()



    """

    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录号
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))  # 房间号
    user_name = db.Column(db.String(20), db.ForeignKey("user.name"))  # 姓名
    rztime = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now()
    )  # 入住时间
    # room_type = db.Column(db.String(20), nullable=False)  # 房间类型
    price = db.Column(db.Float, nullable=False)  # 价格
    tele = db.Column(db.String(20))  # 电话
    user = db.relationship("User", backref=db.backref("u_records"))
    room = db.relationship("Room", backref=db.backref("r_records"))
    db.UniqueConstraint(room_id, user_name, name="unique_room_user")

    @classmethod
    def create_rc(cls, resdict: dict):
        tmp = Records(
            user_name=resdict.get("name"),
            room_id=int(resdict.get("room_num")),  # type:ignore
            price=float(resdict.get("price")),  # type:ignore
            tele=resdict.get("tele"),
        )
        db.session.add(tmp)
        tmp2 = db.session.query(Room).filter(Room.id == resdict.get("room_num")).one()
        tmp2.reservers -= 1
        db.session.commit()

    @classmethod
    def modify_rc(cls, resdict: dict):
        # app.app_context().push()
        # print('jinru02')
        tmp = (
            db.session.query(Records)
            .filter(
                Records.user_name == resdict.get("name"),
                Records.room_id == resdict.get("room_num"),
            )
            .first()
        )
        db.session.delete(tmp)
        db.session.commit()
        Records.create_rc(**resdict)

    @classmethod
    def delete_rc(cls, resdict: dict):
        print(resdict.get("delete_room"))
        print(resdict.get("delete_user"))
        tmp = (
            db.session.query(Records)
            .filter(
                Records.room_id == resdict.get("delete_room"),
                Records.user_name == resdict.get("delete_user"),
            )
            .first()
        )
        db.session.delete(tmp)
        tmp2 = (
            db.session.query(Room).filter(Room.id == resdict.get("delete_room")).one()
        )
        tmp2.reservers += 1
        db.session.commit()

    @classmethod
    def all_detail(cls):
        tmps = db.session.query(Records).all()
        return tmps
