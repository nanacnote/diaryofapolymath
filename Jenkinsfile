pipeline {
    agent any

    environment {
        registry = "registry.hiramlabs.com"
        nameTag = "image/diaryofapolymath"
    }

    stages {
        stage('Test') {
            steps {
                echo 'TODO: look into adding test inside dockerfile build process'
            }
        }
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                script {
                    docker.withRegistry("https://${env.registry}", 'registry-auth-credential') {
                        def image = docker.build("${env.registry}/${nameTag}")
                        image.push()
                        image.push('latest')
                        sh('docker system prune -a -f --volumes')
                    }
                }
            }
        }
    }
}