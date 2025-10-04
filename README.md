# Demo Macro Trading Simulator 1.0

Simulatore macroeconomico che ricrea l'evoluzione di un'economia attraverso rilasci di indicatori economici ed eventi geopolitici, con narrative generate da AI.

## Architettura

Il sistema segue un'architettura MVC modificata:

- **Model**: Gestisce stato macroeconomico, database (Supabase) e logica di evoluzione
- **Controller**: Orchestra la simulazione, coordina agenti LLM e gestisce output
- **View**: Terminal output (nella versione demo)

## Scenario Demo

La simulazione parte da uno scenario "Goldilocks" (crescita moderata, inflazione bassa) ed evolve in un "Boom" economico guidato da:
- Breakthrough tecnologici nell'AI
- Federal Reserve accomodante
- Impulso fiscale governativo

**Durata**: 3 trimestri (Q1-Q3 2025) compressi in modalità demo dove 1 giorno = 2 minuti reali.

## Macro-Variabili

Il sistema traccia 3 variabili fondamentali:
1. **Growth** (Crescita)
2. **Inflation** (Inflazione)
3. **Volatility** (Volatilità di mercato)

## Tecnologie

- **Database**: Supabase (PostgreSQL)
- **LLM**: OpenAI GPT-4o-mini
- **Language**: Python 3.9+

## Setup

*(Istruzioni dettagliate verranno aggiunte nelle fasi successive)*

### Prerequisiti
- Python 3.9+
- Account Supabase
- API Key OpenAI

### Variabili d'Ambiente

