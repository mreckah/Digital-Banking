// Question: Quelle est la différence entre un contrôleur et une route ?
// Réponse: Une route définit l'URL et la méthode HTTP (GET, POST, etc.), tandis qu'un contrôleur contient la logique métier pour traiter les requêtes associées à cette route.

// Question : Pourquoi séparer la logique métier des routes ?
// Réponse : Séparer la logique métier des routes permet de maintenir un code plus propre, réutilisable et testable, et rend l'application plus facile à étendre et à maintenir.

const { ObjectId } = require('mongodb');
const db = require('../config/db');
const mongoService = require('../services/mongoService');
const redisService = require('../services/redisService');

async function createCourse(req, res) {
  try {
    // Exemple de logique métier via les services
    const courseData = req.body;
    const newCourse = await mongoService.createCourse(courseData);
    await redisService.cacheCourse(newCourse);
    res.status(201).json(newCourse);
  } catch (err) {
    res.status(500).json({ message: 'Erreur lors de la création du cours', error: err });
  }
}

// Export des contrôleurs
module.exports = {
  createCourse, // Exporter la fonction createCourse
};
