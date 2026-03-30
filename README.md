## 🎵 Darkmoon Records — Music Discovery API

Uma API para descobrir e recomendar álbuns musicais aleatórios baseado em gênero. Popula o catálogo via Last.fm e recomenda do banco local.

**Status:** v1.0.0 — Em desenvolvimento ativo 🚀

---

## 🎯 Funcionalidades

- ✅ **Recomendação Aleatória** — Retorna um álbum aleatório de um gênero específico
- 🔍 **Integração Last.fm** — Popula banco de dados com álbuns reais via API
- 📊 **Listagem por Gênero** — Filtra e lista álbuns do catálogo
- 🔐 **Autenticação JWT** — Rotas administrativas protegidas por token
- 🗄️ **Persistência Local** — SQLite com SQLAlchemy ORM
- 📚 **Documentação Interativa** — Swagger/OpenAPI automático

---

## 🚀 Quick Start

### 1. Clone e navegue
```bash
git clone https://github.com/renanpchaves/darkmoon-records
cd darkmoon-records
```

### 2. Setup do ambiente
```powershell
python -m venv venv
venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o `.env` com suas chaves:
```env
LASTFM_API_KEY=sua_chave_lastfm
LASTFM_API_SECRET=seu_secret_lastfm
ADMIN_API_KEY=sua_chave_admin
JWT_SECRET=seu_jwt_secret
```

Para gerar `ADMIN_API_KEY` e `JWT_SECRET`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Execute a API
```bash
cd src
uvicorn main:app --reload
```

Servidor rodando em: **http://localhost:8000**

---

## 📚 Documentação Interativa

```
http://localhost:8000/docs
```

---

## 🔐 Autenticação

Rotas administrativas (`POST /populate`, `DELETE /albums/{id}`) exigem JWT.

**1. Obtenha um token:**
```
POST /auth/token
Content-Type: application/json

{ "api_key": "SUA_ADMIN_API_KEY" }
```

**2. Use o token nas rotas protegidas:**
```
Authorization: Bearer SEU_TOKEN
```

No Swagger (`/docs`), clique em **Authorize** (cadeado) e cole o token.

O token expira em **24 horas**.

---

## 🛣️ Endpoints

| Método | Rota | Auth | Descrição |
|--------|------|:----:|-----------|
| `GET` | `/` | — | Informações da API |
| `POST` | `/auth/token` | — | Gera JWT via ADMIN_API_KEY |
| `POST` | `/populate` | ✅ | Popula gênero via Last.fm |
| `GET` | `/recommend` | — | Recomenda álbum aleatório por gênero |
| `GET` | `/albums` | — | Lista todos os álbuns |
| `DELETE` | `/albums/{id}` | ✅ | Remove álbum por ID |
| `GET` | `/genres` | — | Lista gêneros disponíveis |
| `GET` | `/stats` | — | Total de álbuns no banco |

---

## 🗄️ Estrutura do Banco de Dados

### Tabela: `albums`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | Integer | Primary Key |
| `name` | String | Nome do álbum |
| `artist` | String | Artista |
| `genre` | JSON | Lista de gêneros (ex: `["rock", "progressive"]`) |
| `image_url` | String | URL da capa |
| `external_link` | String | Link Last.fm |

---

## 🛠️ Estrutura do Projeto

```
darkmoon-records/
├── src/
│   ├── main.py                 # Endpoints da API
│   └── auth.py                 # JWT — geração e verificação
├── models/
│   └── database.py             # Modelos e helpers SQLAlchemy
├── services/
│   └── music_service.py        # Integração Last.fm
├── .env.example                # Variáveis de ambiente (modelo)
├── requirements.txt
└── darkmoon_records.db         # SQLite (gerado automaticamente)
```

---

## ⚙️ Tech Stack

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.9+ | Runtime |
| **FastAPI** | 0.135+ | Framework Web |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3 | Database local |
| **Pydantic** | 2.0+ | Validação |
| **PyJWT** | 2.12+ | Autenticação JWT |

---

## 🔮 Roadmap

- [ ] 💾 Histórico de recomendações
- [ ] 🎨 Frontend web

---

**Made with 🎵 by Renan Chaves**
