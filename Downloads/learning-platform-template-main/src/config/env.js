// Question: Pourquoi est-il important de valider les variables d'environnement au démarrage ?
// Réponse : Valider les variables d'environnement garantit que l'application dispose de toutes les configurations nécessaires avant de démarrer, réduisant ainsi les erreurs et améliorant la sécurité.

// Question: Que se passe-t-il si une variable requise est manquante ?
// Réponse : Si une variable requise est manquante, l'application risque de ne pas fonctionner correctement, ce qui peut entraîner des erreurs ou des comportements imprévus. Il est essentiel d'arrêter l'application ou de lancer une erreur claire pour éviter de continuer dans un état incorrect.


const dotenv = require('dotenv');
dotenv.config();

const requiredEnvVars = [
  'MONGODB_URI',
  'MONGODB_DB_NAME',
  'REDIS_URI'
];

// Validation des variables d'environnement
function validateEnv() {
  const missingVars = requiredEnvVars.filter((varName) => !process.env[varName]);

  if (missingVars.length > 0) {
    console.error(
      `Erreur : Les variables d'environnement suivantes sont manquantes : ${missingVars.join(', ')}`
    );
    process.exit(1); // Arrêter l'application avec un code d'erreur
  }

  console.log('Toutes les variables d\'environnement requises sont présentes.');
}

// Valider les variables dès le chargement
validateEnv();

module.exports = {
  mongodb: {
    uri: process.env.MONGODB_URI,
    dbName: process.env.MONGODB_DB_NAME
  },
  redis: {
    uri: process.env.REDIS_URI
  },
  port: process.env.PORT || 3000
};
