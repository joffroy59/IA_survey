# Backlog d'evolution de l'application IA Survey

Date: 2026-04-17
Statut: Propose

## Objectif
Structurer les evolutions majeures demandees en un backlog executable, avec priorites, criteres d'acceptation et ordre de livraison.

## Priorites globales
- P0: Historique/comparaison fiable, settings, export configuration
- P1: Base de donnees + migration des donnees actuelles
- P1: Multi-provider (Gemini, OpenAI, Claude, OpenRouter, Ollama, LM Studio)
- P2: Enrichissement massif des outils CLI et agentiques

## Epic 1 - Qualite des donnees outils (CLI + agentiques)

### US-001 - Definir un modele de pertinence des outils (P2)
Description: En tant que mainteneur, je veux un score de pertinence standardise pour mieux trier les outils.

Critieres d'acceptation:
- [ ] Le modele de score inclut au minimum: popularite, activite recente, qualite doc, maturite, licence.
- [ ] Le score est stocke dans les donnees outils.
- [ ] La logique est documentee.

### US-002 - Elargir la couverture des CLI connus (P2)
Description: En tant qu'utilisateur, je veux trouver plus de CLI reconnus et actuels.

Critieres d'acceptation:
- [ ] La source de donnees couvre significativement plus de CLI qu'aujourd'hui.
- [ ] Une regle de deduplication gere aliases et variantes de nom.
- [ ] Un champ date de derniere verification est present.

### US-003 - Elargir les outils agentiques (P2)
Description: En tant qu'utilisateur, je veux plus de frameworks et tools agentiques.

Critieres d'acceptation:
- [ ] Les outils agentiques incluent des metadonnees dediees (tool-calling, memory, multi-agent, self-hosted/cloud).
- [ ] Les pages rendent ces metadonnees sans regression visuelle.

## Epic 2 - Historique et comparaison fiables

### US-004 - Corriger les faux positifs de comparaison (P0)
Description: En tant qu'utilisateur, je veux des diffs justes entre snapshots.

Critieres d'acceptation:
- [ ] Les changements d'ordre n'apparaissent plus comme des modifications fonctionnelles.
- [ ] Les renamings/aliases sont detectes correctement.
- [ ] Le rendu distingue Ajoute, Supprime, Modifie, Inchange.

### US-005 - Stabiliser l'historique (P0)
Description: En tant que mainteneur, je veux un historique coherent et tracable.

Critieres d'acceptation:
- [ ] Chaque snapshot contient timestamp et identifiant stable.
- [ ] Le workflow de generation produit un historique reproductible.
- [ ] Des tests evitent les regressions sur la comparaison.

## Epic 3 - Settings + persistance en base de donnees

### US-006 - Ajouter un panneau de settings (P0)
Description: En tant qu'utilisateur, je veux configurer l'application via une interface dediee.

Critieres d'acceptation:
- [ ] Un panneau settings permet de modifier provider, timeouts, options d'affichage et filtres.
- [ ] Les valeurs sont validees et persistent entre sessions.
- [ ] Un reset vers les valeurs par defaut est disponible.

### US-007 - Introduire une base de donnees (P1)
Description: En tant que mainteneur, je veux remplacer la persistance fragile par une base de donnees.

Critieres d'acceptation:
- [ ] Une base SQLite est integree (premiere etape).
- [ ] Un schema couvre outils, queries, snapshots, providers, settings.
- [ ] Une migration initiale depuis les JSON existants est disponible.

### US-008 - Ajouter un repository layer (P1)
Description: En tant que developpeur, je veux isoler l'acces aux donnees.

Critieres d'acceptation:
- [ ] Les lectures/ecritures passent par une couche de services/repositories.
- [ ] Les scripts critiques ne manipulent plus directement les fichiers JSON principaux.

## Epic 4 - Export/Import de configuration

### US-009 - Exporter la configuration complete (P0)
Description: En tant qu'utilisateur, je veux exporter ma configuration incluant les queries.

Critieres d'acceptation:
- [ ] Export JSON incluant settings, queries, providers et mappings.
- [ ] Option d'export sans secrets.
- [ ] Le format est versionne (ex: configVersion).

### US-010 - Importer et valider la configuration (P1)
Description: En tant qu'utilisateur, je veux reimporter une configuration en securite.

Critieres d'acceptation:
- [ ] Validation de schema avant application.
- [ ] Mode dry-run indiquant les changements a appliquer.
- [ ] Gestion d'erreurs claire si incompatibilite de version.

## Epic 5 - Mode multi-provider

### US-011 - Definir une interface provider commune (P1)
Description: En tant que developpeur, je veux une abstraction unique pour les providers LLM.

Critieres d'acceptation:
- [ ] Interface unique pour generation, liste modeles, healthcheck.
- [ ] Le provider Gemini actuel est adapte a cette interface.

### US-012 - Integrer OpenAI, Claude, OpenRouter (P1)
Description: En tant qu'utilisateur, je veux choisir entre plusieurs providers cloud.

Critieres d'acceptation:
- [ ] Chaque provider est configurable via settings.
- [ ] Les erreurs API sont gerees proprement.
- [ ] Les differences de modeles sont exposees dans l'UI.

### US-013 - Integrer Ollama et LM Studio (P1)
Description: En tant qu'utilisateur, je veux utiliser des providers locaux.

Critieres d'acceptation:
- [ ] Detection de disponibilite locale (healthcheck).
- [ ] Configuration endpoint/modeles locale depuis settings.
- [ ] Fallback vers provider secondaire si indisponible (optionnel configurable).

## Epic 6 - Hygiene branches et reprise de travaux

### US-014 - Verifier les branches existantes avant nouveau dev (P0)
Description: En tant que mainteneur, je veux detecter les branches existantes qui contiennent deja des travaux lies a un item du backlog pour soit continuer dessus, soit la supprimer proprement.

Critieres d'acceptation:
- [ ] Avant de commencer un item backlog, le process inspecte les branches locales et distantes pour trouver des correspondances (nom de feature, mots-cles, commits recents, fichiers touches).
- [ ] Si une branche pertinente est trouvee avec progression utile, la decision par defaut est de continuer sur cette branche.
- [ ] Si une branche est obsolete ou non pertinente, le process cree d'abord une archive de sauvegarde au format `.tga` dans un dossier `backup/`.
- [ ] La suppression de branche (locale et/ou distante) n'est autorisee qu'apres creation et verification de la sauvegarde.
- [ ] Le resultat (continuer/supprimer + chemin de backup) est trace dans la note de travail.

## Sprint propose (ordre de livraison)
- Sprint 1: US-004, US-005, US-006, US-009
- Sprint 2: US-007, US-008, US-010
- Sprint 3: US-011, US-012, US-013
- Sprint 4: US-001, US-002, US-003

Note processus transverse: US-014 s'applique en pre-check avant chaque sprint.

## Risques et points d'attention
- Migration JSON -> DB: risque de perte de donnees sans procedure de backup.
- Multi-provider: variabilite des APIs et des politiques de quotas.
- Export/import: risque de fuite de secrets si la sanitization n'est pas stricte.

## Definition of Done (globale)
- [ ] Fonctionnalite implementee selon criteres d'acceptation.
- [ ] Non-regression validee sur generation de pages.
- [ ] Documentation et note de changelog mises a jour.
