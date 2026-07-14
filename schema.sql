-- Blueprint Técnico v1: Esquema de Base de Datos para Proyecto Mercury
-- Optimizado para PostgreSQL / Supabase / Render Free Tier

-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. PAYLOAD CRUDO (Schema-on-read - Ingesta pura)
CREATE TABLE IF NOT EXISTS raw_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source TEXT NOT NULL,                    -- 'kalshi' | 'polymarket'
    source_id TEXT NOT NULL,                 -- ticker/id original de la plataforma
    raw_payload JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'RECIBIDO', -- RECIBIDO | NORMALIZADO | PENDIENTE_REVISION_TECNICA
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    purge_after TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '72 hours')
);
CREATE INDEX IF NOT EXISTS idx_raw_events_status ON raw_events(status);
CREATE INDEX IF NOT EXISTS idx_raw_events_purge ON raw_events(purge_after);

-- 2. EVENTOS CANÓNICOS (Esquema normalizado y limpio)
CREATE TABLE IF NOT EXISTS canonical_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    raw_event_id UUID REFERENCES raw_events(id) ON DELETE SET NULL,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_url TEXT NOT NULL,                -- Obligatorio, nunca vacío (patrón Resolver v1)
    categoria TEXT NOT NULL,                 -- 'deporte' (único valor válido Fase 1)
    deporte TEXT,                            -- 'futbol', 'beisbol', etc.
    titulo TEXT NOT NULL,
    descripcion TEXT,
    precio_si NUMERIC(6,4),
    precio_no NUMERIC(6,4),
    fecha_cierre TIMESTAMPTZ NOT NULL,
    estado TEXT NOT NULL DEFAULT 'ABIERTO', -- ABIERTO | CERRADO
    resultado BOOLEAN,                       -- NULL hasta el settlement
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_canonical_events_estado ON canonical_events(estado);
CREATE INDEX IF NOT EXISTS idx_canonical_events_fecha_cierre ON canonical_events(fecha_cierre);
CREATE INDEX IF NOT EXISTS idx_canonical_events_deporte ON canonical_events(deporte);

-- 3. CACHÉ DE ENTIDADES Y CLASIFICACIÓN (Protocolo cuota mínima)
CREATE TABLE IF NOT EXISTS entity_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo TEXT NOT NULL,                      -- 'jugador' | 'equipo' | 'clasificacion_deporte'
    clave TEXT NOT NULL,                     -- Texto o tag original visto
    valor JSONB NOT NULL,                    -- Datos resueltos (stats, nombres normalizados)
    ttl_expira_at TIMESTAMPTZ,               -- NULL = permanente (ej. reglas de tags)
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(tipo, clave)
);

-- 4. TARJETAS DE APUESTA (Decisiones del núcleo Mercury)
CREATE TABLE IF NOT EXISTS bet_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    canonical_event_id UUID REFERENCES canonical_events(id) ON DELETE CASCADE,
    tipo_tarjeta TEXT NOT NULL,              -- 'A' (Óptimo) | 'B' (Hedge)
    tarjeta_pareja_id UUID REFERENCES bet_cards(id), -- Auto-referencia A <-> B
    monto_sugerido NUMERIC(10,2) NOT NULL,
    probabilidad_calculada NUMERIC(6,4) NOT NULL,
    edge NUMERIC(6,4) NOT NULL,
    perfil_riesgo TEXT NOT NULL,             -- 'conservador' | 'medio' | 'agresivo'
    status TEXT NOT NULL DEFAULT 'GENERADA',-- GENERADA | PENDIENTE_SETTLEMENT | GANADA | PERDIDA
    fecha_cierre_estimada TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_bet_cards_status ON bet_cards(status);
CREATE INDEX IF NOT EXISTS idx_bet_cards_fecha_cierre ON bet_cards(fecha_cierre_estimada);

-- 5. VERSIONES DE MODELO (Seguimiento Walk-Forward por Skill)
CREATE TABLE IF NOT EXISTS model_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    deporte TEXT NOT NULL,
    ventana_meses INTEGER NOT NULL,
    brier_score NUMERIC(6,4) NOT NULL,
    parametros JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'ENTRENANDO', -- ENTRENANDO | ACTIVO | REEMPLAZADO
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_model_versions_activo ON model_versions(deporte, status);
