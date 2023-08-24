from exts import db


# 用户表
class User(db.Model):
    """
    [用户表]
        介绍: 用于记录 所有已注册的用户

        字段:
            id:int 主键 用户号
            name:string 用户名
            sfz:string 身份证
            password:密码

        [method]
            user_r_fn(cls, **redict)

    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    name = db.Column(db.String(20), unique=True, nullable=False)  # 用户名/账号
    sfz = db.Column(db.String(50), unique=True, nullable=True)  # 身份证号
    password = db.Column(db.String(50), nullable=False)  # 密码
    identifier = db.Column(db.String(5), nullable=False)  # 身份识别

    def __str__(self):
        return "%s, %s" % (User.id, User.name)

    @classmethod
    def user_r_fn(cls, resdict: dict):
        """
        [note]
             # result是一个 Records类, 支持 '.' 出属性值, 如 result.id --> 返回 记录的id号
        """
        try:
            aim_user = (
                db.session.query(User)
                .filter(User.name == resdict.get("name")).one()
            )
            sex_str = str(aim_user.sfz)[16]
            sex_req = resdict.get("sex")
            if not sex_req:
                return None

            sex_check = ((int(sex_req) % 2) == (int(sex_str) % 2))

            # result = None

            if sex_check:
                tmp = db.session.query(User)\
                    .filter(User.name == resdict.get("name"))\
                    .one()
                result = tmp.u_records
            else:
                raise Exception

        except Exception as error:
            print("Exception1 :%s" % error)
            db.session.rollback()
            result = None
            return result

        else:
            new_dict = {}
            count = 0
            for i in result:
                i_dict = {
                    "id": i.id,
                    "user_name": i.user_name,
                    "price": i.price,
                    "rztime": i.rztime,
                    "tele": i.tele,
                }
                new_dict[str(count)] = i_dict
                count += 1
            return new_dict

    @classmethod
    def isPass(cls, resdict: dict):
        try:
            db.session.query(User).filter(
                User.name == resdict.get("name"),
                User.password == resdict.get("pwd"),
            ).one()
        except Exception:
            return False
        else:
            return True

    @classmethod
    def isAdmin(cls, resdict: dict):
        tmp = db.session.query(User)\
            .filter(User.name == resdict.get("name")).one()
        print(tmp)
        return tmp.identifier  # type:ignore

    @classmethod
    def register(cls, resdict: dict):
        isExists = db.session.query(User)\
            .filter(User.name == resdict.get("name")).first()

        if isExists:
            return False
        else:
            tmp = User(
                name=resdict.get("name"),
                sfz=resdict.get("passID"),
                password=resdict.get("pwd"),
            )
            db.session().add(tmp)
            db.session().commit()

        return True
