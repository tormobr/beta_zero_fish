import React, { useState, useEffect } from "react"
import "./SaveModal.css"


const SaveModal =  ({ handleSubmit }) => {
    const [name, setName] = useState(null)
    return(
        <div className="popup">
            <p>
                Enter name and click submit to save
            </p>
            <input placeholder="Name:" onChange={e => setName(e.target.value)}/>
            <button onClick={() => handleSubmit(name)}> Submit </button>
        </div>
    )

}

export default SaveModal
