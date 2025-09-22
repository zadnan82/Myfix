"""
file_watcher.py - File system monitoring for auto-compilation

This module handles watching for file changes and triggering recompilation.
"""

import asyncio
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    """Handles file system events for frontend input files."""

    def __init__(
        self,
        compilation_callback: Callable[[Path], None],
        notification_callback: Callable[[], None],
    ):
        self.compilation_callback = compilation_callback
        self.notification_callback = notification_callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"Frontend file changed: {event.src_path}")
            self.compilation_callback(Path(event.src_path))
            asyncio.run(self.notification_callback())

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"Frontend file created: {event.src_path}")
            self.compilation_callback(Path(event.src_path))
            asyncio.run(self.notification_callback())


class BackendFileChangeHandler(FileSystemEventHandler):
    """Handles file system events for backend input files."""

    def __init__(
        self,
        compilation_callback: Callable[[Path], None],
        server_restart_callback: Callable[[], None],
        notification_callback: Callable[[], None],
    ):
        self.compilation_callback = compilation_callback
        self.server_restart_callback = server_restart_callback
        self.notification_callback = notification_callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"Backend file changed: {event.src_path}")
            self.compilation_callback(Path(event.src_path))
            asyncio.run(self.server_restart_callback())
            asyncio.run(self.notification_callback())

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"Backend file created: {event.src_path}")
            self.compilation_callback(Path(event.src_path))
            asyncio.run(self.server_restart_callback())
            asyncio.run(self.notification_callback())


class FileWatcherManager:
    """Manages file system watching for both frontend and backend files."""

    def __init__(
        self,
        input_dir: Path,
        backend_input_dir: Path,
        compilation_manager,
        server_manager,
        notification_callback,
    ):
        self.input_dir = input_dir
        self.backend_input_dir = backend_input_dir
        self.compilation_manager = compilation_manager
        self.server_manager = server_manager
        self.notification_callback = notification_callback
        self.observer: Optional[Observer] = None

    def start_watching(self):
        """Start the file system watcher."""
        # Frontend file handler
        frontend_handler = FileChangeHandler(
            self.compilation_manager.compile_frontend_file, self.notification_callback
        )

        # Backend file handler
        backend_handler = BackendFileChangeHandler(
            self.compilation_manager.compile_backend_file,
            self.server_manager.restart_server,
            self.notification_callback,
        )

        self.observer = Observer()
        self.observer.schedule(frontend_handler, str(self.input_dir), recursive=False)
        self.observer.schedule(
            backend_handler, str(self.backend_input_dir), recursive=False
        )
        self.observer.start()

        print(f"Started watching {self.input_dir} and {self.backend_input_dir}")

    def stop_watching(self):
        """Stop the file system watcher."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("Stopped file watcher")
