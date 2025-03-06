// Question: Pourquoi séparer les routes dans différents fichiers ?
// Réponse : Séparer les routes permet d'améliorer la lisibilité et l'organisation du code, de faciliter la gestion de grandes applications et de maintenir un code modulaire.

// Question : Comment organiser les routes de manière cohérente ?
// Réponse : Organiser les routes par ressource (ex. cours, utilisateurs) et par fonction (création, lecture, mise à jour, suppression) pour rendre le code plus intuitif et facile à maintenir.

const express = require('express');
const router = express.Router();
const courseController = require('../controllers/courseController');

// Routes pour les cours
router.post('/', courseController.createCourse);
router.get('/:id', courseController.getCourse);
router.get('/stats', courseController.getCourseStats);

module.exports = router;
