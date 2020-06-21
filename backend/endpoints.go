package main

import (
    log "github.com/sirupsen/logrus"
    "strings"
    "net/http"
    "github.com/gin-gonic/gin"
)

// Initiates all available routes in the app
func InitializeRoutes(app *gin.Engine) {
    app.GET("/commands", GetAllCommands)
    app.POST("/command/ping", CommandPing)
    app.POST("/command/pong", CommandPong)
    app.POST("/command/repeat", CommandRepeat)
}

// The format a command request should take
// Command is the requested command. Should match its endpoint
// Arguments is a string array of each arguments. Each string may or may not have spaces
// UserID is the user snowflake of the sender of the command
// MessageID is the id of the message itself
// MessageChannelID is the id of the channel the message was sent on
// IsPrivate indicates whether the channel is a private/dm or a server channel
type CommandRequest struct {
    Command string          `json:"command"`
    Arguments []string      `json:"arguments"`
    UserID int              `json:"user_id"`
    MessageID int           `json:"message_id"`
    MessageChannelID int    `json:"message_channel_id"`
    IsPrivate bool          `json:"is_private"`
}

// Returns as "command" an array of every available command
func GetAllCommands(ctx *gin.Context) {
    payload := gin.H{"commands": []string{
            "ping", "pong", "repeat",
        },
    }
    ctx.JSON(http.StatusOK, payload)
}

// Replies "Pong!" as response
func CommandPing(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, gin.H{"response": "Pong!"})
}

// Replies "Ping!" as response
func CommandPong(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, gin.H{"response": "Ping!"})
}

// Returns the user's own message as response, or tells the user to 
// provide something to respond to if no message is present
func CommandRepeat(ctx *gin.Context) {
    var params CommandRequest
    err := ctx.BindJSON(&params)
    if err != nil {
        log.Errorf("Error occurred parsing paramters")
        log.Error(err)
    } else {
        reply := strings.Join(params.Arguments, " ")
        if reply == "" {
            reply = "Specify something for me to repeat back!"
        }
        ctx.JSON(http.StatusOK, gin.H{"response": reply})
    }
}
