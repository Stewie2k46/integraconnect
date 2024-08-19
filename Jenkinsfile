pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('jenkins-docker') // Make sure this matches the ID of your Docker credentials
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
                    dockerImage = docker.build("${DOCKER_CREDENTIALS_USR}/${APP_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub with credentials: ${DOCKER_CREDENTIALS_USR}"
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS}") {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withKubeConfig([credentialsId: "${KUBE_CONFIG}"]) {
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
