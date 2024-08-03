import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"파일 변경 감지: {event.src_path}")
            self.rebuild_and_run()

    def rebuild_and_run(self):
        print("도커 이미지 빌드 중...")
        subprocess.run(["docker", "build", "-t", "myapp", "."])

        print("기존 컨테이너 중지 및 제거 중...")
        subprocess.run(["docker", "stop", "myapp-container"])
        subprocess.run(["docker", "rm", "myapp-container"])

        print("새 컨테이너 실행 중...")
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "-p",
                "8000:8000",
                "--name",
                "myapp-container",
                "myapp",
            ]
        )


if __name__ == "__main__":
    path = "."  # 현재 디렉토리를 감시
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
