import React, { useState, useEffect } from 'react';
import Positions from "./Positions"
import Chessboard from "chessboardjsx"
import './App.css';
import  Chess from "chess.js"
const App = () => {
    // state vars
    const [chess, setChess] = useState(new Chess())
    const [pos, setPos] = useState(chess.fen())
    const [nextMove, setNextMove] = useState("")
    const [from, setFrom] = useState(0)
    const [to, setTo] = useState(0)

    const [fromSquare, setFromSquare] = useState(null)

    // Updates the chess board after a new move is fetched from server
    useEffect(() => {
        console.log("moving to best loc", nextMove)
        chess.move(nextMove.move)
        setPos(chess.fen())
        
    }, [nextMove])

    // Handles the submit for user moves
    const handleSubmit = () => {
        console.log("from: ", from, "to:", to)
        chess.move({from: from, to: to})
        setPos(chess.fen())
    }

    // Sets the board to a certain layout given by fen
    const changeBoard = (fen) => {
        chess.load(fen)
        setPos(chess.fen())
    }
    
    // Fetches the best move from server based on current fen
    const getBestMove = (moves, turn, fen) => {
        const body = JSON.stringify({ moves: moves, turn: turn, fen:fen})
        console.log(moves)
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        }
        fetch("/hax", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("response: ", data)

                console.log(data.best)
                setNextMove({turn: turn, move: data.best})
            })

    }
    
    // Makes a new move on the chess board
    const move = async () => {
        console.log("moving now")

        const possibleMoves = chess.moves({verbose: true});
        const fen = chess.fen()

        if (chess.game_over() === true || 
            chess.in_draw() === true || 
            possibleMoves.length === 0){
                alert("game over")
                return
        }
        getBestMove(possibleMoves, chess.turn(), fen)

    }

    // manual moving with nmouse
    const onDrop = (e) => {
        const move = chess.move({
            from: e.sourceSquare,
            to: e.targetSquare,
            promotion: "q"
        })
        if (move != null){
            setPos(chess.fen())
        }
    }

    return (
        <div className="App">
            <header className="App-header">
                Best chess engine evah
            </header>
            <div className="App-container">
                <Chessboard position={pos} onDrop={onDrop}/>
            </div>
                <div className="App-container">
                <button onClick={move}> Engine Move! </button>
                <input placeholder="Move From:" onChange={(e) => setFrom(e.target.value)} type="text" name="from" />
                <input placeholder="Move To:" onChange={(e) => setTo(e.target.value)} type="text" name="to" />
                <button onClick={handleSubmit}> Submit </button>
                <Positions fen={pos} changeBoard={changeBoard}/>
            </div>
                
        </div>
    )
}
export default App
