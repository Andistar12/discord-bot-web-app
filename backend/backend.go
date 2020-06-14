package main

import (
    "github.com/gin-gonic/gin"
    log "github.com/sirupsen/logrus"
)

// The main app that runs
var app *gin.Engine

// This function initiates then runs the app
func main() {
    // Initialize app
    log.Infof("Creating app and initializing routes")
    app = gin.Default()
    InitializeRoutes(app)

    // Run app
    log.Infof("Running app")
    app.Run()
}
