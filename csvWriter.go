package main
import (
    "encoding/json"
    "github.com/google/uuid"
    "log"
    "encoding/xml"
    "net/http"
)
func writeToCSV(question, solution string){
	file, err := os.Open("sample.csv")
	checkError("Cannot create file", err)
    defer file.Close()

    var data = [][] string {{question, solution}}
    writer := csv.NewWriter(file)
    defer writer.Flush()
    for _, value := range data {
        err := writer.Write(value)
        checkError("Cannot write to file", err)
    }
}

 
func main() {
    var handle
    http.HandleFunc("/", handler) // each request calls handler
    http.ListenAndServe("0.0.0.0:7652", handle)
    fmt.Fprintf(handle)
    json.Unmarshal([]byte(handle[0]), &question)
    json.Unmarshal([]byte(handle[1]), &solution)
    writeToCSV(question,solution)
}

// handler echoes the Path component of the requested URL.
func handler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "URL.Path = %q\n", r.URL.Path)
}