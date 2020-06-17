@256
D = A
@SP
M = D
@RETURN_Sys.init_0
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@0
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Sys.init
0 ; JMP
(RETURN_Sys.init_0)
(Main.fibonacci)
@0
D = A
(LOOP_INIT_LOCAL_Main.fibonacci_0)
@NO_ARG_Main.fibonacci_0
D ; JEQ
@SP
A = M
M = 0
@SP
M = M+1
D = D-1
@LOOP_INIT_LOCAL_Main.fibonacci_0
D ; JNE
(NO_ARG_Main.fibonacci_0)
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
@2
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
D = M-D
@IS_LT_0
D;JLT
@SP
A = M
M = 0
@INC_SP_LT_0
0;JMP
(IS_LT_0)
@SP
A = M
M = -1
(INC_SP_LT_0)
@SP
M = M+1
@SP
AM = M-1
D = M
@IF_TRUE
D ; JNE
@IF_FALSE
0 ; JMP
(IF_TRUE)
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
@R13
M = D
@5
D = A
@R13
A = M-D
D = M
@R14
M = D
@SP
AM = M-1
D = M
@ARG
A = M
M = D
@ARG
D = M+1
@SP
M = D
@1
D = A
@R13
A = M-D
D = M
@THAT
M = D
@2
D = A
@R13
A = M-D
D = M
@THIS
M = D
@3
D = A
@R13
A = M-D
D = M
@ARG
M = D
@4
D = A
@R13
A = M-D
D = M
@LCL
M = D
@R14
A = M
0 ; JMP
(IF_FALSE)
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
@2
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
@RETURN_Main.fibonacci_1
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0 ; JMP
(RETURN_Main.fibonacci_1)
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
@RETURN_Main.fibonacci_2
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0 ; JMP
(RETURN_Main.fibonacci_2)
@SP
AM = M-1
D = M
@SP
AM = M-1
M = M+D
@SP
M = M+1
@LCL
D = M
@R13
M = D
@5
D = A
@R13
A = M-D
D = M
@R14
M = D
@SP
AM = M-1
D = M
@ARG
A = M
M = D
@ARG
D = M+1
@SP
M = D
@1
D = A
@R13
A = M-D
D = M
@THAT
M = D
@2
D = A
@R13
A = M-D
D = M
@THIS
M = D
@3
D = A
@R13
A = M-D
D = M
@ARG
M = D
@4
D = A
@R13
A = M-D
D = M
@LCL
M = D
@R14
A = M
0 ; JMP
(Sys.init)
@0
D = A
(LOOP_INIT_LOCAL_Sys.init_1)
@NO_ARG_Sys.init_1
D ; JEQ
@SP
A = M
M = 0
@SP
M = M+1
D = D-1
@LOOP_INIT_LOCAL_Sys.init_1
D ; JNE
(NO_ARG_Sys.init_1)
@4
D = A
@SP
A = M
M = D
@SP
M = M+1
@RETURN_Main.fibonacci_3
D = A
@SP
A = M
M = D
@SP
M = M+1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M+1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M+1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M+1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M+1
@SP
D = M
@1
D = D-A
@5
D = D-A
@ARG
M = D
@SP
D = M
@LCL
M = D
@Main.fibonacci
0 ; JMP
(RETURN_Main.fibonacci_3)
(WHILE)
@WHILE
0 ; JMP
