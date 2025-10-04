-- =============================================================================
-- SIMULATORE MACROECONOMICO - DATABASE SCHEMA
-- =============================================================================

-- Abilita l'estensione UUID se non già attiva
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- TABELLA: release_types
-- Definisce i tipi di rilasci economici supportati (GDP, NFP, PMI, etc.)
-- =============================================================================
CREATE TABLE release_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indice per ricerca rapida per nome
CREATE INDEX idx_release_types_name ON release_types(name);

-- =============================================================================
-- TABELLA: economic_releases
-- Calendario dei rilasci economici con consensus, actual e impatti
-- =============================================================================
CREATE TABLE economic_releases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    release_date TIMESTAMPTZ NOT NULL,
    release_type_id UUID NOT NULL REFERENCES release_types(id) ON DELETE CASCADE,
    
    -- Valori del rilascio
    consensus DECIMAL(10, 4) NOT NULL,
    actual DECIMAL(10, 4) NOT NULL,
    
    -- Impatti sulle 3 macro-variabili
    impact_growth DECIMAL(10, 6) NOT NULL DEFAULT 0,
    impact_inflation DECIMAL(10, 6) NOT NULL DEFAULT 0,
    impact_volatility DECIMAL(10, 6) NOT NULL DEFAULT 0,
    
    -- Stato del rilascio
    has_happened BOOLEAN NOT NULL DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX idx_economic_releases_date ON economic_releases(release_date);
CREATE INDEX idx_economic_releases_happened ON economic_releases(has_happened);
CREATE INDEX idx_economic_releases_type ON economic_releases(release_type_id);

-- =============================================================================
-- TABELLA: macro_events
-- Eventi macro-economici e geopolitici che impattano l'economia
-- =============================================================================
CREATE TABLE macro_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_date TIMESTAMPTZ NOT NULL,
    headline TEXT NOT NULL,
    
    -- Impatti sulle 3 macro-variabili
    impact_growth DECIMAL(10, 6) NOT NULL DEFAULT 0,
    impact_inflation DECIMAL(10, 6) NOT NULL DEFAULT 0,
    impact_volatility DECIMAL(10, 6) NOT NULL DEFAULT 0,
    
    -- Stato dell'evento
    has_happened BOOLEAN NOT NULL DEFAULT FALSE,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX idx_macro_events_date ON macro_events(event_date);
CREATE INDEX idx_macro_events_happened ON macro_events(has_happened);

-- =============================================================================
-- TABELLA: macro_variables_history
-- Storico dell'evoluzione delle 3 variabili macroeconomiche
-- =============================================================================
CREATE TABLE macro_variables_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL,
    
    -- Valori delle 3 macro-variabili
    growth DECIMAL(10, 6) NOT NULL,
    inflation DECIMAL(10, 6) NOT NULL,
    volatility DECIMAL(10, 6) NOT NULL,
    
    -- Riferimento alla causa del cambiamento
    cause_type TEXT NOT NULL CHECK (cause_type IN ('release', 'event', 'initial')),
    cause_id UUID, -- NULL per lo stato iniziale
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX idx_macro_variables_timestamp ON macro_variables_history(timestamp DESC);
CREATE INDEX idx_macro_variables_cause ON macro_variables_history(cause_type, cause_id);

-- =============================================================================
-- TABELLA: narratives
-- Log di tutte le narrative generate dall'agente LLM
-- =============================================================================
CREATE TABLE narratives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL,
    
    -- Tipo di narrative
    narrative_type TEXT NOT NULL CHECK (narrative_type IN ('pre_release', 'post_release', 'event')),
    
    -- Contenuto (circa 400 parole)
    content TEXT NOT NULL,
    
    -- Riferimento flessibile a release o event
    reference_type TEXT NOT NULL CHECK (reference_type IN ('release', 'event')),
    reference_id UUID NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indici per performance
CREATE INDEX idx_narratives_timestamp ON narratives(timestamp DESC);
CREATE INDEX idx_narratives_type ON narratives(narrative_type);
CREATE INDEX idx_narratives_reference ON narratives(reference_type, reference_id);

-- =============================================================================
-- COMMENTI SULLE TABELLE (per documentazione)
-- =============================================================================
COMMENT ON TABLE release_types IS 'Tipi di indicatori economici supportati dal sistema';
COMMENT ON TABLE economic_releases IS 'Calendario dei rilasci economici con dati consensus e actual';
COMMENT ON TABLE macro_events IS 'Eventi macro-economici e geopolitici esterni';
COMMENT ON TABLE macro_variables_history IS 'Storico completo dell''evoluzione delle variabili macroeconomiche';
COMMENT ON TABLE narratives IS 'Log delle narrative generate dall''agente AI';

COMMENT ON COLUMN macro_variables_history.cause_type IS 'Tipo di causa: release, event, o initial per lo stato di partenza';
COMMENT ON COLUMN economic_releases.has_happened IS 'TRUE se il rilascio è già avvenuto, FALSE se futuro';
COMMENT ON COLUMN macro_events.has_happened IS 'TRUE se l''evento è già avvenuto, FALSE se futuro';

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) CONFIGURATION
-- =============================================================================

-- Abilita RLS su tutte le tabelle
ALTER TABLE release_types ENABLE ROW LEVEL SECURITY;
ALTER TABLE economic_releases ENABLE ROW LEVEL SECURITY;
ALTER TABLE macro_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE macro_variables_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE narratives ENABLE ROW LEVEL SECURITY;

-- =============================================================================
-- POLICY PER DEMO: Accesso completo per service_role
-- =============================================================================

-- release_types: lettura pubblica, scrittura solo service_role
CREATE POLICY "Allow public read access on release_types"
    ON release_types FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow service_role full access on release_types"
    ON release_types FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- economic_releases: lettura pubblica, scrittura solo service_role
CREATE POLICY "Allow public read access on economic_releases"
    ON economic_releases FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow service_role full access on economic_releases"
    ON economic_releases FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- macro_events: lettura pubblica, scrittura solo service_role
CREATE POLICY "Allow public read access on macro_events"
    ON macro_events FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow service_role full access on macro_events"
    ON macro_events FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- macro_variables_history: lettura pubblica, scrittura solo service_role
CREATE POLICY "Allow public read access on macro_variables_history"
    ON macro_variables_history FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow service_role full access on macro_variables_history"
    ON macro_variables_history FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- narratives: lettura pubblica, scrittura solo service_role
CREATE POLICY "Allow public read access on narratives"
    ON narratives FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Allow service_role full access on narratives"
    ON narratives FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);