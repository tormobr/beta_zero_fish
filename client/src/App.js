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
    const [orientation, setOrientation] = useState("white")
    const [autoFlip, setAutoFlip] = useState(false)

    // Updates the chess board after a new move is fetched from server
    useEffect(() => {
        console.log("moving to best loc", nextMove)
        makeMove(nextMove.from, nextMove.to)
        afterMove()
    }, [nextMove])

    // Sets the board to a certain layout given by fen
    const changeBoard = (fen) => {
        chess.load(fen)
        setPos(chess.fen())
    }

    const afterMove = () =>{
        setPos(chess.fen())
        if (autoFlip) {
            flipBoard()
        }

    }

    // Fetches the best move from server based on current fen
    const getBestMove = async (moves, turn, fen) => {
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
                console.log(data.best)
                setNextMove(data.best)
            })

    }
    
    // Makes a new move on the chess board
    const move = async () => {

        const possibleMoves = chess.moves({verbose: true});
        const fen = chess.fen()

        if (chess.game_over() === true || 
            chess.in_draw() === true || 
            possibleMoves.length === 0){
                alert("game over")
                return
        }
        await getBestMove(possibleMoves, chess.turn(), fen)

    }

    // manual moving with nmouse
    const makeMove = (sourceSquare, targetSquare) => {
        const move = chess.move({
            from: sourceSquare,
            to: targetSquare,
            promotion: "q"
        })
        if (move != null){
            afterMove()
        }
    }

    // Undo the last move
    const undoMove = () => {
        console.log("undo happens here")
        chess.undo()
        setPos(chess.fen())
    }

    
    const flipBoard = () => {
        if (autoFlip){
            chess.turn() == "w"? setOrientation("White") : setOrientation("black")
            return
        }

        if (orientation == "white"){
            setOrientation("black")
        }
        else{
            setOrientation("white")
        }
    }

    return (
        <div className="App">
            <header className="App-header">
                Best chess engine evah
            </header>
            <div className="App-container">
                <Chessboard 
                    key={chess.fen()}
                    position={chess.fen()} 
                    transitionDuration="0"
                    orientation={orientation}
                    onDrop={e => makeMove(e.sourceSquare, e.targetSquare)}
                    />
            </div>

            <div className="App-container">
                <button onClick={move}> Engine Move! </button>

                <button onClick={undoMove}> 
                    Go Back!
                </button>
                <button onClick={flipBoard}> 
                    Flip Board
                </button>
                <button onClick={() => setAutoFlip(!autoFlip)}> 
                    Toggle AutoFlip
                </button>

                <Positions fen={pos} changeBoard={changeBoard}/>
            </div>
                
        </div>
    )
}
export default App
