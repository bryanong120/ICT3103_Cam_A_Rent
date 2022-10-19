pipeline {
agent any
stages {
	stage('Build') {
	parallel {
		stage('Build') {
		steps {
			sh 'echo "building the repo"'
		}
		}
	}
	}

	stage('Test') {
	steps {
		sh '''#!/bin/bash
		echo "hello world" 
		virtualenv venv
		. venv/bin/activate
		pip3 install -r requirements.txt
		pytest
		'''
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
