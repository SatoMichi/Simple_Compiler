@0
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
M = M-1
@LCL
D = M
@0
D = D+A
@R13
M = D
@SP
A = M
D = M
@R13
A = M
M = D
(LOOP_START)
@ARG
D = M
@0
D = D+A
A = D
D = M
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@0
D = D+A
A = D
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
AM = M-1
D = M
@SP
AM = M-1
M = M+D
@SP
M = M+1
@SP
M = M-1
@LCL
D = M
@0	
D = D+A
@R13
M = D
@SP
A = M
D = M
@R13
A = M
M = D
@ARG
D = M
@0
D = D+A
A = D
D = M
@SP
A = M
M = D
@SP
M = M+1
@1
D = A
@SP
A = M
M = D
@SP
M = M+1
@SP
AM = M-1
D = M
@SP
AM = M-1
M = M-D
@SP
M = M+1
@SP
M = M-1
@ARG
D = M
@0
D = D+A
@R13
M = D
@SP
A = M
D = M
@R13
A = M
M = D
@ARG
D = M
@0
D = D+A
A = D
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
AM = M-1
D = M
@LOOP_START
D ; JNE
@LCL
D = M
@0
D = D+A
A = D
D = M
@SP
A = M
M = D
@SP
M = M+1
