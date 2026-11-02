"""Entry point - runs the Abu_Malk-Services app."""
import os
import sys
import subprocess
import signal
import logging

# ضمان توفر مسار vendor الدائم للحزم
_vendor_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "vendor"))
if os.path.isdir(_vendor_dir) and _vendor_dir not in sys.path:
    sys.path.insert(0, _vendor_dir)

try:
    import requests
    import flask
    import flask_socketio
    from telethon.sessions import Session
except ImportError as _imp_err:
    print(f"⚠️ تنبيه استيراد الحزم: {_imp_err}")

from app import app, socketio

def free_port(port):
    """تحرير المنفذ إذا كان مشغولاً"""
    try:
        if os.environ.get('RENDER'):
            return

        import psutil
        current_pid = os.getpid()
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr and conn.laddr.port == port:
                if conn.pid and conn.pid != current_pid:
                    try:
                        p = psutil.Process(conn.pid)
                        p.terminate()
                        p.wait(timeout=2)
                    except Exception:
                        try:
                            os.kill(conn.pid, signal.SIGKILL)
                        except Exception:
                            pass
        import time
        time.sleep(0.5)
    except Exception:
        pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if os.environ.get('RENDER'):
        port = int(os.environ.get("PORT", 3000))
        print(f"🌐 تشغيل Abu_Malk-Services على المنفذ {port} في بيئة Render")
        socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
    else:
        port = int(os.environ.get("APP_PORT", os.environ.get("PORT", 3000)))
        free_port(port)
        print(f"🌐 تشغيل Abu_Malk-Services على المنفذ {port}")
        socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
