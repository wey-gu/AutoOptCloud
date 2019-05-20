from .app import create_backend_instance, create_data_watchdog_instance, socketio


def wsgi():
    app = create_backend_instance()
    socketio.run(app)