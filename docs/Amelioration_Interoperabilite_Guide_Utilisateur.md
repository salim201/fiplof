# Guide Utilisateur - Améliorations de l'Interopérabilité

## 1. Attribution des dates et CRL

### Fenêtre : Attribution des dates et CRL

**Accès :** Menu `Certificat Foncier > Demande de certificat > Attribution des dates et CRL`

#### Bouton "Assigner" (CRL)

Ce bouton permet d'assigner les membres de la Commission de Reconnaissance Locale (CRL) aux demandes sélectionnées.

**Fonctionnement :**

1. Ajoutez des membres CRL via le bouton `+` dans le cadre "Gestion CRL"
2. Remplissez les informations : Rôle, Titulaire, Suppléant
3. Recherchez des demandes via les critères (N° Décision, Fokontany, Hameau)
4. Cochez les demandes à assigner dans le tableau
5. Cliquez sur **Assigner**

**Nouveautés :**
- Une **barre de progression** s'affiche pendant l'assignation
- L'interface reste **responsive** (ne se bloque pas)
- Les messages de succès ou d'erreur sont clairement affichés
- Si un rôle n'existe pas encore dans la base, il est **créé automatiquement**

---

## 2. Transformation des demandes (Interopérabilité)

**Accès :** Menu `Interropérabilité > Transformation en demande`

Cette fonction permet d'importer des demandes issues d'un système externe (JSON) vers la base Fiplof.

#### Nouveautés

### Insertion automatique des membres CRL

Désormais, lors de la transformation d'une demande, les **membres de la CRL** sont automatiquement insérés dans la base de données :

- Chaque membre (avec son rôle, ses informations personnelles) est créé dans la table `personne`
- Le statut **président** est préservé si indiqué dans les données
- Le rôle est automatiquement créé dans `role_crl` s'il n'existe pas
- Les membres sont liés à la demande via `demande_crl`

**Données importées :**
- Rôle du membre (Président, Secrétaire, Membre, etc.)
- Nom, prénom et informations personnelles
- Statut titulaire/suppléant
- Flag président de la commission

### Gestion des transactions

Les opérations de transformation sont maintenant **transactionnelles** :
- Toutes les insertions sont validées ensemble (`COMMIT`)
- En cas d'erreur, toutes les modifications sont annulées (`ROLLBACK`)
- Plus de blocage de l'application après une erreur

### Barre de progression

Une barre de progression est affichée pendant le chargement et le traitement des données.

---

## 3. Envoi des retours (API)

**Accès :** Menu `Interropérabilité > Envoi des retours`

### Nouveautés

- **Proposition de réessai** : si le serveur répond avec une erreur (HTTP 500), une boîte de dialogue vous propose de **réessayer** avant d'abandonner
- Le statut d'envoi est affiché en temps réel
- Gestion améliorée des erreurs réseau et serveur

---

## Résolution des problèmes courants

### L'application se bloque après une action

**Avant correction :** Une transaction non fermée pouvait bloquer toutes les opérations suivantes sur la base de données, forçant le redémarrage de Fiplof.

**Après correction :**
- Toutes les transactions sont correctement validées ou annulées
- En cas d'erreur, la base revient à son état précédent
- Plus besoin de redémarrer Fiplof après une action dans le menu Interopérabilité

### Les membres CRL n'apparaissent pas après transformation

Vérifiez que le fichier JSON d'entrée contient bien la structure suivante :

```json
{
  "rl": {
    "date_rl": "2024-01-15",
    "avis_crl": true,
    "obs_crl": "",
    "membres_crl": [
      {
        "role": "President",
        "personne": { "nom": "RAKOTO", "prenom": "Jean" },
        "titulaire": true,
        "president": true
      },
      {
        "role": "Secretaire",
        "personne": { "nom": "RANDRIANARISOA", "prenom": "Marie" },
        "titulaire": false,
        "president": false
      }
    ]
  }
}
```
