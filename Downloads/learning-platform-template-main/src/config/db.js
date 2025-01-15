// Question : Pourquoi créer un module séparé pour les connexions aux bases de données ?
// Réponse : Un module séparé centralise la gestion des connexions, améliore la réutilisabilité et simplifie la maintenance du code.

// Question : Comment gérer proprement la fermeture des connexions ?
// Réponse : Utiliser des blocs `try...finally` ou des gestionnaires de contexte pour garantir la fermeture des connexions même en cas d'erreur.

const { MongoClient } = require('mongodb');
const redis = require('redis');
const config = require('./env');

let mongoClient, redisClient, db;

// Connexion à MongoDB
async function connectMongo() {
  try {
    mongoClient = new MongoClient(config.mongodb.uri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    await mongoClient.connect();
    db = mongoClient.db(config.mongodb.dbName);
    console.log('Connexion à MongoDB réussie');
    return db;
  } catch (error) {
    console.error('Erreur de connexion à MongoDB :', error);
    process.exit(1); // Arrêter l'application si la connexion échoue
  }
}

// Connexion à Redis
async function connectRedis() {
  return new Promise((resolve, reject) => {
    redisClient = redis.createClient({
      url: config.redis.uri,
    });

    redisClient.on('connect', () => {
      console.log('Connexion à Redis réussie');
      resolve(redisClient);
    });

    redisClient.on('error', (error) => {
      console.error('Erreur de connexion à Redis :', error);
      reject(error);
    });

    redisClient.connect().catch((error) => {
      console.error('Impossible de connecter Redis :', error);
      process.exit(1);
    });
  });
}

// Fermeture des connexions
async function closeConnections() {
  if (mongoClient) {
    await mongoClient.close();
    console.log('Connexion à MongoDB fermée');
  }
  if (redisClient) {
    await redisClient.quit();
    console.log('Connexion à Redis fermée');
  }
}

// Gestion des signaux système pour une fermeture propre
process.on('SIGINT', async () => {
  console.log('Arrêt de l\'application...');
  await closeConnections();
  process.exit(0);
});

// Export des fonctions et clients
module.exports = {
  connectMongo,
  connectRedis,
  getMongoClient: () => mongoClient,
  getRedisClient: () => redisClient,
  getDb: () => db,
};
