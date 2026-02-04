pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = '74.242.218.126:3000'
        IMAGE_NAME = 'user-mgmt-api'
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                echo '🔨 Building Docker image...'
                sh """
                    docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG} .
                    docker tag ${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                """
            }
        }

        stage('Push to Gitea Registry') {
            steps {
                echo '📤 Pushing image to Gitea...'
                withCredentials([usernamePassword(
                    credentialsId: 'gitea-docker-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}
                        docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                        docker logout ${DOCKER_REGISTRY}
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Build & Push SUCCESS'
        }
        failure {
            echo '❌ Build FAILED'
        }
    }
}