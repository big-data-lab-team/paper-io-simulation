#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

int main(int argc, char ** argv)
{

    if(argc != 4)
    {
        printf("usage: read_write <file_in> <file_out> <log_file>\n");
        return 1;
    }

    // Parse arguments
    char * in_file_name = argv[1];
    char * out_file_name = argv[2];
    char * log_file_name = argv[3];

    FILE * log_file = fopen(log_file_name, "a");

    struct timeval  start;
    struct timeval  end;

    gettimeofday(&start, NULL);
    // Get file size
    FILE * in_file = fopen(in_file_name, "rb");
    fseek(in_file, 0, SEEK_END);
    long fsize = ftell(in_file);
    fseek(in_file, 0, SEEK_SET);  

    // Read file in buffer
    char * buff = malloc(fsize + 1);
    fread(buff, fsize, 1, in_file);
    fclose(in_file);

    gettimeofday(&end, NULL);

    double read_start_in_mil = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    double read_end_in_mil = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    printf("Read %s in: %lf\n", in_file_name, (read_end_in_mil - read_start_in_mil) / 1000);
    printf("Avg read bw: %4.2lf MBps\n\n", fsize / ((read_end_in_mil - read_start_in_mil) * 1000));

    // Increment buffer
    gettimeofday(&start, NULL);
    long int i;
    for(i = 0 ; i < fsize ; i++)
        buff[i]++;
    gettimeofday(&end, NULL);

    double cpu_start_in_mil = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    double cpu_end_in_mil = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    gettimeofday(&start, NULL);
//     Write buffer
    FILE * out_file = fopen(out_file_name, "wb");
    fwrite(buff, fsize, 1, out_file);
    fclose(out_file);
    gettimeofday(&end, NULL);

    double write_start_in_mil = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    double write_end_in_mil = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    fprintf(log_file, "%lf, %lf, %lf, %lf, %lf, %lf\n",
        read_start_in_mil/1000, read_end_in_mil/1000,
        cpu_start_in_mil/1000, cpu_end_in_mil/1000,
        write_start_in_mil/1000, write_end_in_mil/1000);
    printf("Write %s in: %lf\n", out_file_name, (write_end_in_mil - write_start_in_mil) / 1000);
    printf("Avg write bw: %4.2lf MBps\n\n", fsize / ((write_end_in_mil - write_start_in_mil) * 1000));

    fclose(log_file);

    return 0;
}