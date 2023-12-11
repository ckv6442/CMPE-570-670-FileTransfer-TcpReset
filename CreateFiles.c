#include <stdio.h>
#include <string.h>

int main() {
    // Array of file sizes in bytes
    const int fileSizes[] = {50, 1024, 5*1024, 10*1024, 25*1024, 50*1024, 100*1024, 1*1024*1024, 
        5*1024*1024, 10*1024*1024, 25*1024*1024, 50*1024*1024, 100*1024*1024, 250*1024*1024, 1024*1024*1024};
    // File names FileSizes/*.txt
    const char *fileNames[] = {"SmallFile", "1KB", "5KB", "10KB", "25KB", "50KB", "100KB", "1MB", "5MB", "10MB", 
        "25MB", "50MB", "100MB", "250MB", "BigFile"};
    
    // Iterate for each file to create
    for (int i = 0; i < 15; i++){
        char str[256] = "FileSizes/";
        strcat(str, fileNames[i]);
        strcat(str, ".txt");
        // Open the file for writing
        FILE *file = fopen(str, "wb");

        // Seek to the desired position in the file
        if (fseek(file, fileSizes[i] - 1, SEEK_SET) != 0) {
            perror("Error seeking to the end of file");
            fclose(file);
            return 1;
        }

        // Write a single byte to the file at the desired position
        if (fwrite("", 1, 1, file) != 1) {
            perror("Error writing to file");
            fclose(file);
            return 1;
        }

        // Close the file
        fclose(file);

        printf("Data written to %s successfully.\n", str);

    }

    return 0;
}
