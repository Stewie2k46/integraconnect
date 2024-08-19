pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('jenkins-docker')  // Docker Hub credentials
        GIT_CREDENTIALS = credentials('git-hub')  // GitHub credentials
        KUBE_CONFIG = credentials('minikube-kubeconfig')  // Kubeconfig for Minikube
        APP_NAME = 'integraconnect'  // Application name
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS}", 
                    url: 'https://github.com/Stewie2k46/integraconnect.git', 
                    branch: 'main'  // Explicitly specifying the 'main' branch
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS}") {
                        docker.image("${DOCKER_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}").push()
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
