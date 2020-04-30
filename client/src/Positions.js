import React, { useState, useEffect } from "react"
import SaveModal from "./SaveModal"

const Positions = ({ fen, changeBoard }) =>{
    // State vars
    const [positions, setPositions] = useState(null)
    const [showModal, setShowModal] = useState(false)

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


    const handleSubmit = (name) => {
        savePos(name)
        setShowModal(!showModal)
        loadAll()
    }

    // Saves current fen to the databse
    const savePos = (name) => {
        const body = JSON.stringify({name: name, fen: fen})
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: body
        }
        fetch("/save_pos", requestOptions)
        .then(response => {console.log(response)})
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
            <button onClick={e => setShowModal(!showModal)}> Save current pos to database </button>
            {showModal?
                <SaveModal handleSubmit={handleSubmit}/>
            :
                null
            }
        </div>
    )
}

export default Positions
