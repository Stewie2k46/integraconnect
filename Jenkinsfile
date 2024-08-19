pipeline {
    agent any

    environment {
        GIT_CREDENTIALS = credentials('git-hub')
        KUBE_CONFIG = credentials('minikube-kubeconfig')
        DOCKERHUB_USER = 'stewiedocker46'  // Hardcoded Docker Hub username
        DOCKERHUB_TOKEN = 'dckr_pat_f1nx9Qp1qNOOccC7-cqIVAA_UnQ'  // Hardcoded Docker Hub token
        APP_NAME = 'integraconnect'
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
                    docker.build("${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKERHUB_USER}:${DOCKERHUB_TOKEN}") {
                        docker.image("${APP_NAME}:${BUILD_NUMBER}").push()
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
