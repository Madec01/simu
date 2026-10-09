# Biosphère V2 — Laboratoire du vivant

**[Ouvrir la simulation](https://biosphere-aster.madec.chatgpt.site)** · Version hébergée privée, accessible à son propriétaire.

Un écosystème interactif en français, livré dans **un fichier HTML autonome**. Ouvrez `index.html` dans un navigateur moderne. Aucun compte, serveur, clé API ou installation n’est requis pour l’utiliser localement.

## Les ateliers

### Observer

Une île procédurale avec sept rôles écologiques : herbivores, prédateurs, pollinisateurs, charognards, décomposeurs, poissons et amphibiens. Les animaux dépensent de l’énergie, se nourrissent, vieillissent, se reproduisent et meurent. Les saisons et les réglages du climat influencent les ressources.

Les sentinelles alertent les herbivores voisins. Les prédateurs partagent une cible au sein d’une meute, approchent leur proie par plusieurs côtés et défendent leur territoire. Une mémoire limitée conserve les ressources rencontrées et les dangers récents. Le mode « Groupes et mémoire » montre territoires et points de nourriture connus. Ces comportements peuvent être désactivés pour comparer leur effet.

Cliquez sur un animal pour inspecter son âge, sa santé, son énergie, ses traits, son groupe, sa mémoire et sa généalogie. Le suivi manuel, les trajectoires, le zoom, le déplacement et le plein écran restent disponibles. Les autres vues montrent les ressources, l’énergie, les générations, la fertilité locale et la pollinisation.

### Façonner

Peignez directement sur la carte : forêt, eau, montagne, barrière, passage ou restauration du terrain d’origine. Le rayon du pinceau est réglable. Les modifications changent réellement les habitats et les déplacements. Les espèces volantes passent au-dessus des barrières ; les poissons restent dans l’eau. Les animaux privés d’habitat cherchent un refuge et peuvent mourir s’ils ne l’atteignent pas.

Chaque tracé crée un point de retour avant modification et met le temps en pause. « Annuler le dernier tracé » restaure le point correspondant. Pour isoler deux populations, dessinez une barrière ; ouvrez ensuite un passage pour les reconnecter.

### Événements

- **Incendie** : propagation entre cellules selon le vent, l’humidité, le combustible et l’intensité ; consommation de végétation, dégâts aux animaux et cendres qui enrichissent le sol.
- **Crue** : hausse temporaire du niveau de l’eau et submersion des terres basses.
- **Gel** : baisse de température, dépense énergétique accrue et ralentissement des poissons.
- **Épidémie** : contamination de proximité entre membres d’une espèce, effet de l’immunité héritée et immunité temporaire après guérison.
- **Sécheresse et pluies** : effets directs sur le renouvellement végétal et les températures.

Réglez l’intensité (0,2 à 2), la durée initiale (5 à 150 jours), la force et la direction du vent. Des commandes permettent d’éteindre les foyers, soigner les infections ou terminer un épisode climatique. La durée d’une épidémie fixe celle des premiers cas ; les contaminations suivantes peuvent prolonger l’épisode.

### Réseau vivant

Introduisez dix individus d’une espèce ou retirez-la pour observer les effets indirects. Un point de retour est conservé avant ces actions.

- Les herbivores consomment les plantes.
- Les prédateurs chassent herbivores et amphibiens.
- Les pollinisateurs déposent du pollen qui favorise la croissance locale.
- Les charognards consomment les carcasses et restituent une partie des nutriments.
- Les décomposeurs transforment les débris organiques en fertilité.
- Les poissons consomment les algues.
- Les amphibiens consomment algues et insectes et circulent entre terre et eau.

Une lente décomposition de fond subsiste sans décomposeurs ; leur présence accélère le recyclage. Les déchets végétaux et animaux alimentent la matière organique.

### Génétique

Sept traits héréditaires : vitesse, vision, longévité, taille, camouflage, résistance au froid et immunité. Le taux de mutation est réglable.

La taille change l’apparence, la santé, la vitesse effective et les besoins énergétiques. Le camouflage change la couleur et réduit la détection en forêt. La résistance au froid protège du gel mais augmente le coût par forte chaleur. L’histogramme montre la distribution d’un trait, sa moyenne et son écart-type pour une population.

L’arbre permet de naviguer entre ancêtres, individu sélectionné, enfants et petits-enfants, y compris les individus morts. Jusqu’à 24 individus sont affichés par niveau ; cliquer sur un nœud ouvre sa branche. Les lignées les plus présentes sont proposées comme points de départ.

### Laboratoire A/B

« Dupliquer A vers B » copie l’état complet du monde A : terrain, ressources, génomes, mémoire, aléatoire et historique. Les deux mondes avancent avec le même pas de temps. Choisissez A ou B pour déterminer la cible des réglages et des outils. La courbe de l’autre monde apparaît en pointillés.

Les **essais répétés** travaillent sur des copies séparées de l’état actuel d’A. Pour chaque paire, le même état initial et le même tirage futur sont utilisés ; un seul paramètre diffère dans B. Choisissez 2 à 10 répétitions et 10 à 300 jours. Les résultats affichent moyennes, écarts-types et différences pour les populations, la végétation et le nombre de rôles présents. Les expériences sont reproductibles, annulables et exportables en CSV ; elles ne modifient pas les mondes affichés.

Les écarts-types décrivent les essais de ce modèle. Ils ne représentent pas une validation écologique ni une prédiction du monde réel.

### Chronologie

Créez des points nommés et revenez à leur état exact. Le présent est sauvegardé avant le retour ; une nouvelle branche est ouverte. Un point contient A et B lorsqu’ils sont présents. Les points automatiques sont créés tous les 60 jours et peuvent être désactivés.

La chronologie garde **jusqu’à 14 points**, avec un budget d’environ 32 Mio pour limiter la mémoire utilisée par les copies. Les plus anciens sont retirés lorsque ce budget est atteint. Téléchargez régulièrement une session pour conserver une expérience longue.

## Sauvegardes et commandes

Le menu **Sauvegarder** exporte la session JSON (mondes et chronologie), les observations CSV ou le fichier HTML. L’import accepte les sessions V2 et les anciennes sauvegardes V1. Une V1 conserve ses populations existantes ; les nouveaux rôles s’ajoutent depuis le réseau vivant. Elle évolue ensuite selon les règles du moteur V2.

Les fichiers invalides sont rejetés avant de remplacer la session courante. Les imports sont limités à 64 Mio. Les données restent sur votre appareil ; la courbe de référence utilise le stockage local du navigateur.

- **Espace** : pause / reprise.
- **Avance d’un jour** : avance les deux mondes d’un jour puis laisse la pause active.
- Vitesses **1×, 3×, 10×, 30×**.
- Molette ou pincement : zoom ; glisser : déplacer ou peindre selon l’outil.
- **Échap** : quitter le pinceau actif.

L’ambiance sonore originale de la V1 reste activable : souffle naturel, oiseaux et accord discret, synthétisés dans le navigateur avec volume réglable. Aucun mode documentaire automatique n’est ajouté.

## Modèle et limites

Le calcul utilise un pas fixe de **0,05 jour**. Les ressources et la propagation du feu sont actualisées tous les cinq pas. Une seconde correspond à un jour à vitesse 1× ; une année dure 240 jours. Le rendu et le son ne consomment pas l’aléatoire du moteur. La vitesse réelle dépend du navigateur et de la charge des deux mondes.

C’est un modèle exploratoire simplifié : reproduction asexuée, climat uniforme, cellules de terrain de 8 unités, comportements locaux et absence de planification globale des trajets. Les extinctions sont possibles et n’entraînent aucune réapparition automatique. Les naissances attendent lorsqu’un monde atteint **600 animaux**. Les courbes conservent **3 000 jours**. L’historique généalogique peut devenir volumineux lors de très longues sessions.

L’eau, les montagnes et les barrières limitent les trajets. Une modification du terrain peut piéger un animal ; il tente de rejoindre un habitat accessible et subit des dégâts pendant ce déplacement. Les couleurs de corps représentent principalement espèce et camouflage, tandis que la taille héritée modifie leur silhouette.

## Développement

`index.html` est le livrable autonome. Les sources lisibles sont séparées pour faciliter les évolutions :

```text
src/engine.js        règles du vivant, terrain, aléatoire, instantanés et migration
src/renderer.js      cartes Canvas, animaux et interaction avec les pinceaux
src/app.js           interface, comparaison, essais, chronologie, son et sauvegardes
src/styles.css      styles et adaptation mobile
src/shell.html      structure de la page
scripts/build.py    assemblage du fichier HTML autonome
```

Après une modification des sources :

```sh
python scripts/build.py
python -m http.server 8080
```

Ouvrez ensuite `http://localhost:8080`.

## Tests

```sh
node tests/test_engine.cjs
python -m pip install playwright
python -m playwright install chromium
python tests/test_browser.py
```

Les tests du moteur couvrent reproductibilité, restauration exacte, habitats et barrières, alertes et partage des cibles, pollinisation et recyclage, incendies, climat, infections, génétique et 1 000 jours de stabilité.

Les tests du navigateur couvrent les deux cartes A/B, l’isolation des paramètres, le pinceau et son annulation, les branches temporelles, les catastrophes, l’introduction/retrait d’espèces, les distributions et arbres généalogiques, les sessions JSON, le rejet atomique des fichiers invalides, les séries appariées et leur annulation, les exports, l’audio et chaque atelier sur mobile. Le script lance son propre serveur ; `CHROMIUM_PATH` peut sélectionner un navigateur installé.

Les visuels et sons sont générés par le code. Les polices DM Sans et Manrope sont chargées facultativement depuis Google Fonts (licence SIL Open Font License), avec repli sur des polices système hors connexion. Aucun asset musical ou visuel tiers n’est nécessaire.

Des outils WebMCP sont enregistrés uniquement lorsque le navigateur expose `document.modelContext`. Leur validation native n’était pas disponible dans l’environnement de développement ; l’interface standard fonctionne sans cette API.
