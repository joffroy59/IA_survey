# Plan : Déploiement GitHub Pages → SharePoint Entreprise

## Contexte

Publier automatiquement les pages HTML générées (index.html, enterprise.html, etc.) sur un site SharePoint d'entreprise via GitHub Actions.

---

## Option 1 — Microsoft Graph API (Recommandée)

**Principe** : Upload des fichiers HTML dans une Document Library SharePoint via l'API Microsoft Graph.

**Avantages** :
- API officielle Microsoft, bien documentée
- Contrôle fin sur les fichiers et dossiers
- Supporte l'authentification app-only (pas besoin d'un compte utilisateur)

**Prérequis** :
- Enregistrer une **App Registration** dans Azure AD (Entra ID)
- Accorder les permissions `Sites.ReadWrite.All` (application)
- Stocker `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` dans les secrets GitHub

**Workflow GitHub Actions** :

```yaml
name: Deploy to SharePoint
on:
  workflow_run:
    workflows: ["pages-build-deployment"]
    types: [completed]

jobs:
  deploy-sharepoint:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get access token
        id: auth
        run: |
          TOKEN=$(curl -s -X POST \
            "https://login.microsoftonline.com/${{ secrets.AZURE_TENANT_ID }}/oauth2/v2.0/token" \
            -d "client_id=${{ secrets.AZURE_CLIENT_ID }}" \
            -d "client_secret=${{ secrets.AZURE_CLIENT_SECRET }}" \
            -d "scope=https://graph.microsoft.com/.default" \
            -d "grant_type=client_credentials" | jq -r '.access_token')
          echo "token=$TOKEN" >> $GITHUB_OUTPUT

      - name: Upload HTML files to SharePoint
        run: |
          SITE_ID="${{ secrets.SHAREPOINT_SITE_ID }}"
          DRIVE_ID="${{ secrets.SHAREPOINT_DRIVE_ID }}"
          FOLDER="IA_Survey"
          TOKEN="${{ steps.auth.outputs.token }}"

          for file in *.html; do
            echo "Uploading $file..."
            curl -s -X PUT \
              "https://graph.microsoft.com/v1.0/sites/${SITE_ID}/drives/${DRIVE_ID}/root:/${FOLDER}/${file}:/content" \
              -H "Authorization: Bearer ${TOKEN}" \
              -H "Content-Type: text/html" \
              --data-binary "@${file}"
          done
          echo "✅ All HTML files uploaded"
```

**Comment trouver SITE_ID et DRIVE_ID** :
```bash
# Site ID
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/votre-tenant.sharepoint.com:/sites/NomDuSite"

# Drive ID (Document Library)
curl -H "Authorization: Bearer $TOKEN" \
  "https://graph.microsoft.com/v1.0/sites/{site-id}/drives"
```

---

## Option 2 — SharePoint REST API + App-Only

**Principe** : Utiliser directement l'API REST SharePoint (pas Graph) avec un certificat ou secret d'app.

**Avantages** :
- Fonctionne même si l'organisation limite l'accès Graph
- API SharePoint native, bien connue des admins SP

**Inconvénients** :
- Auth plus complexe (certificat X.509 recommandé)
- API REST SP moins intuitive que Graph

**Workflow simplifié** :
```yaml
      - name: Upload via SharePoint REST
        run: |
          # Obtenir le digest pour auth
          DIGEST=$(curl -s -X POST \
            "https://votre-tenant.sharepoint.com/sites/NomSite/_api/contextinfo" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Accept: application/json" | jq -r '.FormDigestValue')

          # Upload fichier
          curl -X POST \
            "https://votre-tenant.sharepoint.com/sites/NomSite/_api/web/GetFolderByServerRelativeUrl('/sites/NomSite/Documents/IA_Survey')/Files/add(url='index.html',overwrite=true)" \
            -H "Authorization: Bearer $TOKEN" \
            -H "X-RequestDigest: $DIGEST" \
            -H "Content-Type: application/octet-stream" \
            --data-binary "@index.html"
```

---

## Option 3 — PnP PowerShell

**Principe** : Utiliser le module [PnP.PowerShell](https://pnp.github.io/powershell/) dans GitHub Actions.

**Avantages** :
- Module très populaire dans l'écosystème SharePoint
- Commandes haut niveau (`Add-PnPFile`, `Connect-PnPOnline`)
- Gère bien les sites modernes, les pages, les bibliothèques

**Workflow** :
```yaml
      - name: Install PnP PowerShell
        shell: pwsh
        run: Install-Module -Name PnP.PowerShell -Force -Scope CurrentUser

      - name: Deploy to SharePoint
        shell: pwsh
        env:
          TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
          SITE_URL: ${{ secrets.SHAREPOINT_SITE_URL }}
        run: |
          $secSecret = ConvertTo-SecureString $env:CLIENT_SECRET -AsPlainText -Force
          Connect-PnPOnline -Url $env:SITE_URL -ClientId $env:CLIENT_ID `
            -ClientSecret $secSecret -Tenant $env:TENANT_ID

          Get-ChildItem -Filter "*.html" | ForEach-Object {
            Add-PnPFile -Path $_.FullName -Folder "Documents/IA_Survey" -ErrorAction Stop
            Write-Host "✅ $($_.Name) uploaded"
          }

          # Optionnel : copier aussi les data JSON
          Get-ChildItem "data/*.json" | ForEach-Object {
            Add-PnPFile -Path $_.FullName -Folder "Documents/IA_Survey/data" -ErrorAction Stop
          }
```

---

## Option 4 — CLI for Microsoft 365 (m365)

**Principe** : Utiliser [CLI for Microsoft 365](https://pnp.github.io/cli-microsoft365/) (Node.js).

**Avantages** :
- Cross-platform, fonctionne en CI/CD
- Commandes simples : `m365 spo file add`

**Workflow** :
```yaml
      - name: Install CLI for M365
        run: npm install -g @pnp/cli-microsoft365

      - name: Login and deploy
        run: |
          m365 login --authType secret \
            --tenant ${{ secrets.AZURE_TENANT_ID }} \
            --appId ${{ secrets.AZURE_CLIENT_ID }} \
            --secret ${{ secrets.AZURE_CLIENT_SECRET }}

          for file in *.html; do
            m365 spo file add \
              --webUrl "${{ secrets.SHAREPOINT_SITE_URL }}" \
              --folder "Documents/IA_Survey" \
              --path "$file"
          done
```

---

## Option 5 — Azure Logic App / Power Automate (No-Code)

**Principe** : Un webhook GitHub déclenche un flux Power Automate qui copie les fichiers.

**Avantages** :
- Pas de code, configurable par des non-devs
- Intégré nativement à SharePoint

**Inconvénients** :
- Limité pour des fichiers volumineux
- Dépend des licences Power Platform
- Moins contrôlable depuis GitHub Actions

---

## Comparatif

| Option | Complexité | Maintenance | Fiabilité | Recommandé |
|--------|-----------|-------------|-----------|------------|
| **1. Graph API** | Moyenne | Faible | ★★★★★ | ✅ Oui |
| **2. SP REST API** | Élevée | Moyenne | ★★★★ | Cas spéciaux |
| **3. PnP PowerShell** | Faible | Faible | ★★★★★ | ✅ Oui |
| **4. CLI M365** | Faible | Faible | ★★★★ | Bonne alternative |
| **5. Power Automate** | Faible | Faible | ★★★ | Non-devs uniquement |

---

## Étapes de mise en place (Option 1 ou 3)

### 1. Azure AD App Registration
1. Aller dans **Azure Portal** → **Entra ID** → **App registrations** → **New registration**
2. Nom : `GitHub-IA-Survey-SP-Deploy`
3. Ajouter un **Client secret** (noter la valeur)
4. API Permissions → **Microsoft Graph** → Application → `Sites.ReadWrite.All`
5. **Grant admin consent**

### 2. Secrets GitHub
Ajouter dans **Settings** → **Secrets and variables** → **Actions** :
- `AZURE_TENANT_ID`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `SHAREPOINT_SITE_URL` (ex: `https://votre-tenant.sharepoint.com/sites/IA-Tools`)
- `SHAREPOINT_SITE_ID` (si Option 1)
- `SHAREPOINT_DRIVE_ID` (si Option 1)

### 3. Créer le workflow
Copier le YAML de l'option choisie dans `.github/workflows/deploy-sharepoint.yml`

### 4. Tester
Déclencher manuellement ou pousser un commit sur main.

---

## Notes de sécurité
- Ne jamais stocker de secrets dans le code
- Limiter les permissions de l'app Azure AD au minimum nécessaire
- Utiliser un certificat X.509 plutôt qu'un client secret en production
- Activer l'audit logging sur le site SharePoint
- Considérer un **Managed Identity** si le runner est hébergé sur Azure
