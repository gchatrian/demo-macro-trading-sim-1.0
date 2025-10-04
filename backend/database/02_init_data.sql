-- =============================================================================
-- SIMULATORE MACROECONOMICO - INITIALIZATION SCRIPT
-- Scenario: Goldilocks → Boom (3 Quarters)
-- Drivers: AI Breakthrough, Accomodating Fed, Fiscal Stimulus
-- =============================================================================

BEGIN;

-- =============================================================================
-- 1. POPOLAZIONE RELEASE TYPES
-- =============================================================================
INSERT INTO release_types (name, description) VALUES
    ('GDP', 'Gross Domestic Product - Misura la crescita economica trimestrale'),
    ('NFP', 'Non-Farm Payrolls - Nuovi posti di lavoro creati nel mese'),
    ('PMI', 'Purchasing Managers Index - Salute del settore manifatturiero'),
    ('Initial Jobless Claims', 'Richieste iniziali di sussidio di disoccupazione'),
    ('Unemployment', 'Tasso di disoccupazione'),
    ('CPI', 'Consumer Price Index - Inflazione al consumo');

-- =============================================================================
-- 2. STATO INIZIALE MACRO-VARIABILI (Goldilocks)
-- Data: Inizio Q1
-- =============================================================================
INSERT INTO macro_variables_history (timestamp, growth, inflation, volatility, cause_type, cause_id)
VALUES (
    '2025-01-02 09:00:00+00',
    2.3,  -- Growth: moderato, sostenibile
    2.1,  -- Inflation: vicino al target Fed (2%)
    12.0, -- Volatility: bassa, mercati calmi
    'initial',
    NULL
);

-- =============================================================================
-- 3. ECONOMIC RELEASES - Q1 (Goldilocks inizia a scaldarsi)
-- Gennaio - Marzo 2025
-- =============================================================================

-- ========== GENNAIO 2025 ==========

-- NFP Gennaio: primi segnali di forza nel mercato del lavoro
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls January', '2025-01-10 13:30:00+00', id, 180.0, 215.0, 0.08, 0.02, 0.3, FALSE
FROM release_types WHERE name = 'NFP';

-- Initial Jobless Claims Gennaio: mercato del lavoro solido
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Initial Jobless Claims January', '2025-01-16 13:30:00+00', id, 220.0, 210.0, 0.03, 0.01, -0.2, FALSE
FROM release_types WHERE name = 'Initial Jobless Claims';

-- CPI Gennaio: inflazione ancora sotto controllo
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI January', '2025-01-15 13:30:00+00', id, 2.2, 2.3, 0.0, 0.05, 0.2, FALSE
FROM release_types WHERE name = 'CPI';

-- ========== FEBBRAIO 2025 ==========

-- PMI Febbraio: settore manifatturiero in accelerazione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'PMI February', '2025-02-03 14:00:00+00', id, 52.5, 55.2, 0.10, 0.03, 0.4, FALSE
FROM release_types WHERE name = 'PMI';

-- NFP Febbraio: momentum continua
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls February', '2025-02-07 13:30:00+00', id, 190.0, 235.0, 0.12, 0.04, 0.5, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Febbraio: primi segnali di pressione inflazionistica
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI February', '2025-02-13 13:30:00+00', id, 2.3, 2.6, 0.0, 0.08, 0.4, FALSE
FROM release_types WHERE name = 'CPI';

-- Unemployment Febbraio: disoccupazione in calo
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Unemployment Rate February', '2025-02-07 13:30:00+00', id, 4.0, 3.7, 0.05, 0.02, 0.2, FALSE
FROM release_types WHERE name = 'Unemployment';

-- ========== MARZO 2025 ==========

-- GDP Q1: conferma della forza economica
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'GDP Q1 2025', '2025-03-27 12:30:00+00', id, 2.5, 3.1, 0.20, 0.05, 0.8, FALSE
FROM release_types WHERE name = 'GDP';

-- NFP Marzo: crescita robusta dell'occupazione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls March', '2025-03-07 13:30:00+00', id, 200.0, 265.0, 0.15, 0.06, 0.6, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Marzo: inflazione in aumento
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI March', '2025-03-12 13:30:00+00', id, 2.6, 3.0, 0.0, 0.12, 0.6, FALSE
FROM release_types WHERE name = 'CPI';

-- =============================================================================
-- 4. ECONOMIC RELEASES - Q2 (Transizione verso il Boom)
-- Aprile - Giugno 2025
-- =============================================================================

-- ========== APRILE 2025 ==========

-- PMI Aprile: espansione accelerata
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'PMI April', '2025-04-01 14:00:00+00', id, 55.0, 58.5, 0.15, 0.05, 0.7, FALSE
FROM release_types WHERE name = 'PMI';

-- NFP Aprile: boom dell'occupazione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls April', '2025-04-04 13:30:00+00', id, 220.0, 290.0, 0.18, 0.08, 0.9, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Aprile: pressioni inflazionistiche evidenti
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI April', '2025-04-10 13:30:00+00', id, 3.0, 3.4, 0.0, 0.15, 0.8, FALSE
FROM release_types WHERE name = 'CPI';

-- ========== MAGGIO 2025 ==========

-- Initial Jobless Claims Maggio: minimo storico
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Initial Jobless Claims May', '2025-05-08 13:30:00+00', id, 210.0, 195.0, 0.08, 0.03, 0.3, FALSE
FROM release_types WHERE name = 'Initial Jobless Claims';

-- NFP Maggio: crescita sostenuta
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls May', '2025-05-02 13:30:00+00', id, 240.0, 305.0, 0.20, 0.10, 1.0, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Maggio: inflazione sopra il 3.5%
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI May', '2025-05-13 13:30:00+00', id, 3.4, 3.7, 0.0, 0.18, 1.0, FALSE
FROM release_types WHERE name = 'CPI';

-- Unemployment Maggio: piena occupazione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Unemployment Rate May', '2025-05-02 13:30:00+00', id, 3.7, 3.4, 0.10, 0.05, 0.5, FALSE
FROM release_types WHERE name = 'Unemployment';

-- ========== GIUGNO 2025 ==========

-- GDP Q2: accelerazione confermata
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'GDP Q2 2025', '2025-06-26 12:30:00+00', id, 3.2, 4.1, 0.25, 0.08, 1.2, FALSE
FROM release_types WHERE name = 'GDP';

-- PMI Giugno: settore manifatturiero in forte espansione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'PMI June', '2025-06-02 14:00:00+00', id, 58.0, 61.3, 0.18, 0.07, 0.9, FALSE
FROM release_types WHERE name = 'PMI';

-- NFP Giugno: mercato del lavoro surriscaldato
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls June', '2025-06-06 13:30:00+00', id, 260.0, 320.0, 0.22, 0.12, 1.2, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Giugno: inflazione al 4%
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI June', '2025-06-11 13:30:00+00', id, 3.7, 4.1, 0.0, 0.20, 1.3, FALSE
FROM release_types WHERE name = 'CPI';

-- =============================================================================
-- 5. ECONOMIC RELEASES - Q3 (Boom Pieno)
-- Luglio - Settembre 2025
-- =============================================================================

-- ========== LUGLIO 2025 ==========

-- NFP Luglio: crescita robusta continua
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls July', '2025-07-03 13:30:00+00', id, 280.0, 335.0, 0.25, 0.14, 1.4, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Luglio: inflazione consolidata sopra 4%
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI July', '2025-07-10 13:30:00+00', id, 4.1, 4.4, 0.0, 0.22, 1.5, FALSE
FROM release_types WHERE name = 'CPI';

-- PMI Luglio: picco di espansione
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'PMI July', '2025-07-01 14:00:00+00', id, 61.0, 63.8, 0.20, 0.09, 1.1, FALSE
FROM release_types WHERE name = 'PMI';

-- ========== AGOSTO 2025 ==========

-- NFP Agosto: mercato del lavoro al massimo
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls August', '2025-08-01 13:30:00+00', id, 300.0, 345.0, 0.28, 0.16, 1.6, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Agosto: inflazione verso il 4.5%
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI August', '2025-08-13 13:30:00+00', id, 4.4, 4.7, 0.0, 0.25, 1.7, FALSE
FROM release_types WHERE name = 'CPI';

-- Unemployment Agosto: disoccupazione minima
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Unemployment Rate August', '2025-08-01 13:30:00+00', id, 3.4, 3.1, 0.12, 0.08, 0.8, FALSE
FROM release_types WHERE name = 'Unemployment';

-- ========== SETTEMBRE 2025 ==========

-- GDP Q3: boom confermato
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'GDP Q3 2025', '2025-09-25 12:30:00+00', id, 4.0, 4.8, 0.30, 0.10, 1.8, FALSE
FROM release_types WHERE name = 'GDP';

-- NFP Settembre: crescita sostenibile nel boom
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'Non-Farm Payrolls September', '2025-09-05 13:30:00+00', id, 320.0, 350.0, 0.30, 0.18, 1.8, FALSE
FROM release_types WHERE name = 'NFP';

-- CPI Settembre: inflazione stabilizzata alta
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'CPI September', '2025-09-10 13:30:00+00', id, 4.7, 4.9, 0.0, 0.28, 1.9, FALSE
FROM release_types WHERE name = 'CPI';

-- PMI Settembre: espansione matura
INSERT INTO economic_releases (name, release_date, release_type_id, consensus, actual, impact_growth, impact_inflation, impact_volatility, has_happened)
SELECT 'PMI September', '2025-09-01 14:00:00+00', id, 63.0, 64.2, 0.22, 0.10, 1.3, FALSE
FROM release_types WHERE name = 'PMI';

-- =============================================================================
-- 6. MACRO EVENTS (Driver della Transizione)
-- =============================================================================

-- Evento 1: AI Breakthrough Announcement (Febbraio)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-02-15 16:00:00+00',
    'Major Tech Companies Announce Revolutionary AI Breakthrough: Productivity Set to Surge',
    0.35,  -- Forte impatto positivo su crescita
    0.05,  -- Lieve pressione inflazionistica iniziale
    2.5,   -- Aumento volatilità per incertezza
    FALSE
);

-- Evento 2: Federal Reserve Maintains Dovish Stance (Marzo)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-03-20 18:00:00+00',
    'Federal Reserve Signals Accommodative Policy to Support AI-Driven Economic Transformation',
    0.25,  -- Stimolo alla crescita
    0.15,  -- Pressione inflazionistica da politica accomodante
    -0.8,  -- Riduzione volatilità per certezza policy
    FALSE
);

-- Evento 3: Massive Fiscal Stimulus Package (Aprile)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-04-18 20:00:00+00',
    'Congress Passes $800B AI Infrastructure and Innovation Act: Largest Tech Investment in History',
    0.40,  -- Grande impulso fiscale
    0.18,  -- Pressione inflazionistica da spesa pubblica
    1.5,   -- Volatilità da dimensione del programma
    FALSE
);

-- Evento 4: Corporate Investment Boom (Maggio)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-05-22 15:00:00+00',
    'S&P 500 Companies Announce Record $2T Investment in AI Infrastructure Over Next 3 Years',
    0.38,  -- Investimenti massicci
    0.12,  -- Pressione su prezzi beni strumentali
    1.2,   -- Volatilità da riallocazione capitale
    FALSE
);

-- Evento 5: Labor Market Tightness (Giugno)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-06-17 14:00:00+00',
    'Tech Sector Talent War Intensifies: Average Salaries Jump 22% as AI Skills in High Demand',
    0.15,  -- Effetto su produttività e consumi
    0.25,  -- Forte pressione salariale
    1.0,   -- Volatilità da tensioni mercato lavoro
    FALSE
);

-- Evento 6: Inflation Concerns Emerge (Luglio)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-07-15 13:00:00+00',
    'Economists Warn of Overheating Risks as Growth and Inflation Both Exceed Expectations',
    -0.05, -- Lieve freno da preoccupazioni
    0.20,  -- Aspettative inflazionistiche
    2.0,   -- Aumento incertezza
    FALSE
);

-- Evento 7: Fed Hints at Future Tightening (Agosto)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-08-20 18:00:00+00',
    'Fed Chair Signals Possible Policy Shift if Inflation Remains Elevated Above 4.5%',
    -0.10, -- Raffreddamento aspettative
    -0.08, -- Calmieramento aspettative inflazione
    2.5,   -- Forte volatilità da incertezza policy
    FALSE
);

-- Evento 8: Productivity Data Surprises (Settembre)
INSERT INTO macro_events (event_date, headline, impact_growth, impact_inflation, impact_volatility, has_happened)
VALUES (
    '2025-09-18 12:30:00+00',
    'Labor Productivity Surges 8% Annually: AI Delivering on Promise, May Ease Inflation Pressures',
    0.30,  -- Forte impatto positivo da produttività
    -0.15, -- Potenziale riduzione pressioni
    -1.0,  -- Riduzione volatilità da news positiva
    FALSE
);

COMMIT;

-- =============================================================================
-- VERIFICA POPOLAZIONE
-- =============================================================================
SELECT 'Release Types:' as table_name, COUNT(*) as records FROM release_types
UNION ALL
SELECT 'Economic Releases:', COUNT(*) FROM economic_releases
UNION ALL
SELECT 'Macro Events:', COUNT(*) FROM macro_events
UNION ALL
SELECT 'Macro Variables History:', COUNT(*) FROM macro_variables_history;

-- Visualizza stato iniziale
SELECT 
    timestamp,
    growth,
    inflation,
    volatility,
    cause_type
FROM macro_variables_history
WHERE cause_type = 'initial';