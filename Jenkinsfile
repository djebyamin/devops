pipeline {
    agent any
    stages {
        stage('Cloner le Dépôt') {
            steps {
                git branch:'master',url:'https://github.com/djebyamin/devops.git'
            }
        }
        stage('Construire l\'Image Docker') {
            steps {
                script{
                    dir('frontend'){
                    bat 'docker build -t music-genre-classifier:latest .'

                    }
                }
            }
        }
        stage('Lancer le Conteneur Docker') {
            steps {
                bat 'docker run -d -p 3000:3000 music-genre-classifier:latest'
            }
        }
    }
     ************************
    stage('Construire l\'Image Docker') {
            steps {
                script{
                    dir('SVM'){
                    bat 'docker build -t svm .'

                    }
                }
            }
        }
        stage('Lancer le Conteneur Docker') {
            steps {
                bat 'docker run -d -p 5000:5000 svm'
            }
        }
    }
  stage('Construire l\'Image Docker') {
            steps {
                script{
                    dir('vgg19  '){
                    bat 'docker build -t vgg19 .'

                    }
                }
            }
        }
        stage('Lancer le Conteneur Docker') {
            steps {
                bat 'docker run -d -p 5000:5000 vgg19'
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
   