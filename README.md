## 🎵 Darkmoon Records — Music Discovery

Uma aplicação para descobrir e recomendar álbuns musicais aleatórios baseado em gênero. Popula o catálogo via Last.fm e recomenda do banco local.

**Status:** v1.0.0 — Em desenvolvimento ativo 🚀

---

## 🎯 Funcionalidades

- ✅ **Recomendação Aleatória** — Retorna um álbum aleatório de um gênero específico
- 🔍 **Integração Last.fm** — Popula banco de dados com álbuns reais via API
- 📊 **Listagem por Gênero** — Filtra e lista álbuns do catálogo
- 🔐 **Autenticação JWT** — Rotas administrativas protegidas por token
- 🗄️ **Persistência Local** — SQLite com SQLAlchemy ORM
- 🌐 **Frontend Web** — Interface HTML/CSS para descoberta e administração
- 📚 **Documentação Interativa** — Swagger/OpenAPI automático

---

## 🛠️ Estrutura do Projeto

```
darkmoon-records/
├── backend/
│   ├── main.py                 # Endpoints da API + CORS
│   ├── models/
│   │   └── database.py         # Modelos e helpers SQLAlchemy
│   ├── services/
│   │   └── music_service.py    # Integração Last.fm
│   ├── auth/
│   │   └── auth.py             # JWT — geração e verificação
│   ├── testAPI.py              # Script de teste Last.fm
│   └── darkmoon_records.db     # SQLite (gerado automaticamente)
├── frontend/
│   ├── index.html              # Página de descoberta
│   ├── admin.html              # Painel administrativo
│   ├── style.css               # Estilos globais
│   └── public/
│       └── img/
│           └── darkmoon.jpg    # Imagem do header
├── .env                        # Variáveis de ambiente
├── .env.example                # Modelo de variáveis
├── requirements.txt
└── README.md
```

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
pip install -r backend/requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp backend/.env.example backend/.env
```

Edite o `backend/.env` com suas chaves:
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

### 4. Inicie o backend
```bash
cd backend
uvicorn main:app --reload
```

API rodando em: **http://localhost:8000**

### 5. Abra o frontend

Abra `frontend/index.html` diretamente no navegador, ou sirva com Live Server / qualquer servidor estático.

---

## 🌐 Frontend

| Página | Arquivo | Descrição |
|--------|---------|-----------|
| Descoberta | `frontend/index.html` | Recomendação por gênero, listagem de álbuns e stats |
| Admin | `frontend/admin.html` | Login, popular gêneros e deletar álbuns |

O frontend consome a API em `http://localhost:8000`. Para alterar, edite a constante `API` no `<script>` de cada página.

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

No frontend, o token é obtido pelo painel Admin e salvo no `localStorage` (válido por 24 horas).

No Swagger (`/docs`), clique em **Authorize** (cadeado) e cole o token.

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

## ⚙️ Tech Stack

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.9+ | Runtime |
| **FastAPI** | 0.135+ | Framework Web |
| **SQLAlchemy** | 2.0+ | ORM |
| **SQLite** | 3 | Database local |
| **Pydantic** | 2.0+ | Validação |
| **PyJWT** | 2.12+ | Autenticação JWT |
| **HTML/CSS/JS** | — | Frontend (vanilla) |

---

## 🔮 Roadmap

- [ ] 💾 Histórico de recomendações
- [ ] 🔎 Busca de álbuns por nome/artista

---

**Made with 🎵 by Renan Chaves**
