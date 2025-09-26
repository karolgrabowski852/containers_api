# --- Build stage ---
FROM python:3.12-slim-bookworm AS runtime

# Ustawienia Pythona
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Podstawowe narzędzia
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl && rm -rf /var/lib/apt/lists/*

# Instalacja UV
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh
RUN cp /root/.local/bin/uv /usr/local/bin/uv
ENV PATH="/usr/local/bin:${PATH}"

# Utworzenie użytkownika
RUN useradd --create-home --uid 10001 appuser
WORKDIR /app

# Kopiowanie plików zarządzających zależnościami UV
COPY pyproject.toml uv.lock ./

# Instalacja zależności przez UV
RUN uv sync

# Kopiowanie całego projektu
COPY . .

# Zmiana właściciela plików
RUN chown -R appuser:appuser /app

# Przełączenie na użytkownika nie-root
USER appuser

# Uruchomienie aplikacji przez UV
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]


