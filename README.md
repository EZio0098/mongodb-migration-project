#  Migration de Données Médicales vers MongoDB avec Docker

##  Objectif
Ce projet vise à migrer automatiquement un dataset médical au format CSV vers une base MongoDB en utilisant des conteneurs Docker.

##  Contenu du projet
- `migrate_to_mongodb.py` : script Python de migration
- `Dockerfile` : conteneurisation du script
- `docker-compose.yml` : déploiement orchestré avec MongoDB
- `requirements.txt` : dépendances Python
- `healthcare_dataset.csv` : dataset à migrer (à placer manuellement)

## Étapes de migration
1. Le service MongoDB démarre avec les identifiants `admin/password`
2. Un conteneur Python est lancé pour exécuter `migrate_to_mongodb.py`
3. Le script lit `healthcare_dataset.csv`, nettoie les données :
   - supprime les doublons
   - gère les types (dates, float)
   - vérifie les colonnes
4. Les données sont insérées dans MongoDB (`medical_db.patients`)
5. Le volume `mongo_data` permet de conserver les données

## Commandes utiles
```bash
docker-compose up --build
docker exec -it mongodb_container mongosh -u admin -p password
```

## Vérification
```js
use medical_db
db.patients.countDocuments()
db.patients.find().limit(5)
```

##  Remarques
- Le fichier `healthcare_dataset.csv` doit être copié à la racine du projet.
- Assurez-vous que Docker fonctionne avec internet pour télécharger les images.
