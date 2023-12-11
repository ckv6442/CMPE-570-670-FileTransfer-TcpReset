#include <stdio.h>

int main() {
    int fileSizeMB = 1024;
    int fileSizeB = fileSizeMB * 1024 * 1024;
    // Open the file for writing
    FILE *file = fopen("BigFile.txt", "wb");


    // Seek to the desired position in the file
    if (fseek(file, fileSizeB - 1, SEEK_SET) != 0) {
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

    printf("Data written to BigFile.txt successfully.\n");

    return 0;
}
