import sys, select, os, msvcrt, time
  
# class for checking keyboard input
class Getchar:
    def __init__(self): #클래스 만들때 써줌 
        pass                #아무것도 동작하지 안해도 될때 사용
  
    def getch(self):
        if os.name == 'nt': # ':'를 사용해서 들여쓰기로 함수를 구분
            timeout = 0.1
            startTime = time.time()
            while(1):
                if msvcrt.kbhit():
                    if sys.version_info[0] >= 3:
                        return msvcrt.getch().decode()
                    else:
                        return msvcrt.getch()
                elif time.time() - startTime > timeout:
                    return ''

        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key