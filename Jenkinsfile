pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = '74.242.218.126:5000'
        IMAGE_NAME = 'user-mgmt-api'
        CONTAINER_NAME = 'user-api'
        PORT = '3000'
        DOCKER_CREDENTIALS = credentials('gitea-docker-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checkout code...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                script {
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} .
                        docker tag ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('Push to Gitea') {
            steps {
                echo '📤 Pushing to Gitea registry...'
                script {
                    sh """
                        echo \$DOCKER_CREDENTIALS_PSW | docker login -u \$DOCKER_CREDENTIALS_USR --password-stdin ${DOCKER_REGISTRY}
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                        docker logout ${DOCKER_REGISTRY}
                    """
                }
            }
        }
        

    }
    
    post {
        success {
            echo '✅ Build and Deploy SUCCESS!'
        }
        failure {
            echo '❌ Build FAILED!'
        }
    }
}