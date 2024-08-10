package helpers

import (
    "bufio"
    "encoding/csv"
    "os"
    "fmt"
)

func ParseTSV(filename string) ([][]string, error) {
    file, err := os.Open(filename)
    if err != nil {
        return nil, fmt.Errorf("failed to open file: %w", err)
    } 
    defer file.Close()

    // Create a new reader for the file
    reader := csv.NewReader(bufio.NewReader(file))
    reader.Comma = '\t'

    records, err := reader.ReadAll()
    if err != nil {
        return nil, fmt.Errorf("failed ot read file: %w", err)
    }

    return records, nil
}
