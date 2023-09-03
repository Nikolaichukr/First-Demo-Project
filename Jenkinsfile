pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh  '''
                    echo "Building docker image..."
                    echo "BUILD_NUMBER=${BUILD_NUMBER}" > .env
                    docker build -t demo-project:latest .
                    docker rm $(docker ps -aq) 2>/dev/null || true
                    docker images -f "dangling=true" -q | xargs -r docker rmi --force
                    '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'docker run --rm demo-project python -m unittest discover -s tests'
            }
        }
        stage('Push to ECR') {
            steps {
                echo 'Pushing to ECR...'
                    withCredentials([string(credentialsId: 'AWS_ECR_STRING', variable: 'AWS_ECR_STRING'), string(credentialsId: 'REGION', variable: 'REGION')]) {
                        sh 'aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ECR_STRING}'
                        sh 'docker tag demo-project:latest ${AWS_ECR_STRING}/demo-project:latest'
                        sh 'docker push ${AWS_ECR_STRING}/demo-project:latest'
                }
            }
        }
        stage('Deploy on EC2 from ECR') {
            steps {
                echo 'Deploying...'
                withCredentials([
                    sshUserPrivateKey(credentialsId: 'webserver-ssh-key', 
                    keyFileVariable: 'SSH_KEY', usernameVariable: 'USER'), 
                    string(credentialsId: 'webserver-private-ip', variable: 'IP'), 
                    string(credentialsId: 'AWS_ECR_STRING', variable: 'AWS_ECR_STRING'), 
                    string(credentialsId: 'REGION', variable: 'REGION')
                    ]) {
                        sh '''
                            ssh -oStrictHostKeyChecking=no -i ${SSH_KEY} ${USER}@${IP} """
                                    aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ECR_STRING}
                                    docker pull ${AWS_ECR_STRING}/demo-project:latest
                                    docker stop demoproject 2>/dev/null || true
                                    docker run -d --rm --name demoproject -p 5000:5000 ${AWS_ECR_STRING}/demo-project:latest
                                    docker images --filter "dangling=true" --quiet | xargs -r docker rmi
                                """
                        '''
                }
            }
        }
    }
}