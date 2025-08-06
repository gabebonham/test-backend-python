from models.formulario import Formulario 
from DTOs.formulario import FormularioDTO
from DTOs.pergunta import PerguntaDTO
from DTOs.resposta import RespostaDTO
from models.resposta import Resposta
from models.pergunta import Pergunta
def dict_to_object(data_dict, class_type):
    obj = class_type(**data_dict)
    return obj
def obj_to_dict(obj):
    if obj is None:
        return None
    if isinstance(obj, list):
        return [obj_to_dict(item) for item in obj]
    if hasattr(obj, "_mapping"): 
        return dict(obj._mapping)
    elif hasattr(obj, "__dict__"): 
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
    else:
        return {attr: getattr(obj, attr) for attr in dir(obj) if not attr.startswith("_")}
    
    

def map_formulario_to_dto(model: Formulario|FormularioDTO, perguntas: list=[]) -> FormularioDTO:
    return model if isinstance(model,FormularioDTO) else FormularioDTO(
        id=model.id,
        titulo=model.titulo,
        descricao=model.descricao,
        perguntas=[map_to_pergunta_dto(p) for p in perguntas],
        ordem=model.ordem,
        createdAt=model.createdat,
    )
def map_formulario_to_dto_no_pergunta(model: Formulario|FormularioDTO, perguntas: list=[]) -> FormularioDTO:
    return model if isinstance(model,FormularioDTO) else FormularioDTO(
        id=model.id,
        titulo=model.titulo,
        descricao=model.descricao,
        perguntas=perguntas,
        ordem=model.ordem,
        createdAt=model.createdat)
def map_to_pergunta_dto(pergunta: Pergunta|PerguntaDTO, respostas: list = []) -> PerguntaDTO:
    return pergunta if isinstance(pergunta,PerguntaDTO) else PerguntaDTO(
        id=pergunta.id,
        idformulario=pergunta.idformulario,
        titulo=pergunta.titulo,
        codigo=pergunta.codigo,
        orientacaoresposta=pergunta.orientacaoresposta,
        ordem=pergunta.ordem,
        obrigatoria=pergunta.obrigatoria,
        subpergunta=pergunta.subpergunta,
        createdat=pergunta.createdat,
        tipopergunta=pergunta.tipopergunta,
        respostas=[map_resposta_to_dto(r) for r in respostas]
    )

def map_resposta_to_dto(resposta:Resposta|RespostaDTO, vezesRespondidas:int=None):
    return resposta if isinstance(resposta,RespostaDTO) else RespostaDTO(
        id=resposta.id,
        idpergunta=str(resposta.idpergunta),
        resposta=resposta.resposta,
        ordem=resposta.ordem,
        respostaaberta=resposta.respostaaberta,
        vezesrespondidas=vezesRespondidas or [],
        createdat=resposta.createdat
    )