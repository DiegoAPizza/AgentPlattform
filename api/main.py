from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from api.routes.agent import router, limiter
import logging

# ESTO ES LO QUE FALTA: Le dice a Python que muestre los INFO en consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


app = FastAPI(title="AgentPlatform")

# Configuramos slowapi en la app principal
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Incluimos las rutas
app.include_router(router)