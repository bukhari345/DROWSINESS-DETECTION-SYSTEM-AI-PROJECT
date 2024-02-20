import React, {
  Component,
  useEffect,
  useState,
  useRef,
  createRef,
} from "react";
import * as htmlToImage from "html-to-image";
import Webcam from "react-webcam";
import { useScreenshot, createFileName } from "use-react-screenshot";
export default function UserHome({ userData }) {
  const logOut = () => {
    window.localStorage.clear();
    window.location.href = "./sign-in";
  };
  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(",");
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  };

  const ref = createRef(null);
  const takeScreenShot = async (node) => {
    console.log("this is", node);
    const dataURI = await htmlToImage.toJpeg(node);
    console.log(dataURI);
    return dataURI;
  };

  const download = (image, { name = "img", extension = "jpg" } = {}) => {
    const a = document.createElement("a");
    a.href = image;
    a.download = createFileName(extension, name);
    a.click();
  };
  const capture = React.useCallback(
    async ({ name = "img", extension = "jpg" } = {}) => {
      const imageSrc = ref.current.getScreenshot();
      const fileName = createFileName({ prefix: "screenshot", extension: "jpg" });
      const formData = new FormData();
      formData.append("image", dataURLtoFile(imageSrc, fileName));
      fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        crossDomain: true,
        headers: {
          "Access-Control-Allow-Origin": "*",
        },
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          console.log(data, "data");
        });
      console.log("first", imageSrc);
      const a = document.createElement("a");
      a.href = imageSrc;
      a.download = createFileName(extension, name);
      a.click();
    },
    [ref]
  );

  const downloadScreenshot = () => takeScreenShot(ref.current).then(download);
  const videoConstraints = {
    width: 680,
    height: 520,
    facingMode: "user",
  };
  return (
    <>
      <div style={{ backgroundColor: "lightblue" }}>
        <div
          className="container text-center mt-2"
          style={{ alignItems: "center", marginLeft: 600 }}
        >
          <div
            class="card"
            style={{ width: 300, backgroundColor: "lightcyan" }}
          >
            <div class="card-body">
              <h4 class="card-title" style={{ fontWeight: "bold" }}>
                DROWSINESS <br /> DETECTION <br /> SYSTEM
              </h4>
            </div>
          </div>
        </div>
        <br />
        <div className="text-center">
          <button className="btn" style={{ backgroundColor: "lightskyblue" }}>
            Welcome {userData.fname}!
          </button>
        </div>
        <br />
        <div className="container text-center" style={{ marginLeft: 450 }}>
          <div
            className="card"
            style={{ width: 600, backgroundColor: "lightcyan" }}
          >
            <div className="card-body">
              <h5 className="card-title">About System</h5>
              <p
                className="card-text"
                style={{ color: "black", fontWeight: "bold" }}
              >
                A drowsiness detection system is a technology that monitors a
                person's physiological signals such as heart rate, eye movement,
                and brain activity to detect when they are becoming drowsy or
                fatigued. The system alerts the person to take a break or stop
                their activity to prevent accidents caused by lack of focus or
                attention. Drowsiness detection systems are especially important
                for individuals who work long hours, drive long distances, or
                operate heavy machinery. These systems promote safety and
                prevent accidents in various settings.
              </p>
            </div>
          </div>
        </div>
        <br />
        <div className="container text-center" style={{ marginLeft: 400 }}>
          <div
            className="card"
            style={{ width: 750, backgroundColor: "lightcyan" }}
          >
            <div className="card-body">
              <h5 className="card-title">System Functions</h5>
              <br />
              <div style={{ height: "100", width: "100" }}>
                <Webcam
                  audio={false}
                  height={520}
                  ref={ref}
                  screenshotFormat="image/jpeg"
                  width={680}
                  videoConstraints={videoConstraints}
                />{" "}
              </div>
              <button onClick={capture}>captureimage</button>
            </div>
            <br />
            <br />

            <button
              onClick={logOut}
              className="btn btn-primary"
              style={{ width: 150 }}
            >
              Log Out
            </button>
          </div>
        </div>
      </div>
      <br />
    </>
  );
}
