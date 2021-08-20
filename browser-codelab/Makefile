.PHONY: http-bg firefox

http-bg:
	tmux new-session -n http_server -d 'python -m http.server'

firefox:
	tmux new-window -n ff -d 'firefox localhost:8000'
