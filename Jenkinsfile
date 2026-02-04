pipeline {
    agent any
    
    stages {
        stage('Hello World') {
            steps {
                echo '🎉 Hello World from Jenkins!'
                echo 'Build triggered by GitHub webhook'
            }
        }
        
        stage('Check Files') {
            steps {
                echo 'Listing files...'
                sh 'ls -la'
            }
        }
        
        stage('Python Test') {
            steps {
                echo 'Testing Python...'
                sh 'python --version'
            }
        }
    }
    
    post {
        success {
            echo '✅ Build SUCCESS!'
        }
        failure {
            echo '❌ Build FAILED!'
        }
    }
}