#!/usr/bin/env python3
"""
数据库迁移脚本
用于在 Railway 等生产环境中添加新字段，而不丢失现有数据
"""

import os
import sys

# 确保在 backend 目录下运行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from database import engine, DATABASE_URL
import sqlalchemy

def migrate_database():
    """执行数据库迁移"""

    print("🔄 开始数据库迁移...")

    insp = sqlalchemy.inspect(engine)

    if not insp.has_table("courses"):
        print("ℹ️  courses 表不存在，无需迁移")
        return

    # 获取现有列
    existing_columns = {col["name"] for col in insp.get_columns("courses")}
    print(f"📋 现有字段: {', '.join(sorted(existing_columns))}")

    # 需要添加的新列
    new_columns = {
        "teacher": "VARCHAR DEFAULT ''",
        "start_time": "VARCHAR DEFAULT ''",
        "end_time": "VARCHAR DEFAULT ''",
    }

    # 检查并添加缺失的列
    added = []
    with engine.connect() as conn:
        for col_name, col_type in new_columns.items():
            if col_name not in existing_columns:
                try:
                    sql = f"ALTER TABLE courses ADD COLUMN {col_name} {col_type}"
                    conn.execute(sqlalchemy.text(sql))
                    conn.commit()
                    added.append(col_name)
                    print(f"✅ 已添加字段: {col_name}")
                except Exception as e:
                    print(f"❌ 添加字段 {col_name} 失败: {e}")
                    conn.rollback()
            else:
                print(f"ℹ️  字段已存在: {col_name}")

    if added:
        print(f"\n🎉 迁移完成！已添加 {len(added)} 个字段: {', '.join(added)}")
    else:
        print("\n✅ 数据库已是最新状态，无需迁移")

    # 验证最终结果
    final_columns = {col["name"] for col in insp.get_columns("courses")}
    print(f"\n📋 最终字段: {', '.join(sorted(final_columns))}")

    required = {"name", "classroom", "day_of_week", "start_period", "duration", "teacher", "start_time", "end_time"}
    missing = required - final_columns
    if missing:
        print(f"⚠️  仍缺少字段: {', '.join(missing)}")
    else:
        print("✅ 所有必需字段都已存在")

if __name__ == "__main__":
    migrate_database()
