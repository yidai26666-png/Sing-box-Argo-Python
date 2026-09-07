import os
import subprocess
import threading
from flask import Flask, Response

# 环境变量配置；填入 ARGO_DOMAIN 和 ARGO_AUTH 使用固定隧道
os.environ.setdefault('UPLOAD_URL', '')
os.environ.setdefault('PROJECT_URL', '')
os.environ.setdefault('AUTO_ACCESS', 'false')
os.environ.setdefault('FILE_PATH', '.cache')
os.environ.setdefault('SUB_PATH', 'sub')
os.environ.setdefault('UUID', 'b3a383e5-2732-4e85-880d-a6dd8fcff5ad')
os.environ.setdefault('ARGO_DOMAIN', 'pella.xike.kdns.fr')
os.environ.setdefault('ARGO_AUTH', 'eyJhIjoiYWUxZjBiZWUzNTY4ZDc0MTg4MjY2YjJiZTM2YjJjNjYiLCJ0IjoiOGI1MmNhMDQtMTQ4NS00MWJjLWE4YjYtNGRlMTdlNGE4ODc3IiwicyI6Ik5EazJOV001TVRRdE5qRTVNeTAwWXpkbUxXSmpOR1F0T0dSbE5ESTBOVFUyT0RRNCJ9')
os.environ.setdefault('ARGO_PORT', '8137')
os.environ.setdefault('CFIP', 'saas.sin.fan')
os.environ.setdefault('CFPORT', '443')
os.environ.setdefault('PORT', '3000')
os.environ.setdefault('NAME', 'pella')
os.environ.setdefault('CHAT_ID', '662214858')
os.environ.setdefault('BOT_TOKEN', '8369440526:AAE_wH6ujnjfNLCIqZo8-nIc369IPb64uuQ')
os.environ.setdefault('DISABLE_ARGO', 'false')

# 提取并解析关键运行时变量
SUB_PATH = os.environ['SUB_PATH'].strip('/')
PORT = int(os.environ['PORT'])
FILE_PATH = os.path.abspath(os.environ['FILE_PATH'])
sub_path = os.path.join(FILE_PATH, '.tmp')

app = Flask(__name__)

@app.route('/')
def home():
    return "Service is running perfectly!"

@app.route(f'/{SUB_PATH}')
def sub():
    if os.path.exists(sub_path):
        try:
            with open(sub_path, 'r', encoding='utf-8') as f:
                return Response(f.read(), mimetype='text/plain')
        except Exception:
            pass
    return Response("Subscription not ready yet", status=404)

def start_go_binary():
    go_bin = os.path.join(os.getcwd(), 'main')
    if os.path.exists(go_bin):
        try:
            os.chmod(go_bin, 0o775)
            # 继承所有环境变量并启动 Go 二进制
            subprocess.Popen([go_bin], env=os.environ.copy())
            print("Successfully launched ./main Go binary in background!")
        except Exception as e:
            print(f"Error launching ./main: {e}")

# 在后台守护线程中启动 Go 二进制
threading.Thread(target=start_go_binary, daemon=True).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
