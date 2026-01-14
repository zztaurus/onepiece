"""
SQLAlchemy数据库配置和初始化
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db():
    """初始化数据库表和数据"""
    # 导入所有模型
    from onepiece.models.user import User
    from onepiece.models.crew_member import CrewMember
    from onepiece.models.pirate_group import PirateGroup

    # 创建所有表
    db.create_all()
    print("✅ 数据表创建成功")

    # 初始化默认数据
    init_users()
    init_pirate_groups()
    init_crew_members()


def init_users():
    """初始化默认用户"""
    from onepiece.models.user import User

    if User.query.count() == 0:
        users = [
            User(username='admin', password='admin123'),
            User(username='user', password='user123')
        ]
        for user in users:
            db.session.add(user)
        db.session.commit()
        print("✅ 默认用户创建成功")
    else:
        print("ℹ️  用户数据已存在")


def init_pirate_groups():
    """初始化海贼团数据"""
    from onepiece.models.pirate_group import PirateGroup

    if PirateGroup.query.count() == 0:
        groups = [
            PirateGroup(
                name='草帽海贼团',
                captain='蒙奇·D·路飞',
                ship_name='千阳号',
                total_bounty='88.16亿贝里',
                flag_description='带草帽的骷髅旗',
                origin='东海',
                member_count=10,
                description='由蒙奇·D·路飞创建的海贼团，梦想是找到ONE PIECE成为海贼王。船员之间情同手足，经历了无数冒险。'
            ),
            PirateGroup(
                name='红发海贼团',
                captain='香克斯',
                ship_name='雷德·佛斯号',
                total_bounty='40.48亿贝里以上',
                flag_description='三道伤疤的骷髅旗',
                origin='西海',
                member_count=10,
                description='四皇之一香克斯率领的海贼团，实力强大，船员个个都是精英。'
            ),
            PirateGroup(
                name='白胡子海贼团',
                captain='爱德华·纽盖特（已故）',
                ship_name='莫比迪克号',
                total_bounty='未知',
                flag_description='卍字骷髅旗',
                origin='新世界',
                member_count=1600,
                description='曾经的世界最强海贼团，白胡子视所有船员为家人。'
            ),
            PirateGroup(
                name='黑胡子海贼团',
                captain='马歇尔·D·蒂奇',
                ship_name='剑刃号',
                total_bounty='39.96亿贝里以上',
                flag_description='三个骷髅头',
                origin='伟大航路',
                member_count=10,
                description='四皇之一黑胡子领导的海贼团，拥有震震果实和暗暗果实两种能力。'
            ),
            PirateGroup(
                name='红心海贼团',
                captain='特拉法尔加·罗',
                ship_name='潜水艇北极潜航号',
                total_bounty='30亿贝里以上',
                flag_description='带笑脸的骷髅旗',
                origin='北海',
                member_count=21,
                description='罗率领的海贼团，以潜水艇为主要交通工具，船员多为医疗人员。'
            )
        ]
        for group in groups:
            db.session.add(group)
        db.session.commit()
        print("✅ 海贼团数据初始化完成")
    else:
        print("ℹ️  海贼团数据已存在")


def init_crew_members():
    """初始化船员数据"""
    from onepiece.models.crew_member import CrewMember
    from onepiece.models.pirate_group import PirateGroup

    if CrewMember.query.count() == 0:
        # 获取草帽海贼团ID
        straw_hat = PirateGroup.query.filter_by(name='草帽海贼团').first()

        # 使用本地角色图片
        members = [
            CrewMember(
                name='蒙奇·D·路飞',
                role='船长',
                bounty='30亿贝里',
                image_url='/images/luffy.jpg',
                description='橡胶果实能力者，拥有将身体橡胶化的能力。性格乐观开朗，极度重视伙伴，拥有强大的意志力和战斗天赋。',
                devil_fruit='橡胶果实（尼卡形态）',
                haki_types='霸王色霸气、武装色霸气、见闻色霸气',
                special_skills='四档、五档变身',
                signature_moves='橡胶火箭炮、橡胶象枪、橡胶猿王枪、橡胶大猿王枪',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='罗罗诺亚·索隆',
                role='战斗员/剑士',
                bounty='11.11亿贝里',
                image_url='/images/zoro.jpg',
                description='三刀流剑士，梦想成为世界第一大剑豪。虽然是路痴，但实力强大，是船上的副手。',
                devil_fruit='无',
                haki_types='武装色霸气、见闻色霸气、霸王色霸气',
                special_skills='三刀流剑术、阎魔剑',
                signature_moves='三千世界、九刀流阿修罗、狮子歌歌、死·狮子歌歌',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='娜美',
                role='航海士',
                bounty='3.66亿贝里',
                image_url='/images/nami.jpg',
                description='天才航海士，对天气有着超乎常人的感知能力。虽然爱财，但对伙伴十分关心。',
                devil_fruit='无',
                haki_types='无',
                special_skills='气象预测、魔法天候棒、宙斯',
                signature_moves='雷光枪、雷鸣蛋、雷云天气',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='乌索普',
                role='狙击手',
                bounty='5亿贝里',
                image_url='/images/usopp.jpg',
                description='出色的狙击手和发明家，拥有超远距离的狙击能力。虽然胆小爱吹牛，但关键时刻总能挺身而出。',
                devil_fruit='无',
                haki_types='见闻色霸气',
                special_skills='超远距离狙击、独角仙弹弓',
                signature_moves='绿星系列、流星火鸟星、必杀绿星冲击狼草',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='香吉士',
                role='厨师',
                bounty='10.32亿贝里',
                image_url='/images/sanji.jpg',
                description='一流的厨师和战斗员，使用脚技战斗以保护做菜的双手。梦想找到传说中的ALL BLUE。',
                devil_fruit='无',
                haki_types='武装色霸气、见闻色霸气',
                special_skills='黑足流踢技、恶魔风脚、外骨骼',
                signature_moves='首肉、羊肉SHOT、牛肉BURST、恶魔风脚·画龙点睛',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='托尼托尼·乔巴',
                role='船医',
                bounty='1000贝里',
                image_url='/images/chopper.jpg',
                description='人人果实能力者，是一只能够说话和变身的驯鹿。医术高超，心地善良。',
                devil_fruit='人人果实',
                haki_types='无',
                special_skills='七段变身、蓝波球强化',
                signature_moves='角强化、腕力强化、毛皮强化、怪物强化',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='妮可·罗宾',
                role='考古学家',
                bounty='9.3亿贝里',
                image_url='/images/robin.jpg',
                description='花花果实能力者，世界上唯一能解读历史正文的考古学家。成熟稳重，知识渊博。',
                devil_fruit='花花果实',
                haki_types='武装色霸气',
                special_skills='身体部位开花、巨大化',
                signature_moves='千紫万红巨大树、万轮花、恶魔之花',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='弗兰奇',
                role='船匠',
                bounty='3.94亿贝里',
                image_url='/images/franky.jpg',
                description='改造人船匠，千阳号的建造者。身体藏有各种武器和机关。',
                devil_fruit='无',
                haki_types='无',
                special_skills='改造人身体、弗兰奇将军',
                signature_moves='风来炮、激光光束、弗兰奇火球、铁拳重锤',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='布鲁克',
                role='音乐家',
                bounty='3.83亿贝里',
                image_url='/images/brook.jpg',
                description='黄泉果实能力者，死后灵魂回归躯体变成骷髅。优雅绅士，擅长剑术和音乐。',
                devil_fruit='黄泉果实',
                haki_types='无',
                special_skills='灵魂出窍、黄泉冷气',
                signature_moves='鼻歌三丁·箭尾斩、前奏·抛射、魂之挽歌',
                pirate_group_id=straw_hat.id if straw_hat else None
            ),
            CrewMember(
                name='甚平',
                role='舵手',
                bounty='11亿贝里',
                image_url='/images/jinbe.jpg',
                description='鱼人族的空手道高手，前王下七武海成员。沉稳可靠，经验丰富。',
                devil_fruit='无',
                haki_types='武装色霸气、见闻色霸气',
                special_skills='鱼人空手道、鱼人柔术、水中战斗',
                signature_moves='武赖贯、海流一本背负投、群鲛、梅花皮',
                pirate_group_id=straw_hat.id if straw_hat else None
            )
        ]

        for member in members:
            db.session.add(member)
        db.session.commit()
        print("✅ 草帽海贼团船员数据初始化完成")
    else:
        print("ℹ️  船员数据已存在")