pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gowthamkumarks/petcare-app:latest"
        KUBE_CONFIG = credentials('kubeconfig-jenkins') // Jenkins credential ID for kubeconfig
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(env.DOCKER_IMAGE)
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                 withCredentials([usernamePassword(
                 credentialsId: 'dockerhub-credentials',
                 usernameVariable: 'DOCKERHUB_USER',
                 passwordVariable: 'DOCKERHUB_PASS'
        )]) {
            sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
            sh "docker push ${env.DOCKER_IMAGE}"
        }
    }
}


        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-jenkins', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f deployment.yml'
                    sh 'kubectl apply -f service.yml'
                    sh 'kubectl apply -f ingress.yml || true'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
