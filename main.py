from multiprocessing import Process

import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])
    
def main():
    script1_thread = Process(target=run_script, args=("image.py",))
    script2_thread = Process(target=run_script, args=("control.py",))

    script1_thread.start()
    script2_thread.start()

    script1_thread.join()
    script2_thread.join()

    print("Both scripts have finished executing.")

if __name__ == '__main__':
    main()

