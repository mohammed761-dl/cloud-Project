pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = '74.242.218.126:3000'
        BACKEND_IMAGE = 'mohammed/user-mgmt-api'
        FRONTEND_IMAGE = 'mohammed/frontend'
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build & Push Backend') {
            steps {
                echo '🔨 Building & Pushing Backend...'
                withCredentials([usernamePassword(credentialsId: 'gitea-docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${BACKEND_IMAGE}:${TAG} ./backend
                        docker tag ${DOCKER_REGISTRY}/${BACKEND_IMAGE}:${TAG} ${DOCKER_REGISTRY}/${BACKEND_IMAGE}:latest
                        
                        echo \$DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_REGISTRY}/${BACKEND_IMAGE}:${TAG}
                        docker push ${DOCKER_REGISTRY}/${BACKEND_IMAGE}:latest
                    """
                }
            }
        }

        stage('Build & Push Frontend') {
            steps {
                echo '🎨 Building & Pushing Frontend...'
                withCredentials([usernamePassword(credentialsId: 'gitea-docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:${TAG} ./frontend
                        docker tag ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:${TAG} ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:latest
                        
                        echo \$DOCKER_PASS | docker login ${DOCKER_REGISTRY} -u \$DOCKER_USER --password-stdin
                        docker push ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:${TAG}
                        docker push ${DOCKER_REGISTRY}/${FRONTEND_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG_FILE')]) {
                    echo '🚀 Running Ansible Playbook...'
                    sh """
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        ansible-playbook ansible/deploy.yml
                    """
                }
            }
        }

        stage('Force Refresh for Demo') {
            steps {
                withCredentials([file(credentialsId: 'k3s-config', variable: 'KUBECONFIG_FILE')]) {
                    echo '🔄 Forcing Kubernetes to pull the LATEST images...'
                    sh """
                        export KUBECONFIG=${KUBECONFIG_FILE}
                        # This triggers a rolling restart to pick up the fresh :latest images
                        kubectl rollout restart deployment user-management-app
                        kubectl rollout restart deployment frontend-app
                        
                        # Wait for the frontend to be ready so you don't refresh too early
                        kubectl rollout status deployment frontend-app
                    """
                }
            }
        }
    }

    post {
        success { 
            echo '✅ Pipeline Finished Successfully! Your demo is ready.' 
        }
        failure { 
            echo '❌ Pipeline Failed. Check the console logs.' 
        }
    }
}