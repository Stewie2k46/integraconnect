pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('jenkins-docker')
        GITHUB_CREDENTIALS = credentials('git-hub')
    }

    stages {
        stage('Clone repository') {
            steps {
                git url: 'https://github.com/Stewie2k46/integraconnect.git', branch: 'main', credentialsId: 'git-hub'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m unittest discover -s app/tests'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def app = docker.build("stewiedocker46/integraconnect:1.0", ".")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'jenkins-docker') {
                        app.push("latest")
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f kubernetes/deployment.yaml
                kubectl apply -f kubernetes/service.yaml
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
