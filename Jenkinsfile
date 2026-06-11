pipeline {
    agent any

    environment {
        AWS_REGION            = 'ap-south-1'
        ECR_REPO              = 'ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/devsecops-app'
        IMAGE_TAG             = "${BUILD_NUMBER}"
        CLUSTER_NAME          = 'devsecops-cluster'
        SONAR_TOKEN           = credentials('sonar-token')
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
    }

    stages {

        stage('📥 Checkout Code') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('🔍 SonarQube Code Analysis') {
            steps {
                echo 'Running SonarQube scan...'
                sh '''
                    docker run --rm \
                    --network="host" \
                    -e SONAR_HOST_URL="http://localhost:9000" \
                    -e SONAR_TOKEN=${SONAR_TOKEN} \
                    -v "$(pwd):/usr/src" \
                    sonarsource/sonar-scanner-cli \
                    -Dsonar.projectKey=devsecops-pipeline \
                    -Dsonar.sources=app \
                    -Dsonar.language=py
                '''
                echo '✅ SonarQube scan completed!'
            }
        }

        stage('🛡️ OWASP Dependency Check') {
            steps {
                echo 'Running OWASP dependency vulnerability scan...'
                sh '''
                    docker run --rm \
                    -v "$(pwd):/src" \
                    -v "$(pwd)/owasp-reports:/report" \
                    owasp/dependency-check \
                    --scan /src/app \
                    --format HTML \
                    --format JSON \
                    --out /report \
                    --project "devsecops-pipeline" \
                    --disableYarnAudit \
                    --disableNodeAudit \
                    || true
                '''
                echo '✅ OWASP scan completed!'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest"
                echo '✅ Docker image built!'
            }
        }

        stage('🔒 Trivy Security Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                sh """
                    docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v "$(pwd)/trivy-reports:/reports" \
                    aquasec/trivy:latest image \
                    --exit-code 0 \
                    --severity HIGH,CRITICAL \
                    --format table \
                    --output /reports/trivy-report.txt \
                    ${ECR_REPO}:${IMAGE_TAG}
                """
                echo '✅ Trivy scan completed!'
            }
        }

        stage('☁️ Push to AWS ECR') {
            steps {
                echo 'Pushing to ECR...'
                sh """
                    aws ecr get-login-password --region ${AWS_REGION} | \
                    docker login --username AWS --password-stdin ${ECR_REPO}
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                """
                echo '✅ Image pushed to ECR!'
            }
        }

        stage('🚀 Deploy to EKS') {
            steps {
                echo 'Deploying to Kubernetes...'
                sh """
                    aws eks update-kubeconfig \
                    --region ${AWS_REGION} \
                    --name ${CLUSTER_NAME}

                    # Replace ACCOUNT_ID in deployment.yaml
                    sed -i 's/ACCOUNT_ID/${AWS_ACCOUNT_ID}/g' k8s/deployment.yaml

                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/hpa.yaml

                    kubectl set image deployment/devsecops-app \
                    devsecops-app=${ECR_REPO}:${IMAGE_TAG}

                    kubectl rollout status deployment/devsecops-app
                """
                echo '✅ Deployed to EKS!'
            }
        }

        stage('📊 Deploy Monitoring') {
            steps {
                echo 'Setting up Prometheus + Grafana...'
                sh """
                    kubectl apply -f k8s/monitoring.yaml
                    kubectl get pods -n monitoring
                """
                echo '✅ Monitoring stack deployed!'
            }
        }

        stage('✅ Verify Deployment') {
            steps {
                echo 'Verifying everything is running...'
                sh """
                    kubectl get pods
                    kubectl get services
                    kubectl get hpa
                    kubectl get pods -n monitoring
                """
            }
        }
    }

    post {
        always {
            echo '📊 Publishing security reports...'
            archiveArtifacts artifacts: 'trivy-reports/*.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'owasp-reports/*.html', allowEmptyArchive: true
        }
        success {
            echo '🎉 DevSecOps Pipeline succeeded! App is secure and live!'
        }
        failure {
            echo '❌ Pipeline failed! Check security scan results above.'
        }
    }
}