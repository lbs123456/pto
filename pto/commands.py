import click

from pto import app, db
from pto.models import User, Usern, Intro

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

    name = [{"name": "杨颖"}, {"name": "周杰伦"},{"name": "张三"},{"name": "PDD"}]
    profiles = {"年龄": "35",
                "身高": "170",
                "性别": "女",
                "籍贯": "香港"}
    profiles1 = {"年龄": "45",
                 "身高": "177",
                 "性别": "男",
                 "籍贯": "香港"}
    profiles2 = {"年龄": "45",
                 "身高": "187",
                 "性别": "男",
                 "籍贯": "湖南"}
    profiles3 = {"年龄": "31",
                 "身高": "170",
                 "性别": "男",
                 "籍贯": "四川成都"}

    for n in name:
        user = User(name=n["name"])
        db.session.add(user)

    intro = Intro(age=profiles["年龄"], height=profiles["身高"], gender=profiles["性别"], origo=profiles["籍贯"], user_id=1)
    intro1 = Intro(age=profiles1["年龄"], height=profiles1["身高"], gender=profiles1["性别"], origo=profiles1["籍贯"],user_id=2)
    intro2 = Intro(age=profiles2["年龄"], height=profiles2["身高"], gender=profiles2["性别"], origo=profiles2["籍贯"],user_id=3)
    intro3 = Intro(age=profiles3["年龄"], height=profiles3["身高"], gender=profiles3["性别"], origo=profiles3["籍贯"],user_id=4)
    db.session.add(intro)
    db.session.add(intro1)
    db.session.add(intro2)
    db.session.add(intro3)

    usern = Usern(username="libs", name='Admin')
    usern.set_password("1234567")  # 设置密码
    db.session.add(usern)
    db.session.commit()
    click.echo('Done.')

@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""


    usern = Usern.query.first()
    if usern is not None:
        click.echo('Updating user...')
        usern.username = username
        usern.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        usern = Usern(username=username, name='Admin')
        usern.set_password(password)  # 设置密码
        db.session.add(usern)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')

