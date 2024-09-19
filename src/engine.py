import chess
import chess.engine
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize a new chess board
board = chess.Board()

# Path to the Stockfish engine (adjust the path as needed)
ENGINE_PATH = "path/to/your/stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

@app.route("/move", methods=["POST"])
def make_move():
    move = request.json.get("move")
    if move:
        try:
            board.push_uci(move)
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
            return jsonify({"move": result.move.uci(), "status": "ok"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "No move provided"})

@app.route("/reset", methods=["POST"])
def reset_board():
    global board
    board = chess.Board()
    return jsonify({"status": "ok"})

@app.route("/board", methods=["GET"])
def get_board():
    return jsonify({"board": board.fen(), "status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)