"""
Ruta Camp Bot — Generador automático de contenido via Claude API
Usado por GitHub Actions para generar contenido programado.
"""
import os
import json
import anthropic
from datetime import datetime, timezone

BRAND_NAME = os.getenv("BRAND_NAME", "Ruta Camp")
BRAND_TONE = os.getenv("BRAND_TONE", "empresa de turismo outdoor, aventurero y apasionado por la naturaleza")
BRAND_TAGS = os.getenv("BRAND_TAGS", "#rutacamp #outdoor #aventura #senderismo #naturaleza")
PERIOD     = os.getenv("PERIOD", "week")   # week | month | semester
DATA_FILE  = "data/posts.json"

PERIOD_PROMPTS = {
    "week":     f"Crea 5 publicaciones para Instagram para esta semana laboral (lunes a viernes) de {BRAND_NAME}. Varía entre posts, reels e historias.",
    "month":    f"Crea 12 publicaciones para Instagram distribuidas durante un mes completo para {BRAND_NAME}. Incluye posts, reels, historias y carruseles.",
    "semester": f"Planifica 24 publicaciones para Instagram para los próximos 6 meses de {BRAND_NAME}. Estrategia completa con contenido variado y estacional.",
}

SYSTEM_PROMPT = f"""Eres el asistente de redes sociales de {BRAND_NAME}.
Descripción: {BRAND_TONE}
Hashtags de la marca: {BRAND_TAGS}

Cuando generes contenido, SIEMPRE devuelve SOLO JSON válido con este formato:

Para planificación (semana/mes/semestre):
{{
  "batch": true,
  "posts": [
    {{
      "type": "post|reel|story|carousel",
      "caption": "Texto del post con emojis",
      "hashtags": "#hashtag1 #hashtag2 ...",
      "imageDescription": "Descripción de imagen/video ideal",
      "scheduleHint": "Ej: Lunes 9:00am"
    }}
  ]
}}

Incluye siempre los hashtags de la marca más hashtags relevantes al contenido.
"""


def load_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_posts(posts):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


def generate():
    client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
    prompt = PERIOD_PROMPTS.get(PERIOD, PERIOD_PROMPTS["week"])

    print(f"[{datetime.now()}] Generando contenido para período: {PERIOD}")

    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = msg.content[0].text
    # Extract JSON
    import re
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        print("ERROR: No se encontró JSON en la respuesta")
        print(raw)
        return

    data = json.loads(match.group())
    now  = datetime.now(timezone.utc).isoformat()

    posts = load_posts()
    new_count = 0

    if data.get("batch") and isinstance(data.get("posts"), list):
        for p in data["posts"]:
            post_id = f"{int(datetime.now().timestamp()*1000)}_{new_count}"
            posts.insert(0, {
                "id":               post_id,
                "type":             p.get("type", "post"),
                "caption":          p.get("caption", ""),
                "hashtags":         p.get("hashtags", ""),
                "imageDescription": p.get("imageDescription", ""),
                "scheduleHint":     p.get("scheduleHint", ""),
                "status":           "pending",
                "createdAt":        now,
                "source":           f"github-actions-{PERIOD}",
            })
            new_count += 1

    save_posts(posts)
    print(f"[OK] {new_count} publicaciones agregadas a data/posts.json")


if __name__ == "__main__":
    generate()
