# services/__init__.py
from .auth_service import AuthService
from .batalha_de_equipes_service import BatalhaDeEquipesService
from .desafio_service import DesafioService
from .mini_prova_service import MiniProvaService
from .participacao_service import ParticipacaoService
from .quiz_ao_vivo_service import QuizAoVivoService
from .votacao_service import VotacaoService

# Instanciações unificadas do Monólito Modular
auth_service = AuthService()
batalha_service = BatalhaDeEquipesService()
desafio_service = DesafioService()
mini_prova_service = MiniProvaService()
participacao_service = ParticipacaoService()
quiz_service = QuizAoVivoService()
votacao_service = VotacaoService()
