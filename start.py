"""
一键启动课表应用：后端 + 前端 + 内网穿透
用法：cd E:\course && python start.py
"""

import subprocess
import sys
import time
import re
import shutil
import signal
import os

# ── 配置 ──────────────────────────────────────────────
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

processes: list[subprocess.Popen] = []


def cleanup(sig=None, frame=None):
    print("\n\n🛑 正在关闭所有服务...")
    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass
    for p in processes:
        try:
            p.wait(timeout=5)
        except Exception:
            p.kill()
    print("✅ 已全部关闭。")
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def banner(text):
    width = 52
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def find_tunnel_tool():
    """检测可用的穿透工具，返回 (名称, 命令列表)"""
    # 优先 ngrok（更稳定）
    if shutil.which("ngrok"):
        return "ngrok", ["ngrok", "http", str(FRONTEND_PORT), "--log=stdout", "--log-format=json"]
    # 回退到 localtunnel（免注册，npx 直接用）
    return "localtunnel", ["npx", "--yes", "localtunnel", "--port", str(FRONTEND_PORT)]


def start_backend():
    banner("🚀 启动后端 (FastAPI)")
    p = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload",
         "--host", "127.0.0.1", "--port", str(BACKEND_PORT)],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    processes.append(p)
    # 等待启动
    time.sleep(2)
    if p.poll() is not None:
        print("❌ 后端启动失败！")
        sys.exit(1)
    print(f"   ✅ 后端运行中 → http://127.0.0.1:{BACKEND_PORT}")


def seed_database():
    banner("🌱 写入测试课程数据")
    p = subprocess.run(
        [sys.executable, "seed.py"],
        cwd=BACKEND_DIR,
        capture_output=True, text=True,
    )
    if p.returncode == 0:
        print(f"   ✅ {p.stdout.strip()}")
    else:
        print(f"   ⚠️  seed 跳过或失败: {p.stderr.strip()}")


def start_frontend():
    banner("🚀 启动前端 (Vite)")
    p = subprocess.Popen(
        ["npm.cmd" if os.name == "nt" else "npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    processes.append(p)
    time.sleep(4)
    if p.poll() is not None:
        print("❌ 前端启动失败！请确认已运行 npm install")
        sys.exit(1)
    print(f"   ✅ 前端运行中 → http://127.0.0.1:{FRONTEND_PORT}")


def start_tunnel():
    tool_name, cmd = find_tunnel_tool()
    banner(f"🌐 启动内网穿透 ({tool_name})")

    if tool_name == "ngrok":
        return start_ngrok(cmd)
    else:
        return start_localtunnel(cmd)


def start_ngrok(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    processes.append(p)

    public_url = None
    deadline = time.time() + 15

    while time.time() < deadline:
        line = p.stdout.readline()
        if not line:
            time.sleep(0.3)
            continue
        # ngrok json 日志里找 public_url
        m = re.search(r'"url":"(https://[^"]+)"', line)
        if m:
            public_url = m.group(1)
            break

    if public_url:
        print_url(public_url)
    else:
        print("   ⚠️  未能自动获取 ngrok URL，请查看 ngrok 窗口或访问 http://127.0.0.1:4040")
    return public_url


def start_localtunnel(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    processes.append(p)

    public_url = None
    deadline = time.time() + 30

    while time.time() < deadline:
        line = p.stdout.readline()
        if not line:
            time.sleep(0.3)
            continue
        print(f"   [lt] {line.strip()}")
        # localtunnel 输出格式: your url is: https://xxx.loca.lt
        m = re.search(r"(https://[a-z0-9-]+\.loca\.lt)", line)
        if m:
            public_url = m.group(1)
            break

    if public_url:
        print_url(public_url)
    else:
        print("   ⚠️  未能自动获取穿透 URL，请查看上方日志")
    return public_url


def print_url(url):
    print()
    print("   ┌──────────────────────────────────────────┐")
    print("   │                                          │")
    print(f"   │  📱 手机访问地址:                          │")
    print(f"   │                                          │")
    print(f"   │  {url:<40s} │")
    print("   │                                          │")
    print("   │  在手机浏览器打开上方地址即可              │")
    print("   │  (localtunnel 首次会有一个确认页面，       │")
    print("   │   点 Click to Continue 即可)              │")
    print("   │                                          │")
    print("   └──────────────────────────────────────────┘")
    print()
    print("   💡 Ctrl+C 退出所有服务")
    print()


# ── 主流程 ────────────────────────────────────────────
if __name__ == "__main__":
    banner("📅 课表应用 — 一键启动")

    start_backend()
    seed_database()
    start_frontend()
    public_url = start_tunnel()

    # 保持运行，等待 Ctrl+C
    print("\n⏳ 服务运行中... 按 Ctrl+C 退出\n")
    try:
        while True:
            time.sleep(1)
            # 检查子进程是否意外退出
            for i, p in enumerate(processes):
                if p.poll() is not None:
                    print(f"\n⚠️  进程 #{i} 意外退出 (code={p.returncode})")
    except KeyboardInterrupt:
        cleanup()
