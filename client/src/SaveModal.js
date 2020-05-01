import React, { useState, useEffect } from "react"
import "./SaveModal.css"


const SaveModal =  ({ handleSubmit, handleClose }) => {
    const [name, setName] = useState(null)
    return(
        <div className="popup">
            <h3 style={{color:"white"}}>
                Enter name and click submit to save
            </h3>
            <input placeholder="Name:" onChange={e => setName(e.target.value)}/>
            <button onClick={() => handleSubmit(name)}> Submit </button>
            <button onClick={() => handleClose()}> Close </button>
        </div>
    )

}

export default SaveModal
