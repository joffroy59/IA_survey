# Plan: Augmenter les tokens gratuits LLM avec stratégie multi-fournisseur

## Objectif
Remplacer la dépendance unique à Gemini par une stratégie multi-fournisseur pour augmenter le volume gratuit total tout en gardant les mises à jour GitHub Actions stables et fiables.

## Contraintes
- Sorties JSON doivent rester compatibles avec parsers existants → pas de changement schéma
- Workflows GitHub Actions doivent rester fiables pour exécutions non-supervisées
- Fallback automatique si un provider atteint sa limite quota
- Zéro perte de données ou HTML generés

## Architecture proposée (Option B: OpenRouter + Gemini)

### Fournisseurs sélectionnés
1. **Primary**: OpenRouter (modèles free listés)
   - Modèles candidats: `mistralai/mistral-7b-instruct:free`, `meta-llama/llama-2-7b-chat:free`
   - Avantages: quota gratuit renouvelable, bonne qualité pour extraction JSON
   - Limite: peut être saturé, d'où fallback

2. **Fallback 1**: Gemini (actuel)
   - `gemini-2.5-flash` (moins cher que pro)
   - Quota connu: ~1,500 req/jour
   - Utilisé uniquement si OpenRouter épuisé

3. **Fallback 2**: Groq (optionnel, si doublement saturé)
   - `mixtral-8x7b-32768` avec offre free généreuse
   - Comme dernière ligne de défense

### Provider adapter layer
```python
# Nouvelle fonction dans scripts/update.py
def get_llm_provider(env_config: dict) -> LLMProvider:
    """Sélectionne et retourne le provider LLM basé sur env vars."""
    priority_list = env_config.get('LLM_PROVIDERS', 'openrouter,gemini,groq').split(',')

    for provider_name in priority_list:
        if is_provider_available(provider_name):
            return init_provider(provider_name, env_config)

    raise NoProviderAvailableError("Tous les providers sont indisponibles")

def call_llm(provider: LLMProvider, prompt: str) -> dict:
    """Appel unifié retournant toujours {'success': bool, 'content': str}."""
    try:
        response = provider.generate(prompt)
        return {'success': True, 'content': response}
    except QuotaExhausted:
        return {'success': False, 'error': 'quota_exceeded'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### Secrets GitHub requis
```
OPENROUTER_API_KEY        (nouveau)
GEMINI_API_KEY            (existant, gardé)
GROQ_API_KEY              (optionnel)
LLM_PROVIDERS             (optionnel, défaut: "openrouter,gemini,groq")
LLM_TIMEOUT_SECONDS       (optionnel, défaut: 30)
```

### Modification workflows
**File**: `.github/workflows/update-profile-unit.yml`
```yaml
env:
  LLM_PROVIDERS: ${{ secrets.LLM_PROVIDERS || 'openrouter,gemini' }}
  LLM_TIMEOUT_SECONDS: 30

steps:
  - name: Install LLM provider dependencies
    run: |
      pip install --upgrade ddgs google-generativeai openrouter-client groq

  - name: Update profile dataset
    env:
      OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
      GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
    run: python scripts/update.py --profile "$PROFILE"
```

### Logique fallback dans update.py
```python
def ask_llm(prompt: str, env_config: dict) -> str:
    """Essaie les providers dans l'ordre jusqu'au succès."""
    providers_chain = env_config['LLM_PROVIDERS'].split(',')

    for i, provider_name in enumerate(providers_chain):
        try:
            provider = init_provider(provider_name, env_config)
            result = provider.generate(prompt, timeout=env_config['LLM_TIMEOUT_SECONDS'])
            log(f"✓ Provider {provider_name} succeeded")
            return result
        except QuotaExhausted as e:
            log(f"⚠ Provider {provider_name} quota exceeded, trying next...")
            if i == len(providers_chain) - 1:  # dernière tentative
                raise FatalLLMError(f"All providers exhausted: {e}")
        except TimeoutError as e:
            log(f"⚠ Provider {provider_name} timed out, trying next...")
        except Exception as e:
            log(f"✗ Provider {provider_name} error: {e}")

    raise FatalLLMError("No provider available")
```

### Gestion des erreurs et observabilité
1. **Logs structurés** → écris à `$GITHUB_STEP_SUMMARY` le provider utilisé, fallback count
2. **Retry exponential** → wait 5s, puis 10s, puis abandon (par provider)
3. **Non-blocking fallback** → si OpenRouter fail mais Gemini OK → continue sans break
4. **Monitoring** → collecte `usage_tokens`, `provider_latency_ms` pour analyse post-run

## Plan d'exécution

### Phase 1: Adapter layer + Gemini comme fallback (MAINTENANT)
1. Créer `LLMProvider` classe abstraite et implémentations pour chaque provider
2. Remplacer `ask_gemini()` par appel au nouveau adapter
3. Ajouter env vars `LLM_PROVIDERS`, secrets `OPENROUTER_API_KEY`
4. Tester localement avec `--profile discovery`

### Phase 2: Validation CI
1. Créer feature branch `feature/multi-provider-llm`
2. Tester GitHub Action sur un profil unique
3. Vérifier commits/push automatiques
4. Tester fallback en "simulant" quota exhausted

### Phase 3: Rollout complet
1. Merger à develop, puis main
2. Exécuter `update.yml` complet (matrice 11 profils)
3. Monitorer durée totale, fallback count, génération HTML
4. Mettre à jour README et WORK_DONE_NOTE

## Fichiers à modifier
- `scripts/update.py` → adapter layer + fallback logic
- `.github/workflows/update-profile-unit.yml` → env vars, dependencies, secrets
- `.github/workflows/update.yml` → héritage secrets
- `README.md` → section "Setup LLM Providers"
- `WORK_DONE_NOTE.md` → entrée de changement

## Tests de validation
```bash
# Local test
python scripts/update.py --profile discovery --llm-provider openrouter

# Dry-run with fallback simulation
OPENROUTER_API_KEY="" python scripts/update.py --profile general

# Full matrix
gh workflow run update.yml
```

## Avantages de cette approche
✓ Augmente quota gratuit total d'~50-200% selon saturation
✓ Zero impact sur sortie JSON/HTML
✓ Fallback automatique → CI reste robuste
✓ Secrets GitHub gérés proprement
✓ Extensible pour ajouter 4e provider sans refactor

## Risques mitigés
- **Quota OpenRouter saturé** → fallback Gemini automatique
- **Latency haute cloud** → timeout configurable per-provider
- **API incompatibilité** → adapter abstract layer absorbe la différence
- **Secret rotation** → variables centralisées faciles à updater

## Next steps
1. Décider si tu veux OpenRouter + Gemini, ou autre combinaison
2. Créer OpenRouter account gratuit + générer clef (si oui)
3. Ajouter secrets dans GitHub repo settings
4. Je crée la feature branch et implémente Phase 1
