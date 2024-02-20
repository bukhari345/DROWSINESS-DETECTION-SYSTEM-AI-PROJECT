import React from "react";
import Webcam from "react-webcam";
import { useRef } from "react";

function Web() {
    const Webref=useRef(null);
    const showImage=()=>{
    console.log(Webref.current);
    }
    return (
        <>
        <h1>hello</h1>
            <div className="Web">
             webcam
             <Webcam  ref={Webref} />
             <button onClick={()=>{showImage();}}>show image in console</button>      
            </div>
        </>
    );
}

export default Web;


