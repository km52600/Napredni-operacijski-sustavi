#include <poll.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    srand(time(NULL));

    int fds_counter = argc - 1;
    struct pollfd fds[fds_counter];

    // Otvaranje datoteka i popunjavanje fds-a
    int i = 0;
    while (i < fds_counter) {
        fds[i].fd = open(argv[i + 1], O_WRONLY);
        fds[i].events = POLLOUT;
        printf("File: '%s' successfully opened with file descriptor: fd%d\n", argv[i + 1], fds[i].fd);
        i++;
    }

    for (int count = 40; count > 0; count--) { // broj iteracija
        sleep(2);
        int ready = poll(fds, fds_counter, 5000); // čekaj 5 sekundi
        if (ready < 0) {
            perror("poll");
            break;
        } else if (ready == 0) {
            printf("No file descriptors ready for writing.\n");
        } else {
            int ready_fds[fds_counter];
            int num_ready = 0;
            
            for (int i = 0; i < fds_counter; i++) {
                if (fds[i].revents & POLLOUT) {
                    ready_fds[num_ready++] = i;  // Pohranjujemo indekse spremnih deskriptora
                }
            }
            if (num_ready > 0) {
                int rand_idx = rand() % num_ready;  // nasumični spremni deskriptor
                int chosen_fd_index = ready_fds[rand_idx];
                
                char c = 'a' + (rand() % 26); // Nasumičan znak
                if (write(fds[chosen_fd_index].fd, &c, 1) == -1) {
                    fprintf(stderr, "Error writing to %s: %s\n", argv[chosen_fd_index + 1], strerror(errno));
                } else {
                    printf("Written '%c' to %s (fd%d)\n", c, argv[chosen_fd_index + 1], fds[chosen_fd_index].fd);
                }
            }
        }
    }

    i = 0;
    while (i < fds_counter) {
        close(fds[i].fd);
        i++;
    }


    return 0;
}
