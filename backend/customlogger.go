// adopted from https://github.com/x-cray/logrus-prefixed-formatter/blob/master/formatter.go
package main

import (
    "bytes"
    "fmt"
    "log"
    "os"
    "strings"

    "github.com/sirupsen/logrus"
)

type LogFormat struct {
	TimestampFormat string
	Name string
}

func (f *LogFormat) Format(entry *logrus.Entry) ([]byte, error) {
    var b *bytes.Buffer

    if entry.Buffer != nil {
        b = entry.Buffer
    } else {
        b = &bytes.Buffer{}
    }

    b.WriteByte('[')
	b.WriteString(strings.ToUpper(entry.Level.String()))
	b.WriteString("] [")
	b.WriteString(f.Name)
	b.WriteString(" ")
    b.WriteString(entry.Time.Format(f.TimestampFormat))
    b.WriteString("] ")

    if entry.Message != "" {
        b.WriteString(entry.Message)
    }

    if len(entry.Data) > 0 {
        b.WriteString(" || ")
    }
    for key, value := range entry.Data {
        b.WriteString(key)
        b.WriteByte('=')
        b.WriteByte('{')
        fmt.Fprint(b, value)
        b.WriteString("}, ")
    }

    b.WriteByte('\n')
    return b.Bytes(), nil
}

func InitLogger(Name string, TimestampFormat string) {
    formatter := LogFormat{}
	formatter.TimestampFormat = TimestampFormat//"2006-01-02 15:04:05"
	formatter.Name = Name

	logrus.SetFormatter(&formatter)
    log.SetOutput(os.Stdout)
}