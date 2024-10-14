const rawGetImageData = CanvasRenderingContext2D.prototype.getImageData;

let noisify = function (canvas, context) {
    let ctxIdx = ctxArr.indexOf(context);
    let info = ctxInf[ctxIdx];
    const width = canvas.width, height = canvas.height;
    const imageData = rawGetImageData.apply(context, [0, 0, width, height]);
    if (info.useArc || info.useFillText) {
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                const n = ((i * (width * 4)) + (j * 4));
                // RBGA adds random salt to all 4 dimensions
                imageData.data[n + 0] = imageData.data[n + 0] + -1;
                imageData.data[n + 1] = imageData.data[n + 1] + -2;
                imageData.data[n + 2] = imageData.data[n + 2] + -3;
                imageData.data[n + 3] = imageData.data[n + 3] + 0;
            }
        }
    }
    context.putImageData(imageData, 0, 0);
};

let ctxArr = [];
let ctxInf = [];

(function mockGetContext() {
    let rawGetContext = HTMLCanvasElement.prototype.getContext

    Object.defineProperty(HTMLCanvasElement.prototype, "getContext", {
        "value": function () {
            let result = rawGetContext.apply(this, arguments);
            if (arguments[0] === '2d') {
                ctxArr.push(result)
                ctxInf.push({})
            }
            return result;
        }
    });

    Object.defineProperty(HTMLCanvasElement.prototype.constructor, "length", {
        "value": 1
    });

    Object.defineProperty(HTMLCanvasElement.prototype.constructor, "toString", {
        "value": () => "function getContext() { [native code] }"
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.constructor, "name", {
        "value": "getContext"
    });
})();

(function mockArc() {
    let rawArc = CanvasRenderingContext2D.prototype.arc
    Object.defineProperty(CanvasRenderingContext2D.prototype, "arc", {
        "value": function () {
            let ctxIdx = ctxArr.indexOf(this);
            ctxInf[ctxIdx].useArc = true;
            return rawArc.apply(this, arguments);
        }
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.arc, "length", {
        "value": 5
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.arc, "toString", {
        "value": () => "function arc() { [native code] }"
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.arc, "name", {
        "value": "arc"
    });
})();

(function mockFillText() {
    const rawFillText = CanvasRenderingContext2D.prototype.fillText;
    Object.defineProperty(CanvasRenderingContext2D.prototype, "fillText", {
        "value": function () {
            let ctxIdx = ctxArr.indexOf(this);
            ctxInf[ctxIdx].useFillText = true;
            return rawFillText.apply(this, arguments);
        }
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.fillText, "length", {
        "value": 4
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.fillText, "toString", {
        "value": () => "function fillText() { [native code] }"
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.fillText, "name", {
        "value": "fillText"
    });
})();


(function mockToBlob() {
    const toBlob = HTMLCanvasElement.prototype.toBlob;

    Object.defineProperty(HTMLCanvasElement.prototype, "toBlob", {
        "value": function () {
            noisify(this, this.getContext("2d"));
            return toBlob.apply(this, arguments);
        }
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toBlob, "length", {
        "value": 1
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toBlob, "toString", {
        "value": () => "function toBlob() { [native code] }"
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toBlob, "name", {
        "value": "toBlob"
    });
})();

(function mockToDataURL() {
    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
    Object.defineProperty(HTMLCanvasElement.prototype, "toDataURL", {
        "value": function () {
            noisify(this, this.getContext("2d"));
            return toDataURL.apply(this, arguments);
        }
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toDataURL, "length", {
        "value": 0
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toDataURL, "toString", {
        "value": () => "function toDataURL() { [native code] }"
    });

    Object.defineProperty(HTMLCanvasElement.prototype.toDataURL, "name", {
        "value": "toDataURL"
    });
})();


(function mockGetImageData() {
    Object.defineProperty(CanvasRenderingContext2D.prototype, "getImageData", {
        "value": function () {
            noisify(this.canvas, this);
            return rawGetImageData.apply(this, arguments);
        }
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.getImageData, "length", {
        "value": 4
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.getImageData, "toString", {
        "value": () => "function getImageData() { [native code] }"
    });

    Object.defineProperty(CanvasRenderingContext2D.prototype.getImageData, "name", {
        "value": "getImageData"
    });
})();

console.log('random_canvas script run!')