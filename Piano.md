FASE 1: Setup Iniziale

Task 1.1: Inizializzazione Progetto

 Creare struttura directory del progetto
 Inizializzare repository git
 Creare .gitignore con patterns Python standard
 Creare README.md con overview del progetto
 Creare .env.example con variabili richieste

Output: Skeleton del progetto pronto

Task 1.2: Setup Database Supabase

 Creare progetto Supabase
 Eseguire schema.sql per creare le tabelle
 Eseguire rls_policies.sql per configurare sicurezza
 Eseguire seed_data.sql per popolare i dati
 Verificare che tutte le tabelle siano popolate correttamente
 Ottenere SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY

Output: Database Supabase configurato e popolato

Task 1.3: Setup Ambiente Python

 Creare requirements.txt con dipendenze (supabase, anthropic, python-dotenv)
 Creare virtual environment
 Installare dipendenze
 Creare file .env con credenziali reali
 Ottenere ANTHROPIC_API_KEY

Output: Ambiente Python pronto per sviluppo

FASE 2: Sviluppo Model Layer
Task 2.1: Configuration Module

 Implementare config/settings.py
 Caricare variabili d'ambiente con validazione
 Definire costanti di simulazione (DEMO_DAY_DURATION, etc.)
 Testare che le configurazioni vengano caricate correttamente

Output: Sistema di configurazione funzionante
Task 2.2: Database Manager

 Implementare model/database_manager.py
 Creare connessione a Supabase usando service_role_key
 Implementare metodi base: query(), insert(), update()
 Gestire errori di connessione e query
 Testare connessione al database

Output: Interfaccia funzionante con Supabase
Task 2.3: Macro Evolution Engine

 Implementare model/macro_evolution_engine.py
 Metodo apply_release_impact(): applica impatti da economic_releases
 Metodo apply_event_impact(): applica impatti da macro_events
 Metodo get_current_state(): restituisce ultimo stato macro-variabili
 Inserisce nuovo record in macro_variables_history ad ogni update
 Testare logica di calcolo con dati mock

Output: Engine di evoluzione macro-variabili funzionante
Task 2.4: Data Provider

 Implementare model/data_provider.py
 Metodo get_next_event(): restituisce prossimo release o event da processare
 Metodo get_release_by_id(): recupera dettagli di un release
 Metodo get_event_by_id(): recupera dettagli di un event
 Metodo get_macro_history(): restituisce storico recente variabili
 Metodo mark_as_happened(): aggiorna flag has_happened
 Testare con query reali al database

Output: API per accedere ai dati pronta
Task 2.5: Initialization Scripts (opzionale)

 Implementare model/initialization_scripts.py
 Metodo check_database_populated(): verifica se DB è già inizializzato
 Metodo run_initialization(): esegue script SQL se necessario
 Gestire caso database già popolato

Output: Sistema di auto-inizializzazione (se richiesto)

FASE 3: Sviluppo Controller Layer
Task 3.1: Timeline Scheduler

 Implementare controller/timeline_scheduler.py
 Caricare tutti gli eventi (releases + events) ordinati per data
 Implementare conversione tempo: 1 giorno simulato = 120 secondi reali
 Metodo get_next_event(): calcola quando avviene il prossimo evento
 Metodo wait_until_next(): sleep fino al momento giusto
 Gestire compressione temporale correttamente

Output: Scheduler che controlla il timing della simulazione
Task 3.2: Terminal Output Manager

 Implementare controller/terminal_output_manager.py
 Metodo print_narrative(): formatta e stampa narrative LLM
 Metodo print_system_log(): stampa log minimali di sistema
 Metodo print_header(): stampa intestazione con timestamp simulato
 Aggiungere colori/formattazione per leggibilità (opzionale)
 Testare output su terminale

Output: Manager per output formattato
Task 3.3: Narrative Templates

 Implementare prompts/narrative_templates.py
 Funzione build_pre_release_prompt(): crea prompt per narrative pre-release
 Funzione build_post_release_prompt(): crea prompt per narrative post-release
 Funzione build_event_prompt(): crea prompt per eventi macro
 Ogni funzione riceve contesto (stato macro, storico, dati specifici)
 Definire istruzioni chiare per l'LLM (stile, lunghezza ~400 parole)

Output: Sistema di prompt engineering pronto
Task 3.4: LLM Orchestrator

 Implementare controller/llm_orchestrator.py
 Inizializzare client Anthropic
 Metodo generate_pre_release_narrative(): chiama LLM con contesto
 Metodo generate_post_release_narrative(): chiama LLM con contesto
 Metodo generate_event_narrative(): chiama LLM con contesto
 Gestire errori API e retry logic
 Salvare narrative generate in tabella narratives
 Testare con chiamate reali all'API

Output: Orchestrator per generazione narrative funzionante
Task 3.5: Simulation Loop

 Implementare controller/simulation_loop.py
 Metodo initialize(): setup di tutti i componenti
 Metodo run(): loop principale della simulazione
 Logica: chiede scheduler il prossimo evento
 Switch su tipo evento (pre_release / release / event)
 Per ogni tipo, chiama LLM Orchestrator e Data Provider appropriatamente
 Per release/event, chiama Macro Evolution Engine per update
 Stampa output via Terminal Output Manager
 Metodo shutdown(): cleanup risorse e graceful exit
 Gestire signal CTRL+C per interrupt

Output: Loop di simulazione completo

FASE 4: Integrazione e Main Entry Point
Task 4.1: Main Entry Point

 Implementare main.py
 Caricare configurazioni
 Inizializzare Simulation Loop
 Gestire CTRL+C con signal handler
 Try/except per error handling globale
 Log di avvio e chiusura

Output: Applicazione completa e avviabile
Task 4.2: Testing End-to-End

 Eseguire simulazione completa da inizio a fine
 Verificare che eventi vengano processati nell'ordine corretto
 Verificare che macro-variabili evolvano correttamente
 Verificare che narrative siano contestualizzate e di qualità
 Verificare che CTRL+C chiuda pulitamente
 Controllare che il database venga aggiornato correttamente

Output: Demo funzionante end-to-end

FASE 5: Finalizzazione
Task 5.1: Documentazione

 Completare README.md con:

Descrizione progetto
Prerequisiti
Istruzioni setup (database, env variables)
Istruzioni per eseguire la demo
Architettura del sistema


 Aggiungere commenti al codice dove necessario
 Creare documentazione API interna (docstrings)

Output: Documentazione completa
Task 5.2: Testing e Bug Fixing

 Scrivere test unitari per componenti critici (opzionale)
 Test di stress: eseguire più volte la simulazione
 Identificare e fixare bug
 Ottimizzare performance se necessario

Output: Sistema stabile e testato
Task 5.3: Polish

 Migliorare output terminale (colori, spacing)
 Aggiungere progress indicator (opzionale)
 Verificare gestione errori in tutti i punti critici
 Code cleanup e refactoring se necessario

Output: Demo pronta per presentazione