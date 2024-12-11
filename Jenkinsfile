pipeline {
    agent any
    stages {
        stage('Cloner le Dépôt') {
            steps {
                git branch: 'master', url: 'https://github.com/djebyamin/devops.git'
            }
        }
        stage('Construire et Lancer le Conteneur Docker pour le Frontend') {
            steps {
                script {
                    dir('frontend') {
                        bat 'docker build -t music-genre-classifier:latest .'
                        bat 'docker run -d -p 3000:3000 music-genre-classifier:latest'
                    }
                }
            }
        }
        stage('Construire et Lancer le Conteneur Docker pour SVM') {
            steps {
                script {
                    dir('SVM') {
                        bat 'docker build -t svm .'
                        bat 'docker run -d -p 5000:5000 svm'
                    }
                }
            }
        }
        stage('Construire et Lancer le Conteneur Docker pour VGG19') {
            steps {
                script {
                    dir('vgg19') {
                        bat 'docker build -t vgg19 .'
                        bat 'docker run -d -p 5001:5001 vgg19' // Utilisation d'un port différent pour éviter les conflits
                    }
                }
            }
        }
    }
    post {
        success {
            echo 'Déploiement réussi !'
        }
        failure {
            echo 'Le pipeline a échoué.'
        }
    }
}
