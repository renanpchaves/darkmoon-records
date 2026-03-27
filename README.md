## 🎵 Darkmoon Records — Music Discovery API

Uma API robusta para descobrir e recomendar álbuns musicais aleatórios baseado em gênero. Inicia com dados da Last.fm e recomenda do catálogo local com busca otimizada.

**Status:** v1.0.0 — Em desenvolvimento ativo 🚀

---

## 🎯 Funcionalidades

- ✅ **Recomendação Aleatória** — Retorna um álbum aleatório de um gênero específico
- 🔍 **Integração Last.fm** — Popula banco de dados com álbuns reais via API
- 📊 **Busca por Gênero** — Filtra álbuns com índices otimizados
- 🗄️ **Persistência Local** — SQLite com SQLAlchemy ORM
- 📚 **Documentação Interativa** — Swagger/OpenAPI automático

---

## 🚀 Quick Start

### 1. Clone e navegue
```bash
git clone https://github.com/renanpchaves/darkmoon-records
cd darkmoon-records/api
```

### 2. Setup do Ambiente
```powershell
# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate.ps1

# Instale dependências
pip install -r ../requirements.txt
```

### 3. Execute a API
```bash
python -m main
```

Servidor rodando em: **http://localhost:8000**


---

## 📚 Documentação Interativa

Acesse o Swagger UI após iniciar a API:

```
http://localhost:8000/docs
```

Todos os endpoints podem ser testados diretamente pela interface! 🎮

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `albums`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Integer | Primary Key |
| `name` | String | Nome do álbum |
| `artist` | String | Artista |
| `genre` | JSON | Lista de gêneros (ex: ["rock", "progressive"]) |
| `image_url` | String | URL da capa |
| `external_id` | String | ID Last.fm |
| `external_link` | String | Link Last.fm |

---

## ⚙️ Tech Stack

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.9+ | Runtime |
| **FastAPI** | 0.104+ | Framework Web |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3 | Database Local |
| **Pydantic** | 2.0+ | Validação |

---

## 🔮 Roadmap (Próximas Versões)

- [ ] 🔐 Autenticação de usuários
- [ ] 💾 Histórico de recomendações
- [ ] 🎨 Frontend web

---

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
api/
├── main.py                 # Endpoints da API
├── models/
│   └── database.py         # Configuração SQLAlchemy
├── services/
│   └── music_service.py    # Integração Last.fm
└── darkmoon_records.db     # SQLite (gerado)
```

### Rodar com Hot Reload
```bash
pip install uvicorn
uvicorn main:app --reload
```

---

**Made with 🎵 by Renan Chaves** 