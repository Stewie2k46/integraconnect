pipeline {
    agent any

    environment {
        DOCKERHUB_TOKEN = credentials('dockerhub-token')  // Reference the Secret Text ID here
        GIT_CREDENTIALS = credentials('git-hub')
        KUBE_CONFIG = credentials('minikube-kubeconfig')
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
                    def dockerImage = docker.build("${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKERHUB_TOKEN}") {
                        def dockerImage = docker.image("${APP_NAME}:${BUILD_NUMBER}")
                        dockerImage.push()
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
