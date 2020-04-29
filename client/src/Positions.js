import React, { useState, useEffect } from "react"

const Positions = ({ fen, changeBoard }) =>{
    // State vars
    const [positions, setPositions] = useState(null)

    useEffect(() => {
        loadAll()
    }, [])

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
            {positions?
                <select onChange={e => changeBoard(e.target.value)}>
                    {positions.map(item => {
                        return <option value={item.fen_string}> {item.name} </option>
                    })}
                </select>
            : 
                null
            }
            <button onClick={savePos}> Save current pos to database </button>
        </div>
    )
}

export default Positions
