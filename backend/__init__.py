from fastapi import FastAPI

def create_app():
    app=FastAPI()
    app.state.my_state=False

    return app

app=create_app()