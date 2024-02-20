import React, { Component } from "react";
import html2canvas from "html2canvas";

import Sample from "./template/Sample";

export default class ScreenCapture extends Component {
  ref = React.createRef();

  handleClickTakeScreenShot = () => {
    const { cropPositionTop, cropPositionLeft, cropWidth, cropHeigth } = {
      cropPositionTop: 0,
      cropPositionLeft: 0,
      cropWidth: 1400,
      cropHeigth: 1800
    };

    html2canvas(this.ref.current).then(canvas => {
      let croppedCanvas = document.createElement("canvas");
      let croppedCanvasContext = croppedCanvas.getContext("2d");

      croppedCanvas.width = cropWidth;
      croppedCanvas.height = cropHeigth;

      croppedCanvasContext.drawImage(canvas, cropPositionLeft, cropPositionTop);

      const a = document.createElement("a");
      a.href = croppedCanvas.toDataURL();
      a.download = "receipt.png";
      a.click();
    });
  };

  render() {
    const { children } = this.props;

    return (
      <div>
        {children}
        <button onClick={this.handleClickTakeScreenShot}>Download</button>
        <div
          id="#screenshot"
          // style={{ position: "relative", left: "-1000px" }}
          ref={this.ref}
        >
          <Sample />
        </div>
      </div>
    );
  }
}