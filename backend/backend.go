package main

import (
    "github.com/gin-gonic/gin"
    log "github.com/sirupsen/logrus"
    "os"
    "io/ioutil"
    "encoding/json"
)

// The main app that runs
var app *gin.Engine

// The necessary parameters in the config file
type Config struct {
    Port    string  `json:"backend_addr_port"` 
    Target  string  `json:"target"`
}

// This function initiates then runs the app
func main() {
    // Open config file
    configFile, err := os.Open(os.Getenv("CONFIG_LOC"))
    if err != nil {
        log.Fatal("Error opening config: " + err.Error())
    }
    byteData, err := ioutil.ReadAll(configFile)
    if err != nil {
        log.Fatal("Error reading config file: " + err.Error())
    }
    defer configFile.Close()
    config := &Config {
        Port: "2468",
        Target: "debug",
    }
    err = json.Unmarshal(byteData, &config)
    if err != nil {
        log.Error("Error parsing config file: " + err.Error()) 
    }

    // Initialize app
    log.Infof("Creating app and initializing routes")
    app = gin.Default()
    gin.SetMode(config.Target)
    os.Setenv("PORT", config.Port)
    InitializeRoutes(app)

    // Run app
    log.Infof("Running app")
    app.Run()
}
