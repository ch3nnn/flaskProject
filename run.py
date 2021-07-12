from app import create_app, db

app = create_app("develop")


@app.cli.command()
def create_all_table():
    """创建所有表"""
    db.create_all()


if __name__ == '__main__':
    app.run()


