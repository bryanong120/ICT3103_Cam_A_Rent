pipeline {
    agent {
        dockerfile { filename 'Dockerfile.Jenkins' }
    }
stages {
	//stage('Build') {
	// parallel {
		stage('Build') {
		steps {
			sh 'echo "building the repo"'
		}
		}
	// }
	//}

	stage('Test') {
	steps {
		sh '''#!/bin/bash
		echo "hello world"
		python3 --version 
		pytest
		'''
		//pip3 install --no-cache-dir -r requirements.txt --user
		//input(id: "Deploy Gate", message: "Deploy ${params.project_name}?", ok: 'Deploy')
	}
	}

	// stage('Deploy')
	// {
	// steps {
	// 	echo "deploying the application"
	// 	sh "sudo nohup python3 app.py > log.txt 2>&1 &"
	// }
	// }
}

post {
		always {
			echo 'The pipeline completed'
		}
		success {				
			echo "Flask Application Up and running!!"
		}
		failure {
			echo 'Build stage failed'
			error('Stopping early…')
		}
	}
}
