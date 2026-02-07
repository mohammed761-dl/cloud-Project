pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = '74.242.218.126:3000'
        IMAGE_NAME = 'mohammed/user-mgmt-api'
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

        stage('Deploy to Azure K8s') {
            steps {
                withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG_FILE')]) {
                    script {
                        echo '☸️ Deploying to Azure K8s...'
                        sh """
                            export KUBECONFIG=${KUBECONFIG_FILE}
                            
                            # We use --server to ensure it hits the public IP directly
                            # We use --insecure-skip-tls-verify to skip certificate handshake issues
                            # We increase the request-timeout to 1 minute
                            
                            kubectl apply -f k8s-deploy.yaml \
                                --server=https://74.242.218.126:6443 \
                                --insecure-skip-tls-verify=true \
                                --validate=false \
                                --request-timeout=60s
                            
                            kubectl set image deployment/user-management-app \
                                fastapi-user-mgmt=${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG} \
                                --server=https://74.242.218.126:6443 \
                                --insecure-skip-tls-verify=true \
                                --request-timeout=60s
                        """
                    }
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