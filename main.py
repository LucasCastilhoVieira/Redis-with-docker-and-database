from fastapi import FastAPI
from app.controllers.user_register_controller import router as RouterRegister
from app.controllers.user_consult_controller import router as RouterConsult
from app.controllers.user_update_controller import router as RouterUpdate
from app.controllers.user_delete_controller import router as RouterDelete


app = FastAPI()

app.include_router(RouterRegister)
app.include_router(RouterUpdate)
app.include_router(RouterConsult)
app.include_router(RouterDelete)


