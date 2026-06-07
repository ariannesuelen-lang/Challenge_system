from .repository import MiniProvaRepository
from .models import CorrecaoRequest
from .strategies import ShuffleStrategy, NoOpStrategy
from core.exceptions import NotFoundException, BadRequestException
from uuid import UUID

class MiniProvaService:
    def __init__(self):
        self.repo = MiniProvaRepository()

    def iniciar_prova(self, prova_id: UUID, usuario_id: int):
        prova_res = self.repo.get_prova(prova_id)
        if not prova_res.data: raise NotFoundException("Mini-prova não encontrada.")
        prova = prova_res.data

        if prova["status"] != "liberada":
             raise BadRequestException(f"Prova não disponível. Status: {prova['status']}")

        questoes = self.repo.get_questoes_da_disciplina(prova["disciplina_id"], prova["quantidade_questoes"]).data

        q_strategy = ShuffleStrategy() if prova["randomizar_questoes"] else NoOpStrategy()
        a_strategy = ShuffleStrategy() if prova["randomizar_alternativas"] else NoOpStrategy()

        questoes = q_strategy.execute(questoes)
        payload = []
        
        for q in questoes:
            alts = a_strategy.execute(q.get("alternativas", []))
            payload.append({
                "id": q["id"], "enunciado": q["enunciado"], "nivel_dificuldade": q["nivel_dificuldade"], "pontos": q["pontos"],
                "alternativas": [{"id": a["id"], "texto": a["texto"]} for a in alts]
            })

        return {"prova_titulo": prova["titulo"], "duracao_minutos": prova["duracao_minutos"], "quantidade_questoes": len(payload), "questoes": payload}

    def corrigir_prova(self, correcao: CorrecaoRequest):
        nota_final = 0.0
        total_acertos = 0
        
        for resp in correcao.respostas:
            alt_correta = self.repo.get_alternativa_correta(resp.questao_id).data
            if not alt_correta: continue
            
            pontos = float(self.repo.get_pontos_questao(resp.questao_id).data["pontos"])
            eh_correta = (str(resp.alternativa_id) == alt_correta["id"])
            pontos_ganhos = pontos if eh_correta else 0.0
            
            nota_final += pontos_ganhos
            if eh_correta: total_acertos += 1
                
            # Inserção com a nova coluna usuario_id
            self.repo.salvar_resposta({
                "usuario_id": correcao.usuario_id, 
                "questao_id": str(resp.questao_id),
                "alternativa_id": str(resp.alternativa_id) if resp.alternativa_id else None,
                "texto_resposta": resp.texto_resposta,
                "nota": pontos_ganhos,
                "correta": eh_correta,
                "respondida_em": "now()"
            })
            
        return {"mensagem": "Prova corrigida.", "nota_final": round(nota_final, 2), "total_acertos": total_acertos}