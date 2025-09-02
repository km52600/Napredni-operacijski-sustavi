#include <poll.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    struct pollfd fds[argc - 1];
    int i = 0;
    while (i < argc - 1) {
        fds[i].fd = open(argv[i + 1], O_RDONLY);
        if (fds[i].fd == -1) {
            perror("open");
            exit(EXIT_FAILURE);
        }
        fds[i].events = POLLIN;
        i++;
    }

    while (1) {
        int ready = poll(fds, argc - 1, -1);
        if (ready == -1) {
            perror("poll");
            exit(EXIT_FAILURE);
        }
        i = 0;
        while (i < argc - 1) {
            if (fds[i].revents != 0) {
                // Ispisivanje događaja fajl-deskriptora
                printf("fd=%d; event: ", fds[i].fd);

                if (fds[i].revents & POLLIN) {
                    printf("POLLIN\n");
                }
                if (fds[i].revents & POLLHUP) {
                    printf("POLLHUP\n");
                }
                if (fds[i].revents & POLLERR) {
                    printf("POLLERR\n");
                }

                if (fds[i].revents & POLLIN) {
                    char buf;
                    ssize_t s = read(fds[i].fd, &buf, 1);
                    if (s == -1) {
                        perror("read");
                        exit(EXIT_FAILURE);
                    }
                    printf("read : %.*s\n", (int)s, &buf);
                    printf("\n");
                } else {  // POLLERR | POLLHUP
                    close(fds[i].fd);
                }
            }
            i++;
        }

    }
}
