from fastapi import APIRouter, FastAPI
from controller.formularios_controller import FormulariosController
from controller.pergunta_controller import PerguntaController
from controller.resposta_controller import RespostasController
from controller.rasposta_pergunta_controller import RespostaPerguntaController
app = FastAPI()
formularios_controller = FormulariosController()
perguntas_controller = PerguntaController()
respostas_controller = RespostasController()
respostas_perguntas_controller = RespostaPerguntaController()
app.include_router(formularios_controller.router)
app.include_router(perguntas_controller.router)
app.include_router(respostas_controller.router)
app.include_router(respostas_perguntas_controller.router)
