import React, { useState } from "react"

const Positions = ({ fen, changeBoard }) =>{
    // State vars
    const [positions, setPositions] = useState(null)

    // Loads all fen's from databse
    const loadAll = () => {
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        }

        fetch("/positions", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("response: ", data)
                setPositions(data.result)
            })
    }

    // Saves current fen to the databse
    const savePos = () => {
        const body = JSON.stringify({fen: fen})
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        }
        fetch("/save_pos", requestOptions)
    }

    return(
        <div>
            <button onClick={loadAll}> Load Positions! </button>
            {positions?
                <select onChange={e => changeBoard(e.target.value)}>
                    {positions.map(item => {
                        return <option value={item.fen_string}> {item.fen_string} </option>
                    })}
                </select>
            : 
                <h1> nothing here </h1>
            }
            <button onClick={savePos}> Save current pos to database </button>
        </div>
    )
}

export default Positions
