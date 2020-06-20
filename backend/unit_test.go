package main

import (
    "bytes"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/gin-gonic/gin"
	"encoding/json"
)

var unit_app *gin.Engine

// Returns a new router for use in tests 
func GetTestRouter() *gin.Engine {
    if unit_app == nil {
        unit_app = gin.Default()
        InitializeRoutes(unit_app)
    }
    return unit_app
}

// Helper function to process a request and its response
func getHTTPResponse(req *http.Request) *httptest.ResponseRecorder {
    // Get router
    r := GetTestRouter()

	// Create a response recorder
	w := httptest.NewRecorder()

	// Create the service and process the above request.
	r.ServeHTTP(w, req)

    // Return the response
    return w
}

// Tests that the command "ping" properly returns "Pong!" in "response"
func TestCommandPing(t *testing.T) {

    // Fetch response
    req, _ := http.NewRequest("POST", "/command/ping", nil)
    w := getHTTPResponse(req)

    // Check status == 200 
    if w.Code != http.StatusOK {
        t.Errorf("Bad status code. Expected %v, got %v\n", http.StatusOK, w.Code)
    }

    // Define response format
    type ExpectedResponse struct {
        Response string `json:"response"`
    }

    // Read response
    p, err := ioutil.ReadAll(w.Body)
    if err != nil {
        t.Errorf("Error occurred reading response: %v\n", err)
    }

    // Unmarshal JSON response
    var response ExpectedResponse
    err = json.Unmarshal([]byte(p), &response)
    if err != nil {
        t.Errorf("Error occurred unmarshalling response: %v\n", err)
    }

    // Check response good
    if response.Response != "Pong!" {
        t.Errorf("Wrong output. Expected: %v. Got: %v\n", "Pong!", response.Response)
    }
}

// Tests that the command "pong" properly returns "Ping!" in "response"
func TestCommandPong(t *testing.T) {

    // Fetch response
    req, _ := http.NewRequest("POST", "/command/pong", nil)
    w := getHTTPResponse(req)

    // Check status == 200 
    if w.Code != http.StatusOK {
        t.Errorf("Bad status code. Expected %v, got %v\n", http.StatusOK, w.Code)
    }

    // Define response format
    type ExpectedResponse struct {
        Response string `json: response`
    }

    // Read response
    p, err := ioutil.ReadAll(w.Body)
    if err != nil {
        t.Errorf("Error occurred reading response: %v\n", err)
    }

    // Unmarshal JSON response
    var response ExpectedResponse
    err = json.Unmarshal([]byte(p), &response)
    if err != nil {
        t.Errorf("Error occurred unmarshalling response: %v\n", err)
    }

    // Check response good
    if response.Response != "Ping!" {
        t.Errorf("Wrong output. Expected: %v. Got: %v\n", "Ping!", response.Response)
    }
}

// Tests that the command "repeat" properly returns a message in "response"
func TestCommandRepeat(t *testing.T) {

    payload := &CommandRequest{
        Command: "repeat",
        Arguments: []string {"id?"},
        UserID: 0,
    }
    body, _ := json.Marshal(payload)

    // Fetch response
    req, _ := http.NewRequest("POST", "/command/repeat", bytes.NewBuffer(body))
    w := getHTTPResponse(req)

    // Check status == 200 
    if w.Code != http.StatusOK {
        t.Errorf("Bad status code. Expected %v, got %v\n", http.StatusOK, w.Code)
    }

    // Define response format
    type ExpectedResponse struct {
        Response string `json: response`
    }

    // Read response
    p, err := ioutil.ReadAll(w.Body)
    if err != nil {
        t.Errorf("Error occurred reading response: %v\n", err)
    }

    // Unmarshal JSON response
    var response ExpectedResponse
    err = json.Unmarshal([]byte(p), &response)
    if err != nil {
        t.Errorf("Error occurred unmarshalling response: %v\n", err)
    }

    // Check response good
    if response.Response != "id?" {
        t.Errorf("Wrong output. Expected: %v. Got: %v\n", "id?", response.Response)
    }
}
