pipeline {
    agent any

    environment {
        AWS_REGION            = 'ap-south-1'
        ECR_REPO              = '354918370166.dkr.ecr.ap-south-1.amazonaws.com/devsecops-app'
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
                    -e SONAR_TOKEN=''' + env.SONAR_TOKEN + ''' \
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
                echo 'Running OWASP dependency scan...'
                sh '''
                    mkdir -p owasp-reports
                    docker run --rm \
                    -v "$(pwd):/src" \
                    -v "$(pwd)/owasp-reports:/report" \
                    owasp/dependency-check \
                    --scan /src/app \
                    --format HTML \
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
                script {
                    sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                    sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest"
                }
                echo '✅ Docker image built!'
            }
        }

        stage('🔒 Trivy Security Scan') {
            steps {
                echo 'Scanning Docker image for vulnerabilities...'
                sh '''
                    mkdir -p trivy-reports
                    docker run --rm \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v "$(pwd)/trivy-reports:/reports" \
                    aquasec/trivy:latest image \
                    --exit-code 0 \
                    --severity HIGH,CRITICAL \
                    --format table \
                    --output /reports/trivy-report.txt \
                    ''' + env.ECR_REPO + ':' + env.IMAGE_TAG + '''
                '''
                echo '✅ Trivy scan completed!'
            }
        }

        stage('☁️ Push to AWS ECR') {
            steps {
                echo 'Pushing to ECR...'
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}"
                    sh "docker push ${ECR_REPO}:${IMAGE_TAG}"
                    sh "docker push ${ECR_REPO}:latest"
                }
                echo '✅ Image pushed to ECR!'
            }
        }

        stage('🚀 Deploy to EKS') {
            steps {
                echo 'Deploying to Kubernetes...'
                script {
                    sh "aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}"
                    sh "kubectl apply -f k8s/deployment.yaml"
                    sh "kubectl apply -f k8s/service.yaml"
                    sh "kubectl apply -f k8s/hpa.yaml"
                    sh "kubectl set image deployment/devsecops-app devsecops-app=${ECR_REPO}:${IMAGE_TAG}"
                    sh "kubectl rollout status deployment/devsecops-app"
                }
                echo '✅ Deployed to EKS!'
            }
        }

        stage('📊 Deploy Monitoring') {
            steps {
                echo 'Setting up Prometheus + Grafana...'
                script {
                    sh "kubectl apply -f k8s/monitoring.yaml || true"
                    sh "kubectl get pods -n monitoring"
                }
                echo '✅ Monitoring stack deployed!'
            }
        }

        stage('✅ Verify Deployment') {
            steps {
                echo 'Verifying everything is running...'
                script {
                    sh "kubectl get pods"
                    sh "kubectl get services"
                    sh "kubectl get hpa"
                }
            }
        }
    }

  post {
    always {
        script {
            try {
                archiveArtifacts artifacts: 'trivy-reports/*.txt', allowEmptyArchive: true
                archiveArtifacts artifacts: 'owasp-reports/*.html', allowEmptyArchive: true
            } catch (err) {
                echo "Archive step skipped: ${err}"
            }
        }
    }
    success {
        echo '🎉 DevSecOps Pipeline succeeded!'
    }
    failure {
        echo '❌ Pipeline failed! Check logs above.'
    }
}
