# Biosphère — Laboratoire du vivant

Simulation interactive d’un écosystème, en français, dans **un seul fichier HTML**. Ouvrez `index.html` dans un navigateur moderne. Aucun serveur, compte, clé API ou outil de compilation n’est nécessaire.

## Explorer

- Île procédurale, forêts, rivières et archipel ; terrain reproductible à partir d’une graine.
- Herbivores et prédateurs autonomes : alimentation, énergie, fuite, chasse, naissance et mort.
- Transmission des traits de vitesse, vision et longévité, avec mutations réglables.
- Saisons, température, précipitations, fertilité et renouvellement des ressources.
- Huit paramètres en direct ; quatre scénarios de départ.
- Sécheresse, pluies, introduction de prédateurs et floraison.
- Pause, avance d’un jour, vitesses 1× / 3× / 10× / 30×, zoom, déplacement et plein écran.
- Inspection d’un animal, parent et descendants, suivi de caméra et trajectoires.
- Vues naturelle, ressources, énergie et générations.
- Graphiques des populations, des traits héréditaires et des ressources ; courbe de référence pour comparer des expériences.
- Sauvegarde/restauration JSON de l’état complet et export CSV des observations.
- Ambiance sonore originale, synthétisée dans le navigateur : souffle naturel, oiseaux et accord discret. Activation volontaire et volume réglable.
- Interface adaptée au tactile et au mobile, guide intégré et commandes accessibles au clavier.

## Une première expérience

1. Laissez évoluer la graine `ASTER-42` jusqu’au jour 150, à la vitesse souhaitée.
2. Cliquez sur **Mémoriser cette expérience**.
3. Recréez un monde avec la même graine et le même scénario.
4. Déclenchez une sécheresse au jour choisi, ou modifiez un paramètre.
5. Activez **Comparer à la courbe de référence**. Les anciennes courbes apparaissent en pointillés.

**Espace** met le temps en pause. La molette et le pincement zooment ; glisser déplace la carte. Un clic sur un animal ouvre sa fiche. La simulation s’interrompt quand l’onglet est masqué.

## Modèle

Le calcul utilise un pas fixe de 0,05 jour et un générateur pseudo-aléatoire initialisé par la graine. Une seconde correspond à un jour à vitesse 1× ; une année dure 240 jours. L’affichage et le son ne consomment pas l’aléatoire du modèle. Une sauvegarde restaure l’état du générateur, les ressources, les animaux et leur généalogie.

La végétation se renouvelle selon la température, la pluie, la fertilité et la croissance. Les herbivores recherchent les ressources et évitent les prédateurs. La chasse alimente les prédateurs. Les naissances exigent de l’énergie, un âge adulte et un délai entre reproductions. Les traits hérités peuvent muter. Les animaux ne traversent pas l’eau.

C’est un modèle exploratoire simplifié, pas une prévision écologique. La reproduction est asexuée ; les quatre saisons sont raccourcies ; le climat est uniforme sur la carte. Le plafond est de 600 animaux vivants : les naissances attendent une place quand il est atteint. L’historique des courbes conserve les 3 000 derniers jours. Les extinctions sont possibles et n’entraînent aucune réapparition automatique. Les ressources et paramètres peuvent produire des résultats très différents d’une graine à l’autre.

Les sauvegardes se téléchargent sur votre appareil ; elles ne sont pas envoyées sur un serveur. La courbe de référence utilise le stockage local du navigateur. La généalogie conserve les individus disparus pendant la session.

## Sources visuelles et sonores

Le terrain, les animaux et les sons sont produits par le code. Aucun asset musical ou visuel tiers n’est requis. Les polices DM Sans et Manrope sont chargées facultativement depuis Google Fonts (licence SIL Open Font License) ; des polices système prennent le relais hors connexion. Le bouton de téléchargement HTML est disponible lorsque la page est servie par HTTP ; en ouverture locale, vous disposez déjà du fichier.

## Développement et vérification

Pour servir le fichier localement :

```sh
python -m http.server 8080
```

Puis ouvrez `http://localhost:8080`.

Tests d’intégration :

```sh
python -m pip install playwright
python -m playwright install chromium
python tests/test_browser.py
```

Le script démarre son propre serveur. Il utilise Chromium installé sur le système s’il est disponible, sinon le navigateur de Playwright. `CHROMIUM_PATH` permet de sélectionner un exécutable.

Vérifications couvertes : reproductibilité exacte, restauration sans divergence, rejet des sauvegardes invalides sans modification de l’état courant, effet réel d’une sécheresse, simulation de 1 000 jours, respect des côtes et de la limite de population, commandes, export, son, inspection des animaux et absence de débordement horizontal sur mobile.

Des outils WebMCP sont enregistrés uniquement si le navigateur expose `document.modelContext` : lecture de l’écosystème, modification des paramètres et lancement d’une expérience. Cette API facultative n’est pas nécessaire à l’application. Sa validation native n’était pas disponible dans l’environnement de développement.
