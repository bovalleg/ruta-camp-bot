# 🏕️ Ruta Camp Bot — Social Media Manager

Bot de gestión de redes sociales para Ruta Camp. Crea, diseña y programa contenido para Instagram a través de Claude AI y Buffer.

## ✨ Características

- **Generación con IA** — Posts, Reels, Historias y Carruseles con Claude
- **Flujo de aprobación** — Revisa, aprueba, pide cambios o rechaza publicaciones
- **Calendario visual** — Ve toda tu programación de contenido
- **Biblioteca de medios** — Navega imágenes y videos de tu Google Drive
- **Buffer integration** — Programa publicaciones directamente en Instagram
- **GitHub Actions** — Generación automática semanal/mensual

---

## 🚀 Setup en GitHub Pages (5 pasos)

### 1. Crear repositorio en GitHub

1. Ve a [github.com/new](https://github.com/new)
2. Nombre: `ruta-camp-bot`
3. Visibilidad: **Private** (recomendado)
4. Crea el repositorio

### 2. Subir el código

```bash
cd ruta-camp-bot
git init
git add .
git commit -m "🏕️ Ruta Camp Bot - initial setup"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/ruta-camp-bot.git
git push -u origin main
```

### 3. Activar GitHub Pages

1. Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Save

Tu bot estará en: `https://TU_USUARIO.github.io/ruta-camp-bot`

### 4. Configurar Secrets (para GitHub Actions)

Settings → Secrets and variables → Actions:

**Secrets:**
| Nombre | Valor |
|--------|-------|
| `CLAUDE_API_KEY` | Tu clave API de Anthropic |

**Variables:**
| Nombre | Valor |
|--------|-------|
| `BRAND_NAME` | `Ruta Camp` |
| `BRAND_TONE` | `empresa de turismo outdoor, aventurero y apasionado` |
| `BRAND_TAGS` | `#rutacamp #outdoor #aventura #senderismo` |

### 5. Configurar el bot en el browser

Abre la URL de GitHub Pages y ve a ⚙️ **Configuración**:

1. **Claude API** → Ingresa tu clave de [console.anthropic.com](https://console.anthropic.com)
2. **Buffer** → Ingresa tu token y haz clic en "Detectar Perfiles"
3. **Google Drive** → Configura las credenciales (ver abajo)
4. **Perfil de marca** → Personaliza el tono y hashtags de Ruta Camp

---

## 📁 Configurar Google Drive

### Crear proyecto en Google Cloud

1. Ve a [console.cloud.google.com](https://console.cloud.google.com)
2. Crear nuevo proyecto: "Ruta Camp Bot"
3. Activar **Google Drive API** (APIs & Services → Enable APIs)
4. Crear credenciales:
   - **API Key** → para leer archivos (restringir a Drive API)
   - **OAuth 2.0 Client ID** → tipo "Web application"
   - Agregar en "Authorized JavaScript origins": `https://TU_USUARIO.github.io`

---

## 📅 Generación automática (GitHub Actions)

| Workflow | Cuándo se ejecuta | Qué genera |
|----------|-------------------|------------|
| `generate-weekly.yml` | Cada lunes 10:00 UTC | 5 publicaciones semanales |
| `generate-monthly.yml` | Primer día del mes | 12 publicaciones mensuales |

También puedes ejecutarlos manualmente desde **Actions → Run workflow**.

Las publicaciones generadas quedan en `data/posts.json` con estado **"pending"** esperando tu aprobación en el bot.

---

## 🔄 Flujo de trabajo

```
Prompt  →  Claude genera  →  Preview en chat
                                    ↓
                          Revisar en Pendientes
                                    ↓
                    Aprobar / Pedir cambios / Rechazar
                                    ↓
                    Programar en Buffer  →  Instagram
```

---

## 🔐 Seguridad

- Las claves API se guardan **solo en tu navegador** (localStorage)
- Nunca subas claves al repositorio
- Usa un repositorio **privado** si tu contenido es confidencial
- Las GitHub Actions usan Secrets cifrados del repositorio

---

## 📦 Estructura del proyecto

```
ruta-camp-bot/
├── index.html                    # Aplicación web completa
├── data/
│   └── posts.json               # Base de datos de publicaciones
├── scripts/
│   └── generate_content.py      # Script de generación automática
├── .github/
│   └── workflows/
│       ├── generate-weekly.yml  # Generación semanal automática
│       └── generate-monthly.yml # Generación mensual automática
└── README.md
```
