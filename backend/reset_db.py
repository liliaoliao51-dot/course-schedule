#!/usr/bin/env python3
"""
数据库重置脚本
用于删除旧数据库并重新创建包含所有字段的新数据库
"""

import os
import sys

# 确保在 backend 目录下运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, DATABASE_URL
import models  # 确保模型被导入

def reset_database():
    """重置数据库"""

    if DATABASE_URL.startswith("sqlite"):
        # SQLite: 删除文件并重建
        db_path = os.path.join(os.path.dirname(__file__), "courses.db")

        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✅ 已删除旧数据库: {db_path}")
        else:
            print(f"ℹ️  数据库文件不存在: {db_path}")

        # 创建新表
        Base.metadata.create_all(bind=engine)
        print("✅ 已创建新数据库表")

        # 验证表结构
        import sqlalchemy
        insp = sqlalchemy.inspect(engine)
        if insp.has_table("courses"):
            columns = [col["name"] for col in insp.get_columns("courses")]
            print(f"✅ courses 表包含以下字段: {', '.join(columns)}")

            required = {"name", "classroom", "day_of_week", "start_period", "duration", "teacher", "start_time", "end_time"}
            missing = required - set(columns)
            if missing:
                print(f"❌ 缺少字段: {', '.join(missing)}")
                sys.exit(1)
            else:
                print("✅ 所有必需字段都已存在")

    else:
        # PostgreSQL: 直接重建表（会删除所有数据！）
        print("⚠️  警告: 正在重置 PostgreSQL 数据库，所有数据将丢失！")

        # 删除所有表
        Base.metadata.drop_all(bind=engine)
        print("✅ 已删除所有表")

        # 重新创建
        Base.metadata.create_all(bind=engine)
        print("✅ 已重新创建所有表")

    print("\n🎉 数据库重置完成！现在可以启动后端服务了。")
    print("   运行: uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    # 确认操作
    if "--confirm" not in sys.argv:
        print("⚠️  此操作将删除所有课程数据！")
        print("   如果确定要继续，请运行:")
        print("   python reset_db.py --confirm")
        sys.exit(0)

    reset_database()
