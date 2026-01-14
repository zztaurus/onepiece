pipeline {
    agent none

    environment {
        // 全局环境变量
        IMAGE_NAME = 'simple-flask-project'
        CONTAINER_NAME = 'simple-flask-app'
        // 请在 Jenkins 系统配置中设置以下全局变量或在此处修改
        // PROD_HOST = '192.168.1.100' 
    }

    stages {
        // 1. CI 阶段：代码测试与质量检查
        stage('Test & Lint') {
            agent {
                docker { 
                    image 'python:3.11' 
                    // 挂载工作目录，确保容器内可以访问代码
                    args '-u root'
                }
            }
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                
                // 代码风格检查
                sh 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
                
                // 单元测试
                sh 'pytest'
            }
        }

        // 2. CD 阶段：构建镜像 (仅在 main 分支触发)
        stage('Build & Push Docker') {
            when {
                branch 'main'
            }
            agent any
            steps {
                script {
                    // 需要在 Jenkins 凭据管理中创建 ID 为 'docker-hub-creds' 的用户名密码凭据
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}"
                        
                        // 构建镜像，使用 Build Number 作为版本号
                        sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:latest ."
                        
                        // 推送镜像
                        sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        // 3. CD 阶段：部署到生产环境
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            agent any
            steps {
                script {
                    // 需要在 Jenkins 凭据管理中创建 ID 为 'deploy-ssh-key' 的 SSH 私钥凭据
                    // 需要在 Jenkins 凭据管理中创建 ID 为 'db-creds' 的用户名密码凭据用于注入数据库配置
                    withCredentials([
                        sshUserPrivateKey(credentialsId: 'deploy-ssh-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER'),
                        usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS'),
                        usernamePassword(credentialsId: 'db-creds', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')
                    ]) {
                        // 使用 SSH 远程执行部署命令
                        // 注意：需要确保 Jenkins 服务器可以通过 SSH 连接到 PROD_HOST
                        // 建议在 Jenkins 全局环境变量中配置 PROD_HOST、DB_HOST、DB_NAME
                        sh """
                            ssh -o StrictHostKeyChecking=no -i ${SSH_KEY} ${SSH_USER}@\${PROD_HOST} "
                                docker login -u ${DOCKER_USER} -p ${DOCKER_PASS} && 
                                docker pull ${DOCKER_USER}/${IMAGE_NAME}:latest && 
                                docker stop ${CONTAINER_NAME} || true && 
                                docker rm ${CONTAINER_NAME} || true && 
                                docker run -d --name ${CONTAINER_NAME} -p 8080:8080 \
                                -e MYSQL_HOST=\${DB_HOST} \
                                -e MYSQL_USER=${DB_USER} \
                                -e MYSQL_PASSWORD=${DB_PASSWORD} \
                                -e MYSQL_DATABASE=\${DB_NAME} \
                                ${DOCKER_USER}/${IMAGE_NAME}:latest"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // 清理工作空间
            cleanWs()
        }
        success {
            echo '构建与部署成功！'
        }
        failure {
            echo '构建或部署失败，请检查日志。'
        }
    }
}
