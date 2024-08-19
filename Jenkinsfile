pipeline {
    agent any

    environment {
        DOCKERHUB_TOKEN = credentials('docker-hub-token') // Use your secret text ID for Docker Hub PAT
        GIT_CREDENTIALS = credentials('git-hub')
        KUBE_CONFIG = credentials('minikube-kubeconfig')
        APP_NAME = 'integraconnect'
        DOCKER_REPO = "stewiedocker46/${APP_NAME}" // Docker Hub repo will be created automatically
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS}", 
                    url: 'https://github.com/Stewie2k46/integraconnect.git', 
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REPO}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKERHUB_TOKEN}") {
                        docker.image("${DOCKER_REPO}:${BUILD_NUMBER}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig([credentialsId: 'minikube-kubeconfig']) {
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
        success {
            echo 'Deployment Succeeded!'
        }
    }
}
