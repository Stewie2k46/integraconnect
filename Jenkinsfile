pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('jenkins-docker')
        GIT_CREDENTIALS = credentials('git-hub')
        KUBE_CONFIG = credentials('kubeconfig')
        APP_NAME = 'integraconnect' // Make sure APP_NAME or relevant variable is defined
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS}", url: 'https://github.com/Stewie2k46/integraconnect.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_CREDENTIALS_USR}/${APP_NAME}:1.0")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS}") {
                        docker.image("${DOCKER_CREDENTIALS_USR}/${APP_NAME}:1.0").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'kubeconfig']) {
                        sh 'kubectl apply -f deployment.yaml'
                        sh 'kubectl apply -f service.yaml'
                    }
                }
            }
        }
    }

    post {
        failure {
            echo 'Deployment Failed!'
        }
    }
}
