// gcc -fstack-protector-all -Wl,-z,now parent.c -o parent -lseccomp
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/errno.h>
#include <seccomp.h>

void setupFilter(char *childBinary) {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);

    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(rt_sigreturn), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(execve), 1, SCMP_A0(SCMP_CMP_EQ, (scmp_datum_t)(childBinary)));

    seccomp_load(ctx);
}

int main(void) {
    char *childBinary = "./chall";
    char *execArgs[] = { childBinary, NULL };

    pid_t childPID = fork();
    if (childPID == -1) {
        perror("Error forking process");
        return 1;
    }

    if (childPID == 0) {
        setupFilter(childBinary);
        execve(childBinary, execArgs, NULL);
        perror("Error running the challenge binary");
        return 1;
    }

    int status;
    waitpid(childPID, &status, 0);
    return 0;
}